# Top-5 leaderboard saved to a JSON file.

import json
import os
from datetime import date

PATH = "leaderboard.json"
TOP_N = 5

# Jai

# Loads and returns leaderboard entries from JSON file
def load_leaderboard(path=PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save_leaderboard(entries, path=PATH):
    with open(path, "w") as f:
        json.dump(entries, f, indent=2)


def add_score(entries, name, score):
    #Add a new run, keep top N. Returns (new_list, rank or None).
    name = name.strip() or "anon"
    new_entry = {"name": name, "score": int(score),
                 "date": date.today().isoformat()}
    combined = entries + [new_entry]
    # Merge, sort and truncate to top N
    combined.sort(key=lambda e: e["score"], reverse=True)
    top = combined[:TOP_N]

    # find where (or if) the new entry landed
    for i, e in enumerate(top, start=1):
        if e is new_entry:
            return top, i
    return top, None

# Formatting the leaderboard as a display string
def display(entries, title="Leaderboard"):
    if not entries:
        return f"-- {title} --\n  (no scores yet)"
    lines = [f"-- {title} --"]
    for i, e in enumerate(entries, start=1):
        n = e["name"][:20]
        lines.append(f"  {i}. {n:<20}  {e['score']:>5}   {e.get('date', '')}")
    return "\n".join(lines)
