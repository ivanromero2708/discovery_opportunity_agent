from ..state import ResearchGraphState

class WriteReport:
    def write_report(self, state: ResearchGraphState):
        # Full set of sections
        sections = state["sections"]

        # Concat all sections together
        formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

        return {"content": formatted_str_sections}
    
    def run(self, state: ResearchGraphState):
        result = self.write_report(state)
        return result