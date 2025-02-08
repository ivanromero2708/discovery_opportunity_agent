from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from src.patent_researcher_graph.configuration import Configuration
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState, CoreProcessSubFieldsOutput
from src.patent_researcher_graph.state import DomainRelationship
from src.patent_researcher_graph.derive_research_sub_field_graph.prompts import PROMPT_SUBDIVIDE_BY_CORE_TECHNOLOGIES
from typing import List

class SubdivideByCoreProcessTechnology:
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


def main():
    # Crear un estado dummy de prueba, usando una mezcla de objetos DomainRelationship y strings simples.
    dummy_state: ResearchSubFieldsGraphState = {
        "research_statement": "Dummy research statement for testing.",
        "main_domains": [
            # Un objeto DomainRelationship válido
            DomainRelationship(
                domain="Core Process: Doping Techniques",
                elements=["Technique1", "Technique2"],
                relationship="Enhances performance in battery manufacturing."
            ),
            # Una cadena simple para comprobar el manejo de fallbacks
            "End Application: EV Batteries"
        ],
        "strategic_objectives": "Focus on improving efficiency and reducing costs.",
        "technology": "Advanced doping methods combined with innovative manufacturing techniques.",
        "total_sub_fields": []
    }
    
    # Crear una configuración dummy
    dummy_config = RunnableConfig(configurable=Configuration())
    
    # Instanciar y ejecutar el nodo
    node = SubdivideByCoreProcessTechnology()
    output = node.run(dummy_state, dummy_config)
    
    print("Sub-fields based on core process/technology:")
    print(output)

if __name__ == "__main__":
    main()