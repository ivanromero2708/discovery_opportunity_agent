import unittest
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

# Import the compiled patent research graph and required state models.
from src.patent_researcher_graph.graph import patent_research_graph
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState
from src.patent_researcher_graph.configuration import Configuration

class TestPatentResearchGraph(unittest.TestCase):
    def setUp(self):
        """Prepare the initial state for the graph execution."""
        self.test_state: ResearchSubFieldsGraphState = {
            "company_name": "B2B TikAI Solutions",
            "industry": "Artificial Intelligence & Digital Marketing",
            "products_services": "AI-powered marketing analytics and content optimization for B2B brands on TikTok",
            "region": "North America, Europe, Asia",
            "technology": "Machine learning algorithms for ad targeting, generative AI for content creation, sentiment analysis for engagement tracking",
            "strategic_objectives": "Enhance B2B brand engagement on TikTok, optimize ad performance through AI-driven insights, and benchmark AI marketing trends",
            "number_sub_fields": 3,
            "research_statement": "",  
            "main_domains": [],  
            "total_sub_fields": [],  
            "prioritized_sub_fields": [],  
            "research_plans": [],  
            "list_docx_report_dir": [],  
            "consolidated_docx_report_dir": "",  
            "messages": []  
        }

        # Create a dummy configuration (if needed by your nodes).
        self.config = RunnableConfig(configurable=Configuration())

        # Save a reference to the in-memory checkpoint and the compiled graph.
        self.memory = MemorySaver()
        self.graph = patent_research_graph

    def test_graph_execution(self):
        """Test the execution of the patent researcher graph."""
        thread_info = {"configurable": {"thread_id": "test_thread_1"}}
        events = []

        # Run the graph synchronously (since your repo is not async).
        for event in self.graph.stream(self.test_state, thread_info, stream_mode="values"):
            events.append(event)

        # Retrieve the final state from the graph.
        final_state = self.graph.get_state(thread_info).values

        # ✅ Assertions to validate correct graph execution.
        self.assertIn("total_sub_fields", final_state)
        self.assertGreater(len(final_state["total_sub_fields"]), 0, "Expected non-empty sub-fields list.")

        print("\n✅ Final state after full graph execution:")
        print(final_state)

if __name__ == "__main__":
    unittest.main()
