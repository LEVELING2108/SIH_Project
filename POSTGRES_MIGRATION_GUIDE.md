# 🗄️ PostgreSQL Migration Guide

## Overview
This guide covers migrating from SQLite to PostgreSQL for production deployment.

---

## Option 1: Local PostgreSQL (For Testing)

### Step 1: Install PostgreSQL

**Windows:**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer (use default settings)
3. Remember your postgres password
4. PostgreSQL will run on port 5432

**Verify Installation:**
```bash
psql --version
```

### Step 2: Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database (in psql prompt)
CREATE DATABASE railtrack_pro;

# Create user (optional, for development)
CREATE USER railtrack_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE railtrack_pro TO railtrack_user;

# Exit
\q
```

### Step 3: Update Backend Configuration

**Create `.env` file in `backend/` folder:**
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# PostgreSQL Connection String
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/railtrack_pro

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Server Port
PORT=5000
```

### Step 4: Install PostgreSQL Driver

```bash
cd backend
venv\Scripts\activate
pip install psycopg2-binary==2.9.9
```

### Step 5: Run Migration

```bash
python migrate_postgres.py
```

### Step 6: Start Backend

```bash
python app.py
```

---

## Option 2: Railway Deployment (Recommended - Easiest)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Free tier: $5 credit/month (enough for testing)

### Step 2: Create PostgreSQL Database

1. Click "New Project"
2. Select "New Database" → "PostgreSQL"
3. Wait for database to provision
4. Click on database → "Connect" → Copy connection string

### Step 3: Deploy Backend

1. In Railway project, click "New" → "GitHub Repo"
5. Connect your GitHub repository
6. Add environment variables:
   ```
   DATABASE_URL=<paste your Railway PostgreSQL URL>
   SECRET_KEY=<generate random string>
   JWT_SECRET_KEY=<generate random string>
   CORS_ORIGINS=<your frontend URL>
   FLASK_ENV=production
   FLASK_DEBUG=false
   ```
7. Railway auto-deploys!

### Step 4: Deploy Frontend

**Option A: Vercel (Recommended)**
1. Go to https://vercel.com
2. Import your GitHub repo
3. Set root directory to `frontend`
4. Add environment variable:
   ```
   REACT_APP_API_URL=<your Railway backend URL>/api
   ```
5. Deploy!

**Option B: Railway Static Site**
1. In same Railway project, click "New" → "Empty Service"
2. Connect GitHub repo
3. Set root directory to `frontend`
4. Build command: `npm run build`
5. Start command: `npx serve -s build`
6. Add environment variable:
   ```
   REACT_APP_API_URL=<your Railway backend URL>/api
   ```

---

## Option 3: Render.com Deployment

### Step 1: Create Account
1. Go to https://render.com
2. Sign up with GitHub
3. Free tier available

### Step 2: Create PostgreSQL
1. Click "New" → "PostgreSQL"
2. Choose free tier
3. Note the connection string

### Step 3: Deploy Backend
1. Click "New" → "Web Service"
2. Connect GitHub repo
3. Configure:
   - **Name**: railtrack-pro-backend
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add environment variables:
   ```
   DATABASE_URL=<Render PostgreSQL URL>
   SECRET_KEY=<random string>
   JWT_SECRET_KEY=<random string>
   CORS_ORIGINS=<frontend URL>
   ```

### Step 4: Deploy Frontend
1. Click "New" → "Static Site"
2. Connect GitHub repo
3. Configure:
   - **Name**: railtrack-pro-frontend
   - **Root Directory**: frontend
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: build
4. Add environment variable:
   ```
   REACT_APP_API_URL=<backend URL>/api
   ```

---

## Database Migration Script

The `migrate_postgres.py` script will:
1. Create all tables
2. Create default admin user
3. Migrate existing data (if any)

```bash
python migrate_postgres.py
```

---

## Environment Variables Reference

### Backend (.env)
```env
# Required
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-min-32-characters
JWT_SECRET_KEY=your-jwt-secret-key

# Optional
FLASK_ENV=production
FLASK_DEBUG=false
CORS_ORIGINS=https://yourdomain.com
PORT=5000
```

### Frontend (.env)
```env
# Required
REACT_APP_API_URL=https://your-backend-url.com/api

# Optional
PORT=3000
```

---

## Testing Before Deployment

1. **Update backend .env** to use PostgreSQL
2. **Run migration**: `python migrate_postgres.py`
3. **Start backend**: `python app.py`
4. **Test login**: http://localhost:3000
5. **Verify data persistence**

---

## Troubleshooting

### Connection Errors
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check firewall settings

### Migration Fails
- Drop database and recreate
- Check user permissions
- Review error logs

### Frontend Can't Connect
- Verify REACT_APP_API_URL
- Check CORS_ORIGINS in backend
- Ensure backend is running

---

## Next Steps

After successful migration:
1. ✅ Test all features
2. ✅ Verify data persistence
3. ✅ Test with multiple users
4. ✅ Proceed to Phase 5 (Deployment)

---

**Need help?** Check the error messages and logs for details!
