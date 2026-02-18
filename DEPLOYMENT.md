# Deployment Guide - Support Ticket System

## Option 1: Deploy to Render (Recommended - FREE Tier Available)

### Backend Deployment (Django + PostgreSQL)

1. **Create a Render Account:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Push Your Code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/support-ticket-system.git
   git push -u origin main
   ```

3. **Create PostgreSQL Database:**
   - In Render Dashboard → New → PostgreSQL
   - Name: `ticket-db`
   - Plan: Free
   - Copy the **Internal Database URL**

4. **Create Web Service for Backend:**
   - New → Web Service
   - Connect your GitHub repo
   - Name: `support-ticket-backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn support_backend.wsgi:application`
   - Plan: Free

5. **Add Environment Variables:**
   ```
   DJANGO_DEBUG=false
   DJANGO_ALLOWED_HOSTS=support-ticket-backend.onrender.com
   DJANGO_SECRET_KEY=your-random-secret-key-here
   DATABASE_URL=<paste-internal-database-url>
   LLM_API_KEY=AIzaSyBvE6ehvWZF6ucClzWcnEzAsuc3ouPPC60
   ```

6. **Add gunicorn to requirements.txt:**
   ```
   gunicorn==21.2.0
   ```

### Frontend Deployment (React)

1. **Create Static Site:**
   - In Render Dashboard → New → Static Site
   - Connect your GitHub repo
   - Name: `support-ticket-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`

2. **Add Environment Variable:**
   ```
   REACT_APP_API_BASE=https://support-ticket-backend.onrender.com/api/tickets
   ```

3. **Deploy!**
   - Both services will auto-deploy
   - Free tier: Backend sleeps after 15 min inactivity (wakes up on request)

---

## Option 2: Deploy to Railway (FREE $5 Credit)

### Quick Deploy:

1. **Visit:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Add Services:**
   - PostgreSQL (from template)
   - Backend (add env vars)
   - Frontend (add build command)

4. **Environment Variables:**
   Same as Render above

---

## Option 3: Deploy to Vercel + PlanetScale (FREE)

### Backend on Vercel:

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Create `vercel.json`:**
   ```json
   {
     "builds": [{"src": "support_backend/wsgi.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "support_backend/wsgi.py"}]
   }
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

### Frontend on Vercel:

1. **Deploy Frontend:**
   ```bash
   cd frontend
   vercel --prod
   ```

---

## Option 4: Deploy to Heroku (Paid Plans Only Now)

### Setup:

1. **Install Heroku CLI:**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create apps:**
   ```bash
   heroku create support-ticket-backend
   heroku create support-ticket-frontend
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini -a support-ticket-backend
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set DJANGO_DEBUG=false -a support-ticket-backend
   heroku config:set LLM_API_KEY=your_key -a support-ticket-backend
   ```

5. **Create `Procfile`:**
   ```
   web: gunicorn support_backend.wsgi
   release: python manage.py migrate
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

---

## Option 5: Docker + VPS (DigitalOcean/AWS/Linode)

### For Production Docker Deployment:

1. **Get a VPS ($5/month on DigitalOcean)**

2. **SSH into server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

4. **Clone your repo:**
   ```bash
   git clone https://github.com/yourusername/support-ticket-system.git
   cd support-ticket-system
   ```

5. **Create `.env` file:**
   ```bash
   nano .env
   # Add all environment variables
   ```

6. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

7. **Setup Nginx reverse proxy:**
   ```bash
   apt install nginx
   nano /etc/nginx/sites-available/ticket-system
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
       }

       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

8. **Enable site:**
   ```bash
   ln -s /etc/nginx/sites-available/ticket-system /etc/nginx/sites-enabled/
   systemctl restart nginx
   ```

9. **Setup SSL (free with Let's Encrypt):**
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d your-domain.com
   ```

---

## Recommended Deployment: Render (Free)

### Complete Render Deployment Steps:

1. **Prepare Your Code:**
   - Ensure `requirements.txt` has `gunicorn==21.2.0`
   - Update `settings.py` for production (see below)

2. **Update Django Settings for Production:**

Create `support_backend/settings_prod.py`:
```python
from .settings import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Use DATABASE_URL for PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

3. **Add to requirements.txt:**
```
dj-database-url==2.1.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
gunicorn==21.2.0
```

4. **Deploy:**
   - Push to GitHub
   - Create services in Render
   - Add environment variables
   - Done! ✅

---

## Free Tier Comparison:

| Platform | Backend | Database | Frontend | Domain | SSL |
|----------|---------|----------|----------|--------|-----|
| **Render** | ✅ Free | ✅ 90 days free | ✅ Free | ✅ | ✅ |
| **Railway** | ✅ $5 credit | ✅ $5 credit | ✅ $5 credit | ✅ | ✅ |
| **Vercel** | ⚠️ Serverless | ❌ | ✅ Free | ✅ | ✅ |
| **Fly.io** | ✅ Free | ✅ 3GB free | ✅ Free | ✅ | ✅ |

**Recommendation:** Use **Render** for easiest free deployment!

---

## Need Help?

- Check logs in Render dashboard
- Ensure migrations run: `python manage.py migrate`
- Test locally with Docker first: `docker-compose up`
