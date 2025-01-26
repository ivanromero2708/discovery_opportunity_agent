from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from ..state import AgentState
from ..prompts import planning_prompt, format_tools_description
from ..configuration import AgentConfiguration
from .agent_tools import tools

class Planning:
    def __init__(self):
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Nodo de planificación con configuración dinámica"""
        runtime_config = AgentConfiguration.from_runnable_config(config)
        
        model = ChatOpenAI(
            model=runtime_config.llm_model,
            temperature=runtime_config.llm_temperature,
            api_key=runtime_config.openai_api_key
        )

        system_prompt = SystemMessage(
            content=planning_prompt.format(tools=format_tools_description(tools))
        )
        response = model.invoke([system_prompt] + state["messages"])
        
        return {"messages": [response]}