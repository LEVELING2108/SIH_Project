# 🚀 Deployment Guide - RailTrack Pro

Complete guide to deploy the RailTrack Pro Railway Track Fittings Management System on free hosting platforms and production environments.

## 📋 Table of Contents

1. [Deployment Options Overview](#deployment-options-overview)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Railway Deployment (Backend)](#railway-deployment-backend)
5. [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
6. [Render Deployment](#render-deployment)
7. [Alternative Free Hosting Options](#alternative-free-hosting-options)
8. [Production Checklist](#production-checklist)

---

## 🎯 Deployment Options Overview

| Component | Recommended Platform | Alternative Options |
|-----------|---------------------|---------------------|
| **Backend API** | Railway | Render, Fly.io, Google Cloud Run |
| **Frontend** | Vercel | Netlify, GitHub Pages, Cloudflare Pages |
| **Database** | Railway PostgreSQL | Supabase, Neon, ElephantSQL |
| **Full Stack** | Docker + VPS | Render, Fly.io |

### Hybrid Deployment Strategy

This project supports a **hybrid deployment strategy** giving you the best of both worlds:

| Component | Platform | Benefits |
|-----------|----------|----------|
| **Frontend** | Vercel | CDN, Auto HTTPS, Global Edge, Free tier |
| **Backend** | Railway | Auto-scaling, Managed PostgreSQL, Free tier |
| **Local/Self-hosted** | Docker | Full control, Offline use, VPS deployment |

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- Docker (optional)

### Quick Setup

```bash
# Clone repository
cd "C:\Users\suman\Downloads\OLD_PROJECT\SIH PROJECT"

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your keys
python app.py

# Frontend setup (new terminal)
cd frontend
npm install
copy .env.example .env
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

**Default Login:**
- Username: `admin`
- Password: `Admin@123`

⚠️ **Change default password immediately!**

---

## 🐳 Docker Deployment

### Run with Docker Compose (All Services)

```bash
# From project root directory
docker-compose up --build
```

This starts:
- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **PostgreSQL Database**: localhost:5432

### Run Individual Services

```bash
# Backend only
docker-compose up backend

# Frontend only
docker-compose up frontend

# Database only
docker-compose up db
```

### Stop Services

```bash
docker-compose down

# With volume removal (deletes database)
docker-compose down -v
```

### Production Docker Deployment

```bash
# Copy production environment
copy .env.prod.example .env  # Windows
# Edit .env with production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose -f docker-compose.prod.yml down
```

**Production Stack Includes:**
- Flask backend with Gunicorn
- PostgreSQL database
- Redis (rate limiting)
- Nginx reverse proxy
- Health checks
- Persistent volumes

---

## 🚂 Railway Deployment (Backend)

Railway offers a free tier with $5/month credit (sufficient for small apps).

### Step 1: Prepare Your Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab
git remote add origin https://github.com/yourusername/railtrack-pro.git
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect the `backend` folder

### Step 3: Configure Railway

**Set Root Directory:**
```
backend
```

**Set Build Command:**
```
pip install -r requirements.txt
```

**Set Start Command:**
```
gunicorn --bind 0.0.0.0:$PORT app:app
```

### Step 4: Add PostgreSQL Database

1. In your Railway project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway automatically sets `DATABASE_URL` environment variable
3. Database is ready to use!

### Step 5: Configure Environment Variables

In Railway dashboard, add these variables:

```env
# Security Keys (GENERATE SECURE RANDOM VALUES)
SECRET_KEY=your-secure-random-key-here
JWT_SECRET_KEY=your-secure-jwt-key-here

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false

# CORS (add your frontend URL after deployment)
CORS_ORIGINS=https://your-frontend.vercel.app

# Rate Limiting
RATELIMIT_ENABLED=true
RATELIMIT_STORAGE_URL=redis://your-redis-url:6379/0

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

### Step 6: Deploy Frontend to Vercel

**Option A: Deploy as separate Railway service**

1. Create a new service from the same repo
2. Set **Root Directory** to `frontend`
3. Set **Build Command**: `npm run build`
4. Set **Start Command**: `npx serve -s build`
5. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```

**Option B: Use Vercel for frontend** (Recommended for free tier)

See [Vercel Deployment](#vercel-deployment-frontend) below.

### Step 7: Update CORS

Once frontend is deployed, update backend's `CORS_ORIGINS` to include frontend URL:

```env
CORS_ORIGINS=https://your-frontend.vercel.app
```

---

## 🎨 Vercel Deployment (Frontend)

Vercel offers free hosting for personal projects with automatic HTTPS and CDN.

### Step 1: Install Vercel CLI

```bash
npm i -g vercel
```

### Step 2: Configure Frontend

Edit `frontend/.env`:

```env
REACT_APP_API_URL=https://your-backend-url.railway.app
```

### Step 3: Deploy to Vercel

```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

### Step 4: Configure Environment Variables in Vercel

In Vercel dashboard:
1. Go to your project settings
2. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```

### Step 5: Update Build Settings

In Vercel dashboard:
- **Framework Preset**: Create React App
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### Step 6: Custom Domain (Optional)

1. Go to project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

---

## 🎭 Render Deployment

### Step 1: Create Account

Go to [render.com](https://render.com) and sign up.

### Step 2: Deploy Backend

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `railtrack-pro-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: **Free**

### Step 3: Add Database

1. Click **"New"** → **"PostgreSQL"**
2. Choose **Free** tier
3. Note the **Internal Database URL**

### Step 4: Configure Environment Variables

In Render dashboard, add:

```env
DATABASE_URL=<from PostgreSQL service>
SECRET_KEY=<generate secure key>
JWT_SECRET_KEY=<generate secure key>
FLASK_ENV=production
FLASK_DEBUG=false
CORS_ORIGINS=https://your-frontend.onrender.com
```

### Step 5: Deploy Frontend

1. Click **"New"** → **"Static Site"**
2. Connect your repository
3. Configure:
   - **Name**: `railtrack-pro-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

4. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```

### ⚠️ Note on Render Free Tier

- Web services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to wake up
- PostgreSQL free tier expires after 90 days
- Consider upgrading for production use

---

## 🌐 Alternative Free Hosting Options

### Vercel (Frontend) + Railway (Backend) - RECOMMENDED

**Best for:** Production-ready deployment with minimal cost

**Advantages:**
- Vercel: Free CDN, automatic HTTPS, fast global edge network
- Railway: $5/month credit, managed PostgreSQL, auto-scaling
- Easy to set up and maintain

### Netlify (Frontend) + Render (Backend)

**Best for:** Completely free deployment

**Netlify for Frontend:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
cd frontend
npm run build
netlify deploy --prod --dir=build
```

**Render for Backend:**
- Free web service (spins down after idle)
- Free PostgreSQL (90-day expiry)

### Fly.io (Full Stack)

**Best for:** Docker-based deployment

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
fly deploy
```

**Advantages:**
- Free allowance (3 shared-cpu-1x 256 VMs)
- Global deployment
- Docker-based

### Google Cloud Run

**Best for:** Scalable production deployment

```bash
# Build and push to Container Registry
docker build -t gcr.io/your-project/railtrack-pro:latest .
docker push gcr.io/your-project/railtrack-pro:latest

# Deploy to Cloud Run
gcloud run deploy railtrack-pro \
  --image gcr.io/your-project/railtrack-pro \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Advantages:**
- Auto-scaling
- Pay-per-use
- Free tier available

---

## ✅ Production Checklist

Before deploying to production:

### Security
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Change default admin password
- [ ] Configure CORS for your domain only
- [ ] Enable HTTPS/SSL
- [ ] Enable rate limiting
- [ ] Set secure cookie options
- [ ] Review security headers

### Database
- [ ] Set up PostgreSQL database
- [ ] Configure DATABASE_URL
- [ ] Run database migrations
- [ ] Set up database backups
- [ ] Test database connectivity

### Application
- [ ] Set FLASK_ENV=production
- [ ] Set FLASK_DEBUG=false
- [ ] Configure logging
- [ ] Test all API endpoints
- [ ] Test frontend-backend connection
- [ ] Test QR code generation
- [ ] Test QR scanner (requires HTTPS)
- [ ] Test authentication flow

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Configure alerts
- [ ] Set up performance monitoring

### Documentation
- [ ] Update API documentation
- [ ] Document deployment details
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures

---

## 🔧 Post-Deployment Tasks

### 1. Change Default Admin Password

**Via Frontend:**
1. Login with default credentials
2. Go to Profile page
3. Change password immediately

**Via API:**
```bash
curl -X PUT https://your-api-url.com/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"password": "YourNewSecure@Password123"}'
```

### 2. Seed Sample Data (Optional)

```bash
curl -X POST https://your-api-url.com/api/seed \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Test All Features

- [ ] User registration and login
- [ ] Create vendor
- [ ] Create track item
- [ ] Generate QR code
- [ ] Download QR code
- [ ] Scan QR code (camera access)
- [ ] View analytics
- [ ] Create inspection
- [ ] View vendor performance

### 4. Configure Monitoring

**Uptime Monitoring:**
- UptimeRobot (free): https://uptimerobot.com/
- Pingdom (paid): https://www.pingdom.com/

**Error Tracking:**
- Sentry (free tier): https://sentry.io/
- LogRocket (free tier): https://logrocket.com/

**Performance Monitoring:**
- New Relic (free tier): https://newrelic.com/
- Datadog (trial): https://www.datadoghq.com/

---

## 🆘 Troubleshooting

### Backend won't start

**Check logs:**
```bash
# Railway
railway logs

# Render
# View logs in dashboard

# Docker
docker-compose logs backend
```

**Common issues:**
- Missing environment variables
- Database connection failed
- Port binding issues

### Frontend can't connect to backend

**Check:**
- `REACT_APP_API_URL` is correct
- CORS settings on backend
- Backend is running
- Network/firewall rules

### Database connection errors

**Check:**
- Database service is running
- Connection string format is correct
- Credentials are correct
- Firewall/network rules allow connection

### Camera not working in scanner

**Requirements:**
- HTTPS is required for camera access
- Grant camera permissions in browser
- Test in different browser (Chrome, Firefox, Edge)
- Check camera is not used by another application

### Rate limiting issues

**Check:**
- Redis is running and accessible
- `RATELIMIT_STORAGE_URL` is correct
- Rate limit values are appropriate

---

## 📊 Free Tier Limits

| Platform | Free Tier | Limitations |
|----------|-----------|-------------|
| **Railway** | $5 credit/month | ~500 hours of usage |
| **Render** | Free web service | Spins down after 15 min idle, PostgreSQL expires after 90 days |
| **Vercel** | Free for personal | 100GB bandwidth/month |
| **Netlify** | Free tier | 100GB bandwidth/month |
| **Fly.io** | Free allowance | 3 shared-cpu-1x 256 VMs |
| **Google Cloud Run** | Free tier | 2 million requests/month |
| **Supabase** | Free PostgreSQL | 500MB database, 50MB file storage |
| **Neon** | Free PostgreSQL | 0.5 GB storage, 10 hours active time |

---

## 📞 Support

For issues:
1. Check platform-specific documentation
2. Review application logs
3. Verify environment variables
4. Test locally first
5. Check network connectivity

### Useful Commands

```bash
# View logs
docker-compose logs -f
railway logs
render logs

# Restart services
docker-compose restart
railway restart
render restart

# Check status
docker-compose ps
railway status
render status

# Access database
docker-compose exec db psql -U postgres -d vendors
railway run psql $DATABASE_URL
```

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🎯 Quick Deployment Commands

### Railway (Backend)
```bash
railway login
railway init
railway add postgres
railway up
```

### Vercel (Frontend)
```bash
vercel login
cd frontend
vercel --prod
```

### Docker (Full Stack)
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

---

**Happy Deploying! 🚂**

*Last Updated: March 2026*
*Version: 2.0.0*
