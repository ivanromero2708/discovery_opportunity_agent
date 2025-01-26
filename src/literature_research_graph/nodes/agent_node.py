from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from ..state import AgentState, DecisionMakingOutput
from ..prompts import agent_prompt
from .agent_tools import tools

class AgentNode:
    def __init__(self, config: RunnableConfig) -> None:
        self.model = ChatOpenAI(
            model = config.llm_model,
            temperature = config.llm_temperature,
            api_key = config.openai_api_key
        ).bind_tools(tools)
    
    def agent_node(self, state: AgentState):
        """Agent call node that uses the LLM with tools to answer the user query."""
        system_prompt = SystemMessage(content=agent_prompt)
        response = self.model.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}
    
    def run(self, state: AgentState):
        result = self.agent_node(state)
        return result