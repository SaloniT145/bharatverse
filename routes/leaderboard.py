from flask import Blueprint, render_template, session
from models import models
from game_engine import scoring
from routes.utils import login_required

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/leaderboard")
@login_required
def hall_of_legends():
    rows = models.get_leaderboard(limit=20)
    leaderboard = []
    for row in rows:
        stats_like = row  # has water, food, settlement, infrastructure, wellbeing
        score = round((row["water"] + row["food"] + row["settlement"] +
                       row["infrastructure"] + row["wellbeing"]) / 5)
        leaderboard.append({
            "username": row["username"],
            "xp": row["knowledge_xp"],
            "score": score,
            "achievement_count": row["achievement_count"],
            "is_demo": "(Demo)" in row["username"],
        })
    return render_template("leaderboard.html", leaderboard=leaderboard)


@leaderboard_bp.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    user = models.get_user_by_id(user_id)
    stats = models.get_player_stats(user_id)
    treasures = models.get_player_treasures(user_id)
    achievements = models.get_player_achievements(user_id)
    score = models.civilization_score(stats)
    rank = scoring.get_rank(stats["knowledge_xp"] if stats else 0)

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        treasures=treasures,
        achievements=achievements,
        score=score,
        rank=rank,
    )
