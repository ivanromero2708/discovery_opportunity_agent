from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from typing import List
from src.patent_researcher_graph.configuration import Configuration
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState, CoreProcessSubFieldsOutput
from src.patent_researcher_graph.state import DomainRelationship
from src.patent_researcher_graph.derive_research_sub_field_graph.prompts import PROMPT_SUBDIVIDE_BY_STRATEGIC_ANGLE

class SubdivideByStrategicAngle:
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
                lines.append(f"Domain: {str(item)}\n")
        return "\n".join(lines)
    
    def run(self, state: ResearchSubFieldsGraphState, config: RunnableConfig) -> dict:
        """
        Node 3.4: Subdivide by Strategic/Competitive Angle.
        
        Inputs (from the parent state):
          - main_domains: The high-level domain map (as a list of objects or strings).
          - strategic_objectives: A string describing the strategic objectives.
          
        Output:
          - sub_fields_by_strategic: A list of sub-field names (strings) that capture strategic or competitive perspectives.
          
        Example output:
          {
            "sub_fields_by_strategic": [
              "Key Competitor Portfolios",
              "White Spaces for R&D",
              "Collaboration Opportunities"
            ]
          }
        """
        # Extract and format the main domains.
        formatted_domains = self.format_main_domains(state["main_domains"])
        strategic_objectives = state["strategic_objectives"]
        
        # Retrieve configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        
        # Build the prompt using the provided metaprompt guidelines.
        system_instructions = PROMPT_SUBDIVIDE_BY_STRATEGIC_ANGLE.format(
            main_domains=formatted_domains,
            strategic_objectives=strategic_objectives
        )
        
        # Create system and human messages.
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(content="Generate the strategic/competitive sub-fields as a JSON object.")
        
        # Use with_structured_output to obtain a structured output.
        structured_llm = llm.with_structured_output(CoreProcessSubFieldsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])
        
        # Return the result using the expected key.
        return {"sub_fields_by_strategic": result.sub_fields}

# For testing purposes, include a dummy test block.
if __name__ == "__main__":
    # Create a dummy state – here we provide main_domains as a mix of DomainRelationship objects and strings.
    dummy_state: ResearchSubFieldsGraphState = {
        "research_statement": "Dummy research statement for strategic angle node.",
        "main_domains": [
            # A DomainRelationship instance.
            DomainRelationship(
                domain="Core Process: Advanced Doping",
                elements=["Precise Material Application", "Innovative Doping Strategies"],
                relationship="Enhances the efficiency of battery electrodes."
            ),
            # A simple string.
            "End Application: EV Batteries"
        ],
        "strategic_objectives": "Identify competitive advantages, optimize R&D, and explore potential partnerships.",
        "total_sub_fields": []  # Not used in this node.
    }
    
    # Create a dummy RunnableConfig using the Configuration class.
    from langchain_core.runnables import RunnableConfig
    from src.patent_researcher_graph.configuration import Configuration
    dummy_config = RunnableConfig(configurable=Configuration())
    
    node = SubdivideByStrategicAngle()
    output = node.run(dummy_state, dummy_config)
    
    print("Sub-fields based on strategic/competitive angle:")
    print(output)
