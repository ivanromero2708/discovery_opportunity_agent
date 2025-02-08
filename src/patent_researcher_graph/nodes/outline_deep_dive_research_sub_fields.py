from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from ..state import PatentResearchGraphState, OutlineDeepDivePatentResearch, OutlineDeepDivePatentResearchGraphState
from ..configuration import Configuration
from ..prompts import PROMPT_OUTLINE_DEEP_DIVE_PATENT_RESEARCH

class OutlineDeepDiveResearchSubFields:
    def __init__(self):
        self.configurable = None
    
    def outline_deep_dive_patent_research(self, state: OutlineDeepDivePatentResearchGraphState, config: RunnableConfig):
        """
        Node: Outline each deep dive patent research report for the selected sub-fields 
        
        Inputs(state):
            - company_name: Name of the company.
            - industry: Industry category.
            - products_services: Description of the products and services offered.
            - region: Geographic market focus.
            - technology: Key technological innovations relevant to the research.
            - strategic_objectives: Business goals guiding patent research.
            - prioritized_sub_field: A relevant research sub-fields.
        
        Output
            - research_plan(OutlineDeepDivePatentResearch): An outline of the deep dive patent research report for the specific sub_field
        
        """
        
        # Extract the neccesary inputs:
        company_name = state["company_name"]
        industry = state["industry"]
        products_services = state["products_services"]
        region = state["region"]
        technology = state["technology"]
        strategic_objectives = state["strategic_objectives"]
        prioritized_sub_field = state["prioritized_sub_field"]
        
        configurable = Configuration.from_runnable_config(config)
        planner_llm = ChatOpenAI(model = configurable.planner_model, temperature = 0)
        
        system_instructions = PROMPT_OUTLINE_DEEP_DIVE_PATENT_RESEARCH.format(
            company_name=company_name,
            industry=industry,
            products_services=products_services,
            region=region,
            technology=technology,
            strategic_objectives=strategic_objectives,
            prioritized_sub_field=prioritized_sub_field,
        )
        
        system_msg = SystemMessage(content=system_instructions)
        human_msg = HumanMessage(
            content="Generate the required elements for the sub-field patent research report."
        )
        
        structured_llm = planner_llm.with_structured_output(OutlineDeepDivePatentResearch)
        result = structured_llm.invoke([system_msg, human_msg])
        
        return {"research_plans": [result]}
    
    def run(self, state: OutlineDeepDivePatentResearchGraphState, config: RunnableConfig):
        return self.outline_deep_dive_patent_research(state, config)