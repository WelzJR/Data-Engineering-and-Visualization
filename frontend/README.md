# Frontend - NYC Crashes Dashboard UI

Modern React + Vite frontend for the NYC Motor Vehicle Collisions Dashboard.

## Quick Start

### Prerequisites
- Node.js 16+ (with npm)

### Installation

```bash
npm install
```

### Running Locally

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

During development, API calls proxy to `http://localhost:5000` (backend).

### Building for Production

```bash
npm run build
```

Output files are in `dist/` directory.

## Features

- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Real-time filtering (Borough, Year, Factor, Severity)
- ✅ Full-text search across all fields
- ✅ Interactive charts with Plotly
- ✅ Summary statistics
- ✅ Beautiful gradient UI
- ✅ Loading states and error handling

## Environment Variables

During development, create a `.env.local` file:

```env
VITE_BACKEND_URL=http://localhost:5000
```

For production (Netlify), set environment variable:

```env
VITE_BACKEND_URL=https://your-backend.onrender.com
```

## Deployment on Netlify

### Step 1: Push to GitHub (if not already done)

```bash
git init
git add .
git commit -m "Frontend for NYC crashes dashboard"
git remote add origin https://github.com/YOUR_USERNAME/repo.git
git push -u origin main
```

### Step 2: Create Netlify Account

- Go to https://netlify.com
- Sign up with GitHub

### Step 3: Add New Site

1. Click "Add new site" → "Import an existing project"
2. Select GitHub
3. Authorize Netlify to access your repos
4. Select your repository

### Step 4: Configure Build

- **Build Command**: 
  ```
  cd frontend && npm install && npm run build
  ```
- **Publish Directory**: `frontend/dist`
- Click "Deploy site"

### Step 5: Set Environment Variables

1. Go to "Site settings" → "Build & deploy" → "Environment"
2. Click "Edit variables"
3. Add:
   - **Name**: `VITE_BACKEND_URL`
   - **Value**: `https://your-backend.onrender.com`
4. Trigger a new deploy

### Step 6: Get Frontend URL

Your site is now live at:
```
https://your-site-name.netlify.app
```

## File Structure

```
frontend/
├── src/
│   ├── App.jsx           # Main React component
│   ├── main.jsx          # Entry point
│   └── index.css         # All styling
├── index.html            # HTML template
├── package.json          # Node dependencies
├── vite.config.js        # Vite configuration
├── netlify.toml          # Netlify deployment config
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## How It Works

1. **User selects filters** → Stored in React state
2. **User clicks "Generate Report"** → Axios sends POST to `/api/report`
3. **Backend processes request** → Returns chart data + stats
4. **Frontend displays charts** → Uses React Plotly.js to render

## Component Architecture

```
App.jsx
├── Navbar (Header)
├── Filter Section
│   ├── Dropdown filters
│   ├── Search input
│   └── Generate button
├── Summary Box
│   ├── Total crashes
│   ├── Injured count
│   └── Fatalities count
└── Charts Grid
    ├── Borough bar chart
    ├── Time line chart
    ├── Severity pie chart
    └── Heatmap
```

## Styling

All styling is in `src/index.css` using:
- CSS Variables for theme colors
- CSS Grid for responsive layouts
- Gradient backgrounds
- Smooth transitions and animations

Theme colors:
```css
--primary-color: #667eea
--primary-dark: #764ba2
--danger-color: #d62728
--success-color: #2ca02c
--warning-color: #ff7f0e
```

## Responsive Breakpoints

- **Desktop**: 1024px+
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

## API Integration

### Base URL
```javascript
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
```

### Requests

All requests use Axios with JSON content type.

### Error Handling

Errors are displayed in the UI:
```javascript
if (error) {
  return <div className="error-message">{error}</div>
}
```

## Troubleshooting

### API calls not working
- Check `VITE_BACKEND_URL` environment variable
- Ensure backend is running and accessible
- Check browser console for CORS errors

### Charts not rendering
- Ensure Plotly data is valid
- Check browser console for errors
- Clear browser cache

### Build fails
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
npm run build
```

### Environment variables not updating
- Netlify caches builds
- Trigger a new deploy after changing environment variables
- Go to Deploys → Trigger deploy

## Dependencies

- **react**: UI library
- **react-dom**: React DOM rendering
- **react-plotly.js**: Interactive charts
- **plotly.js**: Chart rendering engine
- **axios**: HTTP client
- **vite**: Build tool and dev server
- **@vitejs/plugin-react**: React plugin for Vite

## Performance Tips

1. **Code splitting**: Vite auto-splits chunks
2. **Lazy loading**: Charts only render on demand
3. **Caching**: Netlify CDN caches built files
4. **Optimization**: CSS is minified in production

## Future Enhancements

- Add dark mode toggle
- Implement data export (CSV, PDF)
- Add chart animations
- Implement date range picker
- Add data table view
- Cache API responses

## Next Steps

1. Ensure backend is deployed and working
2. Get the backend URL from Render
3. Update `netlify.toml` with backend URL
4. Deploy frontend to Netlify
5. Test full application flow

## Questions?

Check the main `README.md` in the project root.
