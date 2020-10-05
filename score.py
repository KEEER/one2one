import pandas as pd
import argparse
from consts import *
from form.icc import IccForm
from form.junior import JuniorForm
from form.senior import SeniorForm
import json

picked = pd.read_csv("input/hand-picked.csv")


def find(df, column, str):
    return not df[df[column] == str].empty


def process(cls, younger, elder, verbose):
    print(f"score {cls.title}")
    res = []

    for i in range(0, len(younger)):
        yf = cls(younger.iloc[i], "younger")
        for j in range(0, len(elder)):
            ef = cls(elder.iloc[j], "elder")
            obj = cls.score(yf, ef)
            score = sum([value for (key, value) in obj.items()
                         if key.endswith("score")])
            if find(picked, "IDpair", f"{yf.uid}, {ef.uid}"):
                score = INF
            obj.update({
                "score": score
            })
            res.append(obj)

    print(len(younger), len(elder))
    for obj in res:
        if verbose:
            print(json.dumps(obj, ensure_ascii=False, indent=2), end=",\n")
        else:
            print(obj["younger"]["id"], obj["elder"]["id"], obj["score"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Score.')
    parser.add_argument("types", nargs='+',
                        choices=["icc", "junior", "senior"], help="the type of input")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity")
    args = parser.parse_args()

    if args.types.count("icc"):
        process(IccForm, pd.read_csv(YOUNGER_OUTPUT_ICC),
                pd.read_csv(ELDER_OUTPUT_ICC), args.verbose)
    if args.types.count("junior"):
        process(JuniorForm, pd.read_csv(YOUNGER_OUTPUT_JUNIOR),
                pd.read_csv(ELDER_OUTPUT_JUNIOR), args.verbose)
    if args.types.count("senior"):
        process(SeniorForm, pd.read_csv(YOUNGER_OUTPUT_SENIOR),
                pd.read_csv(ELDER_OUTPUT_SENIOR), args.verbose)
