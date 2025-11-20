import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# =========================
# Load data
# =========================
df = pd.read_csv("integrated_crashes_for_app.csv", parse_dates=["CRASH_DATE"], low_memory=False)

# Ensure some columns exist
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

# =========================
# Helper: apply filters + search
# =========================
def apply_filters(data, borough, year, factor, severity, search_query):
    d = data.copy()

    if borough and borough != "All":
        d = d[d["BOROUGH"] == borough]

    if year and year != "All":
        d = d[d["YEAR"] == int(year)]

    if factor and factor != "All" and "CONTRIBUTING FACTOR VEHICLE 1" in d.columns:
        d = d[d["CONTRIBUTING FACTOR VEHICLE 1"] == factor]

    if severity and severity != "All" and "SEVERITY" in d.columns:
        d = d[d["SEVERITY"] == severity]

    # Simple search mode: look in BOROUGH, PERSON_TYPES, PERSON_INJURIES, factor
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

# =========================
# Dash app
# =========================
app = Dash(__name__)
server = app.server  # for deployment (gunicorn)

borough_options = ["All"] + sorted([b for b in df["BOROUGH"].dropna().unique() if b != "UNKNOWN"])
year_options = ["All"] + sorted(df["YEAR"].dropna().astype(int).unique().tolist())
factor_options = ["All"]
if "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
    factor_options += sorted(df["CONTRIBUTING FACTOR VEHICLE 1"].dropna().unique().tolist())
severity_options = ["All"] + sorted(df["SEVERITY"].dropna().unique().tolist())

# =========================
# Dash app
# =========================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for deployment (gunicorn)

borough_options = ["All"] + sorted([b for b in df["BOROUGH"].dropna().unique() if b != "UNKNOWN"])
year_options = ["All"] + sorted(df["YEAR"].dropna().astype(int).unique().tolist())
factor_options = ["All"]
if "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
    factor_options += sorted(df["CONTRIBUTING FACTOR VEHICLE 1"].dropna().unique().tolist())
severity_options = ["All"] + sorted(df["SEVERITY"].dropna().unique().tolist())

# Custom CSS for modern styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-color: #1f77b4;
                --danger-color: #d62728;
                --success-color: #2ca02c;
                --warning-color: #ff7f0e;
                --light-bg: #f8f9fa;
                --dark-text: #2c3e50;
                --border-color: #e0e0e0;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 0;
                margin: 0;
                color: var(--dark-text);
            }
            
            .navbar-top {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 15px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 0;
            }
            
            .navbar-top h1 {
                color: white;
                font-size: 28px;
                font-weight: 700;
                margin: 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .navbar-top p {
                color: rgba(255,255,255,0.9);
                font-size: 13px;
                margin: 5px 0 0 0;
            }
            
            .main-container {
                background: white;
                border-radius: 0;
                min-height: 100vh;
                padding: 40px;
                margin: 0;
            }
            
            .filter-section {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                border-left: 5px solid var(--primary-color);
            }
            
            .filter-section h5 {
                color: var(--dark-text);
                font-weight: 700;
                margin-bottom: 20px;
                font-size: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .filter-group {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .filter-item {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            .filter-item label {
                font-weight: 600;
                color: var(--dark-text);
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .filter-item .Select-control {
                border: 2px solid var(--border-color);
                border-radius: 6px;
                background: white;
                transition: all 0.3s ease;
            }
            
            .filter-item .Select-control:hover {
                border-color: var(--primary-color);
                box-shadow: 0 2px 8px rgba(31, 119, 180, 0.1);
            }
            
            .search-section {
                display: grid;
                grid-template-columns: 1fr auto;
                gap: 15px;
                align-items: flex-end;
                margin-top: 20px;
            }
            
            .search-input-wrapper {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            .search-input-wrapper label {
                font-weight: 600;
                color: var(--dark-text);
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .search-input-wrapper input {
                padding: 12px 16px;
                border: 2px solid var(--border-color);
                border-radius: 6px;
                font-size: 14px;
                transition: all 0.3s ease;
                background: white;
            }
            
            .search-input-wrapper input:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
            }
            
            .btn-generate {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-weight: 700;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            .btn-generate:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .btn-generate:active {
                transform: translateY(0);
            }
            
            .summary-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 25px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                display: flex;
                align-items: center;
                gap: 15px;
                min-height: 60px;
            }
            
            .summary-box .stat {
                display: flex;
                flex-direction: column;
                gap: 3px;
            }
            
            .summary-box .stat-label {
                font-size: 11px;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .summary-box .stat-value {
                font-size: 18px;
                font-weight: 700;
            }
            
            .divider {
                height: 1px;
                background: rgba(255,255,255,0.2);
                margin: 0 15px;
            }
            
            .charts-section {
                margin-top: 30px;
            }
            
            .charts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
                gap: 25px;
            }
            
            .chart-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                overflow: hidden;
                border: 1px solid var(--border-color);
                transition: all 0.3s ease;
            }
            
            .chart-card:hover {
                box-shadow: 0 8px 20px rgba(0,0,0,0.12);
                transform: translateY(-2px);
            }
            
            .chart-card .dash-graph {
                padding: 0;
            }
            
            .no-data {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 60px 20px;
                text-align: center;
                color: #999;
            }
            
            .no-data svg {
                font-size: 60px;
                margin-bottom: 20px;
                opacity: 0.5;
            }
            
            .no-data p {
                font-size: 16px;
                margin: 0;
            }
            
            /* Responsive Design */
            @media (max-width: 1024px) {
                .charts-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            @media (max-width: 768px) {
                .main-container {
                    padding: 20px;
                }
                
                .filter-section {
                    padding: 20px;
                }
                
                .filter-group {
                    grid-template-columns: 1fr;
                }
                
                .search-section {
                    grid-template-columns: 1fr;
                }
                
                .summary-box {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .divider {
                    height: 0;
                    margin: 10px 0;
                }
                
                .navbar-top h1 {
                    font-size: 22px;
                }
            }
            
            @media (max-width: 480px) {
                .main-container {
                    padding: 15px;
                }
                
                .filter-section {
                    padding: 15px;
                }
                
                .navbar-top h1 {
                    font-size: 18px;
                }
                
                .btn-generate {
                    padding: 10px 20px;
                    font-size: 12px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    style={"margin": "0", "padding": "0"},
    children=[
        # Header
        html.Div(
            className="navbar-top",
            children=[
                html.Div(
                    style={"maxWidth": "1400px", "margin": "0 auto", "paddingLeft": "40px"},
                    children=[
                        html.H1("📊 NYC Motor Vehicle Collisions"),
                        html.P("Interactive Dashboard - Explore and Analyze Crash Data"),
                    ]
                )
            ]
        ),
        
        # Main Container
        html.Div(
            className="main-container",
            style={"maxWidth": "1400px", "margin": "0 auto"},
            children=[
                # Filter Section
                html.Div(
                    className="filter-section",
                    children=[
                        html.H5("🎯 Filter & Search"),
                        
                        # Filter Group
                        html.Div(
                            className="filter-group",
                            children=[
                                html.Div(
                                    className="filter-item",
                                    children=[
                                        html.Label("Borough"),
                                        dcc.Dropdown(
                                            id="filter-borough",
                                            options=[{"label": b, "value": b} for b in borough_options],
                                            value="All",
                                            clearable=False,
                                            searchable=True,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="filter-item",
                                    children=[
                                        html.Label("Year"),
                                        dcc.Dropdown(
                                            id="filter-year",
                                            options=[{"label": str(y), "value": str(y)} for y in year_options],
                                            value="All",
                                            clearable=False,
                                            searchable=True,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="filter-item",
                                    children=[
                                        html.Label("Contributing Factor"),
                                        dcc.Dropdown(
                                            id="filter-factor",
                                            options=[{"label": f, "value": f} for f in factor_options],
                                            value="All",
                                            clearable=True,
                                            searchable=True,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="filter-item",
                                    children=[
                                        html.Label("Severity"),
                                        dcc.Dropdown(
                                            id="filter-severity",
                                            options=[{"label": s, "value": s} for s in severity_options],
                                            value="All",
                                            clearable=False,
                                            searchable=True,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        
                        # Search Row
                        html.Div(
                            className="search-section",
                            children=[
                                html.Div(
                                    className="search-input-wrapper",
                                    children=[
                                        html.Label("📝 Search Query (e.g., 'Brooklyn 2022 pedestrian')"),
                                        dcc.Input(
                                            id="search-query",
                                            type="text",
                                            placeholder="Type keywords to search across all fields…",
                                        ),
                                    ],
                                ),
                                html.Button(
                                    "🔍 Generate Report",
                                    id="btn-generate",
                                    n_clicks=0,
                                    className="btn-generate",
                                ),
                            ],
                        ),
                    ]
                ),
                
                # Summary Box
                html.Div(
                    id="summary-box",
                    className="summary-box",
                    style={"marginTop": "25px", "display": "none"},
                ),
                
                # Charts Section
                html.Div(
                    className="charts-section",
                    children=[
                        html.Div(
                            className="charts-grid",
                            children=[
                                html.Div(
                                    className="chart-card",
                                    children=[dcc.Graph(id="chart-borough")],
                                ),
                                html.Div(
                                    className="chart-card",
                                    children=[dcc.Graph(id="chart-time")],
                                ),
                                html.Div(
                                    className="chart-card",
                                    children=[dcc.Graph(id="chart-severity")],
                                ),
                                html.Div(
                                    className="chart-card",
                                    children=[dcc.Graph(id="chart-heatmap")],
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        ),
    ]
)

# =========================
# Callback: Generate Report button updates all visuals
# =========================
@app.callback(
    [
        Output("chart-borough", "figure"),
        Output("chart-time", "figure"),
        Output("chart-severity", "figure"),
        Output("chart-heatmap", "figure"),
        Output("summary-box", "children"),
        Output("summary-box", "style"),
    ],
    Input("btn-generate", "n_clicks"),
    [
        State("filter-borough", "value"),
        State("filter-year", "value"),
        State("filter-factor", "value"),
        State("filter-severity", "value"),
        State("search-query", "value"),
    ]
)
def update_report(n_clicks, borough, year, factor, severity, search_query):
    # Apply filters & search
    d = apply_filters(df, borough, year, factor, severity, search_query)

    if d.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data for selected filters",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )
        empty_summary = html.Div("❌ No data found for this selection.", style={"padding": "20px"})
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_summary, {"display": "block"}

    # Borough bar chart
    borough_count = d["BOROUGH"].value_counts().reset_index()
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
    fig_borough.update_layout(
        hovermode="x unified",
        title_font_size=16,
        font_size=12,
        margin=dict(l=50, r=50, t=50, b=50),
    )

    # Time line chart (by month in selected year or overall)
    d_time = d.copy()
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
    fig_time.update_layout(
        hovermode="x unified",
        title_font_size=16,
        font_size=12,
        margin=dict(l=50, r=50, t=50, b=50),
    )

    # Severity pie chart
    sev_count = d["SEVERITY"].value_counts().reset_index()
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
    fig_severity.update_layout(
        title_font_size=16,
        font_size=12,
        margin=dict(l=50, r=50, t=50, b=50),
    )

    # Hour vs Day heatmap
    if "HOUR" in d.columns:
        heat = d.groupby(["DAY_OF_WEEK", "HOUR"]).size().reset_index(name="COUNT")
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
        fig_heat.update_layout(
            title_font_size=16,
            font_size=12,
            margin=dict(l=50, r=50, t=50, b=50),
        )
    else:
        fig_heat = go.Figure()
        fig_heat.update_layout(
            title="No HOUR information available",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )

    # Summary statistics
    total_crashes = len(d)
    total_injured = int(d["NUMBER_OF_PERSONS_INJURED"].sum()) if "NUMBER_OF_PERSONS_INJURED" in d.columns else 0
    total_killed = int(d["NUMBER_OF_PERSONS_KILLED"].sum()) if "NUMBER_OF_PERSONS_KILLED" in d.columns else 0

    summary_content = html.Div(
        style={"display": "flex", "alignItems": "center", "justifyContent": "space-around", "width": "100%", "flexWrap": "wrap"},
        children=[
            html.Div(
                className="stat",
                children=[
                    html.Div(className="stat-label", children="Total Crashes"),
                    html.Div(className="stat-value", children=f"{total_crashes:,}"),
                ]
            ),
            html.Div(className="divider"),
            html.Div(
                className="stat",
                children=[
                    html.Div(className="stat-label", children="Injured"),
                    html.Div(className="stat-value", children=f"{total_injured:,}"),
                ]
            ),
            html.Div(className="divider"),
            html.Div(
                className="stat",
                children=[
                    html.Div(className="stat-label", children="Fatalities"),
                    html.Div(className="stat-value", children=f"{total_killed:,}"),
                ]
            ),
        ]
    )

    return fig_borough, fig_time, fig_severity, fig_heat, summary_content, {"display": "flex"}

if __name__ == "__main__":
    app.run(debug=True)
