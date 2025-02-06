class WriteConclusionSubFieldReport:
    def __init__(self, sub_field_report=None):
        # You can store a dummy report if needed.
        self.sub_field_report = sub_field_report

    def run(self, state, config=None) -> dict:
        # Return a dummy conclusion.
        return {"conclusion": "Dummy conclusion for sub-field report."}
