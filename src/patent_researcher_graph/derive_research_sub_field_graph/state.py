from typing import List, TypedDict
from typing_extensions import Annotated
import operator
from ..state import DomainRelationship
from pydantic import BaseModel

# Define a Pydantic model for the expected output of this node.
class CoreProcessSubFieldsOutput(BaseModel):
    sub_fields: list[str]

class ResearchSubFieldsInputState(TypedDict):
    # Inherited from the main graph.
    research_statement: str                   # A concise narrative combining the above inputs.
    main_domains: List[DomainRelationship]    # High-level domain map.
    strategic_objectives: str                 # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    
class ResearchSubFieldsOutputState(TypedDict):
    total_sub_fields: List[str]

class ResearchSubFieldsGraphState(TypedDict):
    # Inherited from the main graph.
    research_statement: str                   # A concise narrative combining the above inputs.
    main_domains: List[DomainRelationship]    # High-level domain map.
    technology: str
    strategic_objectives: str                 # Strategic objectives.
    products_services: str
    region: str
    
    # Intermediate outputs (segmentation by various dimensions):
    sub_fields_by_core: List[str]         # E.g., ["Smelting & Upgrading", "Innovative Hydrometallurgical Processes"]
    sub_fields_by_application: List[str]  # E.g., ["Electrodes for Batteries", "Medical Device Applications"]
    sub_fields_by_region: List[str]       # E.g., ["China-Focused Technologies", "US/EU Market Innovations"]
    sub_fields_by_strategic: List[str]    # E.g., ["Key Competitor Portfolios", "White Spaces for R&D"]
    
    # Final consolidated sub-fields.
    total_sub_fields: List[str]
