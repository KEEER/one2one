from form.question import *


class IccForm(Form):
    title = "icc"

    def __init__(self, data, type):
        super().__init__(data, type)
        self.project = format(data, Project)
        self.application = format(data, Application)

    @staticmethod
    def score(younger, elder):
        res = super().score(younger, elder)
        # print("uid", res["younger"]["id"])
        res["project_score"] = SingleSelection.distance(
            younger.project, elder.project)
        res["application_score"] = SingleSelection.distance(
            younger.application, elder.application)
        return res

    def to_obj(self):
        obj = super().to_obj()
        obj.update({
            "project": self.project.to_obj(),
            "application": self.application.to_obj()
        })
        return obj


class Project(SingleSelection):
    title = "你所在的项目是哪个呢？"
    options = ["AL", "AP", "IB"]
    dis = TupleDict({("AL", "AL"): 9, ("AL", "AP"): 0, ("AL", "IB"): 0,
                     ("AP", "AP"): 9, ("AP", "IB"): 0,
                     ("IB", "IB"): 9})


class Application(SingleSelection):
    title = "你最希望申请哪里呢？"
    options = ["美国", "英国", "中国香港", "加拿大", "澳大利亚", "其他国家或地区"]
    dis = TupleDict({("美国", "美国"): 4, ("美国", "英国"): 3, ("美国", "中国香港"): 1, ("美国", "加拿大"): 3, ("美国", "澳大利亚"): 0, ("美国", "其他国家或地区"): 0,
                     ("英国", "英国"): 4, ("英国", "中国香港"): 2, ("英国", "加拿大"): 2, ("英国", "澳大利亚"): 3, ("英国", "其他国家或地区"): 0,
                     ("中国香港", "中国香港"): 4, ("中国香港", "加拿大"): 1, ("中国香港", "澳大利亚"): 0, ("中国香港", "其他国家或地区"): 0,
                     ("加拿大", "加拿大"): 4, ("加拿大", "澳大利亚"): 0, ("加拿大", "其他国家或地区"): 0,
                     ("澳大利亚", "澳大利亚"): 4, ("澳大利亚", "其他国家或地区"): 0,
                     ("其他国家或地区", "其他国家或地区"): 1})
