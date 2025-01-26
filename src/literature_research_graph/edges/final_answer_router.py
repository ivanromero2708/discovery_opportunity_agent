from ..state import AgentState

class FinalAnswerRouter:
    def __init__(self) -> None:
        pass
    
    def final_answer_router(self, state: AgentState):
        """Router to end the workflow or improve the answer."""
        if state["is_good_answer"]:
            return "end"
        else:
            return "planning"
    
    def run(self, state: AgentState):
        return self.final_answer_router(state)