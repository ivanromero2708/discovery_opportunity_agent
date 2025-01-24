from ..state import ResearchGraphState

class FinalizeReport:
    def __init__(self) -> None:
        pass
    
    def finalize_report(self, state: ResearchGraphState):
        """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
        # Save full final report
        content = state["content"]
        if content.startswith("## Insights"):
            content = content.strip("## Insights")
        if "## Sources" in content:
            try:
                content, sources = content.split("\n## Sources\n")
            except:
                sources = None
        else:
            sources = None

        final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
        if sources is not None:
            final_report += "\n\n## Sources\n" + sources
        return {"final_report": final_report}
    
    def run(self, state: ResearchGraphState):
        result = self.finalize_report(state)
        return result