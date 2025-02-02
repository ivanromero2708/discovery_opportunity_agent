from typing import List, TypedDict
from typing_extensions import Annotated
import operator
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class PatentResearchGraphInputState(TypedDict):
    company_name: str                         # e.g., {"name": "EcoBattery Inc.", "background": "A leader in sustainable battery technologies with extensive R&D."}
    industry: str                             # e.g., "Energy Storage & Battery Manufacturing"
    products_services: str                    # e.g., ["Advanced lithium-titanate battery electrodes"]
    region: str                               # e.g., ["Asia", "Europe"]
    technology: str                           # e.g., ["Li-titanate electrode innovation, including advanced doping techniques"]
    strategic_objectives: str                 # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    number_sub_fields: int

class PatentResearchGraphOutputState(TypedDict):
    consolidated_docx_report_dir: str         # A directory string indicating where the consolidated DOCX report is stored.

# Overall state for the Patent Researcher Graph.
class PatentResearchGraphState(TypedDict):
    # --- Process 1: Define the Overall Research Domain (Inputs) ---
    company_name: str                         # e.g., {"name": "EcoBattery Inc.", "background": "A leader in sustainable battery technologies with extensive R&D."}
    industry: str                             # e.g., "Energy Storage & Battery Manufacturing"
    products_services: str                    # e.g., ["Advanced lithium-titanate battery electrodes"]
    region: str                               # e.g., ["Asia", "Europe"]
    technology: str                           # e.g., ["Li-titanate electrode innovation, including advanced doping techniques"]
    strategic_objectives: str                 # e.g., ["Identify new Li-titanate electrode processes", "Benchmark competitor technologies", ...]
    number_sub_fields: int
    
    # --- Process 1 Output ---
    research_statement: str                   # A concise narrative combining the above inputs.
    
    # --- Process 2 Output ---
    main_domains: List[dict]                  # High-level domain map (each dict contains keys like "domain", "elements", "relationship").
    
    # --- Process 3 Output: Derived Research Sub-Fields ---
    total_sub_fields: List[str]
    
    # --- Process 4 Output: Prioritized Sub-Field List & Research Plans ---
    prioritized_sub_fields: List[str]         # Ranked list of sub-field names.
    research_plans: List[dict]                      # Mapping: sub-field name → research plan (JSON-like dict).
    
    # --- Process 6 Output: List of Research Report Sub-Fields ---
    list_docx_report_dir: Annotated[List[str], operator.add]  # Each str holds the report directory.
    
    # --- Final Output (for example, a consolidated DOCX report directory) ---
    consolidated_docx_report_dir: str         # A directory string indicating where the consolidated DOCX report is stored.
    
    # --- Debugging / Iterative Communication ---
    messages: Annotated[List[AnyMessage], add_messages]
