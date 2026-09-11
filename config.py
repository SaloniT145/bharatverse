"""
config.py
----------
Central place for application settings.

BEGINNER NOTE:
SECRET_KEY is used by Flask to securely sign session cookies (the data
that remembers who is logged in). In a real deployment this should come
from an environment variable, never hard-coded and never committed to
GitHub. We fall back to a default only so the app runs immediately for
local development/hackathon demos.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bharatverse-dev-secret-change-in-production")
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "bharatverse.db")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
