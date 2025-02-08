from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from ..state import PatentResearchGraphState
from ..configuration import Configuration
from ..prompts import PROMPT_SELECT_RESEARCH_SUB_FIELDS


class SelectResearchSubFields:
    def __init__(self):
        pass

    def select_research_sub_fields(
        self, state: PatentResearchGraphState, config: RunnableConfig
    ) -> Dict[str, List[str]]:
        """
        Node: Select the Most Adequate Sub-Fields for Patent Research.

        Inputs (state):
          - company_name: Name of the company.
          - industry: Industry category.
          - products_services: Description of the products and services offered.
          - region: Geographic market focus.
          - technology: Key technological innovations relevant to the research.
          - strategic_objectives: Business goals guiding patent research.
          - number_sub_fields: Desired number of sub-fields.
          - total_sub_fields: List of available sub-fields from previous nodes.

        Output:
          - prioritized_sub_fields: A ranked list of the most strategic and relevant research sub-fields.
        """

        # Extract necessary inputs from the state.
        company_name = state["company_name"]
        industry = state["industry"]
        products_services = state["products_services"]
        region = state["region"]
        technology = state["technology"]
        strategic_objectives = state["strategic_objectives"]
        total_sub_fields = state["total_sub_fields"]

        # Get configuration and initialize the LLM.
        configurable = Configuration.from_runnable_config(config)
        planner_llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
        number_sub_fields = configurable.number_of_sub_fields
        
        # Build the prompt using the predefined template.
        system_instructions = PROMPT_SELECT_RESEARCH_SUB_FIELDS.format(
            company_name=company_name,
            industry=industry,
            products_services=products_services,
            region=region,
            technology=technology,
            strategic_objectives=strategic_objectives,
            total_sub_fields=", ".join(total_sub_fields),
            number_sub_fields=number_sub_fields
        )

        system_msg = SystemMessage(content=system_instructions)
        instruction_msg = HumanMessage(
            content="Generate the prioritized list of research sub-fields as a JSON array."
        )

        # Use structured output for parsing the response.
        class ResearchSubFieldsOutput(BaseModel):
            prioritized_sub_fields: List[str]

        structured_llm = planner_llm.with_structured_output(ResearchSubFieldsOutput)
        result = structured_llm.invoke([system_msg, instruction_msg])

        return {"prioritized_sub_fields": result.prioritized_sub_fields}

    def run(self, state: PatentResearchGraphState, config: RunnableConfig):
        return self.select_research_sub_fields(state, config)
