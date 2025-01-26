import os
import io
import json
import time
import urllib3
import pdfplumber
from typing import List, Optional
from functools import partial
from IPython.display import display, Markdown
from langchain_core.tools import BaseTool, tool
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from datetime import datetime

# Importar configuración
from literature_research_graph.configuration import AgentConfiguration

# Configuración de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CoreAPIWrapper(BaseModel):
    """Wrapper para la API de CORE con manejo dinámico de configuración"""
    base_url: str = "https://api.core.ac.uk/v3"
    api_key: str = Field(default="", description="API Key para CORE Academic")
    max_retries: int = Field(default=5, description="Número máximo de reintentos")
    timeout: int = Field(default=30, description="Tiempo máximo de espera en segundos")

    @classmethod
    def from_config(cls, config: RunnableConfig) -> "CoreAPIWrapper":
        """Crea una instancia desde la configuración de LangGraph"""
        runtime_config = AgentConfiguration.from_runnable_config(config)
        return cls(api_key=runtime_config.core_api_key)

    def _search_with_retry(self, query: str, max_results: int) -> dict:
        """Búsqueda con mecanismo de reintentos"""
        http = urllib3.PoolManager()
        for attempt in range(self.max_retries):
            try:
                response = http.request(
                    'GET',
                    f"{self.base_url}/search/outputs",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    fields={"q": query, "limit": max_results},
                    timeout=self.timeout
                )
                if 200 <= response.status < 300:
                    return json.loads(response.data.decode('utf-8'))
                elif response.status == 429:
                    sleep_time = 2 ** (attempt + 1)
                    time.sleep(sleep_time)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Error en CORE API: {str(e)}") from e
        return {}

    def search(self, query: str, max_papers: int = 1) -> str:
        """Ejecuta una búsqueda académica"""
        try:
            results = self._search_with_retry(query, max_papers).get("results", [])
            if not results:
                return "No se encontraron resultados relevantes"
            
            formatted_results = []
            for paper in results:
                authors = ",\n".join([a["name"] for a in paper.get("authors", [])])
                published_date = paper.get("publishedDate") or paper.get("yearPublished", "Desconocido")
                formatted_results.append(
                    f"**Título**: {paper.get('title', 'Sin título')}\n"
                    f"**Autores**: {authors}\n"
                    f"**Fecha publicación**: {published_date}\n"
                    f"**Resumen**: {paper.get('abstract', 'No disponible')}\n"
                    f"**URLs**: {', '.join(paper.get('sourceFulltextUrls', []))}"
                )
            return "\n\n---\n\n".join(formatted_results)
        except Exception as e:
            return f"⚠️ Error en búsqueda: {str(e)}"

class SearchPapersInput(BaseModel):
    """Input para búsqueda de artículos científicos"""
    query: str = Field(description="Consulta de búsqueda en lenguaje natural")
    max_papers: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Número máximo de artículos a retornar"
    )

class DownloadPaperInput(BaseModel):
    """Input para descarga de papers"""
    url: str = Field(description="URL del documento a descargar")

@tool("search-papers", args_schema=SearchPapersInput)
def search_papers(
    query: str, 
    max_papers: int = 1,
    config: Optional[RunnableConfig] = None
) -> str:
    """Busca artículos académicos usando CORE API. 
    
    Ejemplo:
    {{
        "query": "machine learning applications in healthcare",
        "max_papers": 3
    }}
    """
    try:
        core_api = CoreAPIWrapper.from_config(config)
        return core_api.search(query, max_papers)
    except Exception as e:
        return f"Error crítico: {str(e)}. Notifica al administrador."

@tool("download-paper", args_schema=DownloadPaperInput)
def download_paper(
    url: str,
    config: Optional[RunnableConfig] = None
) -> str:
    """Descarga y extrae texto de un paper académico.
    
    Ejemplo:
    {{
        "url": "https://example.com/paper.pdf"
    }}
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/pdf'
        }
        
        http = urllib3.PoolManager(
            cert_reqs='CERT_NONE',
            headers=headers
        )
        
        for attempt in range(5):
            response = http.request('GET', url)
            if response.status == 200:
                with pdfplumber.open(io.BytesIO(response.data)) as pdf:
                    return "\n".join(page.extract_text() for page in pdf.pages)
            time.sleep(2 ** (attempt + 1))
            
        return "Error: No se pudo descargar el documento después de múltiples intentos"
    except Exception as e:
        return f"Error en descarga: {str(e)}"

@tool("ask-human-feedback")
def ask_human_feedback(question: str) -> str:
    """Solicita feedback humano al usuario. Úsalo solo cuando sea estrictamente necesario.
    
    Ejemplo:
    {{
        "question": "¿Podrías clarificar qué tipo de resultados estás buscando?"
    }}
    """
    return input(f"[Sistema pregunta] {question}\nTu respuesta: ")

# Lista final de herramientas con configuración aplicada
tools = [
    partial(search_papers, config=None),  # Config se inyectará en runtime
    download_paper,
    ask_human_feedback
]

def format_tools_description(tools: List[BaseTool]) -> str:
    """Genera documentación profesional para las herramientas de investigación"""
    tool_docs = []
    for tool in tools:
        params = tool.args_schema.schema() if tool.args_schema else {}
        param_table = "\n".join(
            f"- **{name}**: {schema.get('description', '')} "
            f"(Tipo: {schema.get('type', 'str')}, "
            f"Ejemplo: {schema.get('example', 'N/A')})"
            for name, schema in params.get("properties", {}).items()
        )
        
        example_args = json.dumps(tool.example, indent=2) if hasattr(tool, 'example') else ""
        
        tool_doc = f"""
        ## 🛠️ {tool.name}
        **{tool.description}**

        ### Parámetros:
        {param_table}

        ### Ejemplo de uso:
        ```python
        from agent_tools import {tool.name.replace('-', '_')}

        resultado = {tool.name}(
            {example_args}
        )
        ```
        """
        tool_docs.append(tool_doc)
    
    return "\n\n---\n\n".join(tool_docs)