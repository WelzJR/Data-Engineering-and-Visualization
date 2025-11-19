🚂 RAILWAY + NETLIFY DEPLOYMENT GUIDE
═══════════════════════════════════════════════════════════════

## ⏱️ TOTAL TIME: 20 MINUTES

### Step 1: Push to GitHub (3 min)
```bash
git add .
git commit -m "Full-stack app ready for deployment"
git push -u origin main
```

### Step 2: Deploy Backend on Railway (5 min)

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway with GitHub
5. Select your repository
6. Railway auto-detects Python ✓
7. It deploys automatically!
8. Wait for deployment (2-3 min)
9. Click your service → Settings → Domains
10. Copy your backend URL (e.g., https://your-app.railway.app)

✅ Backend is live!

### Step 3: Deploy Frontend on Netlify (5 min)

1. Go to https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub → Authorize
4. Select your repository
5. Configure:
   - Build: cd frontend && npm install && npm run build
   - Publish: frontend/dist
6. Click "Deploy site"
7. Wait for build (2-3 min)
8. Copy frontend URL (e.g., https://your-site.netlify.app)

✅ Frontend is live!

### Step 4: Connect Backend URL (5 min)

1. In Netlify, go to Site settings → Build & deploy → Environment
2. Click "Add variables"
3. Add:
   - Key: VITE_BACKEND_URL
   - Value: https://your-app.railway.app (your Railway backend URL)
4. Click "Save"
5. Go to Deploys → Trigger deploy → Deploy site
6. Wait for rebuild (1-2 min)

✅ Frontend connected to backend!

### Step 5: Test Everything (2 min)

Test backend health:
```bash
curl https://your-app.railway.app/api/health
```

Expected response:
```json
{"status": "ok", "timestamp": "..."}
```

Open frontend in browser:
```
https://your-site.netlify.app
```

Click "Generate Report" and verify charts load.

✅ Everything works!

═══════════════════════════════════════════════════════════════

## 🎯 YOUR URLS AFTER DEPLOYMENT

Frontend (React UI):
  → https://your-site.netlify.app

Backend (Flask API):
  → https://your-app.railway.app

API Endpoints:
  → https://your-app.railway.app/api/health
  → https://your-app.railway.app/api/filters
  → https://your-app.railway.app/api/report

═══════════════════════════════════════════════════════════════

## 💰 COSTS

Railway Free Tier:
  ✓ $5/month free credits
  ✓ Usually covers small apps completely
  ✓ No card required to start

Netlify Free Tier:
  ✓ $0/month
  ✓ 300 build minutes/month
  ✓ Unlimited deployments

GitHub:
  ✓ $0/month

TOTAL: $0/month (or very cheap if you use Railway credits)

═══════════════════════════════════════════════════════════════

## ✨ AUTO-DEPLOYMENT

After setup, just push code and it auto-deploys!

```bash
# Make changes locally
# Push to GitHub
git add .
git commit -m "New feature"
git push

# Railway auto-deploys backend (2-3 min)
# Netlify auto-deploys frontend (2-3 min)
# Your app is live with new code!
```

═══════════════════════════════════════════════════════════════

## 🔧 RAILWAY SPECIFIC TIPS

1. Monitor Backend Logs:
   - Railway dashboard → Your service → Logs
   - See any errors in real-time

2. Environment Variables:
   - Railway → Service → Variables
   - Add any secrets here

3. Restart Service:
   - Railway → Service → Settings → Restart

4. View Deployment History:
   - Railway → Deployments
   - Rollback if needed

═══════════════════════════════════════════════════════════════

## 🆘 TROUBLESHOOTING

Issue: Frontend shows "Cannot reach backend"
Fix:
  1. Check VITE_BACKEND_URL in Netlify environment vars
  2. Verify it matches your Railway URL exactly
  3. Check Railway logs for errors
  4. Trigger new Netlify deploy

Issue: Railway deployment fails
Fix:
  1. Check Railway logs (red errors)
  2. Verify backend/requirements.txt exists
  3. Verify Procfile is correct
  4. Try restarting service

Issue: Charts don't load
Fix:
  1. Check browser console (F12)
  2. Check Railway backend logs
  3. Verify CSV file is in backend/ folder
  4. Test /api/filters endpoint directly

═══════════════════════════════════════════════════════════════

## 📋 QUICK CHECKLIST

Before deploying:
  ☐ Code pushed to GitHub main branch
  ☐ backend/app.py works locally
  ☐ frontend builds locally (npm run build)
  ☐ CSV file in backend/ folder

After Railway deploys:
  ☐ Backend URL copied
  ☐ /api/health endpoint works
  ☐ /api/filters endpoint works

After Netlify deploys:
  ☐ VITE_BACKEND_URL set
  ☐ Frontend build successful
  ☐ Page loads in browser
  ☐ Filters work
  ☐ Charts load

═══════════════════════════════════════════════════════════════

## 🎉 YOU'RE DONE!

Your app is now:
  ✅ Deployed to Railway (backend)
  ✅ Deployed to Netlify (frontend)
  ✅ Auto-deploys on git push
  ✅ Accessible to anyone online
  ✅ Using free tier

Share your frontend URL and enjoy! 🚀

═══════════════════════════════════════════════════════════════
