from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    occupation = db.Column(db.String(100))
    language = db.Column(db.String(20), default='en')
    privacy_agreed = db.Column(db.Boolean, default=True)
    avatar_color = db.Column(db.String(20), default='#7b2cbf')
    streak_days = db.Column(db.Integer, default=0)
    last_checkin_date = db.Column(db.Date)
    total_checkins = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emotion_logs = db.relationship('EmotionLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    ai_analyses = db.relationship('AIAnalysisResult', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    mood_goals = db.relationship('MoodGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def initials(self):
        if self.full_name:
            parts = self.full_name.strip().split()
            return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][0].upper()
        return self.username[0].upper()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'occupation': self.occupation,
            'streak_days': self.streak_days,
            'total_checkins': self.total_checkins,
            'created_at': self.created_at.isoformat()
        }


class EmotionLog(db.Model):
    __tablename__ = 'emotion_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    emoji = db.Column(db.String(20), nullable=False)
    mood_tag = db.Column(db.String(50), nullable=False)
    mood_score = db.Column(db.Integer, default=5)  # 1–10 scale
    energy_level = db.Column(db.String(20), default='medium')  # low, medium, high
    sleep_hours = db.Column(db.Float)
    journal = db.Column(db.Text)
    triggers = db.Column(db.String(255))  # comma-separated tags e.g. "work,family,health"
    activities = db.Column(db.String(255))  # comma-separated e.g. "exercise,reading"
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'emoji': self.emoji,
            'mood_tag': self.mood_tag,
            'mood_score': self.mood_score,
            'energy_level': self.energy_level,
            'sleep_hours': self.sleep_hours,
            'journal': self.journal,
            'triggers': self.triggers.split(',') if self.triggers else [],
            'activities': self.activities.split(',') if self.activities else [],
            'created_at': self.created_at.isoformat()
        }


class AIAnalysisResult(db.Model):
    __tablename__ = 'ai_analysis'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    risk_level = db.Column(db.String(20), default='low')    # low, medium, high, critical
    emotional_drift_score = db.Column(db.Float, default=0.0)  # 0.0–1.0
    burnout_probability = db.Column(db.Float, default=0.0)    # 0.0–1.0
    dominant_emotion = db.Column(db.String(50))
    mood_trend = db.Column(db.String(20), default='stable')   # improving, stable, declining
    insights = db.Column(db.Text)
    recommendations = db.Column(db.Text)   # JSON list stored as text
    weekly_avg_score = db.Column(db.Float, default=5.0)
    care_pathway = db.Column(db.Integer, default=1)  # 1=self-care, 2=peer, 3=crisis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        recs = []
        try:
            recs = json.loads(self.recommendations) if self.recommendations else []
        except Exception:
            recs = [self.recommendations] if self.recommendations else []
        return {
            'id': self.id,
            'risk_level': self.risk_level,
            'emotional_drift_score': self.emotional_drift_score,
            'burnout_probability': self.burnout_probability,
            'dominant_emotion': self.dominant_emotion,
            'mood_trend': self.mood_trend,
            'insights': self.insights,
            'recommendations': recs,
            'weekly_avg_score': self.weekly_avg_score,
            'care_pathway': self.care_pathway,
            'created_at': self.created_at.isoformat()
        }


class MoodGoal(db.Model):
    __tablename__ = 'mood_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    goal_type = db.Column(db.String(50))  # mindfulness, sleep, exercise, social
    target_days = db.Column(db.Integer, default=7)
    completed_days = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)

    def to_dict(self):
        progress = round((self.completed_days / self.target_days) * 100) if self.target_days > 0 else 0
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'goal_type': self.goal_type,
            'target_days': self.target_days,
            'completed_days': self.completed_days,
            'progress': min(progress, 100),
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat()
        }


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    mood_tag = db.Column(db.String(50))
    sentiment_score = db.Column(db.Float, default=0.0)  # -1.0 to 1.0
    word_count = db.Column(db.Integer, default=0)
    is_private = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'mood_tag': self.mood_tag,
            'sentiment_score': self.sentiment_score,
            'word_count': self.word_count,
            'created_at': self.created_at.isoformat()
        }


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notif_type = db.Column(db.String(30), default='info')  # info, warning, success, danger
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'notif_type': self.notif_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
