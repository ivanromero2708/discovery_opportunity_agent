from ..state import ResearchGraphState
from ..prompts import intro_conclusion_instructions
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class WriteConclusion:
    def __init__(self) -> None:
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    def write_conclusion(self, state: ResearchGraphState):
        # Full set of sections
        sections = state["sections"]
        industry = state["industry"]
        region = state["region"]

        # Concat all sections together
        formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
        
        # Summarize the sections into a final report
        
        instructions = intro_conclusion_instructions.format(industry=industry, region=region, formatted_str_sections=formatted_str_sections)    
        conclusion = self.model.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")]) 
        return {"conclusion": conclusion.content}
    
    def run(self, state: ResearchGraphState):
        result = self.write_conclusion(state)
        return result