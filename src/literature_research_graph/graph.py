from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState

from .configuration import AgentConfiguration
from .nodes import (
    DecisionMaking,
    Planning,
    AgentTools,
    AgentNode,
    JudgeNode,
)

from .edges import (
    Router,
    ShouldContinue,
    FinalAnswerRouter,
)

# Llamado a nodos
decision_making_node = DecisionMaking()
planning_node = Planning()
tools_node = AgentTools()
agent_node = AgentNode()
judge_node = JudgeNode()

# Llamado a edges
router = Router()
should_continue = ShouldContinue()
final_answer_router = FinalAnswerRouter()

# Registro de nodos
workflow = StateGraph(AgentState, config_schema=AgentConfiguration)
workflow.add_node("decision_making", decision_making_node.run)
workflow.add_node("planning", planning_node.run)
workflow.add_node("tools", tools_node.run)
workflow.add_node("agent", agent_node.run)
workflow.add_node("judge", judge_node.run)

# Configuracion de flujo
workflow.set_entry_point("decision_making")

# Add edges between nodes
workflow.add_conditional_edges(
    "decision_making",
    router.run,
    {
        "planning": "planning",
        "end": END,
    }
)

workflow.add_edge("planning", "agent")
workflow.add_edge("tools", "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue.run,
    {
        "continue": "tools",
        "end": "judge",
    },
)

workflow.add_conditional_edges(
    "judge",
    final_answer_router.run,
    {
        "planning": "planning",
        "end": END,
    }
)

# Compilación del flujo
memory = MemorySaver()
workflow = workflow.compile(checkpointer=memory).with_config(run_name="Agent")