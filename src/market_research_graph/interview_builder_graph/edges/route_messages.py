from ..state import InterviewState
from langchain_core.messages import AIMessage

class RouteMessages:
    def __init__(self) -> None:
        pass
    
    def route_messages(self, state: InterviewState, 
                    name: str = "expert"):
        """ Route between question and answer """
        
        # Get messages
        messages = state["messages"]
        max_num_turns = state.get('max_num_turns',4)

        # Check the number of expert answers 
        num_responses = len(
            [m for m in messages if isinstance(m, AIMessage) and m.name == name]
        )

        # End if expert has answered more than the max turns
        if num_responses >= max_num_turns:
            return 'save_interview'

        # This router is run after each question - answer pair 
        # Get the last question asked to check if it signals the end of discussion
        last_question = messages[-2]
        
        if "Thank you so much for your help" in last_question.content:
            return 'save_interview'
        return "ask_question"
    
    def run(self, state: InterviewState, name: str = "expert"):
        result = self.route_messages(state, name)
        return result