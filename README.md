Hpone and Jai
05.13.2026
CSPY 0950 Final Project: Guess That College
Overview
Terminal-based guessing game built on the U.S. Department of Education's College Scorecard dataset. Each round, the game picks a random school and shows you a card of its stats (acceptance rate, SAT average, undergrad enrollment, tuition, graduation rate, median earnings after 10 years, etc.) with the school name hidden. Your job is to figure out which school it is.
The game has a few extras on top of the core guessing loop:
Fuzzy matching on guesses, so typos like “harvrd” and nicknames like “UCLA” or “MIT” both work. 
Hints: You can either reveal one of the hidden stats, or get hot/cold feedback comparing your last wrong guess to the answer. Each hint costs 5 points and you get 2 per round.
Difficulty ramp: Every 3 correct answers, the game hides more stats and the base points go up.
Streak multiplier: Consecutive correct answers stack up to a 3x point multiplier.
Leaderboard: Top 5 scores persist between games in a JSON file.
The dataset is filtered down to ~270 well-known 4-year schools (either big public universities with 10k+ undergrads, or selective schools with under 25% acceptance) so the game is actually guessable.
How to run the program
You need Python 3 and pandas. Paste the below into terminal: 
pip install pandas
python main.py
The cleaned dataset is already in data/cleaned_schools.csv, so you don't need to download anything extra.
If you want to rebuild the cleaned data, download “Most Recent Cohorts: Institution” from https://collegescorecard.ed.gov/data, save it to data/raw_scorecard.csv, then run python data_cleaner.py.
At the in-game prompt you can type:
A school name (fuzzy matched)
Hint: Reveal a stat OR get hot/cold feedback (costs 5 pts)
skip: Give up on this round
Quit: End the game
AI usage
We used Claude Code in our terminals throughout the project. Specifically:
Debugging: When something broke we'd paste the code and ask Claude to help us figure out what was wrong. The most useful cases were a couple of pandas type-conversion bugs in data_cleaner.py (we kept getting “cannot convert NaN to int” until Claude pointed out we needed to drop the NA rows before the .astype(int) call), and a bug in our fuzzy matcher where ‘Cal’ was matching ‘California Institute of Technology’ instead of UC Berkeley.


Learning new stuff: Neither of us had used difflib before, so we asked Claude to explain SequenceMatcher and get_close_matches and how the cutoff parameter actually affects results. We also asked it to walk us through how json.load / json.dump work, since the leaderboard was the first time either of us had persisted data to a file across runs of a Python program. We hadn't covered that in class yet at the point we wrote it.


Implementing code: For some of the trickier bits we'd describe what we wanted in plain English and Claude would draft something we could then read, adjust, and integrate. The hot/cold hint logic in hints.py started this way. We knew we wanted distance-based “burning hot / warm / cool / ice cold” feedback on a few key stats, but we weren't sure how to handle enrollment (which ranges from ~1k to ~50k and needed a log scale) vs. acceptance rate (which is just 0-1). Claude suggested the log-scale approach and the threshold structure we ended up using. 


Every file in the repo we have read and tweaked, and documented so we actually understood it.

Work split
The work was split 50/50 between Jai and Hpone. Roughly:
Module
Jai
Hpone
data_cleaner.py
Wrote the script
Tested output
question.py
Easy/medium difficulty logic
Hard difficulty + clue formatting
game.py
Input handling, fuzzy matching
Round flow, answer reveal
scoring.py
update_score, get_streak
difficulty_ramp, score display
hints.py
Reveal-a-stat logic
Hot/cold feedback system
leaderboard.py
Together
Together
main.py + integration
Together
Together
Polish + README
Together
Together

We were pair-programming the leaderboard, the final integration into main.py, and the polish/README day, and a lot of the different parts so we just pushed and committed when we were using one person’s computer. We also reviewed each other's commits on every module so we both understood the whole code base. 
Time spent on each section
Rough estimates of total hours (both of us combined):
Dataset exploration + picking columns: ~2 hours
Data_cleaner.py: ~3 hours
question.py (school picking + clue card): ~4 hours
game.py (main loop + fuzzy matching): ~6 hours
scoring.py (points, streaks, difficulty): ~3 hours
hints.py (reveal + hot/cold): ~4 hours
leaderboard.py (JSON save/load): ~3 hours
Integration in main.py + first full playthrough: ~2 hours
General bug fixing: ~4 hours
README: ~2 hours
game.py took the longest because the fuzzy matcher went through several iterations. Our first version matched way too aggressively (‘MIT’ matched “Michigan Tech“), so we ended up writing the layered approach in fuzzy_match(). Alias table first, then exact, then unique substring, then token-level fuzzy match, then whole-name fuzzy match as a fallback.
Challenges
A few things tripped us up:
The raw scorecard is huge and messy. It has ~3,000 institutions, most of which are obscure community colleges or for-profits that nobody would recognize. Half the columns we wanted had a lot of missing values or PrivacySuppressed entries. Figuring out the right filters (bachelor's-predominant + big OR selective) took longer than we expected, and we had to drop our original requirement that schools have an SAT_AVG because a ton of well-known schools have stopped reporting SAT averages post-pandemic or requiring SATs at all. The clue card just leaves the SAT line out for those schools now.


Our first attempt at fuzzy matching used difflib.get_close_matches() against the full school names, which gave really bad results. Short guesses like “Cal“ or “Penn“ didn't match anything, and long guesses with typos sometimes matched the wrong school entirely. We ended up needing to break school names into tokens, do per-token fuzzy matching, and add an alias table for common nicknames (UCLA, MIT, Caltech, etc.) that no fuzzy matcher would ever get on its own.


Tuning the difficulty + scoring was a process. We rebalanced it so hints can never turn a correct answer into negative points, and so skipping a round only costs you points if you used hints during it.


Picking what counts as ‘burning hot’ vs. ‘warm’ for enrollment was tricky because schools span two orders of magnitude in size. A 5,000-student difference is huge between two small liberal arts colleges but meaningless between two big state schools. Using log10 on enrollment solved this.


Not repeating schools within a game was difficult. We have a seen_schools set that gets passed into pick_school, but the first version was a module-level global that wasn't getting reset between games. If you played twice in a row, the second game would skip every school from the first. We caught it because Hpone played 3 games in a row during testing and the third game ran out of schools.


Files
data_cleaner.py :one-time script that builds cleaned_schools.csv
question.py :school selection and clue formatting
scoring.py :points, streaks, difficulty
hints.py :reveal-a-stat and hot/cold logic
leaderboard.py :top-5 scores, saved as JSON
game.py :main loop and fuzzy matching
main.py :entry point
data/cleaned_schools.csv :the actual data the game uses
leaderboard.json :created on first game completion
Libraries used
pandas :reading and cleaning the CSV
difflib :fuzzy matching guesses
json :leaderboard persistence
random :picking a school each round
re, math, datetime, os :standard library bits
