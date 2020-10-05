from process import get_uid
import pandas as pd

name = input()
number = int(input())

print(get_uid({"姓名": name, "手机号": number}))
