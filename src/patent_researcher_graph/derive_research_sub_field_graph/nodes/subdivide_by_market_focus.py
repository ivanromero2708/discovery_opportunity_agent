from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from typing import List
from ...configuration import Configuration
from ..state import ResearchSubFieldsGraphState
from ...state import DomainRelationship
from ..prompts import PROMPT_SUBDIVIDE_BY_MARKET_FOCUS

# Define a simple Pydantic model for the expected output.
class MarketFocusSubFieldsOutput(BaseModel):
    sub_fields: List[str]

class SubdivideByMarketFocus:
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
        Node 3.3: Subdivide by Market & Regional Focus.
        
        Inputs (from the parent state):
          - main_domains: The high-level domain map (as a list of objects).
          - region: A string representing the geographic or market region.
          - strategic_objectives: A string describing the strategic objectives.
        
        Output:
          - sub_fields_by_region: A list of sub-field names (strings) segmented by regional or market focus.
          
        Example output:
          {
            "sub_fields_by_region": [
              "China-Focused Technologies",
              "US/EU Market Innovations"
            ]
          }
        """
        # Extract inputs from the state.
        # For this node, we assume the candidate main domains are provided in state["main_domains"].
        formatted_domains = self.format_main_domains(state["main_domains"])   
        region = state["region"]
        strategic_objectives = state["strategic_objectives"]
        
        # Retrieve configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        
        # Build the prompt using the provided guidelines.
        system_instructions = PROMPT_SUBDIVIDE_BY_MARKET_FOCUS.format(
            main_domains=formatted_domains,
            region=region,
            strategic_objectives=strategic_objectives
        )
        
        # Create system and human messages.
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(content="Generate the market/regional focused sub-fields as a JSON object.")
        
        # Use with_structured_output to obtain a structured output.
        structured_llm = llm.with_structured_output(MarketFocusSubFieldsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])
        
        # Return the result with the key expected by the parent state.
        return {"sub_fields_by_region": result.sub_fields}

# For quick local testing:
if __name__ == "__main__":
    # Create a dummy state.
    dummy_state = ResearchSubFieldsGraphState(
        research_statement="Dummy research statement",
        main_domains=["Domain: End Application - EV Batteries, Consumer Electronics. Relationship: Application requirements drive process innovation."],
        strategic_objectives="Focus on market trends in developed regions.",
        sub_fields_by_core=[],
        sub_fields_by_application=[],
        sub_fields_by_region=[],
        sub_fields_by_strategic=[],
        total_sub_fields=[]
    )
    # Create a dummy RunnableConfig (using your Configuration class).
    from langchain_core.runnables import RunnableConfig
    from ...configuration import Configuration
    dummy_config = RunnableConfig(configurable=Configuration())
    
    node = SubdivideByMarketFocus()
    output = node.run(dummy_state, dummy_config)
    print("Sub-fields based on market/regional focus:")
    print(output)
