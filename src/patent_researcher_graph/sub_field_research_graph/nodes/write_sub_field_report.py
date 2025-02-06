class WriteSubFieldReport:
    def __init__(self, sub_field: str = "dummy_sub_field", sub_field_report: str = "dummy_report"):
        self.sub_field = sub_field
        self.sub_field_report = sub_field_report

    def run(self, state, config=None) -> dict:
        # Return a dummy file path (simulate report generation).
        return {"list_docx_report_dir": f"reports/{self.sub_field}.txt"}
