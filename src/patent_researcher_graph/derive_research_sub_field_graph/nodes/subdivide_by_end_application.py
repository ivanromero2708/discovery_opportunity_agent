from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from src.patent_researcher_graph.configuration import Configuration
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState, CoreProcessSubFieldsOutput
from src.patent_researcher_graph.state import DomainRelationship
from src.patent_researcher_graph.derive_research_sub_field_graph.prompts import PROMPT_SUBDIVIDE_BY_END_APPLICATION
from typing import List

class SubdivideByEndApplication:
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

def main():
    # Create a dummy state for testing.
    # The state includes a mix of DomainRelationship objects and simple strings.
    dummy_state: ResearchSubFieldsGraphState = {
        "research_statement": "Test research statement for end-application node.",
        "main_domains": [
            DomainRelationship(
                domain="Core Process: Doping Techniques",
                elements=["TechniqueA", "TechniqueB"],
                relationship="Improves efficiency in battery production."
            ),
            "End Application: EV Batteries"  # A simple string example.
        ],
        "strategic_objectives": "Expand product portfolio and increase market share in Asia and Europe.",
        "products_services": "Battery electrodes and related components",
        "total_sub_fields": []  # This field is not used by this node.
    }
    
    # Create a dummy RunnableConfig using the Configuration class.
    dummy_config = RunnableConfig(configurable=Configuration())
    
    # Instantiate the node and run it.
    node = SubdivideByEndApplication()
    output = node.run(dummy_state, dummy_config)
    
    print("Sub-fields based on end-application or functional use:")
    print(output)

if __name__ == "__main__":
    main()