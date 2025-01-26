from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from ..state import AgentState, JudgeOutput
from ..prompts import judge_prompt
from ..configuration import AgentConfiguration

class JudgeNode:
    def __init__(self):
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Nodo de evaluación con configuración dinámica"""
        runtime_config = AgentConfiguration.from_runnable_config(config)
        
        model = ChatOpenAI(
            model=runtime_config.llm_model,
            temperature=runtime_config.llm_temperature,
            api_key=runtime_config.openai_api_key
        ).with_structured_output(JudgeOutput)

        system_prompt = SystemMessage(content=judge_prompt)
        response = model.invoke([system_prompt] + state["messages"])
        
        output = {
            "is_good_answer": response.is_good_answer,
            "num_feedback_requests": state.get("num_feedback_requests", 0) + 1
        }
        
        if response.feedback:
            output["messages"] = [AIMessage(content=response.feedback)]
            
        return output