# should_continue.py

from ..state import AgentState
from langchain_core.runnables import RunnableConfig
from ..configuration import AgentConfiguration

class ShouldContinue:
    def __init__(self) -> None:
        pass
    
    def should_continue(self, state: AgentState, runtime_config: AgentConfiguration) -> str:
        """Retorna 'continue' o 'end' según la lógica."""

        last_message = state["messages"][-1]
        has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
        
        # Obtenemos el número de ciclos
        current_research_cycles = state.get("research_cycles", 0)

        # Comparamos con lo definido en la config
        max_cycles_reached = current_research_cycles >= runtime_config.max_research_cycles

        # Decidimos si continuar o terminar
        return "continue" if (has_tool_calls and not max_cycles_reached) else "end"
    
    def run(self, state: AgentState, config: RunnableConfig):
        # 1) Creamos la runtime_config
        runtime_config = AgentConfiguration.from_runnable_config(config)
        # 2) Llamamos a should_continue
        return self.should_continue(state, runtime_config)
