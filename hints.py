import math
import random
import question


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
