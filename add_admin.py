#!/usr/bin/env python3
"""
Простой скрипт для добавления админа
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN не найден!")
    print("Создайте файл .env с содержимым:")
    print("BOT_TOKEN=ваш_токен_бота")
    exit(1)

def add_admin():
    """Добавить админа через Telegram API"""
    print("🤖 Бот для добавления админа")
    print("=" * 40)
    
    # Получаем информацию о боте
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            bot_info = response.json()['result']
            print(f"✅ Бот: @{bot_info['username']}")
            print(f"✅ Имя: {bot_info['first_name']}")
        else:
            print(f"❌ Ошибка получения информации о боте: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    print("\n📋 Инструкция:")
    print("1. Попросите пользователя написать боту /start")
    print("2. Нажмите Enter для получения Chat ID")
    
    input("\nНажмите Enter когда пользователь напишет боту...")
    
    # Получаем обновления
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            updates = data.get('result', [])
            
            if not updates:
                print("❌ Нет новых сообщений. Попросите пользователя написать /start")
                return
            
            # Показываем последние сообщения
            print("\n📨 Последние сообщения:")
            print("-" * 50)
            
            for update in updates[-3:]:  # Последние 3
                if 'message' in update:
                    msg = update['message']
                    user = msg.get('from', {})
                    chat = msg.get('chat', {})
                    
                    print(f"👤 {user.get('first_name', 'N/A')} (@{user.get('username', 'N/A')})")
                    print(f"🆔 Chat ID: {chat.get('id')}")
                    print(f"💬 {msg.get('text', 'N/A')}")
                    print("-" * 50)
            
            # Берем последний Chat ID
            last_update = updates[-1]
            if 'message' in last_update:
                chat_id = last_update['message']['chat']['id']
                user_name = last_update['message']['from'].get('first_name', 'Unknown')
                
                print(f"\n✅ Найден пользователь: {user_name}")
                print(f"🆔 Chat ID: {chat_id}")
                
                # Спрашиваем подтверждение
                confirm = input(f"\nДобавить {user_name} (ID: {chat_id}) как админа? (y/n): ")
                
                if confirm.lower() in ['y', 'yes', 'да', 'д']:
                    print(f"\n📝 Добавьте этот Chat ID в Railway:")
                    print(f"ADMIN_CHAT_IDS=318073844,{chat_id}")
                    print(f"\nИли если уже есть другие админы:")
                    print(f"ADMIN_CHAT_IDS=318073844,другие_id,{chat_id}")
                    
                    print(f"\n🔧 В Railway Dashboard:")
                    print("1. Откройте ваш проект")
                    print("2. Перейдите в Variables")
                    print("3. Найдите ADMIN_CHAT_IDS")
                    print("4. Добавьте Chat ID через запятую")
                    print("5. Сохраните и перезапустите бота")
                else:
                    print("❌ Отменено")
        else:
            print(f"❌ Ошибка получения обновлений: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    add_admin()
