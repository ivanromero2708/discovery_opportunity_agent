from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import DataAnalysisGraphState

from .nodes import (
    PatentActivity,
    KeyPlayers,
    TechnologyClusters,
    ConsolidateDataAnalysis,    
)

patent_activity_analysis = PatentActivity()
key_players_analysis = KeyPlayers()
technology_clusters_analysis = TechnologyClusters()
consolidate_data_analysis = ConsolidateDataAnalysis()

# Add nodes and edges
data_analysis_builder = StateGraph(DataAnalysisGraphState)
data_analysis_builder.add_node("patent_activity_analysis", patent_activity_analysis.run)
data_analysis_builder.add_node("key_players_analysis", key_players_analysis.run)
data_analysis_builder.add_node("technology_clusters_analysis", technology_clusters_analysis.run)

# Logic
data_analysis_builder.add_edge(START, "patent_activity_analysis")
data_analysis_builder.add_edge(START, "key_players_analysis")
data_analysis_builder.add_edge(START, "technology_clusters_analysis")
data_analysis_builder.add_edge(["patent_activity_analysis", "key_players_analysis", "technology_clusters_analysis"], "consolidate_data_analysis")
data_analysis_builder.add_edge("consolidate_data_analysis", END)

# Compile
data_analysis_memory_saver = MemorySaver()
data_analysis_graph = data_analysis_builder.compile(checkpointer=data_analysis_memory_saver)