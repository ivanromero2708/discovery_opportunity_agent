# src/patent_researcher_graph/sub_field_research_graph/conduct_interview_graph/nodes/generate_question.py

from langchain_core.messages import HumanMessage, SystemMessage

class GenerateQuestion:
    def __init__(self):
        pass

    def run(self, state):
        # Dummy implementation: append a dummy question message.
        return {"messages": [SystemMessage(content="Dummy generated question.")]}
