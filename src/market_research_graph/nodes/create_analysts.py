from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..state import GenerateAnalystsState, Perspectives
from ..prompts import analyst_instructions

class CreateAnalysts:
    def __init__(self) -> None:
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0) 

    def create_analysts(self, state: GenerateAnalystsState):
        """ Create analysts """
        
        industry = state["industry"]
        region = state["region"]
        product_services = state["product_services"]

        human_analyst_feedback=state.get('human_analyst_feedback', '')
            
        # Enforce structured output
        structured_llm = self.model.with_structured_output(Perspectives)

        # System message
        system_message = analyst_instructions.format(industry=industry,
                                                    region=region,
                                                    product_services=product_services,
                                                    human_analyst_feedback=human_analyst_feedback)

        # Generate question 
        analysts = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Generate the set of analysts.")])
        
        # Write the list of analysis to state
        return {"analysts": analysts.analysts}
    
    def run(self, state: GenerateAnalystsState):
        result  = self.create_analysts(state)
        return result