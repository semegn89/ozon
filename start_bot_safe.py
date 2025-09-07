#!/usr/bin/env python3
"""
Safe bot startup script that handles conflicts and ensures clean startup
"""

import os
import sys
import time
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

def clear_webhook_and_updates():
    """Clear webhook and pending updates"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment")
        return False
    
    try:
        # Clear webhook
        clear_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.post(clear_url, json={"drop_pending_updates": True})
        
        if response.status_code == 200:
            logger.info("✅ Webhook cleared successfully")
        else:
            logger.warning(f"⚠️ Failed to clear webhook: {response.text}")
        
        # Get bot info to verify connection
        info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        info_response = requests.get(info_url)
        
        if info_response.status_code == 200:
            bot_info = info_response.json()
            logger.info(f"✅ Bot connected: @{bot_info['result']['username']}")
            return True
        else:
            logger.error(f"❌ Failed to get bot info: {info_response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during webhook clearing: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("🚀 Starting bot with conflict prevention...")
    
    # Clear webhook and pending updates
    if not clear_webhook_and_updates():
        logger.error("❌ Failed to clear webhook, exiting...")
        sys.exit(1)
    
    # Wait a bit to ensure webhook is cleared
    logger.info("⏳ Waiting 3 seconds for webhook to be fully cleared...")
    time.sleep(3)
    
    # Import and start the main bot
    try:
        logger.info("🤖 Starting main bot application...")
        from bot_new import main as bot_main
        bot_main()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
