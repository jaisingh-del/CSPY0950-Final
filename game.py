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

# Jai with Hpone


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


# tracks which schools we've already used this game
seen_schools = set()
def play_round(df, school_names, score, streak, rounds_correct):
    """Play one round. Returns (new_score, new_streak, new_rounds_correct, outcome)
    where outcome is 'correct', 'wrong', 'skip', or 'quit'."""
    difficulty = scoring.difficulty_ramp(rounds_correct)
    school = question.pick_school(df, exclude=seen_schools)
    seen_schools.add(school["INSTNM"])

    extra_revealed = []
    hints_used = 0
    last_guess_name = None
    guesses_used = 0

    print_separator()
    print(scoring.format_score_line(score, streak, difficulty))
    print_separator()
    print(question.format_clues(school, difficulty, extra_revealed))
    print()
    print("  Type your guess, or 'hint' / 'skip' / 'quit'.")

    while True:
        raw = input("  > ").strip()
        if not raw:
            continue
        cmd = raw.lower()

        if cmd in ("quit", "q", "exit"):
            return score, streak, rounds_correct, "quit"

        if cmd in ("skip", "s"):
            print(f"  Answer was: {school['INSTNM']}.")
            new_score, _ = scoring.update_score(score, difficulty, streak,
                                                hints_used, correct=False)
            return new_score, 0, rounds_correct, "skip"

        if cmd in ("hint", "h"):
            if hints_used >= MAX_HINTS_PER_ROUND:
                print(f"  Out of hints (max {MAX_HINTS_PER_ROUND} per round).")
                continue
            can_reveal = bool(question.hidden_stats(school, difficulty, extra_revealed))
            can_hot_cold = last_guess_name is not None
            choice = ask_hint_choice(can_reveal, can_hot_cold)
            if choice == "reveal":
                result = hints.reveal_stat(school, difficulty, extra_revealed)
                if result is not None:
                    _, msg = result
                    print(f"  {msg}")
                    hints_used += 1
                    print()
                    print(question.format_clues(school, difficulty, extra_revealed))
            elif choice == "hot_cold":
                msg = hints.hot_cold(school, last_guess_name, df)
                # indent the hot/cold output to match the rest of the round
                print("  " + msg.replace("\n", "\n  "))
                hints_used += 1
            continue  # don't count a hint as a guess

        # otherwise it's a guess
        guesses_used += 1
        match = fuzzy_match(raw, school_names)

        if match == school["INSTNM"]:
            new_score, delta = scoring.update_score(score, difficulty, streak,
                                                    hints_used, correct=True)
            new_streak = scoring.get_streak(streak, True)
            mult = scoring.streak_multiplier(streak)
            print(f"  CORRECT -- {school['INSTNM']}.")
            print(f"  +{delta} pts (base {scoring.BASE_POINTS[difficulty]}, "
                  f"x{mult:g} streak, -{scoring.HINT_COST * hints_used} hints).")
            return new_score, new_streak, rounds_correct + 1, "correct"

        # wrong. tell the player what we read their guess as if anything
        if match:
            print(f"  Not quite. (Read your guess as: {match}.)")
            last_guess_name = match
        else:
            print("  Not quite. (Couldn't recognize that name -- try again.)")

        if guesses_used >= MAX_GUESSES_PER_ROUND:
            print(f"  Out of guesses. The answer was: {school['INSTNM']}.")
            new_score, _ = scoring.update_score(score, difficulty, streak,
                                                hints_used, correct=False)
            return new_score, 0, rounds_correct, "wrong"


def run():
    print()
    print("=" * 60)
    print("  GUESS THAT COLLEGE")
    print("  Identify a school from its admissions and outcomes stats.")
    print("=" * 60)

    df = question.load_schools()
    school_names = df["INSTNM"].tolist()
    print(f"  ({len(df)} schools loaded)\n")

    board = leaderboard.load_leaderboard()
    print(leaderboard.display(board))
    print()

    name = input("Your name: ").strip() or "anon"

    seen_schools.clear()  # reset between games

    score = 0
    streak = 0
    rounds_correct = 0
    rounds_played = 0

    while True:
        score, streak, rounds_correct, outcome = play_round(
            df, school_names, score, streak, rounds_correct
        )
        rounds_played += 1
        if outcome == "quit":
            break
        cont = input("\nAnother round? (Y/n) ").strip().lower()
        if cont in ("n", "no", "q", "quit"):
            break

    print_separator()
    print(f"Game over. {name}, you scored {score} across {rounds_played} round(s).")

    board, rank = leaderboard.add_score(board, name, score)
    leaderboard.save_leaderboard(board)
    if rank:
        print(f"You made the leaderboard at rank #{rank}.\n")
    else:
        print()
    print(leaderboard.display(board))
    print()
