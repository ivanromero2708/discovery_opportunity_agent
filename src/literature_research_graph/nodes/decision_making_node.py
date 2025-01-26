from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from ..state import AgentState, DecisionMakingOutput
from ..prompts import decision_making_prompt


class DecisionMaking:
    def __init__(self, config: RunnableConfig) -> None:
        self.model = ChatOpenAI(
            model = config.llm_model,
            temperature = config.llm_temperature,
            api_key = config.openai_api_key
        ).with_structured_output(DecisionMakingOutput)
    
    def decision_making_node(self, state: AgentState):
        """Entry point of the workflow. Based on the user query, the model can either respond directly or perform a full research, routing the workflow to the planning node"""
        system_prompt = SystemMessage(content=decision_making_prompt)
        response: DecisionMakingOutput = self.model.invoke([system_prompt] + state["messages"])
        output = {"requires_research": response.requires_research}
        if response.answer:
            output["messages"] = [AIMessage(content=response.answer)]
        return output
    
    def run(self, state: AgentState):
        result = self.decision_making_node(state)
        return result