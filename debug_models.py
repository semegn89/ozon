#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с моделями
"""

import os
from dotenv import load_dotenv
from models import create_tables, get_session, Model
from services.models_service import ModelsService

load_dotenv()

def debug_models():
    """Диагностика моделей в базе данных"""
    print("🔍 Диагностика моделей в базе данных")
    print("=" * 50)
    
    # Создаем таблицы если их нет
    create_tables()
    
    # Получаем сессию базы данных
    db = get_session()
    try:
        models_service = ModelsService(db)
        
        # Получаем все модели
        models = models_service.get_models(page=0, limit=100)
        total_count = models_service.get_models_count()
        
        print(f"📊 Всего моделей в базе: {total_count}")
        print(f"📋 Найдено моделей: {len(models)}")
        print()
        
        if not models:
            print("❌ Модели не найдены!")
            print("💡 Попробуйте добавить модель через бота")
            return
        
        print("📦 Список моделей:")
        print("-" * 30)
        
        for model in models:
            print(f"🆔 ID: {model.id}")
            print(f"📝 Название: {model.name}")
            print(f"📄 Описание: {model.description or 'Нет описания'}")
            print(f"🏷️ Теги: {model.tags or 'Нет тегов'}")
            print(f"📅 Создано: {model.created_at}")
            print(f"📅 Обновлено: {model.updated_at}")
            print(f"📎 Инструкций: {len(model.instructions)}")
            print("-" * 30)
        
        # Проверяем конкретную модель
        if models:
            first_model = models[0]
            print(f"\n🔍 Проверка модели ID {first_model.id}:")
            
            # Проверяем поиск по ID
            found_model = models_service.get_model_by_id(first_model.id)
            if found_model:
                print(f"✅ Модель найдена по ID: {found_model.name}")
            else:
                print(f"❌ Модель НЕ найдена по ID: {first_model.id}")
            
            # Проверяем поиск по имени
            found_by_name = models_service.get_model_by_name(first_model.name)
            if found_by_name:
                print(f"✅ Модель найдена по имени: {found_by_name.name}")
            else:
                print(f"❌ Модель НЕ найдена по имени: {first_model.name}")
        
    except Exception as e:
        print(f"❌ Ошибка при работе с базой данных: {e}")
    finally:
        db.close()

def test_model_creation():
    """Тест создания модели"""
    print("\n🧪 Тест создания модели")
    print("=" * 30)
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        
        # Создаем тестовую модель
        test_model = models_service.create_model(
            name="Тестовая модель",
            description="Описание тестовой модели",
            tags="тест, проверка"
        )
        
        print(f"✅ Тестовая модель создана:")
        print(f"   ID: {test_model.id}")
        print(f"   Название: {test_model.name}")
        
        # Проверяем, что модель сохранилась
        found_model = models_service.get_model_by_id(test_model.id)
        if found_model:
            print(f"✅ Модель найдена после создания: {found_model.name}")
        else:
            print(f"❌ Модель НЕ найдена после создания!")
        
        # Удаляем тестовую модель
        models_service.delete_model(test_model.id)
        print(f"🗑️ Тестовая модель удалена")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_models()
    test_model_creation()
