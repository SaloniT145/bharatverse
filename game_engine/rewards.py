"""
rewards.py
-----------
Helper functions for formatting treasure/achievement messages.
The actual awarding of rewards happens in engine.py + models.py;
this file just centralizes how we describe rewards to the player.
"""


def treasure_message(treasure):
    if not treasure:
        return None
    return {
        "title": "TREASURE DISCOVERED!",
        "name": treasure["name"],
        "icon": treasure["icon"],
        "description": treasure["description"],
    }


def achievement_message(achievement):
    if not achievement:
        return None
    return {
        "title": "ACHIEVEMENT UNLOCKED!",
        "name": achievement["name"],
        "icon": achievement["icon"],
        "description": achievement["description"],
    }
