# Score, streak, and difficulty math.

BASE_POINTS = {"easy": 10, "medium": 20, "hard": 30}
HINT_COST = 5

# Hpone with Jai

def streak_multiplier(streak):
    # multiplier for `streak` consecutive correct answers
    if streak <= 0: return 1.0
    if streak == 1: return 1.2
    if streak == 2: return 1.5
    if streak == 3: return 2.0
    if streak == 4: return 2.5
    return 3.0  # cap at 3x

# Updates and returns new score and points change after a round
def update_score(score, difficulty, streak, hints_used, correct):
    """Apply the result of a round. Returns (new_score, points_change)."""
    if correct:
        base = BASE_POINTS[difficulty]
        gained = round(base * streak_multiplier(streak)) - HINT_COST * hints_used
        gained = max(gained, 0)  # don't let hints turn a correct answer into negative pts
        return score + gained, gained
    else:
        lost = HINT_COST * hints_used
        return score - lost, -lost

def get_streak(streak, correct):
    # Increments the streak when an answer is correct
    return streak + 1 if correct else 0

# Returns the current difficulty tier, increments tier based on correct answers
def difficulty_ramp(rounds_correct):
    # bump up every 3 correct answers
    if rounds_correct < 3:
        return "easy"
    if rounds_correct < 6:
        return "medium"
    return "hard"

# Returns formmated display 
def format_score_line(score, streak, difficulty):
    mult = streak_multiplier(streak)
    if streak > 0:
        streak_str = f"{streak}-streak ({mult:g}x)"
    else:
        streak_str = "no streak"
    return f"Score: {score}  |  {streak_str}  |  Difficulty: {difficulty.upper()}"
