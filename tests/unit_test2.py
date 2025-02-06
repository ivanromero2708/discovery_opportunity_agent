import unittest
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from src.patent_researcher_graph.graph import patent_research_graph
from src.patent_researcher_graph.state import PatentResearchGraphState
from src.patent_researcher_graph.configuration import Configuration

class TestPatentResearchGraphBreakpoints(unittest.TestCase):
    def setUp(self):
        # Create a dummy state for the patent research graph.
        self.test_state: PatentResearchGraphState = {
            "company_name": "EcoBattery Inc.",
            "industry": "Energy Storage & Battery Manufacturing",
            "products_services": "Advanced lithium-titanate battery electrodes",
            "region": "Asia, Europe",
            "technology": "Li-titanate electrode innovation, including advanced doping techniques",
            "strategic_objectives": "Identify new processes, benchmark competitor technologies",
            "number_sub_fields": 3,
            "research_statement": "",
            "main_domains": [],  # Dummy value, could be filled with a dummy DomainRelationship if needed.
            "total_sub_fields": [],
            "prioritized_sub_fields": [],
            "research_plans": [],
            "list_docx_report_dir": [],
            "consolidated_docx_report_dir": "",
            "messages": []
        }
        self.config = RunnableConfig(configurable=Configuration())
        
        # Assume patent_research_graph is already compiled in your src/patent_researcher_graph/graph.py
        self.graph = patent_research_graph

    def test_graph_until_breakpoint(self):
        # Run the graph until the first breakpoint (for example, after the "define_overall_research_domain" node).
        # Here, we assume that you set a breakpoint in the graph using interrupt_before.
        thread_info = {"configurable": {"thread_id": "test_thread_1"}}
        # Start the graph stream
        events = []
        for event in self.graph.stream(self.test_state, thread_info, stream_mode="values"):
            events.append(event)


        # Check that the state has a research_statement (from the first node).
        current_state = self.graph.get_state(thread_info).values
        self.assertIn("research_statement", current_state)
        print("\nBreakpoint state (after first node):")
        print(current_state)

if __name__ == "__main__":
    unittest.main()
