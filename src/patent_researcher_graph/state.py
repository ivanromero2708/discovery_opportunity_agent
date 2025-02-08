from typing import List, TypedDict
from typing_extensions import Annotated
import operator
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from pydantic import BaseModel

from pydantic import BaseModel, Field
from typing import List

class OutlineDeepDivePatentResearch(BaseModel):
    """
    A structured model defining the key attributes required to conduct a patent research study
    for a specific sub-field within an industry.
    """
    industry_context: str = Field(..., description="The broader industry where the sub-field operates. Example: 'Artificial Intelligence & Digital Marketing'.")
    
    technology_domain: str = Field(..., description="The technological area relevant to the sub-field. Example: 'AI-powered Ad Targeting and Content Optimization'.")
    
    key_applications: List[str] = Field(..., description="The primary applications of the technology in the industry. Example: ['B2B branding campaigns', 'Automated ad creation', 'User engagement tracking'].")
    
    research_objective: str = Field(..., description="The main goal of the patent research study for this sub-field. Example: 'To analyze patent trends in AI-driven B2B marketing technologies on TikTok'.")
    
    supporting_questions: List[str] = Field(..., description="Additional research questions that guide the study. Example: ['Which companies dominate AI-driven marketing patents?', 'What are the key innovations in AI-powered content generation?', 'How is AI being used to track B2B engagement on TikTok?'].")
    
    strategic_relevance: str = Field(..., description="Why this sub-field is important for business, innovation, or market strategy. Example: 'AI is transforming digital advertising, particularly for B2B companies leveraging TikTok for lead generation'.")

# Define a Pydantic model for a single domain relationship.
class DomainRelationship(BaseModel):
    domain: str
    elements: List[str]
    relationship: str

# Define a wrapper model to represent the output as a JSON array.
class DomainRelationshipsOutput(BaseModel):
    domains: List[DomainRelationship]

class OutlineDeepDivePatentResearchGraphState(TypedDict):
    company_name: str                                           # e.g., {"name": "EcoBattery Inc.", "background": "A leader in sustainable battery technologies with extensive R&D."}
    industry: str                                               # e.g., "Energy Storage & Battery Manufacturing"
    products_services: str                                      # e.g., ["Advanced lithium-titanate battery electrodes"]
    region: str                                                 # e.g., ["Asia", "Europe"]
    technology: str                                             # e.g., ["Li-titanate electrode innovation, including advanced doping techniques"]
    strategic_objectives: str                                   # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    prioritized_sub_field: str
    research_plans: OutlineDeepDivePatentResearch

class PatentResearchGraphInputState(TypedDict):
    company_name: str                                           # e.g., {"name": "EcoBattery Inc.", "background": "A leader in sustainable battery technologies with extensive R&D."}
    industry: str                                               # e.g., "Energy Storage & Battery Manufacturing"
    products_services: str                                      # e.g., ["Advanced lithium-titanate battery electrodes"]
    region: str                                                 # e.g., ["Asia", "Europe"]
    technology: str                                             # e.g., ["Li-titanate electrode innovation, including advanced doping techniques"]
    strategic_objectives: str                                   # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    number_sub_fields: int

class PatentResearchGraphOutputState(TypedDict):
    consolidated_docx_report_dir: str                           # A directory string indicating where the consolidated DOCX report is stored.

# Overall state for the Patent Researcher Graph.
class PatentResearchGraphState(TypedDict):
    # --- Process 1: Define the Overall Research Domain (Inputs) ---
    company_name: str                                           # e.g., {"name": "EcoBattery Inc.", "background": "A leader in sustainable battery technologies with extensive R&D."}
    industry: str                                               # e.g., "Energy Storage & Battery Manufacturing"
    products_services: str                                      # e.g., ["Advanced lithium-titanate battery electrodes"]
    region: str                                                 # e.g., ["Asia", "Europe"]
    technology: str                                             # e.g., ["Li-titanate electrode innovation, including advanced doping techniques"]
    strategic_objectives: str                                                               # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    number_sub_fields: int
    
    # --- Process 1 Output ---
    research_statement: str                                                                 # A concise narrative combining the above inputs.
    
    # --- Process 2 Output ---
    main_domains: List[DomainRelationship]                                                  # High-level domain map (each dict contains keys like "domain", "elements", "relationship").
    
    # --- Process 3 Output: Derived Research Sub-Fields ---
    total_sub_fields: List[str]
    
    # --- Process 4 Output: Prioritized Sub-Field List & Research Plans ---
    prioritized_sub_fields: List[str]                                                       # Ranked list of sub-field names.
    research_plans: Annotated[List[OutlineDeepDivePatentResearch], operator.add]            # Mapping: sub-field name → research plan (JSON-like dict).
    
    # --- Process 6 Output: List of Research Report Sub-Fields ---
    list_docx_report_dir: Annotated[List[str], operator.add]    # Each str holds the report directory.
    
    # --- Final Output (for example, a consolidated DOCX report directory) ---
    consolidated_docx_report_dir: str                           # A directory string indicating where the consolidated DOCX report is stored.
    
    # --- Debugging / Iterative Communication ---
    messages: Annotated[List[AnyMessage], add_messages]
