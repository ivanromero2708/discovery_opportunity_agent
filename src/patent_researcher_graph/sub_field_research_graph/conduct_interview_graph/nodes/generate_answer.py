# src/patent_researcher_graph/sub_field_research_graph/conduct_interview_graph/nodes/generate_answer.py

from langchain_core.messages import SystemMessage

class GenerateAnswer:
    def __init__(self):
        pass

    def run(self, state):
        # Dummy implementation: append a dummy answer message.
        return {"messages": [SystemMessage(content="Dummy generated answer.")]}
