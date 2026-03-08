import os
import json
import functools
from datetime import datetime, date, timedelta
from collections import Counter

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, abort
)
from config import Config
from models import db, User, EmotionLog, AIAnalysisResult, MoodGoal, JournalEntry, Notification

# ─── App Factory ─────────────────────────────────────────────────────────────

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ─── Auth Decorator ──────────────────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    return User.query.get(session['user_id']) if 'user_id' in session else None

# ─── AI Engine ───────────────────────────────────────────────────────────────

MOOD_SCORES = {
    'ecstatic': 10, 'happy': 8, 'content': 7, 'grateful': 8,
    'calm': 6, 'tired': 4, 'bored': 3, 'anxious': 2,
    'sad': 2, 'angry': 2, 'overwhelmed': 1, 'burntout': 1,
    'depressed': 1, 'hopeless': 1
}

NEGATIVE_MOODS = {'sad', 'anxious', 'overwhelmed', 'burntout', 'depressed', 'angry', 'hopeless'}
POSITIVE_MOODS = {'ecstatic', 'happy', 'content', 'grateful', 'calm'}

RECOMMENDATIONS_MAP = {
    'low': [
        "Keep logging your emotions daily to build self-awareness.",
        "Try a 5-minute breathing exercise in the Calm Zone.",
        "Read one page of a book before sleeping tonight.",
        "Reach out to a friend and share something positive."
    ],
    'medium': [
        "Consider a short walk outside — even 10 minutes helps.",
        "Practice the 4-7-8 breathing technique to ease anxiety.",
        "Write in your journal about what you're feeling right now.",
        "Reduce screen time tonight and sleep at a regular hour.",
        "Talk to someone you trust about your current stress."
    ],
    'high': [
        "Please consider speaking to a mental health professional.",
        "Use our Peer Support Networks — you are not alone.",
        "Activate our 24/7 Crisis Helpline if you feel unsafe.",
        "Limit isolation — make contact with at least one trusted person today.",
        "Perform a full body scan meditation using our Calm Zone."
    ],
    'critical': [
        "⚠️ We strongly recommend contacting our Crisis Intervention Team NOW.",
        "Call iCall (India): 9152987821 — trained counselors available 24/7.",
        "Please share your location with a trusted person immediately.",
        "Do NOT be alone. If you are in immediate danger, call emergency services."
    ]
}

INSIGHTS_MAP = {
    'low': "Your emotional state looks balanced. Keep up the consistent self-care habits.",
    'medium': "We're detecting moderate stress patterns. Small, intentional actions now can prevent larger issues later.",
    'high': "Our AI has detected significant emotional drift. Your burnout risk is elevated. Please act on the recommendations below.",
    'critical': "CRITICAL ALERT: Our system detected severe emotional distress signals. Immediate professional intervention is recommended."
}

def run_ai_analysis(user_id):
    """
    Core AI-driven emotional drift and risk detection engine.
    Analyzes the last 7 emotion logs to compute risk, drift, and personalized insights.
    """
    recent_logs = (
        EmotionLog.query
        .filter_by(user_id=user_id)
        .order_by(EmotionLog.created_at.desc())
        .limit(7)
        .all()
    )

    if not recent_logs:
        return None

    scores = [log.mood_score for log in recent_logs]
    mood_tags = [log.mood_tag.lower() for log in recent_logs]
    weekly_avg = round(sum(scores) / len(scores), 2)

    # Dominant emotion
    dominant_emotion = Counter(mood_tags).most_common(1)[0][0]

    # Emotional Drift Score: how much scores are declining
    drift_score = 0.0
    if len(scores) >= 2:
        deltas = [scores[i-1] - scores[i] for i in range(1, len(scores))]
        avg_delta = sum(deltas) / len(deltas)
        drift_score = round(min(max(avg_delta / 10.0, 0.0), 1.0), 3)

    # Trend: last 3 vs previous
    if len(scores) >= 4:
        recent_3_avg = sum(scores[:3]) / 3
        older_avg = sum(scores[3:]) / len(scores[3:])
        mood_trend = 'improving' if recent_3_avg > older_avg + 0.5 else (
            'declining' if recent_3_avg < older_avg - 0.5 else 'stable'
        )
    else:
        mood_trend = 'stable'

    # Negative mood frequency
    neg_count = sum(1 for t in mood_tags if t in NEGATIVE_MOODS)
    neg_ratio = neg_count / len(mood_tags)

    # Burnout probability
    burnout_prob = round(min((neg_ratio * 0.6) + (drift_score * 0.4), 1.0), 3)

    # Risk classification
    if weekly_avg <= 2 or burnout_prob >= 0.85:
        risk_level = 'critical'
        care_pathway = 3
    elif weekly_avg <= 4 or burnout_prob >= 0.6:
        risk_level = 'high'
        care_pathway = 3
    elif weekly_avg <= 6 or burnout_prob >= 0.35:
        risk_level = 'medium'
        care_pathway = 2
    else:
        risk_level = 'low'
        care_pathway = 1

    recommendations = json.dumps(RECOMMENDATIONS_MAP[risk_level])
    insights = INSIGHTS_MAP[risk_level]

    # Compose sleep data
    sleep_data = [log.sleep_hours for log in recent_logs if log.sleep_hours is not None]
    avg_sleep = round(sum(sleep_data)/len(sleep_data), 1) if sleep_data else None

    return AIAnalysisResult(
        user_id=user_id,
        risk_level=risk_level,
        emotional_drift_score=drift_score,
        burnout_probability=burnout_prob,
        dominant_emotion=dominant_emotion,
        mood_trend=mood_trend,
        insights=insights,
        recommendations=recommendations,
        weekly_avg_score=weekly_avg,
        care_pathway=care_pathway
    )


def update_user_streak(user):
    """Update check-in streak for the user."""
    today = date.today()
    if user.last_checkin_date == today:
        return  # Already checked in today
    elif user.last_checkin_date == today - timedelta(days=1):
        user.streak_days += 1
    else:
        user.streak_days = 1  # Streak broken
    user.last_checkin_date = today
    user.total_checkins = (user.total_checkins or 0) + 1


def create_notification(user_id, title, message, notif_type='info'):
    notif = Notification(user_id=user_id, title=title, message=message, notif_type=notif_type)
    db.session.add(notif)


# ─── Context Processor ───────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    user = get_current_user()
    unread_count = 0
    if user:
        unread_count = Notification.query.filter_by(user_id=user.id, is_read=False).count()
    return dict(current_user=user, unread_notif_count=unread_count)


# ─── Public Routes ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        occupation = request.form.get('occupation', '').strip()

        if not all([username, email, password]):
            flash('All required fields must be filled.', 'error')
            return redirect(url_for('signup'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists.', 'error')
            return redirect(url_for('signup'))

        user = User(username=username, email=email, full_name=full_name, occupation=occupation)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Welcome notification
        create_notification(
            user.id,
            'Welcome to Feelio! 🎉',
            f'Hi {username}, start your wellness journey with your first emotion check-in.',
            'success'
        )
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.is_active and user.check_password(password):
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}! 👋', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('index'))


# ─── Protected Page Routes ───────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    recent_logs = (
        EmotionLog.query
        .filter_by(user_id=user.id)
        .order_by(EmotionLog.created_at.desc())
        .limit(5)
        .all()
    )
    latest_analysis = (
        AIAnalysisResult.query
        .filter_by(user_id=user.id)
        .order_by(AIAnalysisResult.created_at.desc())
        .first()
    )
    active_goals = (
        MoodGoal.query
        .filter_by(user_id=user.id, is_completed=False)
        .order_by(MoodGoal.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template(
        'dashboard.html',
        logs=recent_logs,
        analysis=latest_analysis,
        goals=active_goals
    )


@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    user = get_current_user()
    if request.method == 'POST':
        emoji = request.form.get('emoji')
        mood_tag = request.form.get('mood_tag', '').lower()
        mood_score = int(request.form.get('mood_score', MOOD_SCORES.get(mood_tag, 5)))
        energy_level = request.form.get('energy_level', 'medium')
        sleep_hours = request.form.get('sleep_hours')
        journal = request.form.get('journal', '').strip()
        triggers = ','.join(request.form.getlist('triggers'))
        activities = ','.join(request.form.getlist('activities'))

        sleep_hours = float(sleep_hours) if sleep_hours else None

        log = EmotionLog(
            user_id=user.id,
            emoji=emoji,
            mood_tag=mood_tag,
            mood_score=mood_score,
            energy_level=energy_level,
            sleep_hours=sleep_hours,
            journal=journal,
            triggers=triggers or None,
            activities=activities or None
        )
        db.session.add(log)

        # Update streak
        update_user_streak(user)

        # Run AI analysis
        analysis = run_ai_analysis(user.id)
        if analysis:
            db.session.add(analysis)

            # Trigger notifications based on risk
            if analysis.risk_level in ('high', 'critical'):
                create_notification(
                    user.id,
                    '⚠️ Emotional Risk Detected',
                    analysis.insights,
                    'warning' if analysis.risk_level == 'high' else 'danger'
                )
            elif analysis.risk_level == 'low' and user.streak_days and user.streak_days % 7 == 0:
                create_notification(
                    user.id,
                    f'🔥 {user.streak_days}-Day Streak!',
                    f'Amazing! You have checked in for {user.streak_days} consecutive days. Keep it up!',
                    'success'
                )

        db.session.commit()
        flash('Check-in saved! Your AI insights have been updated.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('checkin.html')


@app.route('/analytics')
@login_required
def analytics():
    user = get_current_user()
    return render_template('analytics.html', user=user)


@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled').strip()
        content = request.form.get('content', '').strip()
        mood_tag = request.form.get('mood_tag', '').strip()
        if not content:
            flash('Journal content cannot be empty.', 'error')
            return redirect(url_for('journal'))
        word_count = len(content.split())
        # Simple keyword-based sentiment
        positive_words = {'happy', 'great', 'wonderful', 'amazing', 'grateful', 'love', 'joy', 'excited', 'hope'}
        negative_words = {'sad', 'depressed', 'anxious', 'hate', 'terrible', 'awful', 'hopeless', 'lonely', 'fear'}
        words_lower = set(content.lower().split())
        pos_count = len(words_lower & positive_words)
        neg_count = len(words_lower & negative_words)
        sentiment = round((pos_count - neg_count) / max(word_count, 1), 4)

        entry = JournalEntry(
            user_id=user.id, title=title, content=content,
            mood_tag=mood_tag, sentiment_score=sentiment, word_count=word_count
        )
        db.session.add(entry)
        db.session.commit()
        flash('Journal entry saved successfully.', 'success')
        return redirect(url_for('journal'))

    entries = (
        JournalEntry.query
        .filter_by(user_id=user.id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )
    return render_template('journal.html', entries=entries)


@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    user = get_current_user()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        goal_type = request.form.get('goal_type', 'mindfulness')
        target_days = int(request.form.get('target_days', 7))
        if not title:
            flash('Goal title is required.', 'error')
            return redirect(url_for('goals'))
        goal = MoodGoal(
            user_id=user.id, title=title, description=description,
            goal_type=goal_type, target_days=target_days
        )
        db.session.add(goal)
        db.session.commit()
        flash('New wellness goal created!', 'success')
        return redirect(url_for('goals'))

    all_goals = MoodGoal.query.filter_by(user_id=user.id).order_by(MoodGoal.created_at.desc()).all()
    return render_template('goals.html', goals=all_goals)


@app.route('/calm')
@login_required
def calm():
    return render_template('calm.html')


@app.route('/support')
@login_required
def support():
    user = get_current_user()
    latest_analysis = (
        AIAnalysisResult.query
        .filter_by(user_id=user.id)
        .order_by(AIAnalysisResult.created_at.desc())
        .first()
    )
    risk_level = latest_analysis.risk_level if latest_analysis else 'low'
    care_pathway = latest_analysis.care_pathway if latest_analysis else 1
    recommendations = []
    if latest_analysis:
        try:
            recommendations = json.loads(latest_analysis.recommendations or '[]')
        except Exception:
            recommendations = []
    return render_template('support.html', risk_level=risk_level, care_pathway=care_pathway, recommendations=recommendations)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_current_user()
    if request.method == 'POST':
        user.full_name = request.form.get('full_name', user.full_name)
        user.occupation = request.form.get('occupation', user.occupation)
        user.age = request.form.get('age', user.age) or None
        user.gender = request.form.get('gender', user.gender)
        user.language = request.form.get('language', user.language)
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)


@app.route('/notifications')
@login_required
def notifications():
    user = get_current_user()
    notifs = (
        Notification.query
        .filter_by(user_id=user.id)
        .order_by(Notification.created_at.desc())
        .limit(30)
        .all()
    )
    # Mark all as read
    Notification.query.filter_by(user_id=user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('notifications.html', notifications=notifs)


# ─── REST API Endpoints ──────────────────────────────────────────────────────

@app.route('/api/analytics/mood-trend')
@login_required
def api_mood_trend():
    """Returns the last 30 days of mood scores for charts."""
    user_id = session['user_id']
    days = int(request.args.get('days', 30))
    since = datetime.utcnow() - timedelta(days=days)
    logs = (
        EmotionLog.query
        .filter(EmotionLog.user_id == user_id, EmotionLog.created_at >= since)
        .order_by(EmotionLog.created_at.asc())
        .all()
    )
    data = [{'date': l.created_at.strftime('%Y-%m-%d'), 'score': l.mood_score, 'mood': l.mood_tag} for l in logs]
    return jsonify({'success': True, 'data': data})


@app.route('/api/analytics/mood-distribution')
@login_required
def api_mood_distribution():
    """Pie chart: breakdown of mood tags."""
    user_id = session['user_id']
    logs = EmotionLog.query.filter_by(user_id=user_id).all()
    counts = Counter(l.mood_tag for l in logs)
    return jsonify({'success': True, 'data': [{'mood': k, 'count': v} for k, v in counts.items()]})


@app.route('/api/analytics/energy-sleep')
@login_required
def api_energy_sleep():
    """Scatter: energy level vs sleep hours."""
    user_id = session['user_id']
    logs = (
        EmotionLog.query
        .filter(EmotionLog.user_id == user_id, EmotionLog.sleep_hours.isnot(None))
        .order_by(EmotionLog.created_at.desc())
        .limit(30)
        .all()
    )
    data = [{'sleep': l.sleep_hours, 'score': l.mood_score, 'energy': l.energy_level} for l in logs]
    return jsonify({'success': True, 'data': data})


@app.route('/api/analytics/weekly-summary')
@login_required
def api_weekly_summary():
    """Weekly summary stats for dashboard stat cards."""
    user_id = session['user_id']
    week_ago = datetime.utcnow() - timedelta(days=7)
    logs = EmotionLog.query.filter(
        EmotionLog.user_id == user_id,
        EmotionLog.created_at >= week_ago
    ).all()

    scores = [l.mood_score for l in logs]
    avg_score = round(sum(scores)/len(scores), 1) if scores else 0
    best_day = max(logs, key=lambda l: l.mood_score) if logs else None
    worst_day = min(logs, key=lambda l: l.mood_score) if logs else None

    return jsonify({
        'success': True,
        'total_checkins': len(logs),
        'avg_score': avg_score,
        'best_day': best_day.created_at.strftime('%A') if best_day else '—',
        'worst_day': worst_day.created_at.strftime('%A') if worst_day else '—',
    })


@app.route('/api/goals/<int:goal_id>/increment', methods=['POST'])
@login_required
def api_goal_increment(goal_id):
    """Mark one day completed for a goal."""
    user_id = session['user_id']
    goal = MoodGoal.query.filter_by(id=goal_id, user_id=user_id).first_or_404()
    if not goal.is_completed:
        goal.completed_days = min(goal.completed_days + 1, goal.target_days)
        if goal.completed_days >= goal.target_days:
            goal.is_completed = True
            create_notification(user_id, '🏆 Goal Achieved!', f'You completed your goal: "{goal.title}"!', 'success')
        db.session.commit()
    return jsonify({'success': True, 'goal': goal.to_dict()})


@app.route('/api/notifications/unread-count')
@login_required
def api_unread_notif_count():
    count = Notification.query.filter_by(user_id=session['user_id'], is_read=False).count()
    return jsonify({'count': count})


# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000, host='0.0.0.0')
