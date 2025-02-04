from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AnyMessage
from typing import Dict
from ..state import PatentResearchGraphState
from ..prompts import prompt_generate_research_domain
from ..configuration import Configuration
from langchain_openai import ChatOpenAI

class DefineOverallResearchDomain:
    def __init__(self):
        pass
    
    def define_overall_research_domain(self, state: PatentResearchGraphState, config: RunnableConfig) -> Dict:
        """
        Función del nodo: Define the Overall Research Domain.
        
        Entrada (state):
        - company_name: str nombre de la empresa
        - industry: str.
        - products_services: str.
        - region: str.
        - technology: List[str] (o str, según lo configurado en la UI).
        - strategic_objectives: List[str].
        
        Salida:
        - research_statement: Declaración de investigación generada, que combine las entradas para guiar el análisis de patentes.
        """
        company_name = state["company_name"]
        industry = state["industry"]
        products_services = state["products_services"]
        region = state["region"]
        technology = state["technology"]
        strategic_objectives = state["strategic_objectives"]
        
        configurable = Configuration.from_runnable_config(config)
        planner_llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        
        system_instructions = prompt_generate_research_domain.format(
            company_name = company_name,
            industry = industry,
            products_services = products_services,
            region = region,
            technology = technology,
            strategic_objectives = strategic_objectives,
        )
        
        # Crear el mensaje del sistema y el mensaje de instrucción
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(content="Generate the research statement.")

        # Invocar al LLM
        response = planner_llm.invoke([system_msg, instruction_msg])

        # ✅ Corregir la extracción de respuesta
        research_statement = response.content if hasattr(response, "content") else "No research statement generated."

        return {"research_statement": research_statement}
    
    def run(self, state: PatentResearchGraphState, config: RunnableConfig):
        return self.define_overall_research_domain(state, config)
