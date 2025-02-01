from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import ResearchSubFieldsGraphState

from .nodes import (
    SubdivideByCoreProcessTechnology,
    SubdivideByEndApplication,
    SubdivideByMarketFocus,
    SubdivideByStrategicAngle,
    ConsolidateSubResearchFields,
)

subdivide_by_core_process_technology = SubdivideByCoreProcessTechnology()
subdivide_by_end_application = SubdivideByEndApplication()
subdivide_by_market_focus = SubdivideByMarketFocus()
subdivide_by_strategic_angle = SubdivideByStrategicAngle()
consolidate_sub_research_fields = ConsolidateSubResearchFields()

# Add nodes and edges 
derive_sub_research_fields_builder = StateGraph(ResearchSubFieldsGraphState)
derive_sub_research_fields_builder.add_node("subdivide_by_core_process_technology", subdivide_by_core_process_technology.run)
derive_sub_research_fields_builder.add_node("subdivide_by_end_application", subdivide_by_end_application.run)
derive_sub_research_fields_builder.add_node("subdivide_by_market_focus", subdivide_by_market_focus.run)
derive_sub_research_fields_builder.add_node("subdivide_by_strategic_angle", subdivide_by_strategic_angle.run)
derive_sub_research_fields_builder.add_node("consolidate_sub_research_fields", consolidate_sub_research_fields.run)

# Logic
derive_sub_research_fields_builder.add_edge(START, "subdivide_by_core_process_technology")
derive_sub_research_fields_builder.add_edge(START, "subdivide_by_end_application")
derive_sub_research_fields_builder.add_edge(START, "subdivide_by_market_focus")
derive_sub_research_fields_builder.add_edge(START, "subdivide_by_strategic_angle")
derive_sub_research_fields_builder.add_edge(["subdivide_by_core_process_technology", "subdivide_by_end_application", "subdivide_by_market_focus", "subdivide_by_strategic_angle"], "consolidate_sub_research_fields")
derive_sub_research_fields_builder.add_edge("consolidate_sub_research_fields", END)

# Compile
derive_sub_research_fields_memory = MemorySaver()
derive_sub_research_fields_graph = derive_sub_research_fields_builder.compile(checkpointer=derive_sub_research_fields_memory)