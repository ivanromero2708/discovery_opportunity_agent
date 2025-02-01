
class WriteConclusionSubFieldReport:
    def __init__(self, sub_field_report):
        self.sub_field_report = sub_field_report

    def write(self, file_path):
        with open(file_path, 'w') as file:
            file.write(self.sub_field_report.get_conclusion())