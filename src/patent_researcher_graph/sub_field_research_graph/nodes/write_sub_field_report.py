
class WriteSubFieldReport:
    def __init__(self, sub_field, sub_field_report):
        self.sub_field = sub_field
        self.sub_field_report = sub_field_report

    def write(self):
        with open(f"reports/{self.sub_field}.txt", "w") as file:
            file.write(self.sub_field_report)