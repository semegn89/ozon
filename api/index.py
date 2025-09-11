#!/usr/bin/env python3
"""
Simple API for Telegram Mini App - Vercel deployment
In-memory storage for quick deployment
"""
import json
import os
from datetime import datetime

# Simple in-memory storage (will reset on each deployment)
# In production, you'd use a database
STORAGE = {
    'models': [
        {
            'id': 1,
            'name': 'iPhone 15 Pro',
            'description': 'Новейший смартфон от Apple с титановым корпусом и чипом A17 Pro',
            'tags': 'apple, iphone, смартфон, титан',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions_count': 3,
            'recipes_count': 2
        },
        {
            'id': 2,
            'name': 'Samsung Galaxy S24',
            'description': 'Флагманский Android смартфон с ИИ функциями и камерой 200MP',
            'tags': 'samsung, android, смартфон, камера',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions_count': 2,
            'recipes_count': 1
        },
        {
            'id': 3,
            'name': 'MacBook Pro M3',
            'description': 'Мощный ноутбук для профессионалов с чипом M3 и дисплеем Liquid Retina XDR',
            'tags': 'apple, macbook, ноутбук, m3',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions_count': 4,
            'recipes_count': 3
        },
        {
            'id': 4,
            'name': 'iPad Pro 12.9"',
            'description': 'Профессиональный планшет с чипом M2 и дисплеем Liquid Retina XDR',
            'tags': 'apple, ipad, планшет, m2',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions_count': 2,
            'recipes_count': 1
        }
    ],
    'instructions': [
        {
            'id': 1,
            'title': 'Настройка iPhone 15 Pro',
            'type': 'pdf',
            'description': 'Подробная инструкция по настройке нового iPhone',
            'model_id': 1,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'title': 'Перенос данных на iPhone',
            'type': 'video',
            'description': 'Видео-инструкция по переносу данных с предыдущего устройства',
            'model_id': 1,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 3,
            'title': 'Настройка Samsung Galaxy S24',
            'type': 'pdf',
            'description': 'Инструкция по настройке Samsung Galaxy',
            'model_id': 2,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 4,
            'title': 'Настройка MacBook Pro M3',
            'type': 'pdf',
            'description': 'Первоначальная настройка MacBook',
            'model_id': 3,
            'created_at': '2024-01-01T00:00:00Z'
        }
    ],
    'recipes': [
        {
            'id': 1,
            'title': 'Рецепт восстановления iPhone',
            'type': 'video',
            'description': 'Пошаговое восстановление iPhone через iTunes',
            'model_id': 1,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'title': 'Рецепт оптимизации MacBook',
            'type': 'pdf',
            'description': 'Способы оптимизации производительности MacBook',
            'model_id': 3,
            'created_at': '2024-01-01T00:00:00Z'
        }
    ],
    'tickets': [
        {
            'id': 1,
            'user_id': 123456,
            'username': 'test_user',
            'status': 'open',
            'subject': 'Проблема с настройкой iPhone',
            'created_at': '2024-01-01T00:00:00Z',
            'closed_at': None,
            'messages': [
                {
                    'id': 1,
                    'from_role': 'user',
                    'text': 'Не могу настроить Face ID на новом iPhone',
                    'created_at': '2024-01-01T00:00:00Z'
                }
            ]
        }
    ]
}

def handler(request):
    """Vercel serverless function handler"""
    
    try:
        # Vercel passes request as a dictionary
        path = request.get('path', '/')
        method = request.get('httpMethod', 'GET')
        body = request.get('body', '')
        
        # Handle query parameters
        query_params = request.get('queryStringParameters', {}) or {}
        
        # CORS headers
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
        
        if method == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        # Simple test endpoint first
        if path == '/api/test':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'message': 'API is working!',
                    'path': path,
                    'method': method,
                    'timestamp': datetime.now().isoformat()
                })
            }
        
        # Health check
        if path == '/api/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'ok', 
                    'timestamp': datetime.now().isoformat(),
                    'storage': {
                        'models': len(STORAGE['models']),
                        'instructions': len(STORAGE['instructions']),
                        'recipes': len(STORAGE['recipes']),
                        'tickets': len(STORAGE['tickets'])
                    }
                })
            }
        
        # Models endpoints
        if path == '/api/models':
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(STORAGE['models'])
                }
            elif method == 'POST':
                data = json.loads(body) if body else {}
                new_model = {
                    'id': max([m['id'] for m in STORAGE['models']], default=0) + 1,
                    'name': data.get('name', ''),
                    'description': data.get('description', ''),
                    'tags': data.get('tags', ''),
                    'created_at': datetime.now().isoformat(),
                    'instructions_count': 0,
                    'recipes_count': 0
                }
                STORAGE['models'].append(new_model)
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(new_model)
                }
        
        # Model detail endpoint
        if path.startswith('/api/models/') and method == 'GET':
            model_id = int(path.split('/')[-1])
            model = next((m for m in STORAGE['models'] if m['id'] == model_id), None)
            if model:
                # Add related instructions and recipes
                model['instructions'] = [i for i in STORAGE['instructions'] if i['model_id'] == model_id]
                model['recipes'] = [r for r in STORAGE['recipes'] if r['model_id'] == model_id]
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(model)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Model not found'})
                }
        
        # Instructions endpoints
        if path == '/api/instructions':
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(STORAGE['instructions'])
                }
        
        # Recipes endpoints
        if path == '/api/recipes':
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(STORAGE['recipes'])
                }
        
        # Search endpoint
        if path == '/api/search' and method == 'POST':
            data = json.loads(body) if body else {}
            query = data.get('query', '').strip().lower()
            
            if not query:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Query is required'})
                }
            
            # Search in all data
            results = {
                'query': query,
                'models': [m for m in STORAGE['models'] 
                          if query in m['name'].lower() or 
                             query in m['description'].lower() or 
                             query in m['tags'].lower()],
                'instructions': [i for i in STORAGE['instructions'] 
                               if query in i['title'].lower() or 
                                  query in i['description'].lower()],
                'recipes': [r for r in STORAGE['recipes'] 
                          if query in r['title'].lower() or 
                             query in r['description'].lower()]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(results)
            }
        
        # Tickets endpoints
        if path == '/api/tickets':
            if method == 'GET':
                user_id = query_params.get('user_id')
                if user_id:
                    user_tickets = [t for t in STORAGE['tickets'] if t['user_id'] == int(user_id)]
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps(user_tickets)
                    }
                else:
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps(STORAGE['tickets'])
                    }
            
            elif method == 'POST':
                data = json.loads(body) if body else {}
                new_ticket = {
                    'id': max([t['id'] for t in STORAGE['tickets']], default=0) + 1,
                    'user_id': data.get('user_id'),
                    'username': data.get('username'),
                    'subject': data.get('subject', ''),
                    'status': 'open',
                    'created_at': datetime.now().isoformat(),
                    'closed_at': None,
                    'messages': [{
                        'id': 1,
                        'from_role': 'user',
                        'text': data.get('message', ''),
                        'created_at': datetime.now().isoformat()
                    }]
                }
                STORAGE['tickets'].append(new_ticket)
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(new_ticket)
                }
        
        # Default response for any other path
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'API endpoint not found',
                'path': path,
                'method': method,
                'available_endpoints': ['/api/test', '/api/health', '/api/models', '/api/instructions', '/api/recipes', '/api/tickets', '/api/search']
            })
        }
    
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error',
                'path': request.get('path', '/'),
                'method': request.get('httpMethod', 'GET')
            })
        }