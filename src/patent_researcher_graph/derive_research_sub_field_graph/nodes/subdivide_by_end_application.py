from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from ...configuration import Configuration
from ..state import ResearchSubFieldsGraphState, CoreProcessSubFieldsOutput
from ...state import DomainRelationship
from ..prompts import PROMPT_SUBDIVIDE_BY_END_APPLICATION
from typing import List

class SubdivideByEndApplication:
    def format_main_domains(self, main_domains: List[DomainRelationship]) -> str:
        """
        Transforms a list of DomainRelationship Pydantic objects into an organized string.
        
        The output is formatted with headings and bullet points for clarity.
        
        Example output:
        
        High-Level Domain Research Map:
        
        Domain: Core Process
        - Doping Techniques
        - Manufacturing Methods
        Relationship: Innovation in doping directly affects electrode performance.
        
        Domain: End Application
        - EV Batteries
        - Consumer Electronics
        Relationship: Application requirements drive process innovation.
        
        Returns:
            A string representing the formatted domain research map.
        """
        if not main_domains:
            return "No domain relationships provided."
        
        lines = ["High-Level Domain Research Map:\n"]
        for domain_obj in main_domains:
            lines.append(f"Domain: {domain_obj.domain}")
            lines.append("  Elements:")
            for element in domain_obj.elements:
                lines.append(f"    - {element}")
            lines.append(f"Relationship: {domain_obj.relationship}\n")
        return "\n".join(lines)
    
    def run(self, state: ResearchSubFieldsGraphState, config: RunnableConfig) -> dict:
        """
        Node 3.2: Subdivide by End-Application or Functional Use.

        Inputs (from the parent state):
          - Candidate Sub-Fields: a list of defined research sub-fields (for example, state["total_sub_fields"]).
          - Product/Services: a string describing the products or services of the company.
          - Strategic Objectives: a string describing the strategic objectives.

        Output:
          - sub_fields_by_application: A list of sub-field names (strings) that are categorized based on their end applications.

        Example output:
          {
            "sub_fields_by_application": [
              "Electrodes for Batteries",
              "Medical Device Applications",
              "Cosmetic Formulations"
            ]
          }
        """
        # Extract main domains
        main_domains = self.format_main_domains(state["main_domains"])    
        
        # Retrieve product/service info. If not available, use a dummy.
        product_services = state["products_services"]
        # Strategic objectives.
        strategic_objectives = state["strategic_objectives"]

        # Retrieve configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        
        # Build the prompt using the metaprompt guidelines.
        system_instructions = PROMPT_SUBDIVIDE_BY_END_APPLICATION.format(
            main_domains=main_domains,
            product_services=product_services,
            strategic_objectives=strategic_objectives
        )
        
        # Create system and human messages.
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(content="Generate the end-application sub-fields as a JSON object.")
        
        # Use with_structured_output to have the LLM return a structured output.
        structured_llm = llm.with_structured_output(CoreProcessSubFieldsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])
        
        # Return the result with the expected key.
        return {"sub_fields_by_application": result.sub_fields}