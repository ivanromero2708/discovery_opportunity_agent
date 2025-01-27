# src/literature_research_graph/nodes/tools_node.py

import json
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from literature_research_graph.configuration import AgentConfiguration
from ..state import AgentState
from .agent_tools import tools

class AgentTools:
    def __init__(self):
        pass
    
    def run(self, state: AgentState, config: RunnableConfig):
        """Ejecución de herramientas con configuración dinámica"""
        # 1) Convertir el dict config en nuestra configuración de pydantic
        runtime_config = AgentConfiguration.from_runnable_config(config)
        
        # 2) Pasar todas las herramientas a un diccionario, indexadas por su nombre
        tools_dict = {tool.name: tool for tool in tools}
        
        outputs = []
        # 3) Recorremos las tool_calls de la última respuesta
        for tool_call in state["messages"][-1].tool_calls:
            # 3.1) Recuperar la herramienta
            tool_name = tool_call["name"]
            tool = tools_dict[tool_name]
            
            # 3.2) Inyectar la API key (u otros parámetros) en los args si lo deseas
            #     Por ejemplo, si es "search-papers", agregamos la core_api_key.
            args = tool_call["args"]
            if tool_name == "search-papers":
                args["core_api_key"] = runtime_config.core_api_key
            
            # 3.3) Invocar la herramienta con los args ya actualizados
            tool_result = tool.invoke(args)

            # 3.4) Añadir el resultado como ToolMessage
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_name,
                    tool_call_id=tool_call["id"],
                )
            )
        
        return {"messages": outputs}
