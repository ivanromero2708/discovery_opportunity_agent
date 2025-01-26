from ..state import AgentState
from .agent_tools import tools
import json
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from ..configuration import AgentConfiguration

class AgentTools:
    def __init__(self):
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Ejecución de herramientas con configuración dinámica"""
        runtime_config = AgentConfiguration.from_runnable_config(config)
        tools_dict = {tool.name: tool for tool in tools}
        
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            # Inyectar API keys dinámicamente
            if tool_call["name"] == "search-papers":
                tool = tools_dict[tool_call["name"]].partial(
                    core_api_key=runtime_config.core_api_key
                )
            else:
                tool = tools_dict[tool_call["name"]]
                
            tool_result = tool.invoke(tool_call["args"])
            
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        
        return {"messages": outputs}