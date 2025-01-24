from ..state import InterviewState
from langchain_core.messages import get_buffer_string


class SaveInterview:
    def __init__(self) -> None:
        pass
    
    def save_interview(self, state: InterviewState):
        
        """ Save interviews """

        # Get messages
        messages = state["messages"]
        
        # Convert interview to a string
        interview = get_buffer_string(messages)
        
        # Save to interviews key
        return {"interview": interview}
    
    def run(self, state: InterviewState):
        result = self.save_interview(state)
        return result
