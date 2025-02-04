from typing import Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from ..state import PatentResearchGraphState, DomainRelationshipsOutput
from ..configuration import Configuration
from ..prompts import prompt_generate_high_level_domain_map


class CreateHighLevelDomainResearchMap:
    def __init__(self):
        pass

    def create_high_level_domain_research_map(
        self, state: PatentResearchGraphState, config: RunnableConfig
    ) -> DomainRelationshipsOutput:
        """
        Node: Create a High-Level Domain Research Map.

        Inputs (state):
          - industry: String specifying the industry.
          - products_services: String describing the products or services.
          - technology: String (or list) representing the technological innovation angle.
          - research_statement: A concise research statement that guides the patent analysis.
        
        Output:
          - main_domains: A validated list of DomainRelationship objects representing the high-level domain map.
        """
        # Extract inputs from the state.
        industry = state["industry"]
        products_services = state["products_services"]
        technology = state["technology"]
        research_statement = state["research_statement"]

        # Get configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        planner_llm = ChatOpenAI(model=configurable.planner_model, temperature=0)

        # Build the prompt using the provided metaprompt guidelines.
        system_instructions = prompt_generate_high_level_domain_map.format(
            industry=industry,
            products_services=products_services,
            technology=technology,
            research_statement=research_statement,
        )
        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(
            content="Generate the high-level domain research map as a JSON array using the provided schema."
        )

        # Use with_structured_output to directly obtain a DomainRelationshipsOutput object.
        structured_llm = planner_llm.with_structured_output(DomainRelationshipsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])

        # The result should be a DomainRelationshipsOutput instance.
        validated_domains = result.domains

        return {"main_domains": validated_domains}

    def run(self, state: PatentResearchGraphState, config: RunnableConfig):
        return self.create_high_level_domain_research_map(state, config)
