from ..state import GenerateAnalystsState

class HumanFeedback:
    def __init__(self) -> None:
        pass

    def human_feedback(state: GenerateAnalystsState):
        """ No-op node that should be interrupted on """
        pass
    
    def run(self, state: GenerateAnalystsState):
        return self.human_feedback(state)