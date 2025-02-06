# src/patent_researcher_graph/sub_field_research_graph/conduct_interview_graph/nodes/search_web.py

from langchain_core.messages import HumanMessage, SystemMessage

class SearchWeb:
    def __init__(self):
        pass

    def run(self, state):
        # Dummy implementation: simply return a dummy context message.
        # In your real code, this would call your LLM or search service.
        return {"messages": [SystemMessage(content="Dummy search results for web query.")]}
