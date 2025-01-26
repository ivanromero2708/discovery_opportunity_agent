from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from ..state import AgentState, JudgeOutput
from ..prompts import judge_prompt

class JudgeNode:
    def __init__(self, config: RunnableConfig) -> None:
        self.model = ChatOpenAI(
            model = config.llm_model,
            temperature = config.llm_temperature,
            api_key = config.openai_api_key
        ).with_structured_output(JudgeOutput)
    
    # Judge node
    def judge_node(self, state: AgentState):
        """Node to let the LLM judge the quality of its own final answer."""
        # End execution if the LLM failed to provide a good answer twice.
        num_feedback_requests = state.get("num_feedback_requests", 0)
        if num_feedback_requests >= 2:
            return {"is_good_answer": True}

        system_prompt = SystemMessage(content=judge_prompt)
        response: JudgeOutput = self.model.invoke([system_prompt] + state["messages"])
        output = {
            "is_good_answer": response.is_good_answer,
            "num_feedback_requests": num_feedback_requests + 1
        }
        if response.feedback:
            output["messages"] = [AIMessage(content=response.feedback)]
        return output
    
    def run(self, state: AgentState):
        result = self.judge_node(state)
        return result