# Quick Deployment Guide

## 🚀 Deploy to Render in 5 Minutes (100% FREE)

### Step 1: Push to GitHub (2 minutes)
```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/support-ticket-system.git
git push -u origin main
```

### Step 2: Deploy to Render (3 minutes)
1. Go to: https://render.com/deploy
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically read `render.yaml` and create all services
5. Add these environment variables when prompted:
   - `DJANGO_ALLOWED_HOSTS` = `your-backend-name.onrender.com`
   - `LLM_API_KEY` = `AIzaSyBvE6ehvWZF6ucClzWcnEzAsuc3ouPPC60`
6. Click **"Apply"**

### Done! ✅
- Backend: `https://support-ticket-backend.onrender.com`
- Frontend: `https://support-ticket-frontend.onrender.com`
- Database: PostgreSQL (automatically connected)

---

## Alternative: One-Click Deploy Button

Add this to your GitHub README for instant deployment:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/support-ticket-system)

---

## 🐳 Deploy with Docker (VPS/Cloud)

### On Any VPS (DigitalOcean, AWS, etc.):

1. **SSH into your server:**
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

3. **Clone and run:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/support-ticket-system.git
   cd support-ticket-system
   cp .env.example .env
   nano .env  # Add your settings
   docker-compose up -d
   ```

4. **Done!** Access at `http://your-server-ip:3000`

---

## 🌐 Deploy to Vercel + Railway

### Backend on Railway:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Frontend on Vercel:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## Free Hosting Options Comparison:

| Platform | Setup Time | Cost | Best For |
|----------|------------|------|----------|
| **Render** | 5 min | FREE | Complete stack |
| **Railway** | 3 min | $5 credit | Quick prototypes |
| **Vercel + PlanetScale** | 10 min | FREE | Scalable apps |
| **Docker on VPS** | 15 min | $5/month | Full control |

**Recommended:** Start with **Render** (easiest, completely free)

---

## Environment Variables Checklist:

### Backend:
- ✅ `DJANGO_DEBUG=false`
- ✅ `DJANGO_ALLOWED_HOSTS=your-domain.com`
- ✅ `DJANGO_SECRET_KEY=random-secret-key`
- ✅ `DATABASE_URL=postgres://...` (auto-set by Render)
- ✅ `LLM_API_KEY=your-gemini-key`

### Frontend:
- ✅ `REACT_APP_API_BASE=https://your-backend.onrender.com/api/tickets`

---

## Troubleshooting:

### Backend won't start:
```bash
# Check logs in Render dashboard
# Ensure migrations ran: python manage.py migrate
```

### Frontend can't connect to backend:
```bash
# Verify REACT_APP_API_BASE is correct
# Check CORS settings in Django
```

### Database connection failed:
```bash
# Use DATABASE_URL from Render
# Ensure PostgreSQL service is running
```

---

## Production Checklist:

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy backend with PostgreSQL
- [ ] Deploy frontend
- [ ] Add environment variables
- [ ] Test API endpoints
- [ ] Test frontend UI
- [ ] Setup custom domain (optional)
- [ ] Enable SSL (automatic on Render)

**Your app is production-ready!** 🎉
