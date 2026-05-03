# Cleans the raw College Scorecard CSV down to a smaller set of well-known
# 4-year colleges. Run once: python data_cleaner.py

import os
import pandas as pd

RAW_PATH = "data/raw_scorecard.csv"
OUT_PATH = "data/cleaned_schools.csv"

# columns we  use
COLS = [
    "INSTNM", "CITY", "STABBR", "REGION",
    "PREDDEG", "CONTROL",
    "ADM_RATE", "SAT_AVG", "UGDS",
    "TUITIONFEE_IN", "TUITIONFEE_OUT",
    "C150_4", "C150_4_POOLED",
    "MD_EARN_WNE_P10",
]

REGION_NAMES = {
    1: "New England", 2: "Mid East", 3: "Great Lakes", 4: "Plains",
    5: "Southeast", 6: "Southwest", 7: "Rocky Mountains", 8: "Far West",
    9: "Outlying Areas",
}

CONTROL_NAMES = {1: "Public", 2: "Private nonprofit", 3: "Private for-profit"}


def main():
    if not os.path.exists(RAW_PATH):
        print("Couldn't find", RAW_PATH)
        print("Download the Most Recent Cohorts: Institution CSV from")
        print("https://collegescorecard.ed.gov/data and put it there.")
        return

    print("Reading raw scorecard...")
    df = pd.read_csv(
        RAW_PATH,
        usecols=COLS,
        na_values=["NULL", "PrivacySuppressed", ""],
        low_memory=False,
    )
    print(f"  {len(df)} institutions in raw file")

    # only 4-year bachelor's-predominant schools
    df = df[df["PREDDEG"] == 3].copy()

    # use the most-recent grad rate, fall back to the pooled one if missing
    df["GRAD_RATE"] = df["C150_4"].fillna(df["C150_4_POOLED"])

    # required stats for the game.
    # We don't require SAT_AVG because lots of big schools don't report it anymore.
    needed = ["ADM_RATE", "UGDS", "TUITIONFEE_IN", "TUITIONFEE_OUT",
              "GRAD_RATE", "MD_EARN_WNE_P10",
              "INSTNM", "CITY", "STABBR", "REGION"]
    df = df.dropna(subset=needed)

    # filter to recognizable schools: big OR selective
    df = df[(df["UGDS"] >= 10000) | (df["ADM_RATE"] < 0.25)]

    # clean up types
    for col in ["UGDS", "TUITIONFEE_IN", "TUITIONFEE_OUT",
                "MD_EARN_WNE_P10", "REGION", "CONTROL"]:
        df[col] = df[col].astype(int)

    # add region/control labels for the clue card
    df["REGION_NAME"] = df["REGION"].map(REGION_NAMES)
    df["CONTROL_NAME"] = df["CONTROL"].map(CONTROL_NAMES)

    out_cols = ["INSTNM", "CITY", "STABBR", "REGION", "REGION_NAME",
                "CONTROL", "CONTROL_NAME", "ADM_RATE", "SAT_AVG", "UGDS",
                "TUITIONFEE_IN", "TUITIONFEE_OUT", "GRAD_RATE",
                "MD_EARN_WNE_P10"]
    df = df[out_cols].sort_values("INSTNM").reset_index(drop=True)

    print(f"  {len(df)} schools after filtering")
    df.to_csv(OUT_PATH, index=False)
    print("Wrote", OUT_PATH)


if __name__ == "__main__":
    main()
