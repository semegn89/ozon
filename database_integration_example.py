# Пример интеграции с внешней базой данных
# Для Supabase, PlanetScale или другой облачной БД

import os
import json
from datetime import datetime

# Пример с Supabase
def get_supabase_client():
    from supabase import create_client, Client
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    return create_client(url, key)

def handler(request):
    """Vercel function with external database"""
    
    path = request.get('path', '/')
    method = request.get('httpMethod', 'GET')
    body = request.get('body', '')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        # Подключаемся к внешней БД
        supabase = get_supabase_client()
        
        if path == '/api/models':
            if method == 'GET':
                # Получаем модели из БД
                result = supabase.table('models').select('*').execute()
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(result.data)
                }
            
            elif method == 'POST':
                # Добавляем новую модель
                data = json.loads(body) if body else {}
                new_model = {
                    'name': data.get('name'),
                    'description': data.get('description'),
                    'tags': data.get('tags'),
                    'created_at': datetime.now().isoformat()
                }
                
                result = supabase.table('models').insert(new_model).execute()
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(result.data[0])
                }
        
        elif path.startswith('/api/models/') and method == 'DELETE':
            # Удаляем модель
            model_id = path.split('/')[-1]
            supabase.table('models').delete().eq('id', model_id).execute()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Model deleted'})
            }
        
        # Аналогично для инструкций, рецептов, тикетов...
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

# Пример схемы БД для Supabase
SUPABASE_SCHEMA = """
-- Таблица моделей
CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tags VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица инструкций
CREATE TABLE instructions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'pdf', 'video', 'link'
    description TEXT,
    tg_file_id VARCHAR(255),
    url VARCHAR(500),
    model_id INTEGER REFERENCES models(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица рецептов
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    tg_file_id VARCHAR(255),
    url VARCHAR(500),
    model_id INTEGER REFERENCES models(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Таблица тикетов поддержки
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username VARCHAR(255),
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'in_progress', 'closed'
    subject VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    closed_at TIMESTAMP
);

-- Таблица сообщений тикетов
CREATE TABLE ticket_messages (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES tickets(id),
    from_role VARCHAR(50) NOT NULL, -- 'user', 'admin'
    text TEXT,
    tg_file_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
"""
