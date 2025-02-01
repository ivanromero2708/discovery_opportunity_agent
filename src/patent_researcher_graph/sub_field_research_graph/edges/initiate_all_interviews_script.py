class InitiateAllInterviews:
    def __init__(self, graph, interview_script):
        self.graph = graph
        self.interview_script = interview_script

    def run(self):
        for edge in self.graph.edges:
            self.interview_script.run(edge)