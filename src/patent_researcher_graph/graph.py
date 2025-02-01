from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import PatentResearchGraphState
from .edges.initiate_all_sub_field_research import InitiateAllSubFieldResearch

from .nodes import (
    DefineOverallResearchDomain,
    CreateHighLevelDomainResearchMap,
    SelectResearchSubFields,
    OutlineDeepDiveResearchSubFields,
    ConsolidateReport,
    RenderReport, 
    FinalizeReport,   
)

from .sub_field_research_graph.graph import (
    sub_field_research_builder,
)

from .derive_research_sub_field_graph.graph import (
    derive_sub_research_fields_builder,
)

define_overall_research_domain = DefineOverallResearchDomain()
create_high_level_domain_research_map = CreateHighLevelDomainResearchMap()

select_research_sub_fields = SelectResearchSubFields()
outline_deep_dive_research_sub_fields = OutlineDeepDiveResearchSubFields()
iniatiate_all_sub_field_research = InitiateAllSubFieldResearch()
consolidate_report = ConsolidateReport()
finalize_report = FinalizeReport()
render_report = RenderReport()

# Add nodes and edges 
patent_research_builder = StateGraph(PatentResearchGraphState)
patent_research_builder.add_node("define_overall_research_domain", define_overall_research_domain.run)
patent_research_builder.add_node("create_high_level_domain_research_map", create_high_level_domain_research_map.run)
patent_research_builder.add_node("derive_sub_research_fields", derive_sub_research_fields_builder.compile())
patent_research_builder.add_node("select_research_sub_fields", select_research_sub_fields.run)
patent_research_builder.add_node("outline_deep_dive_research_sub_fields", outline_deep_dive_research_sub_fields.run)
patent_research_builder.add_node("sub_field_research", sub_field_research_builder.compile())
patent_research_builder.add_node("consolidate_report", consolidate_report.run)
patent_research_builder.add_node("finalize_report", finalize_report.run)
patent_research_builder.add_node("render_report", render_report.run)

# Logic
patent_research_builder.add_edge(START, "define_overall_research_domain")
patent_research_builder.add_edge("define_overall_research_domain", "create_high_level_domain_research_map")
patent_research_builder.add_edge("create_high_level_domain_research_map", "derive_sub_research_fields")
patent_research_builder.add_edge("derive_sub_research_fields", "select_research_sub_fields")
patent_research_builder.add_edge("select_research_sub_fields", "outline_deep_dive_research_sub_fields")
patent_research_builder.add_conditional_edges("outline_deep_dive_research_sub_fields", iniatiate_all_sub_field_research.run, ["sub_field_research"])
patent_research_builder.add_edge("sub_field_research", "consolidate_report")
patent_research_builder.add_edge("consolidate_report", "finalize_report")
patent_research_builder.add_edge("finalize_report", "render_report")
patent_research_builder.add_edge("render_report", END)

# Compile
patent_research_memory = MemorySaver()
patent_research_graph = patent_research_builder.compile(checkpointer=patent_research_memory)