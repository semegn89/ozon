#!/usr/bin/env python3
"""
Script to clear all webhooks and reset bot state
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not found in .env file")
    exit(1)

def clear_webhook():
    """Clear webhook and reset bot state"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    
    print("🔄 Clearing webhook...")
    response = requests.post(url, json={"drop_pending_updates": True})
    
    if response.status_code == 200:
        print("✅ Webhook cleared successfully")
    else:
        print(f"❌ Failed to clear webhook: {response.text}")
    
    # Get bot info
    print("\n🤖 Getting bot info...")
    info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    info_response = requests.get(info_url)
    
    if info_response.status_code == 200:
        bot_info = info_response.json()
        print(f"✅ Bot: @{bot_info['result']['first_name']}")
        print(f"✅ Username: @{bot_info['result']['username']}")
    else:
        print(f"❌ Failed to get bot info: {info_response.text}")

if __name__ == "__main__":
    clear_webhook()
