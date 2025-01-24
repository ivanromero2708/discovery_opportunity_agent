from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import ResearchGraphState
from .edges import initiate_all_interviews

from interview_builder_graph.nodes import (
    CreateAnalysts,
    WriteReport,
    WriteIntroduction,
    WriteConclusion,
    FinalizeReport,
    HumanFeedback,
)

from interview_builder_graph.graph import (
    interview_builder,
)

create_analysts = CreateAnalysts()
human_feedback = HumanFeedback()
write_report = WriteReport()
write_introduction = WriteIntroduction()
write_conclusion = WriteConclusion()
finalize_report = FinalizeReport()

# Add nodes and edges 
builder = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analysts.run)
builder.add_node("human_feedback", human_feedback.run)
builder.add_node("conduct_interview", interview_builder.compile())
builder.add_node("write_report",write_report.run)
builder.add_node("write_introduction",write_introduction.run)
builder.add_node("write_conclusion",write_conclusion.run)
builder.add_node("finalize_report",finalize_report.run)

# Logic
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", initiate_all_interviews, ["create_analysts", "conduct_interview"])
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
builder.add_edge("finalize_report", END)

# Compile
memory = MemorySaver()
graph = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)