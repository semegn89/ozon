# Bot Deployment Guide

## Problem Solved: Bot Conflict Issues

This guide addresses the "Conflict: terminated by other getUpdates request" error that occurs when multiple bot instances try to poll for updates simultaneously.

## What Was Fixed

### 1. Enhanced Bot Code (`bot_new.py`)
- Added conflict detection and handling
- Implemented graceful shutdown with signal handlers
- Added retry logic for conflict errors
- Improved error handling to distinguish conflicts from other errors

### 2. Safe Startup Script (`start_bot_safe.py`)
- Automatically clears webhooks before starting
- Verifies bot connection
- Provides better logging and error handling
- Ensures clean startup every time

### 3. Updated Deployment Configuration
- Modified `railway.json` to use safe startup script
- Reduced restart retries to prevent infinite loops
- Updated `Procfile` for consistent deployment

### 4. Webhook Clearing Script (`clear_webhook.py`)
- Standalone script to clear webhooks and reset bot state
- Can be run manually when conflicts occur

## Deployment Process

### Option 1: Automatic Deployment (Recommended)
```bash
./deploy_railway.sh
```

### Option 2: Manual Deployment
1. Clear webhooks first:
   ```bash
   python3 clear_webhook.py
   ```

2. Deploy to Railway:
   ```bash
   railway up
   ```

### Option 3: Local Testing
```bash
# Activate virtual environment
source venv/bin/activate

# Test safe startup
python start_bot_safe.py
```

## Key Features Added

### Conflict Prevention
- Automatic webhook clearing on startup
- Drop pending updates to avoid conflicts
- Exponential backoff retry logic
- Better error classification

### Graceful Shutdown
- Signal handlers for SIGINT and SIGTERM
- Proper cleanup of resources
- Prevents zombie processes

### Monitoring
- Enhanced logging with conflict detection
- Health check endpoint at `/health`
- Error reporting to admins (excluding conflicts)

## Environment Variables Required

Make sure these are set in your Railway environment:
- `BOT_TOKEN`: Your Telegram bot token
- `ADMIN_CHAT_IDS`: Comma-separated list of admin chat IDs
- `MODE`: Set to "POLLING" for Railway deployment
- `DB_URL`: Database connection string (optional, defaults to SQLite)

## Troubleshooting

### If conflicts still occur:
1. Run the webhook clearing script:
   ```bash
   python3 clear_webhook.py
   ```

2. Wait 30 seconds before redeploying

3. Check Railway logs for any remaining issues

### If bot doesn't start:
1. Check environment variables are set correctly
2. Verify bot token is valid
3. Check Railway logs for specific error messages

## Files Modified/Created

- `bot_new.py` - Enhanced with conflict handling
- `start_bot_safe.py` - New safe startup script
- `clear_webhook.py` - Webhook clearing utility
- `deploy_railway.sh` - Automated deployment script
- `railway.json` - Updated deployment configuration
- `Procfile` - Updated to use safe startup
- `DEPLOYMENT_GUIDE.md` - This guide

## Next Steps

1. Deploy using the safe startup script
2. Monitor logs for any remaining issues
3. The bot should now handle conflicts gracefully and restart automatically when needed

The bot is now much more robust and should handle deployment conflicts automatically!
