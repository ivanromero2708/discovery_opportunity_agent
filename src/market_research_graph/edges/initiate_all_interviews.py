from ..state import ResearchGraphState
from langchain_core.messages import HumanMessage
from langgraph.constants import Send

class IniateAllInterviews:
    def __init__(self) -> None:
        pass
    
    def initiate_all_interviews(self, state: ResearchGraphState):
        """ This is the "map" step where we run each interview sub-graph using Send API """    

        # Check if human feedback
        human_analyst_feedback=state.get('human_analyst_feedback')
        if human_analyst_feedback:
            # Return to create_analysts
            return "create_analysts"

        # Otherwise kick off interviews in parallel via Send() API
        else:
            industry = state["industry"]
            region = state["region"]
            return [Send("conduct_interview", {"analyst": analyst,
                                                "messages": [HumanMessage(
                                                    content=f"So you said you were writing a market research report on {industry} in the region {region}??"
                                                )
                                                                ]}) for analyst in state["analysts"]]
    
    def run(self, state: ResearchGraphState):
        result = self.initiate_all_interviews(state)
        return result