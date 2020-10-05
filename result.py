from consts import *
import pandas as pd

youngers = pd.read_csv(YOUNGER_OUTPUT_JUNIOR)
elders = pd.read_csv(ELDER_OUTPUT_JUNIOR)
phone = []
name = []
name2 = []

# parser = argparse.ArgumentParser(description='Result.')
# parser.add_argument("types", nargs='+',
#                     choices=["icc", "junior", "senior"], help="the type of input")
# parser.add_argument("-v", "--verbose",
#                     help="increase output verbosity")
# args = parser.parse_args()

with open("match/match_junior.out") as f:
    for line in f:
        line = line.replace("\n", "").replace("\r", "").strip()
        arr = line.split(' ')
        if len(arr) == 1:
            continue

        # print(youngers.loc[youngers["ID"] ==
        #                    '094fc536632cf9871dcb25aa4e6d3170']["姓名"][0])
        younger = youngers.loc[youngers["ID"] == arr[0]]
        elder = elders.loc[elders["ID"] == arr[1]]
        if younger.empty:
            younger = youngers.loc[youngers["ID"] == arr[1]]
            elder = elders.loc[elders["ID"] == arr[0]]
            print(arr[0], arr[1])
            if younger.empty:
                raise Exception()

        phone.append(younger["手机号"].values[0])
        name.append(younger["姓名"].values[0])
        name2.append(elder["姓名"].values[0])
        # df.append([{'手机号': int(elder["手机号"]),
        #             'name': str(elder["姓名"]),
        #             "name2": str(younger["姓名"])}], ignore_index=True)

df = pd.DataFrame({"手机号": phone, "name": name, "name2": name2})
df.to_excel("sms-junior-younger.xls")
