import './App.css'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Plot from 'react-plotly.js'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'

export default function App() {
  const [filters, setFilters] = useState({
    borough: 'All',
    year: 'All',
    factor: 'All',
    severity: 'All',
    search_query: ''
  })

  const [filterOptions, setFilterOptions] = useState({
    boroughs: [],
    years: [],
    factors: [],
    severities: []
  })

  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Fetch filter options on mount
  useEffect(() => {
    fetchFilterOptions()
  }, [])

  const fetchFilterOptions = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/filters`)
      setFilterOptions(response.data)
    } catch (err) {
      console.error('Failed to fetch filter options:', err)
      setError('Failed to load filter options')
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleGenerateReport = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${BACKEND_URL}/api/report`, filters)
      setReport(response.data)
    } catch (err) {
      console.error('Failed to generate report:', err)
      setError('Failed to generate report. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <div className="navbar">
        <div className="navbar-content">
          <h1>📊 NYC Motor Vehicle Collisions</h1>
          <p>Interactive Dashboard - Explore and Analyze Crash Data</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container">
        {/* Filter Section */}
        <div className="filter-section">
          <h2>🎯 Filter & Search</h2>

          <div className="filter-group">
            <div className="filter-item">
              <label>Borough</label>
              <select
                value={filters.borough}
                onChange={(e) => handleFilterChange('borough', e.target.value)}
              >
                {filterOptions.boroughs.map((b) => (
                  <option key={b} value={b}>{b}</option>
                ))}
              </select>
            </div>

            <div className="filter-item">
              <label>Year</label>
              <select
                value={filters.year}
                onChange={(e) => handleFilterChange('year', e.target.value)}
              >
                {filterOptions.years.map((y) => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </div>

            <div className="filter-item">
              <label>Contributing Factor</label>
              <select
                value={filters.factor}
                onChange={(e) => handleFilterChange('factor', e.target.value)}
              >
                {filterOptions.factors.map((f) => (
                  <option key={f} value={f}>{f}</option>
                ))}
              </select>
            </div>

            <div className="filter-item">
              <label>Severity</label>
              <select
                value={filters.severity}
                onChange={(e) => handleFilterChange('severity', e.target.value)}
              >
                {filterOptions.severities.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="search-section">
            <div className="search-input-wrapper">
              <label>📝 Search Query</label>
              <input
                type="text"
                placeholder="e.g., 'Brooklyn 2022 pedestrian'"
                value={filters.search_query}
                onChange={(e) => handleFilterChange('search_query', e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleGenerateReport()}
              />
            </div>
            <button
              className="btn-generate"
              onClick={handleGenerateReport}
              disabled={loading}
            >
              {loading ? '⏳ Generating...' : '🔍 Generate Report'}
            </button>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        {/* Summary Box */}
        {report && report.summary && (
          <div className="summary-box">
            <div className="stat">
              <div className="stat-label">Total Crashes</div>
              <div className="stat-value">{report.summary.crashes.toLocaleString()}</div>
            </div>
            <div className="divider"></div>
            <div className="stat">
              <div className="stat-label">Injured</div>
              <div className="stat-value">{report.summary.injured.toLocaleString()}</div>
            </div>
            <div className="divider"></div>
            <div className="stat">
              <div className="stat-label">Fatalities</div>
              <div className="stat-value">{report.summary.killed.toLocaleString()}</div>
            </div>
          </div>
        )}

        {/* Charts */}
        {report && report.charts && (
          <div className="charts-grid">
            <div className="chart-card">
              <Plot
                data={report.charts.borough.data}
                layout={{...report.charts.borough.layout, height: 400}}
                config={{ responsive: true }}
              />
            </div>
            <div className="chart-card">
              <Plot
                data={report.charts.time.data}
                layout={{...report.charts.time.layout, height: 400}}
                config={{ responsive: true }}
              />
            </div>
            <div className="chart-card">
              <Plot
                data={report.charts.severity.data}
                layout={{...report.charts.severity.layout, height: 400}}
                config={{ responsive: true }}
              />
            </div>
            <div className="chart-card">
              <Plot
                data={report.charts.heatmap.data}
                layout={{...report.charts.heatmap.layout, height: 400}}
                config={{ responsive: true }}
              />
            </div>
          </div>
        )}

        {!report && !loading && (
          <div className="welcome-message">
            <p>👋 Welcome! Select filters and click "Generate Report" to see the data.</p>
          </div>
        )}
      </div>
    </div>
  )
}
