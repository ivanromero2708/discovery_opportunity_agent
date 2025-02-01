
class WriteIntroductionSubFieldReport:
    def __init__(self, sub_field_report):
        self.sub_field_report = sub_field_report

    def write(self):
        introduction = self.sub_field_report.introduction
        return introduction