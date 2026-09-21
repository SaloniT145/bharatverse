"""
auth.py
--------
Handles Register, Login, Logout.

BEGINNER NOTE:
A "Blueprint" is Flask's way of grouping related routes (URLs) into
their own file, instead of putting everything in one giant app.py.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import models

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # ---- basic input validation ----
        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("register.html")

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        if models.get_user_by_username(username):
            flash("That username is already taken.", "error")
            return render_template("register.html")

        if models.get_user_by_email(email):
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        # Never store plain-text passwords. generate_password_hash() turns
        # the password into a secure, irreversible hash.
        password_hash = generate_password_hash(password)
        user_id = models.create_user(username, email, password_hash)

        session["user_id"] = user_id
        session["username"] = username
        flash("Welcome to BharatVerse! Your journey begins now.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if request.form.get("demo_login") == "student":
            username = "Student Demo"
            password = "student123"

        user = models.get_user_by_username(username)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash(f"Welcome back, {user['username']}!", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))
