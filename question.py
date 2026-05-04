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


