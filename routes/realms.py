from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import models
from game_engine import engine
from routes.utils import login_required

realms_bp = Blueprint("realms", __name__)


@realms_bp.route("/realms")
@login_required
def realm_selection():
    realms = models.get_all_realms()
    user_id = session["user_id"]

    realm_progress = {}
    for realm in realms:
        levels = models.get_levels_for_realm(realm["id"])
        if realm["status"] == "active" and levels:
            models.ensure_progress_initialized(user_id, realm["id"])
            progress_rows = models.get_progress_for_realm(user_id, realm["id"])
            done = len([p for p in progress_rows if p["status"] == "completed"])
            realm_progress[realm["id"]] = round((done / len(levels)) * 100)
        else:
            realm_progress[realm["id"]] = 0

    return render_template("realms.html", realms=realms, realm_progress=realm_progress)


@realms_bp.route("/time-machine")
@login_required
def time_machine():
    # Only the Indus Valley realm is a valid travel destination in the MVP
    realm = models.get_realm_by_key("indus_valley")
    return render_template("time_machine.html", realm=realm)


@realms_bp.route("/realm/<realm_key>/levels")
@login_required
def level_selection(realm_key):
    user_id = session["user_id"]
    realm = models.get_realm_by_key(realm_key)

    if not realm:
        flash("That realm does not exist.", "error")
        return redirect(url_for("realms.realm_selection"))

    if realm["status"] != "active":
        flash("This realm is coming soon! Only Indus Valley is playable right now.", "error")
        return redirect(url_for("realms.realm_selection"))

    data = engine.get_realm_journey(user_id, realm_key)
    realm_completed = models.is_realm_completed(user_id, realm["id"])

    return render_template("levels.html", realm=data["realm"], journey=data["journey"],
                            realm_completed=realm_completed)
