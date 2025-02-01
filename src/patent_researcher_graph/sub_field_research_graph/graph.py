from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import SubFieldResearchGraphState
from .edges.assess_patent_collection_script import AssessPatentCollection
from .edges.initiate_all_interviews_script import InitiateAllInterviews

from .nodes import (
    CreateSearchEquation,
    DownloadDataCollection,
    CreateSectionAnalysts,
    WriteConclusionSubFieldReport,
    WriteIntroductionSubFieldReport,
    WriteSubFieldReport,
)

from .conduct_interview_graph.graph import (
    conduct_interview_builder,
)

from .data_analysis_graph.graph import (
    data_analysis_builder,
)

create_search_equation = CreateSearchEquation()
download_data_collection = DownloadDataCollection()
assess_patent_collection = AssessPatentCollection()

create_section_analysts = CreateSectionAnalysts()
initiate_all_interviews = InitiateAllInterviews()
write_conclusion_sub_field_report = WriteConclusionSubFieldReport()
write_introduction_sub_field_report = WriteIntroductionSubFieldReport()
write_sub_field_report = WriteSubFieldReport()

# Add nodes and edges
sub_field_research_builder = StateGraph(SubFieldResearchGraphState)
sub_field_research_builder.add_node("create_search_equation", create_search_equation.run)
sub_field_research_builder.add_node("download_data_collection", download_data_collection.run)
sub_field_research_builder.add_node("data_analysis", data_analysis_builder.compile())
sub_field_research_builder.add_node("create_section_analysts", create_section_analysts.run)
sub_field_research_builder.add_node("conduct_interview", conduct_interview_builder.compile())
sub_field_research_builder.add_node("write_introduction_sub_field_report", write_introduction_sub_field_report.run)
sub_field_research_builder.add_node("write_conclusion_sub_field_report", write_conclusion_sub_field_report.run)
sub_field_research_builder.add_node("write_sub_field_report", write_sub_field_report.run)

# Logic
sub_field_research_builder.add_edge(START, "create_search_equation")
sub_field_research_builder.add_edge("create_search_equation", "download_data_collection")
sub_field_research_builder.add_conditional_edges("download_data_collection", assess_patent_collection.run, ["create_search_equation", "data_analysis"])
sub_field_research_builder.add_edge("data_analysis", "create_section_analysts")
sub_field_research_builder.add_conditional_edges("create_section_analysts", initiate_all_interviews.run, ["conduct_interview"])
sub_field_research_builder.add_edge("conduct_interview", "write_introduction_sub_field_report")
sub_field_research_builder.add_edge("conduct_interview", "write_conclusion_sub_field_report")
sub_field_research_builder.add_edge(["write_conclusion_sub_field_report", "write_introduction_sub_field_report"], "write_sub_field_report")
sub_field_research_builder.add_edge("write_sub_field_report", END)

# Compile
sub_field_research_memory = MemorySaver()
sub_field_research_graph = sub_field_research_builder.compile(checkpointer=sub_field_research_memory)