# Complete Deployment Instructions

## Overview

This is a full-stack application:
- **Backend**: Flask REST API on Render
- **Frontend**: React + Vite on Netlify

## Architecture Diagram

```
User Browser
     ↓
Netlify (Frontend - React/Vite)
     ↓ (HTTP Requests)
Render (Backend - Flask API)
     ↓
Data (CSV in backend folder)
```

---

## Deployment Steps

### Phase 1: GitHub Setup (5 minutes)

#### 1.1 Create GitHub Repository

```bash
# Initialize git locally
git init
git add .
git commit -m "Initial commit - NYC crashes dashboard"

# Go to https://github.com/new
# Create new repository: nyc-crashes-dashboard
# Make it PUBLIC

# Connect local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/nyc-crashes-dashboard.git
git branch -M main
git push -u origin main
```

✅ **Result**: Your code is now on GitHub

---

### Phase 2: Backend Deployment on Render (10 minutes)

#### 2.1 Create Render Account

- Go to https://render.com
- Click "Sign up"
- Choose "Continue with GitHub"
- Authorize Render

#### 2.2 Create Web Service

1. Click "New +" → "Web Service"
2. Click "Connect account" (GitHub)
3. Authorize Render to access your repos
4. Select `nyc-crashes-dashboard` repository

#### 2.3 Configure Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `nyc-crashes-backend` |
| **Environment** | `Python 3` |
| **Build Command** | `cd backend && pip install -r requirements.txt` |
| **Start Command** | `cd backend && gunicorn app:app` |
| **Plan** | Free |

#### 2.4 Deploy

1. Scroll down and click "Create Web Service"
2. Wait for build to complete (~2-3 minutes)
3. You'll see a URL like: `https://nyc-crashes-backend.onrender.com`

✅ **Result**: Backend is live!

📌 **Save this URL** - You need it for the frontend

---

### Phase 3: Frontend Deployment on Netlify (10 minutes)

#### 3.1 Update Frontend Configuration

Update `frontend/netlify.toml`:

```toml
[env]
  VITE_BACKEND_URL = "https://nyc-crashes-backend.onrender.com"
```

Replace with your actual Render URL from Phase 2.

#### 3.2 Push Changes

```bash
git add frontend/netlify.toml
git commit -m "Update backend URL for production"
git push
```

#### 3.3 Create Netlify Account

- Go to https://netlify.com
- Click "Sign up"
- Choose "Continue with GitHub"
- Authorize Netlify

#### 3.4 Deploy Frontend

1. Click "Add new site" → "Import an existing project"
2. Click "GitHub"
3. Select your repository
4. Configure build settings:

| Field | Value |
|-------|-------|
| **Build Command** | `cd frontend && npm install && npm run build` |
| **Publish Directory** | `frontend/dist` |

5. Click "Deploy site"
6. Wait for build (~3-5 minutes)
7. You'll see a URL like: `https://nyc-crashes-dashboard.netlify.app`

✅ **Result**: Frontend is live!

---

### Phase 4: Verification (5 minutes)

#### 4.1 Test Backend

```bash
curl https://nyc-crashes-backend.onrender.com/api/health
```

Expected response:
```json
{"status": "ok", "timestamp": "..."}
```

#### 4.2 Test Frontend

Open in browser:
```
https://nyc-crashes-dashboard.netlify.app
```

Expected: Dashboard loads with filters and charts work when you click "Generate Report"

#### 4.3 Check Logs

**Render Logs:**
- Dashboard → nyc-crashes-backend → Logs

**Netlify Logs:**
- Site settings → Builds & deploy → Deploys → Click latest build → Logs

---

## Troubleshooting

### Frontend shows "Failed to load filter options"

**Problem**: Frontend can't reach backend

**Solution**:
1. Check `VITE_BACKEND_URL` in `frontend/netlify.toml`
2. Verify it matches your Render URL
3. Trigger new Netlify deploy: Site settings → Builds & deploy → Deploys → "Trigger deploy"

### Render backend builds fail

**Problem**: Build error in Render

**Solution**:
1. Check Render logs
2. Ensure `cd backend &&` is in Build Command
3. Verify files are in `backend/` folder:
   - `app.py`
   - `requirements.txt`
   - `integrated_crashes_for_app.csv`

### Charts don't load after filtering

**Problem**: Backend returns error

**Solution**:
1. Check Render logs for Python errors
2. Verify CSV file is in `backend/` folder
3. Restart service: Render dashboard → Settings → Restart service

### API works locally but not after deployment

**Problem**: Environment variables or paths

**Solution**:
1. Verify paths are relative (not absolute)
2. Check environment variables in deployment settings
3. Test with `curl` directly to backend

---

## Environment Variables

### Render (Backend)

No environment variables needed for basic setup.

### Netlify (Frontend)

Set in Site settings → Build & deploy → Environment:

| Key | Value |
|-----|-------|
| `VITE_BACKEND_URL` | `https://your-backend.onrender.com` |

---

## Performance Notes

### Render Free Tier

- ✅ Free hosting
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request takes ~30 seconds after spin-down
- 💰 Upgrade for always-on: $7/month

### Netlify Free Tier

- ✅ Free hosting
- ✅ No spin-down (always fast)
- ✅ 300 build minutes/month
- 💰 Upgrade for more builds: $19/month

---

## Auto-Deployment

Both platforms auto-deploy when you push to GitHub:

1. Push code to `main` branch
2. Render/Netlify detects change
3. Auto-builds and deploys
4. You get a new live version

```bash
# Any code changes
git add .
git commit -m "Feature update"
git push  # → Auto-deploys!
```

---

## File Checklist

### Backend Files

- ✅ `backend/app.py`
- ✅ `backend/requirements.txt`
- ✅ `backend/Procfile`
- ✅ `backend/runtime.txt`
- ✅ `backend/integrated_crashes_for_app.csv`
- ✅ `backend/.gitignore`

### Frontend Files

- ✅ `frontend/src/App.jsx`
- ✅ `frontend/src/main.jsx`
- ✅ `frontend/src/index.css`
- ✅ `frontend/package.json`
- ✅ `frontend/vite.config.js`
- ✅ `frontend/index.html`
- ✅ `frontend/netlify.toml`
- ✅ `frontend/.gitignore`

---

## Next Steps

1. **Monitor**: Check Render & Netlify dashboards regularly
2. **Share**: Give your frontend URL to users
3. **Iterate**: Push code changes for auto-deployment
4. **Scale**: Upgrade to paid plans if needed
5. **Add Features**: Implement more functionality

---

## Support Links

- 📘 [Render Docs](https://render.com/docs)
- 📗 [Netlify Docs](https://docs.netlify.com)
- 📙 [Flask Docs](https://flask.palletsprojects.com)
- 📕 [React Docs](https://react.dev)

---

## Quick Links

Once deployed:

| Service | URL Pattern |
|---------|------------|
| Backend Dashboard | https://dashboard.render.com |
| Frontend Dashboard | https://app.netlify.com |
| Your Dashboard | https://your-site.netlify.app |
| API Health | https://your-backend.onrender.com/api/health |

---

**Congratulations!** Your full-stack application is now deployed! 🎉
