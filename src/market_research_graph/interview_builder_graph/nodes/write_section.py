from ..state import InterviewState
from ..prompts import section_writer_instructions
from langchain_core.messages import HumanMessage, SystemMessage

class WriteSection:
    def __init__(self) -> None:
        pass
    
    def write_section(self, state: InterviewState):

        """ Node to answer a question """

        # Get state
        interview = state["interview"]
        context = state["context"]
        analyst = state["analyst"]
    
        # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
        system_message = section_writer_instructions.format(focus=analyst.description)
        section = self.model.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Use this source to write your section: {context}")]) 
                    
        # Append it to state
        return {"sections": [section.content]}
    
    def run(self, state: InterviewState):
        result = self.write_section(state)
        return result