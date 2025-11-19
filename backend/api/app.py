from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Load data with multiple path attempts
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "integrated_crashes_for_app.csv"),
        os.path.join(os.path.dirname(__file__), "..", "integrated_crashes_for_app.csv"),
        os.path.join(os.path.dirname(__file__), "../..", "integrated_crashes_for_app.csv"),
        "/var/task/integrated_crashes_for_app.csv",
        "integrated_crashes_for_app.csv"
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            print(f"✓ Loaded CSV from: {csv_path}")
            break
    
    if csv_path is None:
        raise FileNotFoundError(f"CSV file not found. Tried: {possible_paths}")
    
    df = pd.read_csv(csv_path, parse_dates=["CRASH_DATE"], low_memory=False)
    return df

try:
    df = load_data()
except Exception as e:
    print(f"Error loading data: {e}")
    df = None

# Ensure columns exist
if df is not None:
    if "BOROUGH" not in df.columns:
        df["BOROUGH"] = "UNKNOWN"

    if "YEAR" not in df.columns:
        df["YEAR"] = df["CRASH_DATE"].dt.year

    if "HOUR" not in df.columns and "CRASH_TIME" in df.columns:
        df["HOUR"] = pd.to_datetime(df["CRASH_TIME"], format="%H:%M", errors="coerce").dt.hour

    if "DAY_OF_WEEK" not in df.columns:
        df["DAY_OF_WEEK"] = df["CRASH_DATE"].dt.day_name()

    if "SEVERITY" not in df.columns:
        def classify_severity(row):
            if row.get("NUMBER_OF_PERSONS_KILLED", 0) > 0:
                return "Fatal"
            elif row.get("NUMBER_OF_PERSONS_INJURED", 0) > 0:
                return "Injury"
            else:
                return "No Injury"
        df["SEVERITY"] = df.apply(classify_severity, axis=1)

# Helper function to apply filters
def apply_filters(data, borough=None, year=None, factor=None, severity=None, search_query=None):
    d = data.copy()

    if borough and borough != "All":
        d = d[d["BOROUGH"] == borough]

    if year and year != "All":
        d = d[d["YEAR"] == int(year)]

    if factor and factor != "All" and "CONTRIBUTING FACTOR VEHICLE 1" in d.columns:
        d = d[d["CONTRIBUTING FACTOR VEHICLE 1"] == factor]

    if severity and severity != "All" and "SEVERITY" in d.columns:
        d = d[d["SEVERITY"] == severity]

    if search_query and search_query.strip():
        q = search_query.strip().lower()
        mask = (
            d["BOROUGH"].fillna("").str.lower().str.contains(q)
            | d.get("PERSON_TYPES", pd.Series("", index=d.index)).fillna("").str.lower().str.contains(q)
            | d.get("PERSON_INJURIES", pd.Series("", index=d.index)).fillna("").str.lower().str.contains(q)
            | d.get("CONTRIBUTING FACTOR VEHICLE 1", pd.Series("", index=d.index)).fillna("").str.lower().str.contains(q)
            | d["YEAR"].astype(str).str.contains(q)
        )
        d = d[mask]

    return d

# ========================
# API Routes
# ========================

@app.route('/api/filters', methods=['GET'])
def get_filters():
    """Get available filter options"""
    if df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    borough_options = ["All"] + sorted([b for b in df["BOROUGH"].dropna().unique() if b != "UNKNOWN"])
    year_options = ["All"] + sorted(df["YEAR"].dropna().astype(int).unique().tolist())
    factor_options = ["All"]
    if "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
        factor_options += sorted(df["CONTRIBUTING FACTOR VEHICLE 1"].dropna().unique().tolist())
    severity_options = ["All"] + sorted(df["SEVERITY"].dropna().unique().tolist())

    return jsonify({
        "boroughs": borough_options,
        "years": [str(y) for y in year_options],
        "factors": factor_options,
        "severities": severity_options
    })

@app.route('/api/report', methods=['POST'])
def generate_report():
    """Generate report with filters and charts"""
    if df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    data = request.json
    borough = data.get("borough", "All")
    year = data.get("year", "All")
    factor = data.get("factor", "All")
    severity = data.get("severity", "All")
    search_query = data.get("search_query", "")

    # Apply filters
    filtered_df = apply_filters(df, borough, year, factor, severity, search_query)

    if filtered_df.empty:
        return jsonify({
            "error": "No data found for selected filters",
            "charts": {},
            "summary": {"crashes": 0, "injured": 0, "killed": 0}
        }), 200

    # Borough bar chart
    borough_count = filtered_df["BOROUGH"].value_counts().reset_index()
    borough_count.columns = ["BOROUGH", "COUNT"]
    fig_borough = px.bar(
        borough_count,
        x="BOROUGH",
        y="COUNT",
        title="Crashes by Borough",
        color="COUNT",
        color_continuous_scale="Viridis",
        labels={"COUNT": "Number of Crashes"}
    )
    fig_borough.update_layout(hovermode="x unified", showlegend=False, height=400)

    # Time line chart
    d_time = filtered_df.copy()
    d_time["MONTH"] = d_time["CRASH_DATE"].dt.to_period("M").astype(str)
    monthly = d_time.groupby("MONTH")["NUMBER_OF_PERSONS_INJURED"].sum().reset_index()
    fig_time = px.line(
        monthly,
        x="MONTH",
        y="NUMBER_OF_PERSONS_INJURED",
        title="Injured Persons Over Time",
        markers=True,
        labels={"NUMBER_OF_PERSONS_INJURED": "Total Injured"}
    )
    fig_time.update_traces(line=dict(color="#667eea", width=3), marker=dict(size=8))
    fig_time.update_layout(hovermode="x unified", height=400)

    # Severity pie chart
    sev_count = filtered_df["SEVERITY"].value_counts().reset_index()
    sev_count.columns = ["SEVERITY", "COUNT"]
    fig_severity = px.pie(
        sev_count,
        values="COUNT",
        names="SEVERITY",
        title="Crash Severity Distribution",
        color_discrete_map={
            "Fatal": "#d62728",
            "Injury": "#ff7f0e",
            "No Injury": "#2ca02c"
        }
    )
    fig_severity.update_layout(height=400)

    # Hour vs Day heatmap
    if "HOUR" in filtered_df.columns:
        heat = filtered_df.groupby(["DAY_OF_WEEK", "HOUR"]).size().reset_index(name="COUNT")
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heat["DAY_OF_WEEK"] = pd.Categorical(heat["DAY_OF_WEEK"], categories=day_order, ordered=True)
        heat = heat.sort_values(["DAY_OF_WEEK", "HOUR"])
        fig_heat = px.density_heatmap(
            heat,
            x="HOUR",
            y="DAY_OF_WEEK",
            z="COUNT",
            title="Crash Density by Hour and Day",
            nbinsx=24,
            color_continuous_scale="RdYlBu_r",
            labels={"COUNT": "Crash Count"}
        )
        fig_heat.update_layout(height=400)
    else:
        fig_heat = go.Figure()
        fig_heat.update_layout(title="No HOUR information available")

    # Summary stats
    total_crashes = len(filtered_df)
    total_injured = int(filtered_df["NUMBER_OF_PERSONS_INJURED"].sum()) if "NUMBER_OF_PERSONS_INJURED" in filtered_df.columns else 0
    total_killed = int(filtered_df["NUMBER_OF_PERSONS_KILLED"].sum()) if "NUMBER_OF_PERSONS_KILLED" in filtered_df.columns else 0

    return jsonify({
        "charts": {
            "borough": json.loads(fig_borough.to_json()),
            "time": json.loads(fig_time.to_json()),
            "severity": json.loads(fig_severity.to_json()),
            "heatmap": json.loads(fig_heat.to_json())
        },
        "summary": {
            "crashes": total_crashes,
            "injured": total_injured,
            "killed": total_killed
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = "ok" if df is not None else "error"
    return jsonify({
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "data_loaded": df is not None
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "name": "NYC Motor Vehicle Collisions API",
        "version": "1.0.0",
        "endpoints": {
            "/api/health": "Health check",
            "/api/filters": "Get available filter options",
            "/api/report": "Generate report with charts (POST)"
        }
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
