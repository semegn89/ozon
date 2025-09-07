#!/bin/bash

# Ozon Bot Deployment Script
# This script helps deploy the bot to various platforms

set -e

echo "🚀 Ozon Bot Deployment Script"
echo "=============================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your bot configuration:"
    echo "BOT_TOKEN=your_bot_token"
    echo "ADMIN_CHAT_IDS=your_chat_id"
    echo "DB_URL=sqlite:///data.db"
    echo "MODE=POLLING"
    exit 1
fi

# Function to deploy locally
deploy_local() {
    echo "📱 Deploying locally..."
    
    # Create virtual environment if not exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Install dependencies
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Initialize database
    echo "Initializing database..."
    python init_db.py
    
    # Make start script executable
    chmod +x start_bot.sh
    
    echo "✅ Local deployment complete!"
    echo "Run './start_bot.sh start' to start the bot"
}

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."
    
    # Build Docker image
    docker build -t ozon-bot .
    
    # Create logs directory
    mkdir -p logs
    
    # Start with docker-compose
    docker-compose up -d
    
    echo "✅ Docker deployment complete!"
    echo "Run 'docker-compose logs -f' to see logs"
}

# Function to deploy to cloud
deploy_cloud() {
    echo "☁️  Cloud deployment options:"
    echo ""
    echo "1. Heroku:"
    echo "   - Install Heroku CLI"
    echo "   - heroku create your-app-name"
    echo "   - heroku config:set BOT_TOKEN=your_token"
    echo "   - heroku config:set ADMIN_CHAT_IDS=your_chat_id"
    echo "   - git push heroku main"
    echo ""
    echo "2. Railway:"
    echo "   - Connect GitHub repository"
    echo "   - Set environment variables"
    echo "   - Deploy automatically"
    echo ""
    echo "3. DigitalOcean App Platform:"
    echo "   - Create new app from GitHub"
    echo "   - Set environment variables"
    echo "   - Deploy automatically"
    echo ""
    echo "4. VPS (Ubuntu/Debian):"
    echo "   - Install Docker: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    echo "   - Clone repository: git clone https://github.com/semegn89/ozon.git"
    echo "   - Copy .env file and run: docker-compose up -d"
}

# Main menu
case "$1" in
    local)
        deploy_local
        ;;
    docker)
        deploy_docker
        ;;
    cloud)
        deploy_cloud
        ;;
    *)
        echo "Usage: $0 {local|docker|cloud}"
        echo ""
        echo "Options:"
        echo "  local  - Deploy locally with virtual environment"
        echo "  docker - Deploy with Docker"
        echo "  cloud  - Show cloud deployment options"
        exit 1
        ;;
esac
