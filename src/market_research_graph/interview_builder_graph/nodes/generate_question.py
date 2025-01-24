from ..state import InterviewState
from ..prompts import question_instructions
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
import os
from utils.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

class GenerateQuestion:
    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            api_key=OPENAI_API_KEY  # <-- Usar variable centralizada
        )

    def generate_question(self, state: InterviewState):
        """ Node to generate a question """

        # Get state
        analyst = state["analyst"]
        messages = state["messages"]

        # Generate question 
        system_message = question_instructions.format(goals=analyst.persona)
        question = self.model.invoke([SystemMessage(content=system_message)]+messages)
            
        # Write messages to state
        return {"messages": [question]}
    
    def run(self, state:InterviewState):
        result = self.generate_question(state)
        return result