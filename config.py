import os
from dotenv import load_dotenv

# Load .env file first (ignored by Git)
load_dotenv()

class Config:
    """Production-grade application configuration.
    All secrets are loaded from environment variables or a .env file.
    NEVER hardcode credentials here — this file IS committed to Git.
    """

    # ─── Database ─────────────────────────────────────────────────────
    # Set DATABASE_URL in your .env file (see .env.example)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,    # Recycle connections before MySQL 5-min timeout
        'pool_pre_ping': True,  # Test connections before use (prevents stale errors)
        'pool_size': 10,
        'max_overflow': 20,
    }

    # ─── Security ──────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

    # ─── App Meta ──────────────────────────────────────────────────────
    APP_NAME = 'Feelio'
    APP_VERSION = '2.0.0'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
