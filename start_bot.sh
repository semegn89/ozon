#!/bin/bash

# Ozon Bot Startup Script
# This script ensures the bot is always running

BOT_DIR="/Users/grigorijs/ozon"
VENV_DIR="$BOT_DIR/venv"
BOT_SCRIPT="$BOT_DIR/bot_new.py"
LOG_FILE="$BOT_DIR/bot.log"
PID_FILE="$BOT_DIR/bot.pid"

# Function to start the bot
start_bot() {
    echo "$(date): Starting Ozon Bot..." >> "$LOG_FILE"
    
    # Activate virtual environment and start bot
    cd "$BOT_DIR"
    source "$VENV_DIR/bin/activate"
    nohup python "$BOT_SCRIPT" >> "$LOG_FILE" 2>&1 &
    
    # Save PID
    echo $! > "$PID_FILE"
    echo "$(date): Bot started with PID $!" >> "$LOG_FILE"
}

# Function to stop the bot
stop_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "$(date): Stopping bot (PID: $PID)..." >> "$LOG_FILE"
            kill $PID
            rm "$PID_FILE"
        fi
    fi
}

# Function to check if bot is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            return 0
        else
            rm "$PID_FILE"
        fi
    fi
    return 1
}

# Main logic
case "$1" in
    start)
        if is_running; then
            echo "Bot is already running"
        else
            start_bot
            echo "Bot started"
        fi
        ;;
    stop)
        stop_bot
        echo "Bot stopped"
        ;;
    restart)
        stop_bot
        sleep 2
        start_bot
        echo "Bot restarted"
        ;;
    status)
        if is_running; then
            echo "Bot is running (PID: $(cat $PID_FILE))"
        else
            echo "Bot is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
