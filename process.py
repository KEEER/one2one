import hashlib

import pandas as pd

from consts import *


def get_uid(stu):
    identity = str([stu[prop] for prop in IDENTITY_PROPERTIES])
    return hashlib.md5(identity.encode('utf-8')).hexdigest()


def process(filename):
    data = pd.read_csv(filename)
    data.drop(columns=USELESS_PROPERTIES, inplace=True)
    data["ID"] = list(map(get_uid, data.transpose().to_dict().values()))
    data = data.groupby("ID").first()  # 提交ID大的在前面，一人多次提交取最后一次
    return data


def check_empty(data):
    data = data.isna()
    data = data.apply(lambda stu: stu.any(), axis=1)
    return data[lambda x: x].index.tolist()


def check_duplicate(data):
    duplicated = []
    for prop in IDENTITY_PROPERTIES:
        distribution = data[prop].value_counts()
        repeated = [answer for (answer, cnt)
                    in distribution.items() if cnt > 1]
        duplicated += [ID for (ID, stu) in data.iterrows()
                       if stu[prop] in repeated]
    return list(set(duplicated))


def check_inaccurate(data):
    inaccurate = []
    try:
        inaccurate.extend(data[data["性别"] == "other"].index.tolist())
    except IndexError as e:
        pass
    finally:
        return inaccurate


def part(form0: pd.DataFrame, check, drop, file=None):
    form = form0.copy()[check]
    form.drop(columns=drop, inplace=True, errors='ignore')
    if file:
        form.to_csv(file)
    return form


all_data = []

younger = process(YOUNGER_INPUT)
younger.rename(columns=YOUNGER_RENAME_STRATEGY, inplace=True)
for (ov, nv) in REPLACE_VALUE.items():
    younger.replace(ov, nv, inplace=True)

# TODO: other genders

all_data.append(part(younger, lambda stu: stu["年级"]
                     == "本部初一", DROP_JUNIOR, YOUNGER_OUTPUT_JUNIOR))
all_data.append(part(younger, lambda stu: stu["年级"]
                     == "本部高一", DROP_SENIOR, YOUNGER_OUTPUT_SENIOR))
all_data.append(part(younger, lambda stu: stu["年级"]
                     == "ICCS1", DROP_ICC, YOUNGER_OUTPUT_ICC))

elder = process(ELDER_INPUT)
elder.rename(columns=ELDER_RENAME_STRATEGY, inplace=True)
for (ov, nv) in REPLACE_VALUE.items():
    elder.replace(ov, nv, inplace=True)

all_data.append(part(elder, lambda stu: stu["年级"]
                     == "本部初二", DROP_JUNIOR, ELDER_OUTPUT_JUNIOR))
all_data.append(part(elder, lambda stu: stu["年级"]
                     == "本部高二", DROP_SENIOR, ELDER_OUTPUT_SENIOR))
all_data.append(part(elder, lambda stu: stu["年级"]
                     == "ICCS2", DROP_ICC, ELDER_OUTPUT_ICC))

incorrect = []
for group in all_data:
    incorrect += check_empty(group.drop(columns=OPTIONAL, errors="ignore"))
duplicated = check_duplicate(pd.concat(all_data))
inaccurate = check_inaccurate(pd.concat(all_data))
print("Incorrect answers:", incorrect)
print("(Probably) inaccurate answers", inaccurate)
print("(Probably) duplicated submissions:", duplicated)
