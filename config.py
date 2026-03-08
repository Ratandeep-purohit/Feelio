import os

class Config:
    """Production-grade application configuration."""

    # ─── Database ────────────────────────────────────────────────────────────
    # Format: mysql+pymysql://username:password@host/database_name
    # URL-encode special characters in the password, e.g., @ → %40
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'mysql+pymysql://root:R%40j%40t2004@localhost/emotion_buddy'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }

    # ─── Security ────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'feelio-dev-secret-key-change-in-production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds

    # ─── App Meta ────────────────────────────────────────────────────────────
    APP_NAME = 'Feelio'
    APP_VERSION = '2.0.0'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
