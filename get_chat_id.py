#!/usr/bin/env python3
"""
Скрипт для получения Chat ID пользователя
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN не найден в .env файле")
    exit(1)

def get_chat_id():
    """Получить Chat ID из последних обновлений"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    print("🔍 Получаем последние обновления...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        updates = data.get('result', [])
        
        if not updates:
            print("❌ Нет обновлений. Попросите пользователя написать боту /start")
            return
        
        print("📋 Последние обновления:")
        print("-" * 50)
        
        for update in updates[-5:]:  # Показываем последние 5
            if 'message' in update:
                msg = update['message']
                user = msg.get('from', {})
                chat = msg.get('chat', {})
                
                print(f"👤 Пользователь: {user.get('first_name', 'N/A')} (@{user.get('username', 'N/A')})")
                print(f"🆔 User ID: {user.get('id')}")
                print(f"🆔 Chat ID: {chat.get('id')}")
                print(f"💬 Сообщение: {msg.get('text', 'N/A')}")
                print("-" * 50)
        
        # Показываем последний Chat ID
        last_update = updates[-1]
        if 'message' in last_update:
            chat_id = last_update['message']['chat']['id']
            user_name = last_update['message']['from'].get('first_name', 'Unknown')
            print(f"\n✅ Последний Chat ID: {chat_id} (пользователь: {user_name})")
            print(f"\n📝 Добавьте этот ID в ADMIN_CHAT_IDS: {chat_id}")
    else:
        print(f"❌ Ошибка получения обновлений: {response.text}")

if __name__ == "__main__":
    get_chat_id()
