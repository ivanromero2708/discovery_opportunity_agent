from ..state import InterviewState
from ..prompts import question_instructions
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
import os

class GenerateQuestion:
    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")  # <-- Aquí
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