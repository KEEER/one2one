from form.common import TupleDict, SingleSelection, MultipleSelection, format
from form.question import Form


class JuniorForm(Form):
    title = "junior"

    def __init__(self, data, type):
        super().__init__(data, type)
        self.subject = format(data, JuniorSubject)

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


class JuniorSubject(MultipleSelection):
    title = "选科-初中"
    options = ["物理", "生化", "地理", "政治", "历史"]
    dis = TupleDict({("物理", "物理"): 6, ("物理", "生化"): 4, ("物理", "地理"): 3, ("物理", "政治"): 0, ("物理", "历史"): 0,
                     ("生化", "生化"): 6, ("生化", "地理"): 0, ("生化", "政治"): 0, ("生化", "历史"): 0,
                     ("地理", "地理"): 6, ("地理", "政治"): 2, ("地理", "历史"): 2,
                     ("政治", "政治"): 6, ("政治", "历史"): 4,
                     ("历史", "历史"): 6})
