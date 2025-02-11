from typing import List, Optional, Dict, TypedDict, Union
from datetime import datetime
from typing_extensions import Annotated
from operator import add
import operator
from ..state import OutlineDeepDivePatentResearch
from langchain_core.messages import (
    BaseMessage,
)
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# Pydantic model for enriched patent details (data validation)
# -------------------------------------------------------------------
class PatentDetails(BaseModel):
    title: str = Field(..., description="Patent title.")
    snippet: str = Field(..., description="Patent snippet.")
    assignee: str = Field(..., description="Patent assignee.")
    publication_number: str = Field(..., description="Patent publication number.")
    link: str = Field(..., description="URL of the patent detail page.")
    priority_date: Optional[datetime] = Field(None, description="Priority date of the patent.")
    abstract: str = Field(..., description="Patent abstract.")
    claims: str = Field(..., description="Patent claims.")
    legal_status: Optional[str] = Field(None, description="Patent legal status.")
    forward_citations: Union[int, str] = Field(..., description="Number of forward citations or error message.")

# ============ Analyst profiles ============ #
class Analyst(TypedDict):
    name: str           # Analyst name.
    affiliation: str    # Analyst affiliation.
    role: str           # Role in research.
    description: str    # Brief description of focus and perspective.


class PatentSearchEquation(BaseModel):
    search_equation: str = Field(..., definition = "The generated search equation for retrieving patent data from Google Patents.")

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
    improve_search_equation: str
    
    # === 6.2 Download data collection on Google Patents output === #
    initial_patent_documents: Dict
    
    # === 6.3 Assess Patent Data output === #
    enriched_patent_documents: List[PatentDetails]
    
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
