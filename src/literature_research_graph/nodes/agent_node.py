from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from ..state import AgentState
from ..configuration import AgentConfiguration
from .agent_tools import tools

class AgentNode:
    def __init__(self):
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Nodo principal del agente con configuración dinámica"""
        runtime_config = AgentConfiguration.from_runnable_config(config)
        
        model = ChatOpenAI(
            model=runtime_config.llm_model,
            temperature=runtime_config.llm_temperature,
            api_key=runtime_config.openai_api_key
        ).bind_tools(tools)

        response = model.invoke(state["messages"])
        return {"messages": [response]}