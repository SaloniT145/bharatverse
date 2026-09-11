"""
engine.py
----------
This is the REUSABLE GAME ENGINE for BharatVerse.

BEGINNER NOTE:
Instead of writing separate code for "Indus Valley Level 3" vs
"Ancient Kingdoms Level 2", this engine reads level/choice DATA from the
database and applies the same logic every time:

    load level -> show choices -> apply chosen effects -> update stats
    -> award XP/treasure/achievement -> unlock next level

This means adding a brand new realm later mostly means adding new DATA
(levels, choices, historical records) rather than new code.
"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import models


def load_level_screen(user_id, level_id):
    """Return everything the game screen template needs for one level."""
    level = models.get_level_by_id(level_id)
    if not level:
        return None

    choices = models.get_choices_for_level(level_id)
    progress = models.get_progress_for_level(user_id, level_id)
    stats = models.get_player_stats(user_id)

    return {
        "level": level,
        "choices": choices,
        "progress": progress,
        "stats": stats,
        "civilization_score": models.civilization_score(stats),
    }


def submit_choice(user_id, level_id, choice_id):
    """
    The heart of the decision/consequence system.

    Steps:
    1. Look up the chosen choice's effects (stored as JSON in the DB).
    2. Apply those effects to the player's stats, and add XP.
    3. Mark the level as completed for this player.
    4. Award any treasure/achievement tied to this level.
    5. Unlock the next level in this realm.
    6. Check whether the whole realm is now completed (unlocks Map/Timeline).

    Returns a result dictionary used by the result screen.
    """
    level = models.get_level_by_id(level_id)
    choice = models.get_choice_by_id(choice_id)

    if not level or not choice or choice["level_id"] != level_id:
        return {"error": "Invalid level or choice."}

    progress = models.get_progress_for_level(user_id, level_id)
    if progress and progress["status"] == "locked":
        return {"error": "This level is locked."}

    effects = json.loads(choice["effects_json"])
    xp_reward = level["xp_reward"]

    new_stats, new_xp = models.update_player_stats(user_id, effects, xp_reward)

    models.complete_level(user_id, level_id, choice_id)

    treasure = models.award_treasure(user_id, level["treasure_id"]) if level["treasure_id"] else None
    achievement = models.award_achievement(user_id, level["achievement_id"]) if level["achievement_id"] else None

    next_level = models.unlock_next_level(user_id, level["realm_id"], level["level_number"])

    realm_completed = models.is_realm_completed(user_id, level["realm_id"])

    stats_row = models.get_player_stats(user_id)

    return {
        "level": level,
        "choice": choice,
        "effects": effects,
        "xp_reward": xp_reward,
        "new_xp_total": new_xp,
        "stats": stats_row,
        "civilization_score": models.civilization_score(stats_row),
        "treasure": treasure,
        "achievement": achievement,
        "next_level": next_level,
        "realm_completed": realm_completed,
    }


def get_realm_journey(user_id, realm_key):
    """Return the realm plus every level with the player's progress status,
    used to render the level-selection 'journey path' page."""
    realm = models.get_realm_by_key(realm_key)
    if not realm:
        return None

    models.ensure_progress_initialized(user_id, realm["id"])

    levels = models.get_levels_for_realm(realm["id"])
    progress_rows = {p["level_id"]: p for p in models.get_progress_for_realm(user_id, realm["id"])}

    journey = []
    for level in levels:
        progress = progress_rows.get(level["id"])
        journey.append({
            "level": level,
            "status": progress["status"] if progress else "locked",
        })

    return {"realm": realm, "journey": journey}
