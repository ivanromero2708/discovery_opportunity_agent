from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from ...configuration import Configuration
from ..state import ResearchSubFieldsGraphState, CoreProcessSubFieldsOutput
from ...state import DomainRelationship
from ..prompts import PROMPT_SUBDIVIDE_BY_CORE_TECHNOLOGIES
from typing import List

class SubdivideByCoreProcessTechnology:
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
        Node 3.1: Subdivide by Core Process or Technology Approach.
        
        Inputs (from the parent state):
          - total_sub_fields: List of defined research sub-fields.
          - technology: A string (or a list converted to a string) with technology details.
          - strategic_objectives: Strategic objectives as a string.
          
        Output:
          - sub_fields_by_core: A list of sub-field names (strings) defined exclusively by their technological process or method.
          
        Example output:
          {
            "sub_fields_by_core": [
              "Smelting & Upgrading",
              "Innovative Hydrometallurgical Processes",
              "Advanced Electrolytic Reduction Methods"
            ]
          }
        """
        # Extract necessary inputs from the state.
        main_domains = self.format_main_domains(state["main_domains"])        
        technology = state["technology"]
        strategic_objectives = state["strategic_objectives"]
                       
        # Retrieve configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        
        # Build the prompt using the provided metaprompt guidelines.
        system_instructions = PROMPT_SUBDIVIDE_BY_CORE_TECHNOLOGIES.format(
            main_domains = main_domains,
            technology=technology,
            strategic_objectives=strategic_objectives,
        )
        
        # Create the system and human messages.
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(content="Generate the core process/technology sub-fields as a JSON object.")
        
        # Use with_structured_output to have the LLM return a CoreProcessSubFieldsOutput instance.
        structured_llm = llm.with_structured_output(CoreProcessSubFieldsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])
        
        # Return the result using the key expected by the parent state.
        return {"sub_fields_by_core": result.sub_fields}
