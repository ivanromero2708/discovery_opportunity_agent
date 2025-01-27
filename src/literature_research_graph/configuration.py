# configuration.py

import os
from dotenv import load_dotenv
from typing import Any, Optional
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig

# Carga automáticamente las variables de entorno del archivo .env
load_dotenv()

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

class AgentConfiguration(BaseModel):
    """
    Configuración para el agente de investigación 
    (p.ej., en literature_research_graph).
    """

    max_research_cycles: int = Field(
        default=3,
        description="Número máximo de ciclos de investigación antes de terminar el flujo."
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="El modelo LLM seleccionado."
    )
    llm_temperature: float = Field(
        default=0.0,
        description="La temperatura a usar con el LLM."
    )
    openai_api_key: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", ""),
        description="OpenAI API key cargada desde .env."
    )
    core_api_key: str = Field(
        default_factory=lambda: os.getenv("CORE_API_KEY", ""),
        description="CORE API key para búsquedas académicas."
    )
    LANGCHAIN_API_KEY: str = Field(
        default_factory=lambda: os.getenv("LANGCHAIN_API_KEY", ""),
        description="Langchain/LangSmith API key para tracking, opcional."
    )

    @classmethod
    def from_runnable_config(
        cls,
        config: Optional[RunnableConfig] = None
    ) -> "AgentConfiguration":
        """
        Genera la configuración final usando:
          1) Valores por defecto o leídos de .env
          2) Sobrescritura con config["configurable"], si existe.
        """
        # Crea una instancia base con los defaults / .env
        instance = cls()

        if config:
            # Lee el dict "configurable" (si existe)
            configurable = config.get("configurable", {})
            
            # Para cada campo que desees sobrescribir
            if "max_research_cycles" in configurable:
                instance.max_research_cycles = configurable["max_research_cycles"]
            if "llm_model" in configurable:
                instance.llm_model = configurable["llm_model"]
            if "llm_temperature" in configurable:
                instance.llm_temperature = configurable["llm_temperature"]
            if "openai_api_key" in configurable:
                instance.openai_api_key = configurable["openai_api_key"]
            if "core_api_key" in configurable:
                instance.core_api_key = configurable["core_api_key"]
            if "LANGCHAIN_API_KEY" in configurable:
                instance.LANGCHAIN_API_KEY = configurable["LANGCHAIN_API_KEY"]

        return instance
