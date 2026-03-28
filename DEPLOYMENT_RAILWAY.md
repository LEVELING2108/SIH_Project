# ☁️ Phase 5: Deployment Guide - Railway.app (Recommended)

## Why Railway?
- ✅ Free tier ($5 credit/month)
- ✅ Easy PostgreSQL setup
- ✅ Auto-deploy from GitHub
- ✅ No credit card required for free tier
- ✅ Perfect for hackathons and prototypes

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All features tested locally
- [ ] No console errors
- [ ] Data persists correctly
- [ ] Password strength validation works
- [ ] Export features work (PDF/CSV)
- [ ] Git repository is up to date

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your GitHub Repository

```bash
# Commit all changes
git add .
git commit -m "Phase 3 complete - Security features added"
git push origin main
```

**Ensure `.gitignore` includes:**
```
.env
*.db
__pycache__/
node_modules/
venv/
instance/
```

---

### Step 2: Create Railway Account

1. Go to **https://railway.app**
2. Click **"Login"** → **"Sign in with GitHub"**
3. Authorize Railway
4. You'll get $5 free credit (no card needed)

---

### Step 3: Create PostgreSQL Database

1. Click **"New Project"**
2. Select **"New Database"** → **"PostgreSQL"**
3. Wait 30 seconds for provisioning
4. Click on the database service
5. Go to **"Connect"** tab
6. **Copy the connection string** (looks like: `postgresql://postgres:xxx@yyy.railway.app:5432/railway`)

---

### Step 4: Deploy Backend

1. In your Railway project, click **"New"** → **"GitHub Repo"**
2. Select your repository: `SIH PROJECT`
3. Railway will auto-detect it's a Python/Flask app

**Configure Service:**
- **Name**: `railtrack-backend`
- **Root Directory**: `backend`
- **Start Command**: `gunicorn app:app`

**Add Environment Variables:**
Click on your backend service → **"Variables"** → Add:

```bash
DATABASE_URL=<paste your PostgreSQL URL from Step 3>
SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_hex(32))">
JWT_SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_hex(32))">
CORS_ORIGINS=*
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
```

**Generate Secret Keys:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Example output: a3f8b2c1d4e5f6789012345678901234
```

**Deploy:**
- Railway will automatically build and deploy
- Wait for "Deployed" status (green checkmark)
- Click **"Generate Domain"** to get a public URL
- Note your URL: `https://railtrack-backend-xxx.railway.app`

---

### Step 5: Test Backend

1. Open your browser
2. Go to: `https://your-backend-url.railway.app/api/health`
3. You should see:
   ```json
   {
     "status": "healthy",
     "service": "QR Vendor Verification API",
     "timestamp": "..."
   }
   ```

---

### Step 6: Deploy Frontend

**Option A: Deploy to Vercel (Recommended)**

1. Go to **https://vercel.com**
2. Click **"Sign Up"** → **"Continue with GitHub"**
3. Click **"Import Project"**
4. Select your repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

**Add Environment Variable:**
```bash
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

6. Click **"Deploy"**
7. Wait for deployment to complete
8. You'll get a URL: `https://your-project.vercel.app`

**Option B: Deploy to Railway (All-in-One)**

1. In same Railway project, click **"New"** → **"GitHub Repo"**
2. Select your repository again
3. Configure:
   - **Name**: `railtrack-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s build`

**Add Environment Variable:**
```bash
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

4. Deploy!

---

### Step 7: Update CORS

Go back to Railway backend → **"Variables"**:

Update `CORS_ORIGINS` to include your frontend URL:
```bash
CORS_ORIGINS=https://your-project.vercel.app,https://yourdomain.com
```

Or use `*` for testing (not recommended for production):
```bash
CORS_ORIGINS=*
```

---

### Step 8: Test Complete Application

1. Open frontend URL: `https://your-project.vercel.app`
2. Login with:
   - **Username**: `admin`
   - **Password**: `Admin@123`
3. Test all features:
   - Add vendor ✅
   - Add track item ✅
   - Generate QR ✅
   - Export PDF/CSV ✅
   - Change password ✅

---

## 🔧 Troubleshooting

### Frontend Can't Connect to Backend

**Error**: "Network Error" or CORS error

**Solution**:
1. Check `REACT_APP_API_URL` in Vercel
2. Check `CORS_ORIGINS` in Railway backend
3. Rebuild frontend:
   ```bash
   cd frontend
   npm run build
   git add .
   git commit -m "Fix API URL"
   git push
   ```

### Backend Not Starting

**Check logs in Railway**:
1. Go to backend service
2. Click **"Deployments"**
3. Click latest deployment
4. View logs

**Common issues**:
- Missing `DATABASE_URL`
- Wrong `SECRET_KEY`
- PostgreSQL not provisioned

### Database Errors

**Solution**:
1. Check PostgreSQL is running (green status)
2. Verify `DATABASE_URL` is correct
3. Run migration in Railway:
   - Go to backend → **"Settings"**
   - Add to **"Start Command"**: `python migrate_postgres.py && gunicorn app:app`

---

## 💰 Railway Pricing

**Free Tier**:
- $5 credit/month
- 500 hours of runtime
- 1GB database
- Enough for prototype/testing

**Hobby Plan** ($5/month):
- $10 credit/month
- More resources
- Priority support

---

## 📊 Monitoring

### Railway Dashboard
- View CPU/Memory usage
- Check database size
- Monitor deployments
- View logs

### Enable Health Checks

Add to Railway backend service:
- **Healthcheck Path**: `/api/health`
- Railway will auto-restart if unhealthy

---

## 🔐 Production Security

After deployment:

1. **Change default admin password**:
   - Login as admin
   - Go to Profile
   - Change password

2. **Update CORS**:
   - Set specific domains (not `*`)
   - `CORS_ORIGINS=https://yourdomain.com`

3. **Enable HTTPS**:
   - Railway provides HTTPS automatically
   - Vercel provides HTTPS automatically

4. **Regular Backups**:
   - Export data regularly (CSV/PDF)
   - Consider automated backups

---

## 📱 Share Your App

Your app is now live! Share these URLs:

- **Frontend**: `https://your-project.vercel.app`
- **Backend API**: `https://your-backend-url.railway.app/api`
- **Health Check**: `https://your-backend-url.railway.app/api/health`

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Test with real users
2. ✅ Monitor performance
3. ✅ Collect feedback
4. ✅ Implement Phase 6 features (optional)

---

## 🆘 Need Help?

**Railway Support**:
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

**Vercel Support**:
- Docs: https://vercel.com/docs

**Check Logs**:
- Railway: Service → Deployments → View Logs
- Vercel: Project → Activity

---

**Deployment Status**: Ready to Deploy! 🚀
