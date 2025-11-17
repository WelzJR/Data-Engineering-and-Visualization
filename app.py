import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

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

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "20px"},
    children=[
        html.H1("NYC Motor Vehicle Collisions – Interactive Dashboard"),

        # Filters row
        html.Div(
            style={"display": "flex", "gap": "10px", "flexWrap": "wrap"},
            children=[
                html.Div([
                    html.Label("Borough"),
                    dcc.Dropdown(
                        id="filter-borough",
                        options=[{"label": b, "value": b} for b in borough_options],
                        value="All",
                        clearable=False,
                    ),
                ], style={"minWidth": "180px"}),

                html.Div([
                    html.Label("Year"),
                    dcc.Dropdown(
                        id="filter-year",
                        options=[{"label": str(y), "value": str(y)} for y in year_options],
                        value="All",
                        clearable=False,
                    ),
                ], style={"minWidth": "120px"}),

                html.Div([
                    html.Label("Contributing Factor (Vehicle 1)"),
                    dcc.Dropdown(
                        id="filter-factor",
                        options=[{"label": f, "value": f} for f in factor_options],
                        value="All",
                        clearable=True,
                    ),
                ], style={"minWidth": "260px"}),

                html.Div([
                    html.Label("Injury Severity"),
                    dcc.Dropdown(
                        id="filter-severity",
                        options=[{"label": s, "value": s} for s in severity_options],
                        value="All",
                        clearable=False,
                    ),
                ], style={"minWidth": "160px"}),
            ],
        ),

        html.Br(),

        # Search row + button
        html.Div(
            style={"display": "flex", "gap": "10px", "flexWrap": "wrap", "alignItems": "center"},
            children=[
                html.Div([
                    html.Label("Search mode (e.g. 'Brooklyn 2022 pedestrian')"),
                    dcc.Input(
                        id="search-query",
                        type="text",
                        placeholder="Type a search query…",
                        style={"width": "350px"},
                    ),
                ]),
                html.Button("Generate Report", id="btn-generate", n_clicks=0,
                            style={"height": "40px", "padding": "0 20px"}),
                html.Div(id="summary-text", style={"marginLeft": "10px", "fontWeight": "bold"}),
            ],
        ),

        html.Hr(),

        # Charts
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                dcc.Graph(id="chart-borough"),
                dcc.Graph(id="chart-time"),
                dcc.Graph(id="chart-severity"),
                dcc.Graph(id="chart-heatmap"),
            ],
        ),
    ],
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
        Output("summary-text", "children"),
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
        return empty_fig, empty_fig, empty_fig, empty_fig, "No data found for this selection."

    # Borough bar chart
    borough_count = d["BOROUGH"].value_counts().reset_index()
    borough_count.columns = ["BOROUGH", "COUNT"]
    fig_borough = px.bar(borough_count, x="BOROUGH", y="COUNT", title="Crashes by Borough")

    # Time line chart (by month in selected year or overall)
    d_time = d.copy()
    d_time["MONTH"] = d_time["CRASH_DATE"].dt.to_period("M").astype(str)
    monthly = d_time.groupby("MONTH")["NUMBER_OF_PERSONS_INJURED"].sum().reset_index()
    fig_time = px.line(monthly, x="MONTH", y="NUMBER_OF_PERSONS_INJURED",
                       title="Injured Persons Over Time")

    # Severity pie chart
    sev_count = d["SEVERITY"].value_counts().reset_index()
    sev_count.columns = ["SEVERITY", "COUNT"]
    fig_severity = px.pie(sev_count, values="COUNT", names="SEVERITY",
                          title="Crash Severity Distribution")

    # Hour vs Day heatmap
    if "HOUR" in d.columns:
        heat = d.groupby(["DAY_OF_WEEK", "HOUR"]).size().reset_index(name="COUNT")
        # order days
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heat["DAY_OF_WEEK"] = pd.Categorical(heat["DAY_OF_WEEK"], categories=day_order, ordered=True)
        heat = heat.sort_values(["DAY_OF_WEEK", "HOUR"])
        fig_heat = px.density_heatmap(
            heat,
            x="HOUR",
            y="DAY_OF_WEEK",
            z="COUNT",
            title="Crash Density by Hour and Day of Week",
            nbinsx=24
        )
    else:
        fig_heat = go.Figure()
        fig_heat.update_layout(
            title="No HOUR information available",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )

    # Summary text
    total_crashes = len(d)
    total_injured = d["NUMBER_OF_PERSONS_INJURED"].sum() if "NUMBER_OF_PERSONS_INJURED" in d.columns else 0
    total_killed = d["NUMBER_OF_PERSONS_KILLED"].sum() if "NUMBER_OF_PERSONS_KILLED" in d.columns else 0

    summary = f"Report generated on {total_crashes:,} crashes | Injured: {total_injured:,} | Fatalities: {total_killed:,}"

    return fig_borough, fig_time, fig_severity, fig_heat, summary

if __name__ == "__main__":
    app.run_server(debug=True)
