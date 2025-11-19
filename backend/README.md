# Backend - NYC Crashes Dashboard API

Clean REST API built with Flask for serving crash data and generating reports.

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

API will be available at `http://localhost:5000`

### Endpoints

#### 1. Health Check
```bash
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2024-11-19T10:30:45.123456"
}
```

#### 2. Get Filter Options
```bash
GET /api/filters
```

Response:
```json
{
  "boroughs": ["All", "BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"],
  "years": ["All", "2012", "2013", ..., "2025"],
  "factors": ["All", "Driver Inattention/Distraction", "Turning Improperly", ...],
  "severities": ["All", "No Injury", "Injury", "Fatal"]
}
```

#### 3. Generate Report
```bash
POST /api/report
Content-Type: application/json

{
  "borough": "All",
  "year": "2023",
  "factor": "All",
  "severity": "Injury",
  "search_query": "Brooklyn"
}
```

Response:
```json
{
  "charts": {
    "borough": { "data": [...], "layout": {...} },
    "time": { "data": [...], "layout": {...} },
    "severity": { "data": [...], "layout": {...} },
    "heatmap": { "data": [...], "layout": {...} }
  },
  "summary": {
    "crashes": 1234,
    "injured": 567,
    "killed": 12
  }
}
```

## Deployment on Render

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Backend API for NYC crashes dashboard"
git remote add origin https://github.com/YOUR_USERNAME/repo.git
git push -u origin main
```

### Step 2: Create Render Account

- Go to https://render.com
- Sign up with GitHub

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repo

### Step 4: Configure Service

- **Name**: `nyc-crashes-backend`
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  cd backend && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  cd backend && gunicorn app:app
  ```
- **Plan**: Free
- Click "Create Web Service"

### Step 5: Get Backend URL

Once deployed, Render will give you a URL like:
```
https://nyc-crashes-backend.onrender.com
```

**Save this URL** - you'll need it for the frontend.

### Monitoring

Check logs in Render dashboard:
- Dashboard → nyc-crashes-backend → Logs

## Environment Variables

No environment variables needed for basic setup.

## File Structure

```
backend/
├── app.py                           # Main Flask application
├── requirements.txt                 # Python dependencies
├── Procfile                         # Gunicorn command for Render
├── runtime.txt                      # Python version
├── .gitignore                       # Git ignore rules
└── integrated_crashes_for_app.csv   # Data file
```

## Data File

Make sure `integrated_crashes_for_app.csv` is in the `backend/` directory.
This file should contain columns:
- CRASH_DATE
- CRASH_TIME
- BOROUGH
- LATITUDE, LONGITUDE
- NUMBER_OF_PERSONS_INJURED
- NUMBER_OF_PERSONS_KILLED
- CONTRIBUTING FACTOR VEHICLE 1
- PERSON_TYPES
- PERSON_INJURIES

## Troubleshooting

### Port already in use
```bash
# Change port in app.py
app.run(port=5001)
```

### CSV file not found
- Ensure `integrated_crashes_for_app.csv` is in `backend/` folder
- Check file permissions

### Module import errors
```bash
pip install --upgrade -r requirements.txt
```

### Gunicorn errors on Render
Check:
1. Build Command is correct: `cd backend && pip install -r requirements.txt`
2. Start Command is correct: `cd backend && gunicorn app:app`
3. Python files are in `backend/` directory

## Performance Tips

- Queries are instant for filters
- Chart generation takes 1-2 seconds for large datasets
- Data is cached in memory on app start
- Consider adding pagination for very large result sets

## Next Steps

1. Deploy backend on Render
2. Get the backend URL
3. Deploy frontend on Netlify (update URL in netlify.toml)
4. Test the full application
