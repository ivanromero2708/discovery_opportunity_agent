from ..state import ResearchGraphState
from langchain_openai import ChatOpenAI
from ..prompts import intro_conclusion_instructions
from langchain_core.messages import HumanMessage
import os
from utils.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, LANGCHAIN_TRACING_V2

class WriteIntroduction:
    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        
    def write_introduction(self, state: ResearchGraphState):
        # Full set of sections
        sections = state["sections"]
        industry = state["industry"]
        region = state["region"]
        
        # Concat all sections together
        formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
        
        # Summarize the sections into a final report
        
        instructions = intro_conclusion_instructions.format(industry=industry, region=region, formatted_str_sections=formatted_str_sections)    
        intro = self.model.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")]) 
        return {"introduction": intro.content}
    
    def run(self, state: ResearchGraphState):
        result = self.write_introduction(state)
        return result