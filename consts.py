from form import *

ELDER_INPUT = "input/2020121-elder.csv"
YOUNGER_INPUT = "input/2020121-younger.csv"
ELDER_OUTPUT_JUNIOR = "output/2020121-elder-j.csv"
ELDER_OUTPUT_SENIOR = "output/2020121-elder-s.csv"
ELDER_OUTPUT_ICC = "output/2020121-elder-icc.csv"
YOUNGER_OUTPUT_JUNIOR = "output/2020121-younger-j.csv"
YOUNGER_OUTPUT_SENIOR = "output/2020121-younger-s.csv"
YOUNGER_OUTPUT_ICC = "output/2020121-younger-icc.csv"

USELESS_PROPERTIES = ["Submission ID", "Time", "欢迎参加 2020 One to One 活动～"]
YOUNGER_RENAME_STRATEGY = {
    "你的选科将是什么呢？": "选科-高中",
    "你的选科将是什么呢？.1": "选科-初中",
    "你对你的大朋友有什么特殊要求吗？": "特殊要求",
    "年级（ICCS1、本部高一已停止招募，请勿选择 ICCS1、本部高一）": "年级"
}
ELDER_RENAME_STRATEGY = {
    "你的选科是什么呢？": "选科-高中",
    "你的选科是什么呢？.1": "选科-初中",
    "你对你的小朋友有什么特殊要求吗？": "特殊要求"
}
REPLACE_VALUE = {
}
DROP_JUNIOR = ["年级", "选科-高中", "你期望出国吗？", "你所在的项目是哪个呢？",
               "你最希望申请哪里呢？", "本部高一的招募已经截止，请勿填写此表单！", "ICC 的招募已经截止，请勿填写此表单！"]
DROP_SENIOR = ["年级", "选科-初中", "你期望出国吗？", "你所在的项目是哪个呢？",
               "你最希望申请哪里呢？", "本部高一的招募已经截止，请勿填写此表单！", "ICC 的招募已经截止，请勿填写此表单！"]
DROP_ICC = ["年级", "选科-初中", "选科-高中", "你期望出国吗？",
            "本部高一的招募已经截止，请勿填写此表单！", "ICC 的招募已经截止，请勿填写此表单！"]
OPTIONAL = ["你平时最喜欢玩的电子游戏是什么呢？", "你最感兴趣的学生组织是？",
            "你还感兴趣哪些领域呢？", "你还有什么想介绍的吗？", "特殊要求"]
IDENTITY_PROPERTIES = ["姓名", "手机号"]

INF = int(1e6 + 5)
