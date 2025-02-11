from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import SubFieldResearchGraphState

from .nodes import (
    CreateSearchEquation,
    RetrievePatentData,
    FetchPatentDetails,
)

from .edges import(
    AsessPatentDataConsistency,
)

create_search_equation = CreateSearchEquation()
retrieve_patent_data = RetrievePatentData()
fetch_patent_details = FetchPatentDetails()
assess_patent_data_consistency = AsessPatentDataConsistency()

# Add nodes and edges
sub_field_research_builder = StateGraph(SubFieldResearchGraphState)
sub_field_research_builder.add_node("create_search_equation", create_search_equation.run)
sub_field_research_builder.add_node("retrieve_patent_data", retrieve_patent_data.run)
sub_field_research_builder.add_node("fetch_patent_details", fetch_patent_details.run)

# Logic
sub_field_research_builder.add_edge(START, "create_search_equation")
sub_field_research_builder.add_edge("create_search_equation", "retrieve_patent_data")
sub_field_research_builder.add_conditional_edges(
    "retrieve_patent_data",
    assess_patent_data_consistency.run,
    {
        "continue": "fetch_patent_details",
        "re_search": "create_search_equation",
    },
)
sub_field_research_builder.add_edge("fetch_patent_details", END)

# Compile
sub_field_research_memory = MemorySaver()
sub_field_research_graph = sub_field_research_builder.compile(checkpointer=sub_field_research_memory)