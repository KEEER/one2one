from form.common import TupleDict, SingleSelection, MultipleSelection, format
from form.question import Form


class SeniorForm(Form):
    title = "senior"

    def __init__(self, data, type):
        super().__init__(data, type)
        self.subject = format(data, SeniorSubject)

    @staticmethod
    def score(younger, elder):
        res = super().score(younger, elder)
        res["subject_score"] = MultipleSelection.distance(
            younger.subject, elder.subject)
        return res

    def to_obj(self):
        obj = super().to_obj()
        obj.update({
            "subject": self.subject.to_obj()
        })
        return obj


class SeniorSubject(MultipleSelection):
    title = "选科-高中"
    options = ["物理", "化学", "生物", "地理", "思想政治", "历史"]
    dis = TupleDict({("物理", "物理"): 6, ("物理", "化学"): 3, ("物理", "生物"): 2, ("物理", "地理"): 3, ("物理", "思想政治"): 0, ("物理", "历史"): 0,
                     ("化学", "化学"): 6, ("化学", "生物"): 4, ("化学", "地理"): 0, ("化学", "思想政治"): 0, ("化学", "历史"): 0,
                     ("生物", "生物"): 6, ("生物", "地理"): 0, ("生物", "思想政治"): 0, ("生物", "历史"): 0,
                     ("地理", "地理"): 6, ("地理", "思想政治"): 2, ("地理", "历史"): 2,
                     ("思想政治", "思想政治"): 6, ("思想政治", "历史"): 4,
                     ("历史", "历史"): 6})
