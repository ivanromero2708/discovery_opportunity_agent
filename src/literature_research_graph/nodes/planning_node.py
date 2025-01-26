from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from ..state import AgentState
from ..prompts import planning_prompt, format_tools_description
from .agent_tools import tools

class Planning:
    def __init__(self, config: RunnableConfig) -> None:
        self.model = ChatOpenAI(
            model = config.llm_model,
            temperature = config.llm_temperature,
            api_key = config.openai_api_key
        )
    
    # Planning node
    def planning_node(self, state: AgentState):
        """Planning node that creates a step by step plan to answer the user query."""
        system_prompt = SystemMessage(content=planning_prompt.format(tools=format_tools_description(tools)))
        response = self.model.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}

    
    def run(self, state: AgentState):
        result = self.planning_node(state)
        return result