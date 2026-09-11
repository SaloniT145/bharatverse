"""
scoring.py
-----------
Small helper functions related to XP levels and score labels.
Kept separate from engine.py so scoring rules can be tuned independently.
"""

# XP required to reach each "Rank" - purely cosmetic progression label
RANKS = [
    (0, "Newcomer"),
    (300, "Apprentice Planner"),
    (800, "City Planner"),
    (1500, "Civilization Builder"),
    (2500, "Master Historian"),
    (4000, "Legend of Bharat"),
]


def get_rank(xp):
    current = RANKS[0][1]
    for threshold, name in RANKS:
        if xp >= threshold:
            current = name
        else:
            break
    return current


def score_label(score):
    if score >= 85:
        return "Thriving Civilization"
    if score >= 65:
        return "Growing Settlement"
    if score >= 40:
        return "Developing Settlement"
    return "Struggling Settlement"
