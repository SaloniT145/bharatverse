"""
utils.py
---------
Small shared helpers used across multiple route files.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """A decorator that blocks access to a route unless the user is
    logged in. Put @login_required directly above any route function
    that should only be visible to logged-in students."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue your journey.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
