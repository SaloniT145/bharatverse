from flask import Blueprint, render_template, session, flash, redirect, url_for
from models import models
from routes.utils import login_required

map_bp = Blueprint("map", __name__)


@map_bp.route("/map/<realm_key>")
@login_required
def civilization_map(realm_key):
    user_id = session["user_id"]
    realm = models.get_realm_by_key(realm_key)

    if not realm:
        flash("That realm does not exist.", "error")
        return redirect(url_for("realms.realm_selection"))

    # The map unlocks once the realm's levels are all completed.
    if realm["status"] == "active" and not models.is_realm_completed(user_id, realm["id"]):
        flash("Complete every level of this realm to unlock the Civilization Map!", "error")
        return redirect(url_for("realms.level_selection", realm_key=realm_key))

    sites = models.get_sites_for_realm(realm["id"])
    return render_template("map.html", realm=realm, sites=sites)
