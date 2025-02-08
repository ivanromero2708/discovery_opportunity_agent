from typing import List, Optional, Dict, TypedDict
from typing_extensions import Annotated
from operator import add
import operator
from ..state import OutlineDeepDivePatentResearch

# ============ Analyst profiles ============ #
class Analyst(TypedDict):
    name: str           # Analyst name.
    affiliation: str    # Analyst affiliation.
    role: str           # Role in research.
    description: str    # Brief description of focus and perspective.

# ============ Input State ============ #
class SubFieldResearchInputState(TypedDict):
    prioritized_sub_fields: List[str]               # Ranked list of sub-field names.
    research_plans: List[Dict]                      # Mapping: sub-field name → research plan (JSON-like dict).

# ============ Output State ============ #
class SubFieldResearchIOutputState(TypedDict):
    list_docx_report_dir: str                      # String with the local dir in which the DOCX report is

# ============ Graph State ============ #
class SubFieldResearchGraphState(TypedDict):
    # === Input: Identification of the sub-field === #
    research_plan: OutlineDeepDivePatentResearch                     # Mapping: sub-field name → research plan (JSON-like dict).
    
    # === 6.1 Create search equation output === #
    search_equation: str
    
    # === 6.2 Download data collection on Google Patents output === #
    patent_documents: List[Dict]
    
    # === 6.3 Assess Patent Data output === #
    collected_patent_dataset: List[Dict]
    
    # === 6.4 Data analysis output === #
    patent_activity_trends: Optional[list[Dict]]
    key_players: Optional[list[Dict]]
    technology_clusters: Optional[list[Dict]]
    
    # === 6.5 Section Analysts output === #
    analysts: List[Analyst]
    
    # === 6.6 Conduct Interview output === #
    sections: Annotated[list, operator.add]         # Send() API key
    
    # === 6.7 Write conclusions output === #
    conclusion: str                                 # Conclusion for the final report
        
    # === 6.8 Write Introduction output === #
    introduction: str                               # Introduction for the final report    
        
    # === 6.9 Render Sub-Field research report output === #
    list_docx_report_dir: str                      # String with the local dir in which the DOCX report is
