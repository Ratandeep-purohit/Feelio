"""
migration.py — Smart Schema Migration for Feelio v2.0
Safely adds new columns to existing tables without data loss.
Run: python migration.py
"""

from app import app
from models import db
import pymysql

# ── Connection helper ──────────────────────────────────────────────
def get_raw_conn():
    """Get a raw PyMySQL connection from SQLAlchemy engine."""
    engine = db.engine
    raw_conn = engine.raw_connection()
    return raw_conn

def column_exists(cursor, table, column):
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema = DATABASE()
          AND table_name   = %s
          AND column_name  = %s
    """, (table, column))
    return cursor.fetchone()[0] > 0

def table_exists(cursor, table):
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND table_name = %s
    """, (table,))
    return cursor.fetchone()[0] > 0

def safe_alter(cursor, table, column, definition):
    if not column_exists(cursor, table, column):
        print(f"  ✚  Adding column '{column}' to '{table}'...")
        cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")
    else:
        print(f"  ✔  Column '{column}' already exists in '{table}'.")

# ── Run migration ──────────────────────────────────────────────────

def run_migration():
    with app.app_context():
        # Step 1: Create all tables that don't exist yet (new tables).
        print("\n📦 Step 1 — Creating new tables if they don't exist...")
        db.create_all()
        print("   Done.\n")

        # Step 2: ALTER existing tables to add new columns safely.
        print("🔧 Step 2 — Upgrading schema for existing tables...\n")

        conn = get_raw_conn()
        cursor = conn.cursor()

        try:
            # ── users table ────────────────────────────────────────
            print("▶  Table: users")
            safe_alter(cursor, 'users', 'full_name',          "VARCHAR(150) DEFAULT NULL")
            safe_alter(cursor, 'users', 'age',                "INT DEFAULT NULL")
            safe_alter(cursor, 'users', 'gender',             "VARCHAR(20) DEFAULT NULL")
            safe_alter(cursor, 'users', 'occupation',         "VARCHAR(100) DEFAULT NULL")
            safe_alter(cursor, 'users', 'avatar_color',       "VARCHAR(20) DEFAULT '#7b2cbf'")
            safe_alter(cursor, 'users', 'streak_days',        "INT DEFAULT 0")
            safe_alter(cursor, 'users', 'last_checkin_date',  "DATE DEFAULT NULL")
            safe_alter(cursor, 'users', 'total_checkins',     "INT DEFAULT 0")
            safe_alter(cursor, 'users', 'is_active',          "TINYINT(1) DEFAULT 1")
            safe_alter(cursor, 'users', 'updated_at',         "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

            # ── emotion_logs table ─────────────────────────────────
            print("\n▶  Table: emotion_logs")
            safe_alter(cursor, 'emotion_logs', 'mood_score',    "INT DEFAULT 5")
            safe_alter(cursor, 'emotion_logs', 'energy_level',  "VARCHAR(20) DEFAULT 'medium'")
            safe_alter(cursor, 'emotion_logs', 'sleep_hours',   "FLOAT DEFAULT NULL")
            safe_alter(cursor, 'emotion_logs', 'triggers',      "VARCHAR(255) DEFAULT NULL")
            safe_alter(cursor, 'emotion_logs', 'activities',    "VARCHAR(255) DEFAULT NULL")
            safe_alter(cursor, 'emotion_logs', 'is_private',    "TINYINT(1) DEFAULT 1")
            safe_alter(cursor, 'emotion_logs', 'updated_at',    "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

            # ── ai_analysis table ──────────────────────────────────
            print("\n▶  Table: ai_analysis")
            safe_alter(cursor, 'ai_analysis', 'emotional_drift_score', "FLOAT DEFAULT 0.0")
            safe_alter(cursor, 'ai_analysis', 'burnout_probability',   "FLOAT DEFAULT 0.0")
            safe_alter(cursor, 'ai_analysis', 'dominant_emotion',      "VARCHAR(50) DEFAULT NULL")
            safe_alter(cursor, 'ai_analysis', 'mood_trend',            "VARCHAR(20) DEFAULT 'stable'")
            safe_alter(cursor, 'ai_analysis', 'recommendations',       "TEXT DEFAULT NULL")
            safe_alter(cursor, 'ai_analysis', 'weekly_avg_score',      "FLOAT DEFAULT 5.0")
            safe_alter(cursor, 'ai_analysis', 'care_pathway',          "INT DEFAULT 1")

            conn.commit()
            print("\n✅ Schema migration completed successfully!")

        except Exception as e:
            conn.rollback()
            print(f"\n❌ Migration failed: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

        print("\n🚀 Feelio v2.0 is ready! Run: python app.py\n")

if __name__ == '__main__':
    run_migration()
