from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from ..state import AgentState, DecisionMakingOutput
from ..prompts import decision_making_prompt
from ..configuration import AgentConfiguration
from langchain_core.runnables import RunnableConfig


class DecisionMaking:
    def __init__(self, config: RunnableConfig) -> None:
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Nodo de toma de decisiones con configuración dinámica"""
        # Obtener configuración en tiempo de ejecución
        runtime_config = AgentConfiguration.from_runnable_config(config)
        
        # Inicializar modelo con configuración actual
        model = ChatOpenAI(
            model=runtime_config.llm_model,
            temperature=runtime_config.llm_temperature,
            api_key=runtime_config.openai_api_key
        ).with_structured_output(DecisionMakingOutput)

        system_prompt = SystemMessage(content=decision_making_prompt)
        response = model.invoke([system_prompt] + state["messages"])
        
        return {
            "requires_research": response.requires_research,
            "messages": [AIMessage(content=response.answer)] if response.answer else []
        }