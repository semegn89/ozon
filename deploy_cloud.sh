#!/bin/bash

# Cloud Deployment Script for Ozon Telegram Bot
# Supports Railway, Render, Heroku, and DigitalOcean

set -e

echo "☁️  Ozon Bot Cloud Deployment"
echo "=============================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your bot configuration:"
    echo "BOT_TOKEN=your_bot_token"
    echo "ADMIN_CHAT_IDS=your_chat_id"
    exit 1
fi

# Function to deploy to Railway
deploy_railway() {
    echo "🚂 Deploying to Railway..."
    
    # Install Railway CLI if not installed
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        curl -fsSL https://railway.app/install.sh | sh
    fi
    
    # Login to Railway
    railway login
    
    # Create new project
    railway init
    
    # Set environment variables
    echo "Setting environment variables..."
    railway variables set BOT_TOKEN=$(grep BOT_TOKEN .env | cut -d '=' -f2)
    railway variables set ADMIN_CHAT_IDS=$(grep ADMIN_CHAT_IDS .env | cut -d '=' -f2)
    railway variables set DB_URL="sqlite:///data.db"
    railway variables set MODE="POLLING"
    
    # Deploy
    railway up
    
    echo "✅ Deployed to Railway!"
    echo "Your bot URL: https://railway.app/dashboard"
}

# Function to deploy to Render
deploy_render() {
    echo "🎨 Deploying to Render..."
    
    echo "1. Go to https://render.com"
    echo "2. Sign up/Login with GitHub"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect your GitHub repository: semegn89/ozon"
    echo "5. Configure:"
    echo "   - Name: ozon-telegram-bot"
    echo "   - Environment: Python 3"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python bot_new.py"
    echo "6. Add Environment Variables:"
    echo "   - BOT_TOKEN: $(grep BOT_TOKEN .env | cut -d '=' -f2)"
    echo "   - ADMIN_CHAT_IDS: $(grep ADMIN_CHAT_IDS .env | cut -d '=' -f2)"
    echo "   - DB_URL: sqlite:///data.db"
    echo "   - MODE: POLLING"
    echo "7. Click 'Create Web Service'"
    
    echo "✅ Render deployment instructions provided!"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🟣 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not installed!"
        echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Login to Heroku
    heroku login
    
    # Create app
    read -p "Enter Heroku app name (or press Enter for auto-generated): " app_name
    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create "$app_name"
    fi
    
    # Set environment variables
    echo "Setting environment variables..."
    heroku config:set BOT_TOKEN=$(grep BOT_TOKEN .env | cut -d '=' -f2)
    heroku config:set ADMIN_CHAT_IDS=$(grep ADMIN_CHAT_IDS .env | cut -d '=' -f2)
    heroku config:set DB_URL="sqlite:///data.db"
    heroku config:set MODE="POLLING"
    
    # Deploy
    git push heroku main
    
    echo "✅ Deployed to Heroku!"
    echo "Your bot is running at: https://$(heroku apps:info --json | jq -r '.app.name').herokuapp.com"
}

# Function to deploy to DigitalOcean
deploy_digitalocean() {
    echo "🌊 Deploying to DigitalOcean..."
    
    echo "1. Go to https://cloud.digitalocean.com/apps"
    echo "2. Click 'Create App'"
    echo "3. Choose 'GitHub' as source"
    echo "4. Select repository: semegn89/ozon"
    echo "5. Configure:"
    echo "   - Name: ozon-telegram-bot"
    echo "   - Type: Worker"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Run Command: python bot_new.py"
    echo "6. Add Environment Variables:"
    echo "   - BOT_TOKEN: $(grep BOT_TOKEN .env | cut -d '=' -f2)"
    echo "   - ADMIN_CHAT_IDS: $(grep ADMIN_CHAT_IDS .env | cut -d '=' -f2)"
    echo "   - DB_URL: sqlite:///data.db"
    echo "   - MODE: POLLING"
    echo "7. Click 'Create Resources'"
    
    echo "✅ DigitalOcean deployment instructions provided!"
}

# Function to show all options
show_options() {
    echo "Available cloud platforms:"
    echo ""
    echo "1. Railway (Recommended - Free tier available)"
    echo "   - Automatic deployments from GitHub"
    echo "   - Free tier: 500 hours/month"
    echo "   - Easy setup with CLI"
    echo ""
    echo "2. Render (Free tier available)"
    echo "   - Web interface deployment"
    echo "   - Free tier: 750 hours/month"
    echo "   - Automatic SSL"
    echo ""
    echo "3. Heroku (Limited free tier)"
    echo "   - Classic platform"
    echo "   - Free tier: 550-1000 hours/month"
    echo "   - Requires credit card"
    echo ""
    echo "4. DigitalOcean App Platform"
    echo "   - $5/month minimum"
    echo "   - Reliable and fast"
    echo "   - Good for production"
    echo ""
    echo "5. VPS (Ubuntu/Debian)"
    echo "   - Full control"
    echo "   - $3-5/month"
    echo "   - Requires server management"
}

# Main menu
case "$1" in
    railway)
        deploy_railway
        ;;
    render)
        deploy_render
        ;;
    heroku)
        deploy_heroku
        ;;
    digitalocean)
        deploy_digitalocean
        ;;
    options)
        show_options
        ;;
    *)
        echo "Usage: $0 {railway|render|heroku|digitalocean|options}"
        echo ""
        echo "Quick start:"
        echo "  $0 railway    # Deploy to Railway (recommended)"
        echo "  $0 render     # Show Render deployment steps"
        echo "  $0 heroku     # Deploy to Heroku"
        echo "  $0 options    # Show all platform options"
        exit 1
        ;;
esac
