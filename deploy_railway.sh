#!/bin/bash

# Railway deployment script with conflict prevention
echo "🚀 Deploying bot to Railway with conflict prevention..."

# Check if we're in the right directory
if [ ! -f "bot_new.py" ]; then
    echo "❌ Error: bot_new.py not found. Please run this script from the project root."
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "Please log in to Railway:"
    railway login
fi

# Clear webhook before deployment
echo "🧹 Clearing webhook before deployment..."
python3 clear_webhook.py

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo "📊 Check your Railway dashboard for deployment status."
echo "🔍 Monitor logs with: railway logs"
