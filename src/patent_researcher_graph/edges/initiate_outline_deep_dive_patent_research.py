from langchain_core.runnables import RunnableConfig
from ..state import PatentResearchGraphState
from langgraph.constants import Send

class InitiateOutlineDeepDivePatentResearch:
    def __init__(self):
        self.configurable = None
    
    def run(self, state: PatentResearchGraphState, config: RunnableConfig):
        
        company_name = state["company_name"]
        industry = state["industry"]
        products_services = state["products_services"]
        region = state["region"]
        technology = state["technology"]
        strategic_objectives = state["strategic_objectives"]
        return [
            Send("outline_deep_dive_research_sub_fields", 
                {
                    "company_name": company_name,
                    "industry": industry,
                    "products_services": products_services,
                    "region": region,
                    "technology": technology,
                    "strategic_objectives": strategic_objectives,
                    "prioritized_sub_field": prioritized_sub_field
                }
            ) 
            for prioritized_sub_field in state["prioritized_sub_fields"]
        ]
