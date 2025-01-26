from ..state import AgentState

class Router:
    def __init__(self) -> None:
        pass
    
    def router(self, state: AgentState):
        """Router directing the user query"""
        return "planning" if state["requires_research"] else "end"
    
    def run(self, state: AgentState):
        return self.router(state)