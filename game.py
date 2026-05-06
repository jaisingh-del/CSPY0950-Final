import difflib
import re

import question
import scoring
import hints
import leaderboard

MAX_HINTS_PER_ROUND = 2
MAX_GUESSES_PER_ROUND = 3
FUZZY_CUTOFF = 0.78   

SKIP_WORDS = {"of", "the", "at", "and", "in", "for", "a", "an"}


def name_tokens(name):
    """Break a school name into significant lowercase words."""
    parts = re.split(r"[\s\-&,]+", name.lower())
    return [p for p in parts if len(p) >= 4 and p not in SKIP_WORDS]


def fuzzy_match(guess, names):
    """Try to map a free-text guess to one of the canonical school names.
    Returns the canonical name or None."""
    guess = guess.strip()
    if not guess:
        return None
    g = guess.lower()

    # 1. alias table (UCLA, MIT, etc)
    alias = question.resolve_alias(guess)
    if alias and alias in names:
        return alias

    # 2. exact case-insensitive match
    for name in names:
        if name.lower() == g:
            return name

    # 3. substring: only accept if exactly one school contains the guess

    if len(g) >= 4:
        hits = [n for n in names if g in n.lower()]
        if len(hits) == 1:
            return hits[0]

    # 4. fuzzy match against each significant word of each school name.
    best_name = None
    best_token_score = 0.0
    best_composite = 0.0
    for name in names:
        full_ratio = difflib.SequenceMatcher(None, g, name.lower()).ratio()
        for tok in name_tokens(name):
            tok_score = difflib.SequenceMatcher(None, g, tok).ratio()
            composite = tok_score + 0.2 * full_ratio
            if composite > best_composite:
                best_composite = composite
                best_token_score = tok_score
                best_name = name
    if best_name is not None and best_token_score >= 0.85:
        return best_name

    # 5. last-ditch: difflib against the whole name
    matches = difflib.get_close_matches(g, [n.lower() for n in names],
                                        n=1, cutoff=FUZZY_CUTOFF)
    if matches:
        for name in names:
            if name.lower() == matches[0]:
                return name

    return None


def print_separator():
    print("-" * 60)


def ask_hint_choice(can_reveal, can_hot_cold):
    """Prompt for a hint type. Returns 'reveal', 'hot_cold', or None."""
    options = []
    if can_reveal:
        options.append(("1", "reveal", "reveal a hidden stat (-5 pts)"))
    if can_hot_cold:
        options.append(("2", "hot_cold", "hot/cold on your last guess (-5 pts)"))

    if not options:
        print("  (No hints available right now.)")
        return None

    print("  Hint options:")
    for tag, _, desc in options:
        print(f"    [{tag}] {desc}")

    while True:
        raw = input("  Pick a hint (or 'cancel'): ").strip().lower()
        if raw in ("cancel", "c", ""):
            return None
        for tag, kind, _ in options:
            if raw == tag or raw == kind:
                return kind
        print("  Didn't get that, try '1', '2', or 'cancel'.")


# tracks which schools we've already used this game so we don't repeat
seen_schools = set()
