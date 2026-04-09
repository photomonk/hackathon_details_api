# 🚀 Hackathon AI API

A **FastAPI + Google Gemini** powered REST API that helps developers find hackathon events, generate project ideas, and design project architectures — all driven by AI.

---

## ✨ Features

| Endpoint | Method | Description |
|---|---|---|
| `/api/hackathons` | GET / POST | Find relevant hackathon events by theme, format & skill level |
| `/api/ideas` | POST | Generate creative, buildable project ideas for your team |
| `/api/architecture` | POST | Design a full tech architecture for your hackathon project |
| `/docs` | GET | Interactive Swagger UI |
| `/health` | GET | Health check |

---

## 🏗️ Project Structure

```
hackathon_api/
├── main.py                     # FastAPI app entry point
├── requirements.txt
├── .env.example                # Environment variable template
├── .gitignore
│
├── core/
│   └── config.py               # pydantic-settings config loader
│
├── models/
│   └── schemas.py              # Pydantic request & response models
│
├── services/
│   └── gemini_service.py       # Gemini prompt builder + JSON parser
│
└── routers/
    ├── hackathon.py            # /api/hackathons routes
    ├── ideas.py                # /api/ideas route
    └── architecture.py         # /api/architecture route
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- A free Gemini API key → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hackathon-ai-api.git
cd hackathon-ai-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
```

### 5. Run the server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

Server: [http://localhost:8000](http://localhost:8000)  
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Usage

### Find Hackathon Events

```bash
curl "http://localhost:8000/api/hackathons?theme=AI&format=remote&skill_level=beginner"
```

Or via POST:

```bash
curl -X POST http://localhost:8000/api/hackathons \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "AI / ML",
    "format": "remote",
    "skill_level": "beginner",
    "extra": "looking for prizes and mentorship"
  }'
```

**Response:**
```json
{
  "query_summary": "Beginner-friendly remote AI/ML hackathons with prizes",
  "events": [
    {
      "name": "Google AI Hackathon",
      "platform": "Devpost",
      "theme": "AI / ML",
      "format": "remote",
      "duration": "48 hours",
      "prize_range": "$500–$5000",
      "difficulty": "beginner",
      "why_good_fit": "Great mentorship and beginner tracks available"
    }
  ],
  "tips": ["Register early", "Join the Discord", "Read past winning projects"]
}
```

---

### Generate Project Ideas

```bash
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "mental health",
    "skills": ["Python", "React", "AI/ML"],
    "team_size": "medium",
    "duration_hours": 24
  }'
```

**Response:**
```json
{
  "theme": "mental health",
  "ideas": [
    {
      "title": "MindBridge",
      "tagline": "AI-powered journaling that detects mood patterns",
      "problem_solved": "People struggle to track their mental health over time",
      "core_features": ["Daily mood check-in", "AI pattern analysis", "Resource suggestions"],
      "tech_stack": ["React", "FastAPI", "Gemini API", "Supabase"],
      "mvp_scope": "Working mood tracker with AI insights in 24 hours",
      "wow_factor": "Real-time sentiment analysis with actionable nudges",
      "difficulty": "medium"
    }
  ],
  "recommended_idea": "MindBridge",
  "quick_tip": "Focus on the AI insight feature — that's your differentiator"
}
```

---

### Design Project Architecture

```bash
curl -X POST http://localhost:8000/api/architecture \
  -H "Content-Type: application/json" \
  -d '{
    "project_title": "MindBridge",
    "description": "AI journaling app that tracks mood patterns and suggests resources",
    "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
    "constraints": "free-tier only, deploy in 24 hours",
    "team_size": "medium"
  }'
```

**Response:**
```json
{
  "project_title": "MindBridge",
  "architecture_style": "REST API + SPA",
  "layers": [
    { "name": "Frontend",  "technology": "React + Vite",        "purpose": "User chat and dashboard", "free_tier": true },
    { "name": "Backend",   "technology": "FastAPI + Python",    "purpose": "API logic and AI calls",  "free_tier": true },
    { "name": "AI Layer",  "technology": "Gemini 1.5 Flash",    "purpose": "Mood analysis and NLP",   "free_tier": true },
    { "name": "Database",  "technology": "Supabase (Postgres)", "purpose": "User data and sessions",  "free_tier": true },
    { "name": "Hosting",   "technology": "Render + Vercel",     "purpose": "Deployment",              "free_tier": true }
  ],
  "data_flow": [
    "Step 1: User submits journal entry via React UI",
    "Step 2: FastAPI validates and forwards to Gemini service",
    "Step 3: Gemini analyzes mood and returns structured response",
    "Step 4: Result stored in Supabase and returned to frontend"
  ],
  "deployment_plan": "Deploy FastAPI to Render, React to Vercel, connect via environment variables",
  "estimated_setup_time": "3 hours",
  "api_endpoints": [
    "POST /api/journal     - submit a journal entry",
    "GET  /api/history     - fetch past entries with mood scores",
    "GET  /api/insights    - get AI-generated weekly insights"
  ],
  "challenges_to_watch": [
    "Gemini free tier rate limits under load",
    "Handling sensitive mental health data responsibly"
  ]
}
```

---

## 🚢 Deployment

### Render (recommended for FastAPI)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `GEMINI_API_KEY=your_key`

### Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway variables set GEMINI_API_KEY=your_key
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t hackathon-api .
docker run -p 8000:8000 --env-file .env hackathon-api
```

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — API framework with auto Swagger docs
- **[Google Gemini](https://ai.google.dev/)** — AI model for all intelligence features
- **[Pydantic v2](https://docs.pydantic.dev/)** — Request validation and response models
- **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Environment variable management
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server

---

## 📄 License

MIT — free to use, modify, and distribute.
