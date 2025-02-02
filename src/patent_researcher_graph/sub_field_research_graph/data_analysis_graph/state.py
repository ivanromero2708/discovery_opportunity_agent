from typing import List, Optional, Dict, TypedDict
from typing_extensions import Annotated
import operator

# ------------------------------------------------------------
# Data Analysis Graph Input State
# ------------------------------------------------------------
class DataAnalysisInputState(TypedDict, total=False):
    """
    Input state for the Data Analysis Graph.
    
    Inputs:
      - collected_patent_dataset: The raw patent dataset collected for a specific sub-field.
    """
    collected_patent_dataset: List[dict]

# ------------------------------------------------------------
# Data Analysis Graph Output State
# ------------------------------------------------------------
class DataAnalysisOutputState(TypedDict, total=False):
    """
    Output state for the Data Analysis Graph.
    
    Outputs:
      --- Patent Activity Analysis ---
      - patent_activity_trends: JSON data with metrics (e.g., annual filing counts, CAGR).
      - trend_analysis_graph_dir: Directory string for the trend analysis graph PNG.
      - growth_metrics: Numeric growth metrics (e.g., CAGR, percentage increases).
      - temporal_analysis: Temporal analysis data as a string.
      - top_cited_patents_links: List of links for the top 5 cited patents per year.
      
      --- Top Assignee Analysis ---
      - key_players: JSON data (list of dictionaries) for top assignees and associated metrics.
      - top_assignees_graph_dir: Directory string for the Top Assignees graph PNG.
      - key_players_metrics: Metrics data for key players.
      - leading_companies: List of leading companies/institutions.
      - top_assignee_patents_links: List of links for top cited patents among key assignees.
      
      --- Technology Cluster Analysis ---
      - technology_clusters: JSON mapping of technology clusters.
      - tech_cluster_graph_dir: Directory string for the Technology Cluster Map PNG.
      - clusters_definition: List of technology clusters with definitions.
      - top_cluster_patents_links: List of links for the top 5 cited patents per technology cluster.
      
      --- Consolidated Analysis Summary ---
      - consolidated_analysis: Final summary (JSON) of all analytical insights.
    """
    # Patent Activity Analysis
    patent_activity_trends: Optional[list[Dict]]
    trend_analysis_graph_dir: Optional[str]
    growth_metrics: Optional[Dict]
    temporal_analysis: Optional[str]
    top_cited_patents_links: Optional[List[str]]
    
    # Top Assignee Analysis
    key_players: Optional[list[Dict]]
    top_assignees_graph_dir: Optional[str]
    key_players_metrics: Optional[Dict]
    leading_companies: Optional[List[str]]
    top_assignee_patents_links: Optional[List[str]]
    
    # Technology Cluster Analysis
    technology_clusters: Optional[list[Dict]]
    tech_cluster_graph_dir: Optional[str]
    clusters_definition: Optional[List[Dict]]
    top_cluster_patents_links: Optional[List[str]]
    
    # Consolidated Analysis Summary
    consolidated_analysis: Optional[Dict]

# ------------------------------------------------------------
# Unified Data Analysis Graph State (Merging Input & Output)
# ------------------------------------------------------------
class DataAnalysisGraphState(TypedDict, total=False):
    """
    Unified state for the Data Analysis Graph.
    
    This state merges both the input and output keys.
    
    Input:
      - collected_patent_dataset: The raw patent dataset for the sub-field.
    
    Outputs:
      - patent_activity_trends: Aggregated JSON metrics.
      - trend_analysis_graph_dir: Directory for the trend analysis graph PNG.
      - growth_metrics: Numeric growth metrics.
      - temporal_analysis: Temporal analysis as a string.
      - top_cited_patents_links: Links for the top 5 cited patents per year.
      
      - key_players: List of top assignees (merged via reducer).
      - top_assignees_graph_dir: Directory for the Top Assignees graph PNG.
      - key_players_metrics: Metrics for key players.
      - leading_companies: List of leading companies/institutions.
      - top_assignee_patents_links: Links for top cited patents among key assignees.
      
      - technology_clusters: Mapping of technology clusters.
      - tech_cluster_graph_dir: Directory for the Technology Cluster Map PNG.
      - clusters_definition: Definitions for each technology cluster.
      - top_cluster_patents_links: Links for top cited patents per cluster.
      
      - consolidated_analysis: Final summary of all analysis insights.
    """
    # Merge input key
    collected_patent_dataset: List[dict]
    
    # Merge output keys (Patent Activity Analysis)
    patent_activity_trends: Optional[Dict]
    trend_analysis_graph_dir: Optional[str]
    growth_metrics: Optional[Dict]
    temporal_analysis: Optional[str]
    top_cited_patents_links: Optional[List[str]]
    
    # Merge output keys (Top Assignee Analysis)
    key_players: Optional[Annotated[List[Dict], operator.add]]
    top_assignees_graph_dir: Optional[str]
    key_players_metrics: Optional[Dict]
    leading_companies: Optional[List[str]]
    top_assignee_patents_links: Optional[List[str]]
    
    # Merge output keys (Technology Cluster Analysis)
    technology_clusters: Optional[Dict]
    tech_cluster_graph_dir: Optional[str]
    clusters_definition: Optional[List[Dict]]
    top_cluster_patents_links: Optional[List[str]]
    
    # Merge output key (Consolidated Analysis)
    consolidated_analysis: Optional[Dict]
