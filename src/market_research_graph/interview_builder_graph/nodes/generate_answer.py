from ..prompts import answer_instructions
from ..state import InterviewState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
import os
from utils.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, LANGCHAIN_TRACING_V2

class GenerateAnswer:
    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
    
    def generate_answer(self, state: InterviewState):
        """ Node to answer a question """

        # Get state
        analyst = state["analyst"]
        messages = state["messages"]
        context = state["context"]

        # Answer question
        system_message = answer_instructions.format(goals=analyst.persona, context=context)
        answer = self.model.invoke([SystemMessage(content=system_message)]+messages)
                
        # Name the message as coming from the expert
        answer.name = "expert"
        
        # Append it to state
        return {"messages": [answer]}
    
    def run(self, state: InterviewState):
        result = self.generate_answer(state)
        return result
    


