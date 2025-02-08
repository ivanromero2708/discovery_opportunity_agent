from langchain_core.runnables import RunnableConfig
from src.patent_researcher_graph.derive_research_sub_field_graph.state import ResearchSubFieldsGraphState

class ConsolidateSubResearchFields:
    def run(self, state: ResearchSubFieldsGraphState, config: RunnableConfig) -> dict:
        """
        Node 3.5: Consolidate sub-field research.

        Inputs (from the parent state):
          - sub_fields_by_core: List of sub-fields based on core process/technology.
          - sub_fields_by_application: List of sub-fields based on end-applications.
          - sub_fields_by_region: List of sub-fields based on market/regional focus.
          - sub_fields_by_strategic: List of sub-fields based on strategic/competitive angle.

        Output:
          - total_sub_fields: A consolidated list of all unique sub-fields.

        Example output:
          {
            "total_sub_fields": [
              "Smelting & Upgrading",
              "Direct Acid Leaching Processes",
              "Electrodes for Batteries",
              "Medical Device Applications",
              "China-Focused Technologies",
              "US/EU Market Innovations",
              "Key Competitor Portfolios",
              "White Spaces for R&D",
              "Collaboration Opportunities"
            ]
          }
        """
        # Start with an empty list and extend with each sub-field list
        combined = []
        for key in ["sub_fields_by_core", "sub_fields_by_application", "sub_fields_by_region", "sub_fields_by_strategic"]:
            # Use .get() to default to an empty list if the key is missing.
            combined.extend(state.get(key, []))
        
        # Remove duplicates while preserving order.
        seen = set()
        consolidated = []
        for item in combined:
            if item not in seen:
                seen.add(item)
                consolidated.append(item)
                
        return {"total_sub_fields": consolidated}

# If running directly, use the following test block:
if __name__ == "__main__":
    # Dummy state for testing purposes.
    dummy_state: ResearchSubFieldsGraphState = {
        "research_statement": "Dummy research statement",
        "main_domains": [],
        "strategic_objectives": "Increase market share and drive innovation",
        "sub_fields_by_core": ["Smelting & Upgrading", "Direct Acid Leaching Processes"],
        "sub_fields_by_application": ["Electrodes for Batteries", "Medical Device Applications"],
        "sub_fields_by_region": ["China-Focused Technologies", "US/EU Market Innovations"],
        "sub_fields_by_strategic": ["Key Competitor Portfolios", "White Spaces for R&D", "Collaboration Opportunities"]
    }
    
    # Create a dummy RunnableConfig using your Configuration.
    from langchain_core.runnables import RunnableConfig
    from src.patent_researcher_graph.configuration import Configuration
    dummy_config = RunnableConfig(configurable=Configuration())
    
    node = ConsolidateSubResearchFields()
    output = node.run(dummy_state, dummy_config)
    print("Consolidated sub-fields:")
    print(output["total_sub_fields"])
