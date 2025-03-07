from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import PatentResearchGraphState
from .edges import(
    InitiateOutlineDeepDivePatentResearch,
    InitiateAllSubFieldResearch
)

from .nodes import (
    DefineOverallResearchDomain,
    CreateHighLevelDomainResearchMap,
    SelectResearchSubFields,
    OutlineDeepDiveResearchSubFields,
    ConsolidateReport,
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
initiate_outline_deep_dive_patent_research = InitiateOutlineDeepDivePatentResearch()
initiate_all_sub_field_research = InitiateAllSubFieldResearch()

"""
iniatiate_all_sub_field_research = InitiateAllSubFieldResearch()
consolidate_report = ConsolidateReport()
"""


# Add nodes and edges 
patent_research_builder = StateGraph(PatentResearchGraphState)
patent_research_builder.add_node("define_overall_research_domain", define_overall_research_domain.run)
patent_research_builder.add_node("create_high_level_domain_research_map", create_high_level_domain_research_map.run)
patent_research_builder.add_node("derive_sub_research_fields", derive_sub_research_fields_builder.compile())
patent_research_builder.add_node("select_research_sub_fields", select_research_sub_fields.run)
patent_research_builder.add_node("outline_deep_dive_research_sub_fields", outline_deep_dive_research_sub_fields.run)
patent_research_builder.add_node("sub_field_research", sub_field_research_builder.compile())

# Logic
patent_research_builder.add_edge(START, "define_overall_research_domain")
patent_research_builder.add_edge("define_overall_research_domain", "create_high_level_domain_research_map")
patent_research_builder.add_edge("create_high_level_domain_research_map", "derive_sub_research_fields")
patent_research_builder.add_edge("derive_sub_research_fields", "select_research_sub_fields")
patent_research_builder.add_conditional_edges("select_research_sub_fields", initiate_outline_deep_dive_patent_research.run, ["outline_deep_dive_research_sub_fields"])
patent_research_builder.add_edge("outline_deep_dive_research_sub_fields", initiate_all_sub_field_research.run, ["sub_field_research"])
patent_research_builder.add_edge("sub_field_research", END)

# Compile
patent_research_memory = MemorySaver()
patent_research_graph = patent_research_builder.compile(checkpointer=patent_research_memory)