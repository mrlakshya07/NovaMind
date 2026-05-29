<div align="center">
  <h1>🚀 NovaMind</h1>
  <p><strong>AI-Powered Student Productivity Platform</strong></p>

  <p>
    <a href="https://github.com/mrlakshya07/NovaMind/stargazers"><img src="https://img.shields.io/github/stars/mrlakshya07/NovaMind?style=for-the-badge&color=ffd700" alt="Stars"></a>
    <a href="https://github.com/mrlakshya07/NovaMind/network/members"><img src="https://img.shields.io/github/forks/mrlakshya07/NovaMind?style=for-the-badge&color=00aaff" alt="Forks"></a>
    <a href="https://github.com/mrlakshya07/NovaMind/issues"><img src="https://img.shields.io/github/issues/mrlakshya07/NovaMind?style=for-the-badge&color=ff5555" alt="Issues"></a>
    <a href="https://github.com/mrlakshya07/NovaMind/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mrlakshya07/NovaMind?style=for-the-badge&color=44cc44" alt="License"></a>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
  </p>

  <p>
    <em>A gamified student productivity platform featuring study analytics, achievement progression, focus integrity tracking, and cloud-powered data management.</em>
  </p>
</div>

<hr />

## 🌟 Why NovaMind?

Most productivity apps track tasks.

NovaMind tracks growth.

By combining:

- 📈 Study Analytics
- 📝 Smart Notes
- 📋 Task Management
- ⏱️ Pomodoro Sessions
- 🏆 Achievement Gamification
- 💎 Focus Integrity Tracking

NovaMind transforms studying into a rewarding and measurable experience.

---

## ✨ Features Showcase

### 🔐 Secure Authentication & User Isolation
- **Supabase Auth Integration**: Robust signup, login, and session management.
- **Data Isolation**: Fully isolated user data leveraging PostgreSQL Row Level Security.

### 📈 Study Progress Tracker
- **Log Sessions**: Accurately log and record study sessions.
- **Track Hours**: Measure total study hours over time.
- **Historical Analytics**: Visualize and analyze historical study data.

### 📝 Smart Notes System
- **Cloud Storage**: Secure note storage and retrieval using Supabase.
- **Quick Search**: Fast retrieval of previously saved notes.
- **CRUD Operations**: Complete create, read, update, and delete note functionality.

### 📋 Task Management
- **Prioritization**: Set custom priorities for tasks (High, Medium, Low).
- **Due Dates**: Organize your workflow with due dates.
- **Completion Tracking**: Seamlessly create, manage, and complete tasks.

### ⏱️ Pomodoro Focus System
- **Real-Time Countdown**: Built-in, persistent timer for tracking focused study blocks.
- **Focus Score**: Calculates session effectiveness.
- **Statistics**: Analyze focus metrics and performance.

---

## 🏗️ Architecture Overview

NovaMind is built with a modern, scalable SaaS architecture:

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla for maximum performance).
- **Backend**: Python with Flask, providing a modular and RESTful API.
- **Database**: Supabase PostgreSQL for relational data, ensuring high performance and data integrity.
- **Authentication**: Supabase Auth for seamless user identity management.
- **AI / Data Processing**: `spaCy` for text analysis, `RapidFuzz` for string matching, and `Matplotlib` for dynamic analytics generation.

---

## 🚀 Major Milestones

✅ Migrated from TXT Storage → Supabase PostgreSQL

✅ Implemented Supabase Authentication

✅ Built User-Isolated Multi-User Architecture

✅ Developed Achievement Dashboard

✅ Added Real-Time Achievement Toast Notifications

✅ Implemented Focus Integrity Tracking

✅ Created XP-Based Gamification System

✅ Built 19 Unlockable Achievements

✅ Integrated Focus Score Analytics

---

## 🗄️ Database Schema

The system utilizes a structured relational database hosted on Supabase:

- `users`: Core identity and profile settings.
- `study_sessions`: Logs of all recorded study periods.
- `notes`: User-created study materials and text notes.
- `tasks`: Action items, including priority and due date details.
- `achievements`: User-unlocked milestones and XP logic.
- `pomodoro_sessions`: Tracking deep-work intervals and focus scores.

### Database Migration

NovaMind originally stored data using local text files.

The project has now been fully migrated to:

✅ Supabase PostgreSQL

Benefits:

- Cloud Persistence
- User Isolation
- Better Scalability
- Secure Authentication Integration
- Real-Time Achievement Tracking

---

## 🏆 Achievement System (Gamification)

Stay motivated by unlocking dynamic achievements, earning XP, and receiving real-time toast notifications!

### Current Progression System

🏅 19 Unlockable Achievements

⭐ XP-Based Reward System

🔥 Real-Time Achievement Notifications

📊 Achievement Progress Tracking

💎 Focus Integrity Achievements

🎯 5 Achievement Categories

**Categories**: Study, Task, Note, Focus, and Consistency Achievements.

<details>
<summary><strong>🏅 View Implemented Achievements</strong></summary>

- **Study**: First Session, Study Apprentice, Knowledge Builder, Study Master
- **Notes**: First Note, Note Taker, Knowledge Scribe
- **Tasks**: First Task, Task Starter, Productivity Starter, Task Champion
- **Focus**: First Focus Session, Focus Builder, Deep Work Master, Focus Perfectionist
- **Consistency**: 3 Day Streak, 7 Day Streak, 30 Day Streak, Consistency Legend
</details>

---

## 🎯 Focus Integrity System

NovaMind goes beyond a traditional Pomodoro timer.

During every focus session NovaMind tracks:

- Browser tab switching
- Page visibility changes
- Session completion integrity
- Real-time focus score calculation

### Focus Score Formula

Focus Score = (Focused Time ÷ Total Session Time) × 100

### Focus Perfectionist Achievement

Students who maintain:

✅ 95%+ Focus Score

✅ 25+ Minute Focus Session

unlock the exclusive:

💎 Focus Perfectionist

This encourages genuine deep work instead of simply leaving a timer running.

---

## 🚀 Installation Guide

Get NovaMind running locally in just a few minutes.

### Prerequisites
- Python 3.9+
- Git
- Supabase Account

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/mrlakshya07/NovaMind.git
   cd NovaMind
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   flask run
   ```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory and add the following keys. You can find these in your Supabase project settings.

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your_secure_flask_secret_key
```

---

## 📁 Project Structure

```text
NovaMind/
│
├── backend/
│   ├── app.py
│   ├── achievements.py
│   ├── auth_service.py
│   ├── notes.py
│   ├── pomodoro.py
│   ├── study_progress_tracker.py
│   ├── tasks.py
│   └── supabase_client.py
│
├── frontend/
│   ├── static/
│   │   ├── main.js
│   │   ├── achievements.js
│   │   ├── style.css
│   │   └── animations.css
│   │
│   └── templates/
│       ├── index.html
│       ├── notes.html
│       ├── tasks.html
│       ├── pomodoro.html
│       ├── progress.html
│       ├── progress_log.html
│       ├── achievements.html
│       ├── login.html
│       └── signup.html
│
├── requirements.txt
└── README.md
```

---

## 🔌 API Overview

NovaMind provides a robust REST API for seamless frontend-backend communication.

Authentication
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/logout

Study Progress
- POST /api/progress/log

Notes
- GET /api/notes
- POST /api/notes/add

Tasks
- POST /api/tasks/add
- POST /api/tasks/toggle
- DELETE /api/tasks/delete

Pomodoro
- POST /api/pomodoro/start
- POST /api/pomodoro/complete

Achievements
- GET /api/achievements
- GET /api/achievements/progress
- GET /api/achievements/stats

---

## 🗺️ Future Roadmap

We are constantly improving NovaMind. Here's what's coming next:

- [ ] **Global Leaderboard**: Compete with students worldwide.
- [ ] **Study Topic Tracking**: Categorize and analyze time spent per subject.
- [ ] **Auto Pause on Tab Switch**: Enforce focus by automatically pausing the timer.
- [ ] **AI Quiz Generation**: Automatically generate quizzes from your notes.
- [ ] **Focus Analytics Dashboard**: Advanced data visualization for study habits.
- [ ] **Production Deployment**: Full deployment on modern cloud infrastructure.

---

## 🤝 Contribution Guide

We welcome contributions from the community! NovaMind is an excellent project for hackathons and programs like GSSoC.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read our `CONTRIBUTING.md` for detailed guidelines.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Developer

**Lakshya**  
B.Tech CSE Student • Open Source Contributor • Building in Public

A first-year engineering student passionate about software development, productivity tools, and open-source collaboration. NovaMind is a project built to learn full-stack development, cloud databases, authentication systems, and scalable application design while solving real student productivity challenges.

- GitHub: [@mrlakshya07](https://github.com/mrlakshya07)
- LinkedIn: [Lakshya](https://www.linkedin.com/in/lakshyarathi1/)

---

<div align="center">
  <p>Made with ❤️ to boost student productivity.</p>
  <p><strong>NovaMind</strong> &copy; 2026. All Rights Reserved.</p>
</div>