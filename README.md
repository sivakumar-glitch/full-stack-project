# Support Ticket System

Full-stack support ticket system with **free** LLM-assisted category and priority suggestions using Google Gemini.

## Tech Stack
- Backend: Django + Django REST Framework + PostgreSQL
- Frontend: React (Create React App)
- LLM: **Google Gemini API** (FREE - 60 requests/min, no payment required)
- Infrastructure: Docker + Docker Compose

## Quick Start - FREE

### 1. Get Free Gemini API Key (2 minutes)
See [GEMINI_API_SETUP.md](GEMINI_API_SETUP.md) for step-by-step instructions.

### 2. Add Key to .env
```bash
LLM_API_KEY=your_free_gemini_key
```

### 3. Run Locally (No Docker)
```bash
# Terminal 1 - Backend
python manage.py runserver --settings=support_backend.settings_dev

# Terminal 2 - Frontend  
cd frontend && npm start
```

Visit `http://localhost:3000`

## Running with Docker
```bash
docker-compose up --build
```
Frontend: `http://localhost:3000`
Backend: `http://localhost:8000`

## 🚀 Deployment

### Quick Deploy to Production (FREE):
See [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md) for 5-minute deployment to Render.

### Detailed Deployment Options:
See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Render (FREE)
- Railway ($5 credit)
- Vercel + PlanetScale
- Docker on VPS
- Heroku

**Recommended:** Deploy to Render for free hosting with PostgreSQL.

## API Endpoints
- `POST /api/tickets/` create a ticket
- `GET /api/tickets/` list tickets (filters: `category`, `priority`, `status`, `search`)
- `PATCH /api/tickets/<id>/` update ticket
- `GET /api/tickets/stats/` aggregated stats
- `POST /api/tickets/classify/` LLM category + priority suggestion

## Environment Variables
See `.env.example` for the full list.

## Notes
- If the LLM is unavailable, ticket creation still works and suggestions are skipped.
- Stats use database-level aggregation only.
