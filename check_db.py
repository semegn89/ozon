#!/usr/bin/env python3
"""
Скрипт для проверки базы данных
"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def check_database():
    """Проверка базы данных"""
    print("🗄️ Проверка базы данных")
    print("=" * 30)
    
    db_path = "data.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Файл базы данных не найден: {db_path}")
        return
    
    print(f"✅ Файл базы данных найден: {db_path}")
    print(f"📏 Размер файла: {os.path.getsize(db_path)} байт")
    
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 Таблицы в базе данных:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Проверяем таблицу models
        if ('models',) in tables:
            cursor.execute("SELECT COUNT(*) FROM models")
            count = cursor.fetchone()[0]
            print(f"\n📦 Моделей в таблице models: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, name, description, created_at FROM models LIMIT 5")
                models = cursor.fetchall()
                
                print(f"\n📋 Первые {len(models)} моделей:")
                for model in models:
                    print(f"   ID: {model[0]}, Название: {model[1]}, Описание: {model[2]}, Создано: {model[3]}")
        else:
            print("❌ Таблица models не найдена!")
        
        # Проверяем таблицу instructions
        if ('instructions',) in tables:
            cursor.execute("SELECT COUNT(*) FROM instructions")
            count = cursor.fetchone()[0]
            print(f"\n📄 Инструкций в таблице instructions: {count}")
        else:
            print("❌ Таблица instructions не найдена!")
        
        # Проверяем таблицу tickets
        if ('tickets',) in tables:
            cursor.execute("SELECT COUNT(*) FROM tickets")
            count = cursor.fetchone()[0]
            print(f"\n🎫 Обращений в таблице tickets: {count}")
        else:
            print("❌ Таблица tickets не найдена!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка при работе с базой данных: {e}")

if __name__ == "__main__":
    check_database()
