import math
import random
import question

# Hpone with Jai

def reveal_stat(school, difficulty, already_revealed):
    #Pick one hidden stat and reveal it. Returns key, message or None.
    candidates = question.hidden_stats(school, difficulty, already_revealed)
    if not candidates:
        return None

    # prefer revealing location/size/type first, since those narrow it down most
    priority = ["STABBR", "REGION_NAME", "CONTROL_NAME", "UGDS",
                "TUITIONFEE_OUT", "MD_EARN_WNE_P10"]
    chosen = None
    for key in priority:
        if key in candidates:
            chosen = key
            break
    if chosen is None:
        chosen = random.choice(candidates)

    label, fmt = question.STATS[chosen]
    already_revealed.append(chosen)
    return chosen, f"Revealed -> {label}: {fmt(school[chosen])}"


def temp_label(distance, far, mid, close):
    """Translate a numeric distance into hot/cold language."""
    if distance < close:
        return "BURNING HOT"
    if distance < mid:
        return "warm"
    if distance < far:
        return "cool"
    return "ice cold"

def hot_cold(answer, guess_name, df):
    rows = df[df["INSTNM"].str.lower() == guess_name.strip().lower()]
    if len(rows) == 0:
        # try substring
        rows = df[df["INSTNM"].str.lower().str.contains(
            guess_name.strip().lower(), regex=False)]
    if len(rows) == 0:
        return "(Can't find that school in the data, no hot/cold available.)"

    g = rows.iloc[0]
    out = [f"Hot/cold vs '{g['INSTNM']}':"]

    # acceptance rate: just absolute difference
    d = abs(float(g["ADM_RATE"]) - float(answer["ADM_RATE"]))
    out.append(f"  Acceptance rate -> {temp_label(d, 0.40, 0.20, 0.07)}")

    # enrollment: log scale because schools range from ~1k to ~50k
    d = abs(math.log10(max(float(g["UGDS"]), 1)) -
            math.log10(max(float(answer["UGDS"]), 1)))
    out.append(f"  Enrollment -> {temp_label(d, 1.0, 0.5, 0.2)}")

    # in-state tuition dollar difference
    d = abs(float(g["TUITIONFEE_IN"]) - float(answer["TUITIONFEE_IN"]))
    out.append(f"  In-state tuition -> {temp_label(d, 30000, 15000, 5000)}")

    # location check
    if str(g["STABBR"]) == str(answer["STABBR"]):
        out.append("  Same state as the answer.")
    elif str(g["REGION"]) == str(answer["REGION"]):
        out.append("  Same region, different state.")
    else:
        out.append("  Different region.")

    return "\n".join(out)