from ..state import AgentState
from .agent_tools import tools
import json
from langchain_core.messages import ToolMessage

tools_dict = {tool.name: tool for tool in tools}

class AgentTools:
    def __init__(self) -> None:
        pass
    
    def tools_node(self, state: AgentState):
        """Tool call node that executes the tools based on the plan."""
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = tools_dict[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    
    def run(self, state: AgentState):
        result = self.tools_node(state)
        return result