from flask import Blueprint, render_template, session
from models import models
from game_engine import scoring
from routes.utils import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user = models.get_user_by_id(user_id)
    stats = models.get_player_stats(user_id)
    realms = models.get_all_realms()
    treasures = models.get_player_treasures(user_id)
    achievements = models.get_player_achievements(user_id)

    score = models.civilization_score(stats)
    rank = scoring.get_rank(stats["knowledge_xp"] if stats else 0)

    # Work out overall progress across all realms/levels for a progress bar
    total_levels = 0
    completed_levels = 0
    realm_progress = {}
    for realm in realms:
        levels = models.get_levels_for_realm(realm["id"])
        if not levels:
            realm_progress[realm["id"]] = 0
            continue
        models.ensure_progress_initialized(user_id, realm["id"]) if realm["status"] == "active" else None
        progress_rows = models.get_progress_for_realm(user_id, realm["id"])
        done = len([p for p in progress_rows if p["status"] == "completed"])
        total_levels += len(levels)
        completed_levels += done
        realm_progress[realm["id"]] = round((done / len(levels)) * 100) if levels else 0

    overall_progress = round((completed_levels / total_levels) * 100) if total_levels else 0

    return render_template(
        "dashboard.html",
        user=user,
        stats=stats,
        score=score,
        rank=rank,
        realms=realms,
        treasures=treasures,
        achievements=achievements,
        overall_progress=overall_progress,
        realm_progress=realm_progress,
    )
