from flask import Blueprint, render_template, session, flash, redirect, url_for
from models import models
from routes.utils import login_required

timeline_bp = Blueprint("timeline", __name__)


@timeline_bp.route("/timeline/<realm_key>")
@login_required
def historical_timeline(realm_key):
    user_id = session["user_id"]
    realm = models.get_realm_by_key(realm_key)

    if not realm:
        flash("That realm does not exist.", "error")
        return redirect(url_for("realms.realm_selection"))

    if realm["status"] == "active" and not models.is_realm_completed(user_id, realm["id"]):
        flash("Complete every level of this realm to unlock the Historical Timeline!", "error")
        return redirect(url_for("realms.level_selection", realm_key=realm_key))

    events = models.get_timeline_for_realm(realm["id"])
    return render_template("timeline.html", realm=realm, events=events)
