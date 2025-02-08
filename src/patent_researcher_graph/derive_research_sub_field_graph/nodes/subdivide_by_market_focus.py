from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from typing import List
from src.patent_researcher_graph.configuration import Configuration
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState
from src.patent_researcher_graph.state import DomainRelationship
from src.patent_researcher_graph.derive_research_sub_field_graph.prompts import PROMPT_SUBDIVIDE_BY_MARKET_FOCUS

# Define a simple Pydantic model for the expected output.
class MarketFocusSubFieldsOutput(BaseModel):
    sub_fields: List[str]

class SubdivideByMarketFocus:
    def format_main_domains(self, main_domains: List) -> str:
        """
        Transforma una lista de dominios en un string formateado.
        Si un elemento es una instancia de DomainRelationship se utilizan sus atributos;
        si es un string, se usa directamente.

        Ejemplo de salida:

        High-Level Domain Research Map:

        Domain: Core Process: Doping Techniques
          Elements:
            - Element1
            - Element2
          Relationship: Affects performance.

        Domain: End Application: EV Batteries

        Returns:
            Un string representando el mapa de dominios.
        """
        if not main_domains:
            return "No domain relationships provided."
        
        lines = ["High-Level Domain Research Map:\n"]
        for item in main_domains:
            if isinstance(item, DomainRelationship):
                lines.append(f"Domain: {item.domain}")
                lines.append("  Elements:")
                for element in item.elements:
                    lines.append(f"    - {element}")
                lines.append(f"Relationship: {item.relationship}\n")
            elif isinstance(item, str):
                lines.append(f"Domain: {item}\n")
            else:
                # En caso de otro tipo, lo convertimos a string.
                lines.append(f"Domain: {str(item)}\n")
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

# Ejemplo de prueba con estado dummy
if __name__ == "__main__":
    # Creamos un estado dummy; se incluye un objeto DomainRelationship y un string.
    dummy_state: ResearchSubFieldsGraphState = {
        "research_statement": "Dummy research statement",
        "main_domains": [
            DomainRelationship(domain="Core Process: Doping Techniques", elements=["Element1", "Element2"], relationship="Affects performance"),
            "End Application: EV Batteries"
        ],
        "strategic_objectives": "Expand market share in Asia and Europe",
        "total_sub_fields": [],
        "region": "Asia"
    }
    
    from langchain_core.runnables import RunnableConfig
    from src.patent_researcher_graph.configuration import Configuration
    dummy_config = RunnableConfig(configurable=Configuration())
    
    node = SubdivideByMarketFocus()
    output = node.run(dummy_state, dummy_config)
    print("Sub-fields based on market & regional focus:")
    print(output)