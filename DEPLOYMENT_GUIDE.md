# 🚀 Deployment Guide - NYC Motor Vehicle Collisions Dashboard

This guide covers deploying your Dash application to various platforms.

## ⚠️ Important Note
**Netlify** and **Vercel** are for static sites only. For a Python Dash app, use:
- **Railway** ⭐ (Recommended - easiest, $5/month free credits)
- **Render** (Free tier available)
- **Heroku** (Paid, $7+/month)

---

## 🚂 Option 1: Deploy to Railway (⭐ RECOMMENDED)

Railway is the easiest and fastest option for deploying Python apps.

### Prerequisites
- GitHub account
- Railway account (https://railway.app)

### Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Dash dashboard"
   git remote add origin https://github.com/YOUR_USERNAME/repo-name.git
   git branch -M main
   git push -u origin main
   ```

2. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

3. **Create New Project**
   - Click "Create New Project"
   - Select "Deploy from GitHub"
   - Authorize Railway
   - Select your repository

4. **Configure Environment**
   - Railway auto-detects Python projects
   - Click on your service
   - Go to "Settings" → "Service"
   - Make sure "Start Command" is set to: `gunicorn app:server`
   - Port will auto-set to 8000

5. **Add Environment Variables** (if needed)
   - Go to Variables tab
   - Add any secrets here

6. **Deploy**
   - Railway deploys automatically
   - Your app will be live at: `https://your-project-name.up.railway.app`

---

## 🎨 Option 2: Deploy to Render

Render is free-tier friendly with generous limits.

### Steps

1. **Push to GitHub** (same as Railway step 1)

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create New Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose the repository

4. **Configure Service**
   - **Name**: `nyc-crashes-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Free Plan**: Select (gives you free tier)

5. **Deploy**
   - Click "Create Web Service"
   - Render deploys automatically
   - Your app will be at: `https://nyc-crashes-dashboard.onrender.com`

---

## 🧙 Option 3: Deploy to Heroku

Heroku is reliable but requires a credit card (free tier ended).

### Steps

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows (download installer from https://devcenter.heroku.com/articles/heroku-cli)
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## 📋 File Requirements Checklist

Your deployment files:
- ✅ `requirements.txt` - All dependencies
- ✅ `Procfile` - How to run the app
- ✅ `runtime.txt` - Python version
- ✅ `app.py` - Main application file
- ✅ `integrated_crashes_for_app.csv` - Data file

---

## 🔧 Local Testing Before Deployment

Test that everything works locally first:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://127.0.0.1:8000
```

---

## ⚡ Performance Tips

1. **CSV File Size**: If your CSV grows large, consider:
   - Uploading to cloud storage (AWS S3, Google Cloud Storage)
   - Using a database (PostgreSQL) instead

2. **Free Tier Limits**: 
   - Railway: $5/month free credits
   - Render: Free tier sleeps after 15 min inactivity
   - Heroku: No free tier (minimum $7/month)

3. **Scale Up Later**:
   - All these platforms have paid tiers for production

---

## 🐛 Troubleshooting

### App crashes after deployment

```bash
# View logs (Railway)
# In dashboard → Service → Logs

# View logs (Render)
# In dashboard → Logs

# View logs (Heroku)
heroku logs --tail
```

### Common Issues

1. **Port Error**: Make sure you're not hardcoding port 8050. Dash auto-detects.

2. **CSV Not Found**: Ensure `integrated_crashes_for_app.csv` is in repo root

3. **Dependencies Missing**: Run `pip freeze > requirements.txt` to update

---

## 📱 After Deployment

Once deployed:
1. Share your live URL
2. Users can access from anywhere
3. No need to run locally
4. App runs 24/7 (on paid tier)

---

## 🎯 My Recommendation

**Use Railway** because:
- ✅ Easiest setup (GitHub connect)
- ✅ Auto-deploys on git push
- ✅ Free tier has $5/month credits
- ✅ Generous free limits
- ✅ Custom domain support
- ✅ No credit card for free tier
