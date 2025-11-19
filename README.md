# NYC Motor Vehicle Collisions Dashboard

## Architecture

This is a **full-stack application** with:
- **Backend**: Flask REST API (deployed on Render)
- **Frontend**: React + Vite (deployed on Netlify)

## Project Structure

```
.
├── backend/                 # Flask REST API
│   ├── app.py              # Main API server
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Render deployment config
│   ├── runtime.txt         # Python version
│   └── integrated_crashes_for_app.csv  # Data file
│
└── frontend/               # React + Vite
    ├── src/
    │   ├── App.jsx         # Main component
    │   ├── main.jsx        # Entry point
    │   └── index.css       # Styling
    ├── package.json        # Node dependencies
    ├── vite.config.js      # Vite configuration
    ├── netlify.toml        # Netlify deployment config
    └── index.html          # HTML template
```

## Local Development

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python app.py
# Backend runs at http://localhost:5000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:5173
```

The frontend will proxy API calls to the backend during development.

## Deployment

### Backend Deployment (Render)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/repo.git
   git push -u origin main
   ```

2. **Deploy Backend on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - **Settings:**
     - Name: `nyc-crashes-backend`
     - Environment: `Python 3`
     - Build Command: `cd backend && pip install -r requirements.txt`
     - Start Command: `cd backend && gunicorn app:app`
     - Root Directory: `/` (leave blank)
   - Select Free Plan
   - Click "Create Web Service"
   - Your backend will be at: `https://nyc-crashes-backend.onrender.com`

3. **Copy Backend URL**
   - Save this URL from Render's dashboard

### Frontend Deployment (Netlify)

1. **Update Environment Variable**
   - In `frontend/netlify.toml`, update `VITE_BACKEND_URL` to your Render backend URL:
     ```toml
     [env]
       VITE_BACKEND_URL = "https://your-backend.onrender.com"
     ```

2. **Deploy Frontend on Netlify**
   - Go to https://netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub
   - Select your repository
   - **Settings:**
     - Build Command: `cd frontend && npm install && npm run build`
     - Publish Directory: `frontend/dist`
   - Click "Deploy site"
   - Your frontend will be at: `https://your-site.netlify.app`

3. **Set Environment Variables in Netlify**
   - Go to Site Settings → Build & Deploy → Environment
   - Add: `VITE_BACKEND_URL = https://your-backend.onrender.com`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/filters` | Get available filter options |
| POST | `/api/report` | Generate report with filters |

### POST /api/report

**Request:**
```json
{
  "borough": "All",
  "year": "All",
  "factor": "All",
  "severity": "All",
  "search_query": ""
}
```

**Response:**
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

## Features

- ✅ Multi-filter dropdowns (Borough, Year, Factor, Severity)
- ✅ Text search across all fields
- ✅ Real-time chart generation
- ✅ Summary statistics
- ✅ Responsive design
- ✅ Fully deployed and scalable

## Technologies

**Backend:**
- Flask (Python web framework)
- Flask-CORS (Cross-origin requests)
- Pandas (Data processing)
- Plotly (Chart generation)
- Gunicorn (Production server)

**Frontend:**
- React 18 (UI library)
- Vite (Build tool)
- React Plotly (Interactive charts)
- Axios (HTTP client)
- CSS3 (Styling)

## Environment Variables

**Netlify (Frontend):**
- `VITE_BACKEND_URL`: Your Render backend URL

**Render (Backend):**
- No environment variables needed

## Troubleshooting

### Backend won't connect
- Check that `VITE_BACKEND_URL` is set correctly in Netlify
- Ensure backend is running and accessible
- Check Render logs for errors

### Charts not loading
- Clear browser cache
- Check browser console for errors
- Verify backend is returning valid chart data

### CSV file not found
- Ensure `integrated_crashes_for_app.csv` is in the `backend/` folder
- Check file permissions

## Future Improvements

- Add data caching to reduce API calls
- Implement user authentication
- Add export to CSV/PDF functionality
- Add date range filtering
- Implement data pagination for large datasets

---

**Questions?** Check the individual README files in `backend/` and `frontend/` folders.
NYC Motor Vehicle Collisions – Data Processing & Insights (Milestone 1)

This repository contains the work for Milestone 1 of the NYC Motor Vehicle Collisions project. It includes the complete workflow for loading, cleaning, integrating, and analyzing NYC crash data using Python and Google Colab. The processed dataset provides insights into temporal patterns, spatial distribution, crash severity, and contributing factors. This milestone also prepares the data foundation required for the interactive dashboard in Milestone 2.

Project Highlights:

Loading data from NYC Open Data (Crashes + Persons)

Pre-cleaning and handling missing values

Standardizing formats and extracting temporal features

Outlier detection and data validation

Aggregating persons data per collision

Integrating datasets into a single analytical table

Visualizing crash patterns (hour, day, borough)

Severity and contributing factor analysis

Research questions with coded answers

Setup Instructions:

Clone the repository using:
git clone https://github.com/
<your-username>/<your-repo>.git

(Optional) Install dependencies locally using:
pip install -r requirements.txt

Open the main notebook (Milestone1_DataProcessing.ipynb) in Google Colab, Jupyter Notebook, or VS Code.

Run all cells to reproduce the cleaning, integration, and analysis steps.

Running the Notebook in Google Colab:

Open Google Colab.

Click File → Upload notebook.

Select Milestone1_DataProcessing.ipynb.

Run all cells.

Deployment Instructions (for Milestone 2 Web App):
The web dashboard will be added in the next milestone. The deployment workflow will include:

Installing necessary web libraries such as Dash, Plotly, and Pandas.

Running the app locally using:
python app/app.py

Deploying to Render, Vercel, or Heroku:

Build command: pip install -r requirements.txt

Start command: gunicorn app:server

Team Members & Contributions:


[Ali Waleed] – Data Exploration , Data Cleaning  , pre and post Data Integration , Visualization.



Milestone 1 Deliverables Completed:

Dataset loading and initial exploration

Cleaning and preprocessing of crashes and persons tables

Extraction of hour, weekday, month features

Borough standardization

Outlier detection and validation

Persons aggregation and dataset integration

Visualizing patterns and severity

Answering research questions

Preparing dataset for dashboard use
