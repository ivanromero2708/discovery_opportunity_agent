from ..state import AgentState
from langchain_core.runnables import RunnableConfig

class ShouldContinue:
    def __init__(self) -> None:
        pass
    
    def should_continue(self, state: AgentState, config: RunnableConfig):
        last_message = state["messages"][-1]
        has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
        max_cycles_reached = state.get("research_cycles", 0) >= config.max_research_cycles
        
        return "continue" if (has_tool_calls and not max_cycles_reached) else "end"
    
    def run(self, state: AgentState, config: RunnableConfig):
        return {"should_continue": self.should_continue(state, config)}