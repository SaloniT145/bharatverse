from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models import models
from game_engine import engine, rewards, scoring
from routes.utils import login_required

game_bp = Blueprint("game", __name__)


@game_bp.route("/game/level/<int:level_id>")
@login_required
def play_level(level_id):
    user_id = session["user_id"]
    screen = engine.load_level_screen(user_id, level_id)

    if not screen:
        flash("That level could not be found.", "error")
        return redirect(url_for("realms.realm_selection"))

    if screen["progress"] and screen["progress"]["status"] == "locked":
        flash("Complete the previous level first to unlock this one.", "error")
        return redirect(url_for("realms.level_selection", realm_key="indus_valley"))

    return render_template(
        "game.html",
        level=screen["level"],
        choices=screen["choices"],
        stats=screen["stats"],
        civilization_score=screen["civilization_score"],
        already_completed=(screen["progress"] and screen["progress"]["status"] == "completed"),
    )


@game_bp.route("/game/level/<int:level_id>/submit", methods=["POST"])
@login_required
def submit_choice(level_id):
    user_id = session["user_id"]
    choice_id = request.form.get("choice_id", type=int)

    if not choice_id:
        flash("Please choose an option before continuing.", "error")
        return redirect(url_for("game.play_level", level_id=level_id))

    result = engine.submit_choice(user_id, level_id, choice_id)

    if "error" in result:
        flash(result["error"], "error")
        return redirect(url_for("realms.realm_selection"))

    treasure_msg = rewards.treasure_message(result["treasure"])
    achievement_msg = rewards.achievement_message(result["achievement"])
    rank = scoring.get_rank(result["new_xp_total"])
    score_label = scoring.score_label(result["civilization_score"])

    return render_template(
        "result.html",
        level=result["level"],
        choice=result["choice"],
        effects=result["effects"],
        xp_reward=result["xp_reward"],
        new_xp_total=result["new_xp_total"],
        stats=result["stats"],
        civilization_score=result["civilization_score"],
        score_label=score_label,
        rank=rank,
        treasure_msg=treasure_msg,
        achievement_msg=achievement_msg,
        next_level=result["next_level"],
        realm_completed=result["realm_completed"],
    )


@game_bp.route("/game/level/<int:level_id>/historical-record")
@login_required
def historical_record(level_id):
    user_id = session["user_id"]
    level = models.get_level_by_id(level_id)
    progress = models.get_progress_for_level(user_id, level_id)

    if not level or not progress or progress["status"] != "completed":
        flash("Complete this level first to view its Historical Record.", "error")
        return redirect(url_for("game.play_level", level_id=level_id))

    chosen_choice = models.get_choice_by_id(progress["chosen_choice_id"]) if progress["chosen_choice_id"] else None
    next_level = None
    if level["level_number"]:
        conn_levels = models.get_levels_for_realm(level["realm_id"])
        for lvl in conn_levels:
            if lvl["level_number"] == level["level_number"] + 1:
                next_level = lvl
                break

    return render_template(
        "historical_record.html",
        level=level,
        chosen_choice=chosen_choice,
        next_level=next_level,
    )
