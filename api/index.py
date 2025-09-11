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
    
    try:
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
        
        # Simple test endpoint
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
        
        # Models endpoints
        elif path == '/api/models':
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
        
        elif path.startswith('/api/models/'):
            model_id = int(path.split('/')[-1])
            
            if method == 'GET':
                # Get model with instructions and recipes
                model = next((m for m in STORAGE['models'] if m['id'] == model_id), None)
                if not model:
                    return {
                        'statusCode': 404,
                        'headers': headers,
                        'body': json.dumps({'error': 'Model not found'})
                    }
                
                # Add related instructions and recipes
                model['instructions'] = [i for i in STORAGE['instructions'] if i['model_id'] == model_id]
                model['recipes'] = [r for r in STORAGE['recipes'] if r['model_id'] == model_id]
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(model)
                }
            
            elif method == 'DELETE':
                STORAGE['models'] = [m for m in STORAGE['models'] if m['id'] != model_id]
                # Also delete related instructions and recipes
                STORAGE['instructions'] = [i for i in STORAGE['instructions'] if i['model_id'] != model_id]
                STORAGE['recipes'] = [r for r in STORAGE['recipes'] if r['model_id'] != model_id]
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Model deleted'})
                }
        
        # Instructions endpoints
        elif path == '/api/instructions':
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(STORAGE['instructions'])
                }
            elif method == 'POST':
                data = json.loads(body) if body else {}
                new_instruction = {
                    'id': max([i['id'] for i in STORAGE['instructions']], default=0) + 1,
                    'title': data.get('title', ''),
                    'type': data.get('type', 'pdf'),
                    'description': data.get('description', ''),
                    'model_id': data.get('model_id'),
                    'created_at': datetime.now().isoformat()
                }
                STORAGE['instructions'].append(new_instruction)
                
                # Update model's instruction count
                for model in STORAGE['models']:
                    if model['id'] == new_instruction['model_id']:
                        model['instructions_count'] += 1
                        break
                
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(new_instruction)
                }
        
        elif path.startswith('/api/instructions/') and method == 'DELETE':
            instruction_id = int(path.split('/')[-1])
            instruction = next((i for i in STORAGE['instructions'] if i['id'] == instruction_id), None)
            
            if instruction:
                STORAGE['instructions'] = [i for i in STORAGE['instructions'] if i['id'] != instruction_id]
                
                # Update model's instruction count
                for model in STORAGE['models']:
                    if model['id'] == instruction['model_id']:
                        model['instructions_count'] = max(0, model['instructions_count'] - 1)
                        break
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Instruction deleted'})
            }
        
        # Recipes endpoints
        elif path == '/api/recipes':
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(STORAGE['recipes'])
                }
            elif method == 'POST':
                data = json.loads(body) if body else {}
                new_recipe = {
                    'id': max([r['id'] for r in STORAGE['recipes']], default=0) + 1,
                    'title': data.get('title', ''),
                    'type': data.get('type', 'pdf'),
                    'description': data.get('description', ''),
                    'model_id': data.get('model_id'),
                    'created_at': datetime.now().isoformat()
                }
                STORAGE['recipes'].append(new_recipe)
                
                # Update model's recipe count
                for model in STORAGE['models']:
                    if model['id'] == new_recipe['model_id']:
                        model['recipes_count'] += 1
                        break
                
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(new_recipe)
                }
        
        elif path.startswith('/api/recipes/') and method == 'DELETE':
            recipe_id = int(path.split('/')[-1])
            recipe = next((r for r in STORAGE['recipes'] if r['id'] == recipe_id), None)
            
            if recipe:
                STORAGE['recipes'] = [r for r in STORAGE['recipes'] if r['id'] != recipe_id]
                
                # Update model's recipe count
                for model in STORAGE['models']:
                    if model['id'] == recipe['model_id']:
                        model['recipes_count'] = max(0, model['recipes_count'] - 1)
                        break
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Recipe deleted'})
            }
        
        # Search endpoint
        elif path == '/api/search':
            if method == 'POST':
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
        elif path == '/api/tickets':
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
        
        elif path.startswith('/api/tickets/') and method == 'PUT':
            ticket_id = int(path.split('/')[-1])
            data = json.loads(body) if body else {}
            
            ticket = next((t for t in STORAGE['tickets'] if t['id'] == ticket_id), None)
            if ticket:
                if 'status' in data:
                    ticket['status'] = data['status']
                    if data['status'] == 'closed':
                        ticket['closed_at'] = datetime.now().isoformat()
                
                if 'message' in data:
                    new_message = {
                        'id': max([m['id'] for m in ticket['messages']], default=0) + 1,
                        'from_role': data.get('from_role', 'admin'),
                        'text': data['message'],
                        'created_at': datetime.now().isoformat()
                    }
                    ticket['messages'].append(new_message)
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(ticket)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Ticket not found'})
                }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found', 'path': path})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }