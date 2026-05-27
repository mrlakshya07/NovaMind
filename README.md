# NovaMind — Study Platform SaaS

> *"The smartest way to study — powered by AI, designed for focus."*

NovaMind is a premium, portfolio-grade student productivity platform inspired by Notion, Forest, and Todoist. It transforms the way you study by combining AI-generated quizzes, a gamified Pomodoro timer, Kanban task management, and deep study analytics into one beautiful, glassmorphic SaaS product.

## 🚀 Key Features

1. **AI Quiz Generator**: Instantly turn your markdown notes into interactive MCQs using spaCy NLP. Tests your knowledge with AI-generated distractors.
2. **Advanced Notes System**: Color-coded, taggable, pinnable notes with full Markdown support.
3. **Smart Kanban Todo Board**: Drag-and-drop task management with priority levels and due dates.
4. **Next-Gen Pomodoro**: Beautiful animated circular timer with focus/break modes, session tracking, and ambient aesthetics.
5. **Deep Analytics**: GitHub-style study heatmaps, weekly area charts, and subject-wise breakdown using Recharts.
6. **Gamification**: Earn XP by studying, taking quizzes, and completing tasks. Level up and maintain daily streaks to boost your Productivity Score.
7. **Premium UI/UX**: Dark mode by default, glassmorphism, Framer Motion animations, toast notifications, and responsive sidebar navigation.

---

## 🛠️ Tech Stack

**Frontend**:
- React 18 + Vite
- Tailwind CSS (Custom Design System)
- Framer Motion (Animations)
- Zustand (Global State)
- Recharts (Data Visualization)
- dnd-kit (Drag and Drop)

**Backend**:
- Python 3 + Flask REST API
- Flask-SQLAlchemy (ORM) & SQLite/PostgreSQL
- Flask-JWT-Extended (Authentication)
- spaCy & RapidFuzz (NLP Quiz Engine)
- Flask-Bcrypt (Password Hashing)

---

## 💻 Local Setup & Development

### 1. Backend Setup

```bash
cd backend
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy NLP model
python -m spacy download en_core_web_sm

# Start the Flask development server (runs on port 5000)
python run.py
```

### 2. Frontend Setup

```bash
cd frontend
# Install dependencies
npm install

# Start the Vite development server (runs on port 5173)
npm run dev
```

Visit `http://localhost:5173` to view the app! The frontend automatically proxies `/api` requests to the Flask backend.

---

## ☁️ Deployment Guide

### Backend (Render / Railway)
1. Push your code to GitHub.
2. Create a new Web Service on Render, connect your repo, and set the root directory to `backend`.
3. Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Start Command: `gunicorn -w 4 -b 0.0.0.0:10000 "app:create_app('production')"`
5. Environment Variables:
   - `DATABASE_URL`: Add a PostgreSQL database string provided by Render.
   - `SECRET_KEY`: Generate a random secure string.
   - `JWT_SECRET_KEY`: Generate a random secure string.
   - `CORS_ORIGINS`: Set to your frontend production URL.

### Frontend (Vercel / Netlify)
1. Create a new project on Vercel and connect your repo.
2. Set the Root Directory to `frontend`.
3. Framework Preset: Vite
4. Build Command: `npm run build`
5. Output Directory: `dist`
6. Add a redirect rule for the API if not using a custom domain or update the `baseURL` in Axios client.

---

## 👔 Portfolio & Career Assets

### Recommended GitHub Repo Name
`novamind-study-platform`

### Resume Bullet Points
- Built **NovaMind**, a full-stack AI-powered student productivity SaaS platform handling authentication, notes, tasks, and analytics.
- Engineered an NLP-based quiz generator using Python, spaCy, and RapidFuzz to dynamically convert markdown notes into interactive MCQs.
- Designed a premium, responsive frontend architecture using React, Vite, Tailwind CSS, and Framer Motion, featuring drag-and-drop Kanban boards and Recharts data visualization.
- Implemented a robust Flask REST API with JWT authentication, SQLAlchemy ORM, and PostgreSQL for secure, scalable data management.

### LinkedIn Project Description
🚀 **Just launched NovaMind — The smartest way to study!**

I built NovaMind from scratch to solve my own productivity challenges. It's a full-stack SaaS platform inspired by Notion and Forest, but supercharged with AI.

✨ **Key Features:**
- 🧠 **AI Quiz Engine:** Automatically generates MCQs from your notes using spaCy NLP.
- ⏱️ **Animated Pomodoro:** A beautiful focus timer with session tracking.
- 📊 **Study Analytics:** GitHub-style heatmaps and Recharts to visualize productivity.
- 🎮 **Gamification:** Earn XP, level up, and maintain streaks by studying.

🛠️ **Tech Stack:** React, Tailwind, Framer Motion, Flask, PostgreSQL, JWT, spaCy.

Check out the code on my GitHub! Would love to hear your feedback in the comments. 👇
*(Attach screenshots or a short demo video here)*

### How to Make it Viral on LinkedIn/GitHub
1. **The Demo Video**: Don't just post screenshots. Record a slick 60-second Loom video showing the UI animations, the drag-and-drop Kanban, and the "Aha!" moment when the AI generates a quiz from a note.
2. **The Story**: Frame the post around a relatable problem: "I had 5 different tabs open for notes, pomodoro, tasks, and quizzes. So I built one app to do it all, beautifully."
3. **Open Source Angle**: Add a "Contributions Welcome" section in the README. Tag popular tech communities or educational influencers.
4. **Visuals**: Add high-quality mockups to your README.

---

## 🎨 UI Mockup Descriptions (For Screenshots)

1. **Dashboard (`/dashboard`)**: A glassmorphic control center. Top stats show XP, Level, and Streak with custom icons. A sleek purple-gradient area chart shows weekly study hours, next to quick action buttons and upcoming tasks.
2. **Notes (`/notes`)**: A masonry-style grid of color-coded note cards. Hovering reveals a subtle glowing border. The note editor is a modal overlay with a Markdown text area and a color palette selector.
3. **Tasks (`/tasks`)**: A 3-column Kanban board (To Do, In Progress, Done). Tasks have priority badges (red/yellow/green) and due dates. Dragging a task tilts it slightly (Framer Motion).
4. **Pomodoro (`/pomodoro`)**: A large, glowing circular SVG timer in the center. Switching between Focus and Break modes smoothly transitions the glow color from Indigo to Emerald.
5. **AI Quiz (`/quiz`)**: A split view. Left side: Pick a note. Right side: Interactive quiz with A/B/C/D buttons. Clicking the correct answer lights it up green with a celebration toast notification!
6. **Analytics (`/analytics`)**: A dark-mode GitHub contribution heatmap tracking daily study hours across 365 days, alongside a donut chart showing subject distribution.

---

## 🗺️ Feature Roadmap (V2 Ideas)
- [ ] Collaborative study rooms (WebSockets)
- [ ] Google Calendar integration
- [ ] AI-generated flashcards (Spaced Repetition System)
- [ ] Mobile app wrap (React Native / PWA)
- [ ] Social leaderboards