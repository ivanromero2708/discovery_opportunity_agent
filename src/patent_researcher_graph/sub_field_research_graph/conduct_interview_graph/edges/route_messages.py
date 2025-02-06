from langchain_core.messages import AIMessage
from ..state import InterviewState

class RouteMessages:
    def __init__(self) -> None:
        pass

    def route_messages(self, state: InterviewState, name: str = "expert"):
        """
        Dummy routing logic:
          - If there is at least one AIMessage in the state, return "save_interview"
          - Otherwise, return "ask_question"
        """
        messages = state.get("messages", [])
        if messages and any(isinstance(m, AIMessage) for m in messages):
            return "save_interview"
        return "ask_question"

    def run(self, state: InterviewState, name: str = "expert"):
        return self.route_messages(state, name)
