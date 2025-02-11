from langchain_core.runnables import RunnableConfig
from ..state import PatentResearchGraphState
from langgraph.constants import Send
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

class InitiateAllSubFieldResearch:
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
            Send("sub_field_research", 
                {
                    "company_name": company_name,
                    "industry": industry,
                    "products_services": products_services,
                    "region": region,
                    "technology": technology,
                    "strategic_objectives": strategic_objectives,
                    "research_plan": research_plan
                }
            ) 
            for research_plan in state["research_plans"]
        ]
