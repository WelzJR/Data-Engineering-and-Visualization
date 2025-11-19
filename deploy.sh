#!/bin/bash
# Quick deployment setup script

echo "🚀 NYC Crashes Dashboard - Deployment Setup"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - NYC Motor Vehicle Collisions Dashboard"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📋 Files ready for deployment:"
echo "  ✅ Procfile - Production server config"
echo "  ✅ runtime.txt - Python version"
echo "  ✅ requirements.txt - Dependencies"
echo "  ✅ .gitignore - Git ignore rules"
echo "  ✅ DEPLOYMENT_GUIDE.md - Detailed instructions"
echo ""

echo "🎯 Next Steps:"
echo ""
echo "1. Create a GitHub repository:"
echo "   https://github.com/new"
echo ""
echo "2. Push your code:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/your-repo.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Choose a deployment platform:"
echo ""
echo "   🚂 RAILWAY (Recommended):"
echo "      - Go to https://railway.app"
echo "      - Sign up with GitHub"
echo "      - Create new project → Deploy from GitHub"
echo "      - Select your repository → Done!"
echo ""
echo "   🎨 RENDER:"
echo "      - Go to https://render.com"
echo "      - Sign up with GitHub"
echo "      - New Web Service → Connect repository"
echo "      - Set start command to: gunicorn app:server"
echo ""
echo "   🧙 HEROKU:"
echo "      - Go to https://dashboard.heroku.com"
echo "      - Create new app"
echo "      - Connect to GitHub"
echo "      - Enable auto deploy from main"
echo ""
echo "✨ That's it! Your app will be deployed automatically."
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
