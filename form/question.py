from form.common import *
import json
import numpy as np
import pandas as pd


class Form:
    def __init__(self, data: pd.DataFrame, _type):
        if type(_type) is str:
            _type = True if _type == "elder" else False
        self.type = _type
        self.uid = data["ID"]
        self.name = data["姓名"]
        self.gender = format(data, Gender)
        self.phone_number = str(data["手机号"])
        self.wechat_name = data["微信名字"]
        self.wechat_id = data["微信号"]
        self.expected_gender = format(
            data, ElderExpectedGender if self.type else YoungerExpectedGender)
        self.junior_school = format(
            data, ElderJuniorSchool if self.type else YoungerJuniorSchool)
        self.broader = format(
            data, ElderBroader if self.type else YoungerBroader)
        self.competition = format(
            data, ElderCompetition if self.type else YoungerCompetition)
        self.software = format(data, Software)
        self.activity = format(data, Activity)
        self.interest = format(data, Interest)
        self.game = data["你平时最喜欢玩的电子游戏是什么呢？"]
        self.other_interest = data["你还感兴趣哪些领域呢？"]
        self.introduction = data["你还有什么想介绍的吗？"]
        self.requirement = data["特殊要求"]

        if not self.type:
            self.organization = data["你最感兴趣的学生组织是？"]

    @staticmethod
    def score(younger, elder):
        res = {
            "younger": younger.to_obj(),
            "elder": elder.to_obj()
        }
        res["younger_expected_gender_score"] = SingleSelection.distance(
            younger.expected_gender, elder.gender)
        res["elder_expected_gender_score"] = SingleSelection.distance(
            younger.gender, elder.expected_gender)  # TODO
        res["junior_school_score"] = SingleSelection.distance(
            younger.junior_school, elder.junior_school)
        res["competition_score"] = MultipleSelection.distance(
            younger.competition, elder.competition)
        res["software_score"] = MultipleSelection.distance(
            younger.software, elder.software)
        res["activity_score"] = SingleSelection.distance(
            younger.activity, elder.activity)
        res["interest_score"] = MultipleSelection.distance(
            younger.interest, elder.interest)
        return res

    def to_obj(self):
        obj = {
            "type": self.type,
            "id": self.uid,
            "number": self.phone_number,
            "gender": self.gender.to_obj(),
            "年级": self.title,
            "name": self.name,
            "微信号": self.wechat_id,
            "微信名": self.wechat_name,
            "人本": self.junior_school.to_obj(),
            "住宿生": self.broader.to_obj(),
            # "竞赛": self.competition.to_obj(),
            # "游戏": self.game,
            "软件": self.software.to_obj(),
            # "活动": self.activity.to_obj(),
            # "领域": self.interest.to_obj(),
            # "其他领域": self.other_interest,
            # "介绍": self.introduction,
            # "要求": self.requirement,
        }

        # if not self.type:
        #     obj["组织"] = self.organization
        return obj


class ExpectedGender(SingleSelection):
    options = ["male", "female", "any"]

# 15 13 -10


class YoungerExpectedGender(ExpectedGender):
    title = "你想匹配的是学长还是学姐？"
    dis = {("male", "male"): 10, ("male", "female"): -5,
           ("female", "male"): -5, ("female", "female"): 10,
           ("any", "male"): 8, ("any", "female"): 8}

    def __init__(self, str):
        if str == "学长":
            self.answer = "male"
        elif str == "学姐":
            self.answer = "female"
        else:
            self.answer = "any"


class ElderExpectedGender(ExpectedGender):
    title = "你想匹配的是学弟还是学妹？"
    dis = {("male", "male"): 10, ("female", "male"): -5,
           ("male", "female"): -5, ("female", "female"): 10,
           ("male", "any"): 8, ("female", "any"): 8}

    def __init__(self, str):
        if str == "学弟":
            self.answer = "male"
        elif str == "学妹":
            self.answer = "female"
        else:
            self.answer = "any"


class Gender(ElderExpectedGender):
    title = "性别"
    options = ["male", "female"]  # TODO other genders

    def __init__(self, str):

        self.answer = str


class JuniorSchool(SingleSelection):
    options = ["是", "否"]
    dis = {("是", "是"): 5, ("是", "否"): 3,
           ("否", "是"): -4, ("否", "否"): 5}  # use map here

    def to_obj(self):
        return self.answer == JuniorSchool.options[0]


class YoungerJuniorSchool(JuniorSchool):
    title = "你初中（将）是在人大附中本部就读的吗？"


class ElderJuniorSchool(JuniorSchool):
    title = "你初中是在人大附中本部就读的吗？"


class Competition(MultipleSelection):
    class NeverGroup(Group):
        options = ["未曾参加"]
        dis = TupleDict({("未曾参加", "未曾参加"): 0})

    class ScienceGroup(Group):
        options = ["数学竞赛", "物理竞赛", "信息学竞赛"]
        dis = TupleDict({("数学竞赛", "数学竞赛"): 8, ("数学竞赛", "物理竞赛"): 4, ("数学竞赛", "信息学竞赛"): 4,
                         ("物理竞赛", "物理竞赛"): 8, ("物理竞赛", "信息学竞赛"): 2,
                         ("信息学竞赛", "信息学竞赛"): 8})

    class BiochemicalGroup(Group):
        options = ["生物学竞赛", "化学竞赛"]
        dis = TupleDict({("化学竞赛", "化学竞赛"): 6, ("化学竞赛", "生物学竞赛"): 3,
                         ("生物学竞赛", "生物学竞赛"): 6})

    class OtherGroup(Group):
        options = ["其他学科竞赛"]
        dis = TupleDict({("其他学科竞赛", "其他学科竞赛"): 1})

    groups = [NeverGroup, ScienceGroup, BiochemicalGroup, OtherGroup]
    group_dis = TupleDict({(NeverGroup, NeverGroup): 0, (NeverGroup, ScienceGroup): 0, (NeverGroup, BiochemicalGroup): 0, (NeverGroup, OtherGroup): 0,
                           (ScienceGroup, ScienceGroup): 0, (ScienceGroup, BiochemicalGroup): 2, (ScienceGroup, OtherGroup): 1,
                           (BiochemicalGroup, BiochemicalGroup): 0, (BiochemicalGroup, OtherGroup): 1,
                           (OtherGroup, OtherGroup): 0})


class YoungerCompetition(Competition):
    title = "你主要参加过/有意向参加哪些学科竞赛呢？"


class ElderCompetition(Competition):
    title = "你主要参加过哪些学科竞赛呢？"


Competition.options = init_options(Competition)
Competition.dis = init_dis(Competition)


class Boarder(SingleSelection):
    dis = {("曾是", "是"): 4, ("曾是", "曾是"): 2, ("曾是", "未曾是"): 0,
           ("未曾是", "是"): 0, ("未曾是", "曾是"): 0, ("未曾是", "未曾是"): 1}  # use map here


class YoungerBroader(Boarder):
    title = "你曾经是住宿生吗？"
    options = ["曾是", "未曾是"]


class ElderBroader(Boarder):
    title = "你现在是住宿生吗？"
    options = ["是", "曾是", "未曾是"]


class Software(MultipleSelection):
    title = "你最常用的软件是哪些呢？"
    options = ["微信聊天", "微信朋友圈", "微博", "知乎", "抖音", "哔哩哔哩",
               "Lofter", "Facebook, Twitter, Instagram", "其他软件"]
    dis = TupleDict({("微信聊天", "微信聊天"): 7, ("微信聊天", "微信朋友圈"): 4, ("微信聊天", "微博"): 1, ("微信聊天", "知乎"): 1, ("微信聊天", "抖音"): 0, ("微信聊天", "哔哩哔哩"): 0, ("微信聊天", "Lofter"): 1, ("微信聊天", "Facebook, Twitter, Instagram"): 3, ("微信聊天", "其他软件"): 0,
                     ("微信朋友圈", "微信朋友圈"): 6, ("微信朋友圈", "微博"): 3, ("微信朋友圈", "知乎"): 0, ("微信朋友圈", "抖音"): 1, ("微信朋友圈", "哔哩哔哩"): 1, ("微信朋友圈", "Lofter"): 0, ("微信朋友圈", "Facebook, Twitter, Instagram"): 1, ("微信朋友圈", "其他软件"): 0,
                     ("微博", "微博"): 5, ("微博", "知乎"): 2, ("微博", "抖音"): 3, ("微博", "哔哩哔哩"): 1, ("微博", "Lofter"): 2, ("微博", "Facebook, Twitter, Instagram"): 1, ("微博", "其他软件"): 0,
                     ("知乎", "知乎"): 6, ("知乎", "抖音"): 0, ("知乎", "哔哩哔哩"): 0, ("知乎", "Lofter"): 0, ("知乎", "Facebook, Twitter, Instagram"): 0, ("知乎", "其他软件"): 0,
                     ("抖音", "抖音"): 7, ("抖音", "哔哩哔哩"): 2, ("抖音", "Lofter"): 0, ("抖音", "Facebook, Twitter, Instagram"): 0, ("抖音", "其他软件"): 0,
                     ("哔哩哔哩", "哔哩哔哩"): 6, ("哔哩哔哩", "Lofter"): 0, ("哔哩哔哩", "Facebook, Twitter, Instagram"): 0, ("哔哩哔哩", "其他软件"): 0,
                     ("Lofter", "Lofter"): 8, ("Lofter", "Facebook, Twitter, Instagram"): 3, ("Lofter", "其他软件"): 0,
                     ("Facebook, Twitter, Instagram", "Facebook, Twitter, Instagram"): 8, ("Facebook, Twitter, Instagram", "其他软件"): 0,
                     ("其他软件", "其他软件"): 1})

    def __init__(self, str):
        str = str.replace("Facebook, Twitter, Instagram", "FTI")
        super().__init__(str)
        self.answer = {"Facebook, Twitter, Instagram" if x ==
                       "FTI" else x for x in self.answer}


class Activity(SingleSelection):
    title = "你最感兴趣哪个校园活动呢？"

    class SportGroup(Group):
        options = ["篮球联赛", "足球联赛"]
        dis = TupleDict({("篮球联赛", "篮球联赛"): 6, ("篮球联赛", "足球联赛"): 4,
                         ("足球联赛", "足球联赛"): 6})

    class VolunteerGroup(Group):
        options = ["志愿活动", "公益 GALA 夜"]
        dis = TupleDict({("志愿活动", "志愿活动"): 6, ("志愿活动", "公益 GALA 夜"): 4,
                         ("公益 GALA 夜", "公益 GALA 夜"): 6})

    class ActivityGroup(Group):
        options = ["歌舞嘉年华", "新年快递", "主持人大赛", "社团文化节", "学生电影节"]
        dis = TupleDict({("歌舞嘉年华", "歌舞嘉年华"): 6, ("歌舞嘉年华", "新年快递"): 0, ("歌舞嘉年华", "主持人大赛"): 2, ("歌舞嘉年华", "社团文化节"): 2, ("歌舞嘉年华", "学生电影节"): 4,
                         ("新年快递", "新年快递"): 4, ("新年快递", "主持人大赛"): 0, ("新年快递", "社团文化节"): 1, ("新年快递", "学生电影节"): 0,
                         ("主持人大赛", "主持人大赛"): 7, ("主持人大赛", "社团文化节"): 4, ("主持人大赛", "学生电影节"): 3,
                         ("社团文化节", "社团文化节"): 6, ("社团文化节", "学生电影节"): 5,
                         ("学生电影节", "学生电影节"): 6})

    class OtherGroup(Group):
        options = ["其他校园活动"]
        dis = TupleDict({("其他校园活动", "其他校园活动"): 1})

    group_dis = TupleDict({(SportGroup, SportGroup): 0, (SportGroup, VolunteerGroup): 0, (SportGroup, ActivityGroup): 1, (SportGroup, OtherGroup): 0,
                           (VolunteerGroup, VolunteerGroup): 0, (VolunteerGroup, ActivityGroup): 2, (VolunteerGroup, OtherGroup): 0,
                           (ActivityGroup, ActivityGroup): 0, (ActivityGroup, OtherGroup): 1,
                           (OtherGroup, OtherGroup): 0})
    groups = [SportGroup, VolunteerGroup, ActivityGroup, OtherGroup]


Activity.options = init_options(Activity)
Activity.dis = init_dis(Activity)


class Interest(MultipleSelection):
    title = "你感兴趣哪些领域呢？"

    class SportGroup(Group):
        options = ["篮球", "足球", "羽毛球", "乒乓球", "滑板", "旱冰",
                   "跑步", "跳绳", "举重", "跳伞", "攀岩", "蹦极", "其他运动"]
        dis = TupleDict({("篮球", "篮球"): 4, ("篮球", "足球"): 2, ("篮球", "羽毛球"): 1, ("篮球", "乒乓球"): 1, ("篮球", "滑板"): 0, ("篮球", "旱冰"): 0, ("篮球", "跑步"): 0, ("篮球", "跳绳"): 0, ("篮球", "举重"): 0, ("篮球", "跳伞"): 0, ("篮球", "攀岩"): 0, ("篮球", "蹦极"): 0, ("篮球", "其他运动"): 0,
                         ("足球", "足球"): 4, ("足球", "羽毛球"): 1, ("足球", "乒乓球"): 1, ("足球", "滑板"): 0, ("足球", "旱冰"): 0, ("足球", "跑步"): 0, ("足球", "跳绳"): 0, ("足球", "举重"): 0, ("足球", "跳伞"): 0, ("足球", "攀岩"): 0, ("足球", "蹦极"): 0, ("足球", "其他运动"): 0,
                         ("羽毛球", "羽毛球"): 4, ("羽毛球", "乒乓球"): 2, ("羽毛球", "滑板"): 0, ("羽毛球", "旱冰"): 0, ("羽毛球", "跑步"): 0, ("羽毛球", "跳绳"): 0, ("羽毛球", "举重"): 0, ("羽毛球", "跳伞"): 0, ("羽毛球", "攀岩"): 0, ("羽毛球", "蹦极"): 0, ("羽毛球", "其他运动"): 0,
                         ("乒乓球", "乒乓球"): 4, ("乒乓球", "滑板"): 0, ("乒乓球", "旱冰"): 0, ("乒乓球", "跑步"): 0, ("乒乓球", "跳绳"): 0, ("乒乓球", "举重"): 0, ("乒乓球", "跳伞"): 0, ("乒乓球", "攀岩"): 0, ("乒乓球", "蹦极"): 0, ("乒乓球", "其他运动"): 0,
                         ("滑板", "滑板"): 4, ("滑板", "旱冰"): 2, ("滑板", "跑步"): 1, ("滑板", "跳绳"): 0, ("滑板", "举重"): 0, ("滑板", "跳伞"): 0, ("滑板", "攀岩"): 0, ("滑板", "蹦极"): 0, ("滑板", "其他运动"): 0,
                         ("旱冰", "旱冰"): 4, ("旱冰", "跑步"): 1, ("旱冰", "跳绳"): 0, ("旱冰", "举重"): 0, ("旱冰", "跳伞"): 0, ("旱冰", "攀岩"): 0, ("旱冰", "蹦极"): 0, ("旱冰", "其他运动"): 0,
                         ("跑步", "跑步"): 4, ("跑步", "跳绳"): 0, ("跑步", "举重"): 0, ("跑步", "跳伞"): 0, ("跑步", "攀岩"): 0, ("跑步", "蹦极"): 0, ("跑步", "其他运动"): 0,
                         ("跳绳", "跳绳"): 4, ("跳绳", "举重"): 0, ("跳绳", "跳伞"): 0, ("跳绳", "攀岩"): 0, ("跳绳", "蹦极"): 0, ("跳绳", "其他运动"): 0,
                         ("举重", "举重"): 4, ("举重", "跳伞"): 0, ("举重", "攀岩"): 0, ("举重", "蹦极"): 0, ("举重", "其他运动"): 0,
                         ("跳伞", "跳伞"): 4, ("跳伞", "攀岩"): 2, ("跳伞", "蹦极"): 2, ("跳伞", "其他运动"): 0,
                         ("攀岩", "攀岩"): 4, ("攀岩", "蹦极"): 2, ("攀岩", "其他运动"): 0,
                         ("蹦极", "蹦极"): 4, ("蹦极", "其他运动"): 0,
                         ("其他运动", "其他运动"): 2})

    class CulturalGroup(Group):
        options = ["音乐", "绘画", "写作", "读书", "电影", "戏剧",
                   "纸艺", "茶艺", "积木", "模型", "拼图", "其他文艺活动"]
        dis = TupleDict({("音乐", "音乐"): 4, ("音乐", "绘画"): 2, ("音乐", "写作"): 1, ("音乐", "读书"): 1, ("音乐", "电影"): 2, ("音乐", "戏剧"): 2, ("音乐", "纸艺"): 0, ("音乐", "茶艺"): 0, ("音乐", "积木"): 0, ("音乐", "模型"): 0, ("音乐", "拼图"): 0, ("音乐", "其他文艺活动"): 0,
                         ("绘画", "绘画"): 4, ("绘画", "写作"): 1, ("绘画", "读书"): 0, ("绘画", "电影"): 1, ("绘画", "戏剧"): 0, ("绘画", "纸艺"): 0, ("绘画", "茶艺"): 0, ("绘画", "积木"): 0, ("绘画", "模型"): 0, ("绘画", "拼图"): 0, ("绘画", "其他文艺活动"): 0,
                         ("写作", "写作"): 4, ("写作", "读书"): 3, ("写作", "电影"): 2, ("写作", "戏剧"): 2, ("写作", "纸艺"): 0, ("写作", "茶艺"): 0, ("写作", "积木"): 0, ("写作", "模型"): 0, ("写作", "拼图"): 0, ("写作", "其他文艺活动"): 0,
                         ("读书", "读书"): 4, ("读书", "电影"): 2, ("读书", "戏剧"): 1, ("读书", "纸艺"): 0, ("读书", "茶艺"): 0, ("读书", "积木"): 0, ("读书", "模型"): 0, ("读书", "拼图"): 0, ("读书", "其他文艺活动"): 0,
                         ("电影", "电影"): 4, ("电影", "戏剧"): 3, ("电影", "纸艺"): 0, ("电影", "茶艺"): 0, ("电影", "积木"): 0, ("电影", "模型"): 0, ("电影", "拼图"): 0, ("电影", "其他文艺活动"): 0,
                         ("戏剧", "戏剧"): 4, ("戏剧", "纸艺"): 0, ("戏剧", "茶艺"): 0, ("戏剧", "积木"): 0, ("戏剧", "模型"): 0, ("戏剧", "拼图"): 0, ("戏剧", "其他文艺活动"): 0,
                         ("纸艺", "纸艺"): 4, ("纸艺", "茶艺"): 2, ("纸艺", "积木"): 1, ("纸艺", "模型"): 1, ("纸艺", "拼图"): 0, ("纸艺", "其他文艺活动"): 0,
                         ("茶艺", "茶艺"): 4, ("茶艺", "积木"): 0, ("茶艺", "模型"): 0, ("茶艺", "拼图"): 0, ("茶艺", "其他文艺活动"): 0,
                         ("积木", "积木"): 4, ("积木", "模型"): 2, ("积木", "拼图"): 2, ("积木", "其他文艺活动"): 2,
                         ("模型", "模型"): 4, ("模型", "拼图"): 2, ("模型", "其他文艺活动"): 0,
                         ("拼图", "拼图"): 4, ("拼图", "其他文艺活动"): 0,
                         ("其他文艺活动", "其他文艺活动"): 2})

    class CollectGroup(Group):
        options = ["汽车", "手表", "鞋", "电子产品", "其他收藏"]
        dis = TupleDict({("汽车", "汽车"): 4, ("汽车", "手表"): 0, ("汽车", "鞋"): 0, ("汽车", "电子产品"): 0, ("汽车", "其他收藏"): 0,
                         ("手表", "手表"): 4, ("手表", "鞋"): 0, ("手表", "电子产品"): 1, ("手表", "其他收藏"): 0,
                         ("鞋", "鞋"): 4, ("鞋", "电子产品"): 0, ("鞋", "其他收藏"): 0,
                         ("电子产品", "电子产品"): 4, ("电子产品", "其他收藏"): 0,
                         ("其他收藏", "其他收藏"): 2})

    class MusicalGroup(Group):
        options = ["钢琴", "吉他", "大号", "小号", "葫芦丝", "萨克斯", "其他乐器"]
        dis = TupleDict({("钢琴", "钢琴"): 3, ("钢琴", "吉他"): 1, ("钢琴", "大号"): 0, ("钢琴", "小号"): 0, ("钢琴", "葫芦丝"): 0, ("钢琴", "萨克斯"): 0, ("钢琴", "其他乐器"): 0,
                         ("吉他", "吉他"): 4, ("吉他", "大号"): 0, ("吉他", "小号"): 0, ("吉他", "葫芦丝"): 0, ("吉他", "萨克斯"): 0, ("吉他", "其他乐器"): 0,
                         ("大号", "大号"): 4, ("大号", "小号"): 2, ("大号", "葫芦丝"): 0, ("大号", "萨克斯"): 1, ("大号", "其他乐器"): 0,
                         ("小号", "小号"): 4, ("小号", "葫芦丝"): 0, ("小号", "萨克斯"): 1, ("小号", "其他乐器"): 0,
                         ("葫芦丝", "葫芦丝"): 4, ("葫芦丝", "萨克斯"): 0, ("葫芦丝", "其他乐器"): 0,
                         ("萨克斯", "萨克斯"): 4, ("萨克斯", "其他乐器"): 0,
                         ("其他乐器", "其他乐器"): 1})

    class GameGroup(Group):
        options = ["动作游戏", "冒险游戏", "模拟游戏", "角色扮演游戏", "休闲游戏", "其他游戏"]
        dis = TupleDict({("动作游戏", "动作游戏"): 4, ("动作游戏", "冒险游戏"): 0, ("动作游戏", "模拟游戏"): 0, ("动作游戏", "角色扮演游戏"): 0, ("动作游戏", "休闲游戏"): 0, ("动作游戏", "其他游戏"): 0,
                         ("冒险游戏", "冒险游戏"): 4, ("冒险游戏", "模拟游戏"): 0, ("冒险游戏", "角色扮演游戏"): 0, ("冒险游戏", "休闲游戏"): 0, ("冒险游戏", "其他游戏"): 0,
                         ("模拟游戏", "模拟游戏"): 4, ("模拟游戏", "角色扮演游戏"): 1, ("模拟游戏", "休闲游戏"): 1, ("模拟游戏", "其他游戏"): 0,
                         ("角色扮演游戏", "角色扮演游戏"): 4, ("角色扮演游戏", "休闲游戏"): 0, ("角色扮演游戏", "其他游戏"): 0,
                         ("休闲游戏", "休闲游戏"): 4, ("休闲游戏", "其他游戏"): 0,
                         ("其他游戏", "其他游戏"): 2})

    group_dis = TupleDict({(SportGroup, SportGroup): 1, (SportGroup, CulturalGroup): 0, (SportGroup, CollectGroup): 0, (SportGroup, MusicalGroup): 0, (SportGroup, GameGroup): 0,
                           (CulturalGroup, CulturalGroup): 1, (CulturalGroup, CollectGroup): 0, (CulturalGroup, MusicalGroup): 0, (CulturalGroup, GameGroup): 0,
                           (CollectGroup, CollectGroup): 1, (CollectGroup, MusicalGroup): 0, (CollectGroup, GameGroup): 0,
                           (MusicalGroup, MusicalGroup): 1, (MusicalGroup, GameGroup): 0,
                           (GameGroup, GameGroup): 1})
    groups = [SportGroup, CulturalGroup, CollectGroup, MusicalGroup, GameGroup]


Interest.options = init_options(Interest)
Interest.dis = init_dis(Interest)
