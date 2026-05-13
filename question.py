# Picks a school for each round and formats the clue card.
# Hpone

import pandas as pd


# formatters for each kind of stat
def pct(v):    return f"{v*100:.1f}%"
def num(v):    return f"{int(v):,}"
def money(v):  return f"${int(v):,}"
def asis(v):   return str(v)


# stat key -> (label shown to player, how to format the value)
STATS = {
    "STABBR":          ("State",                  asis),
    "REGION_NAME":     ("Region",                 asis),
    "CONTROL_NAME":    ("Institution type",       asis),
    "ADM_RATE":        ("Acceptance rate",        pct),
    "SAT_AVG":         ("Average SAT",            num),
    "UGDS":            ("Undergrad enrollment",   num),
    "TUITIONFEE_IN":   ("In-state tuition",       money),
    "TUITIONFEE_OUT":  ("Out-of-state tuition",   money),
    "GRAD_RATE":       ("6-year graduation rate", pct),
    "MD_EARN_WNE_P10": ("Median earnings (10y)",  money),
}

# which stats are visible by default at each difficulty.
# everything else gets hidden.
VISIBLE = {
    "easy":   ["STABBR", "REGION_NAME", "ADM_RATE", "SAT_AVG", "UGDS",
               "TUITIONFEE_IN", "GRAD_RATE", "MD_EARN_WNE_P10"],
    "medium": ["REGION_NAME", "ADM_RATE", "SAT_AVG", "UGDS",
               "TUITIONFEE_IN", "GRAD_RATE"],
    "hard":   ["ADM_RATE", "SAT_AVG", "TUITIONFEE_IN", "GRAD_RATE"],
}

# common nicknames the fuzzy matcher would otherwise miss.
# e.g. "ucla" doesn't fuzzy-match "University of California-Los Angeles".
ALIASES = {
    "ucla":          "University of California-Los Angeles",
    "cal":           "University of California-Berkeley",
    "berkeley":      "University of California-Berkeley",
    "uc berkeley":   "University of California-Berkeley",
    "ucsd":          "University of California-San Diego",
    "ucsb":          "University of California-Santa Barbara",
    "ucsc":          "University of California-Santa Cruz",
    "uci":           "University of California-Irvine",
    "ucr":           "University of California-Riverside",
    "ucd":           "University of California-Davis",
    "mit":           "Massachusetts Institute of Technology",
    "caltech":       "California Institute of Technology",
    "cmu":           "Carnegie Mellon University",
    "georgia tech":  "Georgia Institute of Technology-Main Campus",
    "gtech":         "Georgia Institute of Technology-Main Campus",
    "virginia tech": "Virginia Polytechnic Institute and State University",
    "vt":            "Virginia Polytechnic Institute and State University",
    "penn state":    "Pennsylvania State University-Main Campus",
    "psu":           "Pennsylvania State University-Main Campus",
    "penn":          "University of Pennsylvania",
    "upenn":         "University of Pennsylvania",
    "nyu":           "New York University",
    "usc":           "University of Southern California",
    "umich":         "University of Michigan-Ann Arbor",
    "michigan":      "University of Michigan-Ann Arbor",
    "uiuc":          "University of Illinois Urbana-Champaign",
    "wash u":        "Washington University in St Louis",
    "wustl":         "Washington University in St Louis",
    "tamu":          "Texas A & M University-College Station",
    "ut austin":     "The University of Texas at Austin",
    "uva":           "University of Virginia-Main Campus",
    "unc":           "University of North Carolina at Chapel Hill",
    "osu":           "Ohio State University-Main Campus",
    "uf":            "University of Florida",
    "uw":            "University of Washington-Seattle Campus",
    "rpi":           "Rensselaer Polytechnic Institute",
# Picks a school for each round and formats the clue card.

import pandas as pd


# formatters for each kind of stat
def pct(v):    return f"{v*100:.1f}%"
def num(v):    return f"{int(v):,}"
def money(v):  return f"${int(v):,}"
def asis(v):   return str(v)


# stat key -> (label shown to player, how to format the value)
STATS = {
    "STABBR":          ("State",                  asis),
    "REGION_NAME":     ("Region",                 asis),
    "CONTROL_NAME":    ("Institution type",       asis),
    "ADM_RATE":        ("Acceptance rate",        pct),
    "SAT_AVG":         ("Average SAT",            num),
    "UGDS":            ("Undergrad enrollment",   num),
    "TUITIONFEE_IN":   ("In-state tuition",       money),
    "TUITIONFEE_OUT":  ("Out-of-state tuition",   money),
    "GRAD_RATE":       ("6-year graduation rate", pct),
    "MD_EARN_WNE_P10": ("Median earnings (10y)",  money),
}

# which stats are visible by default at each difficulty.
# everything else gets hidden.
VISIBLE = {
    "easy":   ["STABBR", "REGION_NAME", "ADM_RATE", "SAT_AVG", "UGDS",
               "TUITIONFEE_IN", "GRAD_RATE", "MD_EARN_WNE_P10"],
    "medium": ["REGION_NAME", "ADM_RATE", "SAT_AVG", "UGDS",
               "TUITIONFEE_IN", "GRAD_RATE"],
    "hard":   ["ADM_RATE", "SAT_AVG", "TUITIONFEE_IN", "GRAD_RATE"],
}

# common nicknames the fuzzy matcher would otherwise miss.
# e.g. "ucla" doesn't fuzzy-match "University of California-Los Angeles".
ALIASES = {
    "ucla":          "University of California-Los Angeles",
    "cal":           "University of California-Berkeley",
    "berkeley":      "University of California-Berkeley",
    "uc berkeley":   "University of California-Berkeley",
    "ucsd":          "University of California-San Diego",
    "ucsb":          "University of California-Santa Barbara",
    "ucsc":          "University of California-Santa Cruz",
    "uci":           "University of California-Irvine",
    "ucr":           "University of California-Riverside",
    "ucd":           "University of California-Davis",
    "mit":           "Massachusetts Institute of Technology",
    "caltech":       "California Institute of Technology",
    "cmu":           "Carnegie Mellon University",
    "georgia tech":  "Georgia Institute of Technology-Main Campus",
    "gtech":         "Georgia Institute of Technology-Main Campus",
    "virginia tech": "Virginia Polytechnic Institute and State University",
    "vt":            "Virginia Polytechnic Institute and State University",
    "penn state":    "Pennsylvania State University-Main Campus",
    "psu":           "Pennsylvania State University-Main Campus",
    "penn":          "University of Pennsylvania",
    "upenn":         "University of Pennsylvania",
    "nyu":           "New York University",
    "usc":           "University of Southern California",
    "umich":         "University of Michigan-Ann Arbor",
    "michigan":      "University of Michigan-Ann Arbor",
    "uiuc":          "University of Illinois Urbana-Champaign",
    "wash u":        "Washington University in St Louis",
    "wustl":         "Washington University in St Louis",
    "tamu":          "Texas A & M University-College Station",
    "ut austin":     "The University of Texas at Austin",
    "uva":           "University of Virginia-Main Campus",
    "unc":           "University of North Carolina at Chapel Hill",
    "osu":           "Ohio State University-Main Campus",
    "uf":            "University of Florida",
    "uw":            "University of Washington-Seattle Campus",
    "rpi":           "Rensselaer Polytechnic Institute",
}


def load_schools(path="data/cleaned_schools.csv"):
    return pd.read_csv(path)


def pick_school(df, exclude=None):
    #Pick a random school, skipping ones already used this game.
    if exclude is None:
        exclude = set()
    pool = df[~df["INSTNM"].isin(exclude)]
    if len(pool) == 0:
        pool = df  # ran through everything, start over
    return pool.sample(1).iloc[0].to_dict()


def format_clues(school, difficulty, extra_revealed=None):
    #Build the clue card for the round as a string.
    if extra_revealed is None:
        extra_revealed = []
    visible = set(VISIBLE[difficulty]) | set(extra_revealed)

    lines = []
    for key, (label, fmt) in STATS.items():
        if key in visible and key in school and pd.notna(school[key]):
            lines.append(f"  {label:.<28} {fmt(school[key])}")

    hidden = [label for key, (label, _) in STATS.items() if key not in visible]
    if hidden:
        lines.append("")
        lines.append("  Hidden:")
        for label in hidden:
            lines.append(f"    - {label}")
    return "\n".join(lines)


def hidden_stats(school, difficulty, already_revealed):
    #Return keys that are still hidden AND have a value (so a hint can reveal them).
    visible = set(VISIBLE[difficulty]) | set(already_revealed)
    return [k for k in STATS
            if k not in visible and k in school and pd.notna(school[k])]


def resolve_alias(name):
    return ALIASES.get(name.strip().lower())