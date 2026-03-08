<div align="center">

```
███████╗███████╗███████╗██╗     ██╗ ██████╗ 
██╔════╝██╔════╝██╔════╝██║     ██║██╔═══██╗
█████╗  █████╗  █████╗  ██║     ██║██║   ██║
██╔══╝  ██╔══╝  ██╔══╝  ██║     ██║██║   ██║
██║     ███████╗███████╗███████╗██║╚██████╔╝
╚═╝     ╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ 
```

# 🧠 Feelio — AI-Driven Emotional Awareness Platform

**The most advanced open-source mental wellness application built with Python, Flask, and Vanilla Intelligence.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-blueviolet?style=for-the-badge)](https://github.com/Ratandeep-purohit/Feelio/releases)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)](https://github.com/Ratandeep-purohit/Feelio)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Ratandeep--purohit%2FFelio-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratandeep-purohit/Feelio)

<br/>

> **Feelio** is a proactive mental wellness platform that detects emotional drift, calculates burnout probability using a real AI engine, and routes users to the right support pathway — all before crisis strikes.
>
> 🔗 **Repository:** [github.com/Ratandeep-purohit/Feelio](https://github.com/Ratandeep-purohit/Feelio)

<br/>

---

</div>

## 📌 Table of Contents

- [🌟 Why Feelio?](#-why-feelio)
- [🏗️ Architecture Overview](#️-architecture-overview)
- [⚡ Feature Matrix](#-feature-matrix)
- [🧠 The AI Engine — How It Works](#-the-ai-engine--how-it-works)
- [🗄️ Database Schema](#️-database-schema)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [🔌 REST API Reference](#-rest-api-reference)
- [🎨 Design System](#-design-system)
- [🔐 Security Model](#-security-model)
- [🛠️ Configuration](#️-configuration)
- [📈 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Why Feelio?

Mental health crises rarely appear overnight. They build slowly, **one unnoticed emotional shift at a time**. Feelio was built to intercept this drift **before** it becomes a crisis — using data, AI, and empathy.

| Traditional Apps | 🧠 Feelio |
|---|---|
| Reactive — help after crisis | ✅ Proactive — detects risk early |
| One-size-fits-all content | ✅ AI-personalized care pathways |
| Static mood logs | ✅ Drift scoring + burnout probability |
| No clinical insight | ✅ Validated emotional pattern analysis |
| Ugly, clinical UI | ✅ Premium glassmorphism design |
| Basic charts | ✅ Live Chart.js analytics suite |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          FEELIO v2.0 ARCHITECTURE                       │
├──────────────────┬──────────────────────────────────────────────────────┤
│  PRESENTATION    │  HTML5  ·  Vanilla CSS (Glassmorphism)  ·  Vanilla JS│
│  (Frontend)      │  Chart.js 4.4  ·  Font Awesome 6  ·  Google Fonts    │
├──────────────────┼──────────────────────────────────────────────────────┤
│  ROUTING         │  Flask 3.0 Blueprints-ready  ·  @login_required      │
│  (HTTP Layer)    │  Context Processors  ·  Error Handlers (404, 500)    │
├──────────────────┼──────────────────────────────────────────────────────┤
│  BUSINESS LOGIC  │  AI Engine  ·  Streak Tracker  ·  Sentiment Scorer   │
│  (app.py)        │  Notification Manager  ·  Care Pathway Router        │
├──────────────────┼──────────────────────────────────────────────────────┤
│  DATA LAYER      │  Flask-SQLAlchemy ORM  ·  PyMySQL                    │
│  (models.py)     │  6 Relational Tables  ·  Cascaded Relationships      │
├──────────────────┼──────────────────────────────────────────────────────┤
│  DATABASE        │  MySQL 8.0+  ·  Connection Pooling  ·  Pre-ping      │
│  (Persistence)   │  Pool Size: 10  ·  Max Overflow: 20                  │
└──────────────────┴──────────────────────────────────────────────────────┘

  REST API Layer  →  /api/analytics/*  ·  /api/goals/*  ·  /api/notifications/*
```

### Request Lifecycle

```
Browser Request
     │
     ▼
Flask Router ──► @login_required decorator
     │                   │
     │            Not Authenticated ──► redirect /login
     │
     ▼ Authenticated
Context Processor (injects current_user, unread_notif_count)
     │
     ▼
Route Handler (app.py)
     │
     ├──► DB Query (SQLAlchemy ORM) ──► MySQL
     │
     ├──► AI Engine (run_ai_analysis) ────────────────────────────┐
     │         │                                                  │
     │         └──► Emotional Drift Score                         │
     │         └──► Burnout Probability                           │
     │         └──► Risk Classification (low/medium/high/critical)│
     │         └──► Care Pathway Assignment (1,2,3)               │
     │         └──► Personalized Recommendations (JSON)◄──────────┘
     │
     ├──► Notification Manager (auto-alerts on high/critical risk)
     │
     └──► Jinja2 Template Render ──► HTML Response ──► Browser
```

---

## ⚡ Feature Matrix

### 🔑 Core Platform Features

| Feature | Status | Details |
|---|---|---|
| User Registration & Auth | ✅ Production | Salted Werkzeug password hashing |
| Session Management | ✅ Production | Permanent sessions · HttpOnly cookies · SameSite=Lax |
| Emotion Check-In (4-Step) | ✅ Production | Emoji · Score · Energy · Sleep · Triggers · Activities · Journal |
| AI Behavioral Analysis | ✅ Production | Drift scoring · Burnout probability · Risk classification |
| Check-In Streak Tracker | ✅ Production | Daily streaks reset on miss, stored in DB |
| Notification System | ✅ Production | Auto-generated alerts on high/critical risk |
| Goal Tracker | ✅ Production | CRUD + REST API increment endpoint |
| Private Journal | ✅ Production | Keyword-based sentiment scoring · Word count |
| Analytics Dashboard | ✅ Production | 4 different Chart.js charts via REST API |
| Calm Zone | ✅ Production | Box breathing · Mindfulness timer · Sound tiles |
| Care Pathway Routing | ✅ Production | AI routes to Tier 1/2/3 based on risk level |
| User Profile Management | ✅ Production | Full profile edit · Password change |
| REST JSON API | ✅ Production | 6 endpoints for charts + goal updates |
| Error Pages (404/500) | ✅ Production | Custom branded error templates |
| Mobile Responsive | ✅ Production | Hamburger sidebar · Adaptive grid layouts |

### 📊 Analytics & AI Features

| Metric | Algorithm | Range |
|---|---|---|
| **Mood Score** | User-selected (1–10) + auto-fill from mood tag | `1–10` |
| **Burnout Probability** | `0.6 × neg_ratio + 0.4 × drift_score` | `0.0–1.0` |
| **Emotional Drift Score** | Δ(avg consecutive scores) / 10 | `0.0–1.0` |
| **Mood Trend** | 3-day rolling avg vs historical avg (±0.5 threshold) | `improving/stable/declining` |
| **Dominant Emotion** | Most frequent mood tag (Counter) | Tag string |
| **Care Pathway** | Risk classification → Tier assignment | `1/2/3` |
| **Sentiment Score** | Positive/negative keyword ratio over word count | `-1.0 to 1.0` |
| **Weekly Average** | Mean of last 7 mood scores | `0.0–10.0` |

---

## 🧠 The AI Engine — How It Works

Feelio's AI engine is a **rule-based behavioral pattern analysis system** designed to mimic clinical screening heuristics. It runs on every check-in.

```python
# Simplified core logic from app.py → run_ai_analysis()

def run_ai_analysis(user_id):
    # 1. Fetch last 7 logs
    recent_logs = EmotionLog.query.filter_by(user_id=user_id)
                    .order_by(created_at.desc()).limit(7).all()

    # 2. Compute Weekly Average Score
    weekly_avg = mean([log.mood_score for log in recent_logs])

    # 3. Emotional Drift: average rate of score decline
    deltas      = [scores[i-1] - scores[i] for i in range(1, len(scores))]
    drift_score = min(max(mean(deltas) / 10.0, 0.0), 1.0)

    # 4. Negative mood ratio
    neg_ratio   = count(mood in NEGATIVE_MOODS) / total_logs

    # 5. Burnout Probability
    burnout     = (neg_ratio × 0.6) + (drift_score × 0.4)

    # 6. Risk Classification
    if   weekly_avg ≤ 2  or burnout ≥ 0.85  → CRITICAL  (Pathway 3)
    elif weekly_avg ≤ 4  or burnout ≥ 0.60  → HIGH      (Pathway 3)
    elif weekly_avg ≤ 6  or burnout ≥ 0.35  → MEDIUM    (Pathway 2)
    else                                     → LOW       (Pathway 1)
```

### Risk Classification Table

| Risk Level | Weekly Avg | Burnout Prob | Action |
|---|---|---|---|
| 🟢 `low` | > 6.0 | < 0.35 | Self-care suggestions, keep tracking |
| 🟡 `medium` | 4–6 | 0.35–0.60 | Peer support, stress reduction techniques |
| 🔴 `high` | 2–4 | 0.60–0.85 | Professional referral, crisis preparation |
| 🚨 `critical` | ≤ 2 | ≥ 0.85 | IMMEDIATE crisis intervention + helpline |

---

## 🗄️ Database Schema

```
┌──────────────────────────────────────────────────────────────────────┐
│                         FEELIO DATABASE SCHEMA                       │
├─────────────────┐                                                    │
│   users         │◄──────────────────────────────┐                    │
├─────────────────┤                               │                    │
│ id (PK)         │                               │                    │
│ username        │                               │                    │
│ email           │           ┌──────────────────►│                    │
│ password_hash   │           │  emotion_logs      │                   │
│ full_name       │           ├────────────────   │                    │
│ age             │           │ id (PK)            │                   │
│ gender          │           │ user_id (FK)───────┘                   │
│ occupation      │           │ emoji                                  │
│ language        │           │ mood_tag                               │
│ streak_days     │           │ mood_score (1-10)                      │
│ last_checkin    │           │ energy_level                           │
│ total_checkins  │           │ sleep_hours                            │
│ is_active       │           │ journal (TEXT)                         │
│ created_at      │           │ triggers (CSV)                         │
│ updated_at      │           │ activities (CSV)                       │
└─────────────────┘           └────────────────                        │
        │                                                              │
        │    ┌─────────────────────────────────────────────────────┐   │
        ├───►│ ai_analysis                                         │   │
        │    ├─────────────────────────────────────────────────────┤   │
        │    │ risk_level · emotional_drift_score                  │   │
        │    │ burnout_probability · dominant_emotion              │   │
        │    │ mood_trend · insights · recommendations (JSON)      │   │
        │    │ weekly_avg_score · care_pathway                     │   │
        │    └─────────────────────────────────────────────────────┘   │
        │    ┌──────────────────┐  ┌──────────────────┐                │
        ├───►│ mood_goals       │  │ journal_entries   │               │
        │    │ title · type     │  │ title · content   │               │
        │    │ target/done days │  │ sentiment_score   │               │
        │    │ progress %       │  │ word_count        │               │
        │    └──────────────────┘  └──────────────────┘                │
        │    ┌──────────────────┐                                      │
        └───►│ notifications    │                                      │
             │ title · message  │                                      │
             │ notif_type       │                                      │
             │ is_read          │                                      │
             └──────────────────┘                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Emotion-Buddy/
│
├── 📄 app.py                  # Main Flask application — routing, AI engine, REST APIs
├── 📄 config.py               # DB connection, session config, security settings
├── 📄 models.py               # SQLAlchemy ORM models (6 tables, relationships)
├── 📄 migration.py            # Smart incremental schema migration (no data loss)
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md               # You are here
│
├── 📁 templates/              # Jinja2 HTML templates
│   ├── base.html              # Shell layout (sidebar + topbar + flash toasts)
│   ├── index.html             # Public landing page
│   ├── login.html             # Two-panel login
│   ├── signup.html            # Two-panel registration
│   ├── dashboard.html         # Main dashboard (stat cards, AI insights, charts)
│   ├── checkin.html           # 4-step emotion check-in form
│   ├── analytics.html         # Full analytics with 4 Chart.js charts
│   ├── journal.html           # Private journal with sentiment tagging
│   ├── goals.html             # Wellness goal tracker with progress bars
│   ├── calm.html              # Breathing, mindfulness timer, ambient sounds
│   ├── support.html           # Care pathway tiers + AI recommendations
│   ├── profile.html           # Profile editor + privacy dashboard
│   ├── notifications.html     # Notification feed
│   └── errors/
│       ├── 404.html           # Custom 404 page
│       └── 500.html           # Custom 500 page
│
├── 📁 static/
│   ├── css/
│   │   └── style.css          # Complete design system (1000+ lines, CSS variables)
│   └── js/
│       └── main.js            # Vanilla JS — animations, sidebar, charts, interactions
│
└── 📁 documents/              # Project documentation artifacts
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Minimum Version |
|---|---|
| Python | 3.10+ |
| MySQL Server | 8.0+ |
| pip | Latest |
| Browser | Chrome/Firefox/Edge (modern) |

### Step 1 — Clone & Install

```bash
# Clone the repository
git clone https://github.com/Ratandeep-purohit/Feelio.git
cd Feelio

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install all dependencies
pip install -r requirements.txt
```

### Step 2 — Configure Database

Open `config.py` and set your MySQL credentials:

```python
# config.py
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost/emotion_buddy'
)
```

> ⚠️ **Special characters in passwords** must be URL-encoded.  
> Example: `R@j@t2004` → `R%40j%40t2004`

Create the MySQL database:

```sql
CREATE DATABASE emotion_buddy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 3 — Run Migration

```bash
python migration.py
```

**Expected output:**
```
📦 Step 1 — Creating new tables if they don't exist...
   Done.

🔧 Step 2 — Upgrading schema for existing tables...

▶  Table: users
  ✔  Column 'full_name' already exists in 'users'.
  ✚  Adding column 'streak_days' to 'users'...
  ...

✅ Schema migration completed successfully!
🚀 Feelio v2.0 is ready! Run: python app.py
```

### Step 4 — Launch

```bash
python app.py
```

Then open your browser at: **[http://localhost:5000](http://localhost:5000)** 🚀

---

## 🔌 REST API Reference

All API endpoints require an active authenticated session (cookie-based).

### GET `/api/analytics/mood-trend`

Returns mood score history for line chart rendering.

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `days` | integer | `30` | Number of days to look back |

**Response:**
```json
{
  "success": true,
  "data": [
    { "date": "2025-03-01", "score": 7, "mood": "content" },
    { "date": "2025-03-02", "score": 4, "mood": "anxious" }
  ]
}
```

---

### GET `/api/analytics/mood-distribution`

Returns mood tag frequency counts for donut chart.

**Response:**
```json
{
  "success": true,
  "data": [
    { "mood": "happy", "count": 12 },
    { "mood": "anxious", "count": 5 }
  ]
}
```

---

### GET `/api/analytics/energy-sleep`

Returns sleep hours vs mood score for scatter plot.

**Response:**
```json
{
  "success": true,
  "data": [
    { "sleep": 7.5, "score": 8, "energy": "high" },
    { "sleep": 4.0, "score": 3, "energy": "low" }
  ]
}
```

---

### GET `/api/analytics/weekly-summary`

Returns aggregated stats for the last 7 days.

**Response:**
```json
{
  "success": true,
  "total_checkins": 5,
  "avg_score": 6.4,
  "best_day": "Friday",
  "worst_day": "Tuesday"
}
```

---

### POST `/api/goals/<goal_id>/increment`

Marks one day as completed for a goal. Auto-closes goal if target is reached.

**Response:**
```json
{
  "success": true,
  "goal": {
    "id": 3,
    "title": "Meditate daily",
    "completed_days": 5,
    "target_days": 7,
    "progress": 71,
    "is_completed": false
  }
}
```

---

### GET `/api/notifications/unread-count`

Returns the count of unread notifications.

**Response:**
```json
{ "count": 3 }
```

---

## 🎨 Design System

Feelio uses a **complete custom CSS design system** built from scratch.

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--primary` | `#6c3bef` | Brand, buttons, active nav |
| `--secondary` | `#2dd4bf` | Teal accents, charts |
| `--accent` | `#f472b6` | Pink highlights, journal |
| `--accent-warm` | `#fb923c` | Orange accents, goals |
| `--success` | `#10b981` | Low risk, completed goals |
| `--warning` | `#f59e0b` | Medium risk, cautions |
| `--danger` | `#ef4444` | High risk, errors, crisis |

### Typography

```css
font-family: 'Outfit', system-ui, sans-serif;
/* Weights used: 300, 400, 500, 600, 700, 800, 900 */
```

### Elevation System

```css
--shadow-sm: 0 1px 3px rgba(0,0,0,.06);      /* forms, inputs */
--shadow:    0 4px 24px rgba(108,59,239,.08); /* cards */
--shadow-lg: 0 12px 48px rgba(108,59,239,.14); /* elevated cards */
--shadow-xl: 0 24px 64px rgba(108,59,239,.20); /* hero, modals */
```

### Components Available

| Component | CSS Class | Description |
|---|---|---|
| Glass Card | `.card` | Glassmorphism panels with hover lift |
| Stat Card | `.stat-card` | Icon + value + label + delta |
| Gradient Button | `.btn.btn-primary` | Gradient with shadow glow |
| Emoji Picker | `.emoji-grid .emoji-choice` | Radio-based emoji selector |
| Mood Slider | `.score-slider` | Custom gradient range input |
| Score Ring | `.score-ring` | SVG circle progress ring |
| Risk Meter | `.risk-meter-bar` | Animated fill bar |
| Progress Bar | `.progress-bar .progress-fill` | CSS animated fill |
| Tag Pills | `.tag-pill` | Checkbox-based multi-select |
| Segmented Control | `.seg-control` | iOS-style toggle buttons |
| Flash Toasts | `.flash-toast` | Auto-dismiss notification toasts |
| Breathing Circle | `.breath-ring` | CSS box-breathing animation |
| Pathway Cards | `.pathway-card.tier-*` | Tiered support cards |
| Profile Header | `.profile-header` | Gradient banner with avatar |

---

## 🔐 Security Model

| Layer | Implementation |
|---|---|
| **Password Hashing** | `werkzeug.security.generate_password_hash` (scrypt/pbkdf2) |
| **Session Security** | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'` |
| **Auth Guard** | `@login_required` decorator on all protected routes |
| **DB Error Recovery** | `db.session.rollback()` in global 500 error handler |
| **SQL Injection** | SQLAlchemy ORM parameterized queries (no raw SQL in routes) |
| **Connection Pooling** | `pool_pre_ping=True` prevents stale connections |
| **URL-safe Passwords** | Config supports URL-encoded special chars via PyMySQL |
| **Data Ownership** | All queries filtered by `user_id = session['user_id']` |

> 🔒 **Privacy-First Principle:** No personally identifiable behavioral data is ever exposed through API responses. All endpoints are session-scoped.

---

## 🛠️ Configuration

All configuration lives in `config.py`:

```python
class Config:
    # ─── Database ────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost/emotion_buddy'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,   # Recycle connections every 4.6 min
        'pool_pre_ping': True, # Test connection before using
        'pool_size': 10,       # Concurrent connections
        'max_overflow': 20,    # Extra connections allowed on burst
    }

    # ─── Security ────────────────────────────────────
    SECRET_KEY = 'change-this-in-production'
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

    # ─── App ─────────────────────────────────────────
    DEBUG = True  # Set False in production!
```

### Environment Variables (Production)

```bash
# .env (create this file, never commit it)
DATABASE_URL=mysql+pymysql://produser:securepass@db-host/feelio_prod
SECRET_KEY=your-256-bit-random-secret-key
FLASK_DEBUG=False
```

---

## 📈 Roadmap

### v2.1 — Community & Real-Time
- [ ] 🔔 WebSocket push notifications (Flask-SocketIO)
- [ ] 👥 Anonymous peer support chat rooms
- [ ] 📧 Email reminders (Flask-Mail + Celery)
- [ ] 🌍 Multi-language i18n support (Flask-Babel)

### v2.2 — Intelligence Upgrade  
- [ ] 🤖 Google Gemini AI integration for personalized insights
- [ ] 📊 NLP sentiment analysis on journal entries (spaCy)
- [ ] 🧬 Pattern clustering (7-day Fourier mood cycles)
- [ ] 📱 Voice-based check-in (Web Speech API)

### v3.0 — Platform Expansion
- [ ] 🏥 NGO / therapist integration dashboard
- [ ] 📦 REST API v2 (JWT-based, fully public)
- [ ] 🐳 Docker + docker-compose production setup
- [ ] 🧪 Full pytest + Selenium test suite
- [ ] 📱 Progressive Web App (PWA) with offline mode

---

## 🤝 Contributing

We welcome contributions from developers, mental health advocates, and designers.

```bash
# 1. Fork the repository

# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Run the app and verify your changes
python migration.py
python app.py

# 4. Commit your changes
git commit -m 'feat: Add AmazingFeature'

# 5. Push to your branch
git push origin feature/AmazingFeature

# 6. Open a Pull Request
```

### Code Standards

- **Python**: PEP 8 · Type hints on all functions · Docstrings on all classes
- **HTML**: Semantic HTML5 · ARIA labels on interactive elements
- **CSS**: BEM-inspired class naming · CSS variables only (no hardcoded colors)
- **JS**: Vanilla ES6+ only · No external frameworks · Event delegation

---

## 📦 Dependencies

```
Flask==3.0.0               # Web framework
Flask-SQLAlchemy==3.1.1    # ORM
PyMySQL==1.1.0             # MySQL driver
cryptography==41.0.4       # PyMySQL TLS support
Werkzeug==3.0.1            # Password hashing, WSGI utilities
python-dotenv==1.0.0       # .env file support
```

---

## 📞 Crisis Resources

> ⚠️ **Feelio is not a substitute for professional mental health care.**  
> If you or someone you know is in crisis, please contact:

| Region | Resource | Contact |
|---|---|---|
| 🇮🇳 India | iCall (TISS) | **9152987821** |
| 🇮🇳 India | Vandrevala Foundation | **1860-2662-345** |
| 🇺🇸 USA | National Suicide Hotline | **988** |
| 🇬🇧 UK | Samaritans | **116 123** |
| 🌍 Global | Crisis Text Line | Text **HOME** to **741741** |

---

## 📄 License

```
MIT License

Copyright (c) 2025 Feelio Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

<div align="center">

**Built with ❤️ for mental wellness. Powered by Python. Guided by empathy.**

```
"Technology should protect minds, not exploit them."
                                        — Feelio Manifesto
```

[![GitHub Stars](https://img.shields.io/github/stars/Ratandeep-purohit/Feelio?style=social)](https://github.com/Ratandeep-purohit/Feelio)
[![GitHub Forks](https://img.shields.io/github/forks/Ratandeep-purohit/Feelio?style=social)](https://github.com/Ratandeep-purohit/Feelio/fork)

🔗 **[View on GitHub → github.com/Ratandeep-purohit/Feelio](https://github.com/Ratandeep-purohit/Feelio)**

*If Feelio helped you, consider giving it a ⭐ — it helps others discover it.*

</div>
