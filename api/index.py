#!/usr/bin/env python3
"""
Full API for Telegram Mini App - Vercel deployment
"""
import json
from datetime import datetime

def handler(request):
    """Vercel serverless function handler"""
    
    # Get request info
    path = request.get('path', '/')
    method = request.get('httpMethod', 'GET')
    headers = request.get('headers', {})
    body = request.get('body', '')
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': ''
        }
    
    # Set common headers
    response_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    try:
        # Route handling
        if path == '/api/health':
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps({
                    'status': 'ok',
                    'service': 'webapp-api',
                    'timestamp': datetime.now().isoformat(),
                    'db_available': False
                })
            }
        
        elif path == '/api/models':
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_models())
            }
        
        elif path.startswith('/api/models/'):
            model_id = path.split('/')[-1]
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_model_detail(model_id))
            }
        
        elif path == '/api/instructions':
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_instructions())
            }
        
        elif path.startswith('/api/instructions/'):
            instruction_id = path.split('/')[-1]
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_instruction_detail(instruction_id))
            }
        
        elif path == '/api/recipes':
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_recipes())
            }
        
        elif path.startswith('/api/recipes/'):
            recipe_id = path.split('/')[-1]
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(get_mock_recipe_detail(recipe_id))
            }
        
        elif path == '/api/search':
            return handle_search(method, body, response_headers)
        
        elif path == '/api/tickets':
            return handle_tickets(method, body, response_headers)
        
        else:
            return {
                'statusCode': 404,
                'headers': response_headers,
                'body': json.dumps({'error': 'Not found', 'path': path})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps({'error': str(e)})
        }

def handle_search(method, body, headers):
    """Handle search endpoint"""
    if method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(body) if body else {}
        query = data.get('query', '').strip()
        
        if not query:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Query is required'})
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_search_results(query))
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_search_results(''))
        }

def handle_tickets(method, body, headers):
    """Handle tickets endpoint"""
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_tickets())
        }
    
    elif method == 'POST':
        try:
            data = json.loads(body) if body else {}
            user_id = data.get('user_id')
            username = data.get('username')
            subject = data.get('subject', '')
            message = data.get('message', '')
            
            if not user_id or not message:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'user_id and message required'})
                }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': 1,
                    'status': 'open',
                    'created_at': datetime.now().isoformat()
                })
            }
        except Exception as e:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'id': 1,
                    'status': 'open',
                    'created_at': datetime.now().isoformat()
                })
            }
    
    else:
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }

# Mock data functions
def get_mock_models():
    return [
        {
            'id': 1,
            'name': 'iPhone 15 Pro',
            'description': 'Новейший смартфон от Apple с титановым корпусом и чипом A17 Pro',
            'tags': 'apple, iphone, смартфон, титан',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions_count': 3,
            'recipes_count': 2
        },
        {
            'id': 2,
            'name': 'Samsung Galaxy S24',
            'description': 'Флагманский Android смартфон с ИИ функциями и камерой 200MP',
            'tags': 'samsung, android, смартфон, камера',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions_count': 2,
            'recipes_count': 1
        },
        {
            'id': 3,
            'name': 'MacBook Pro M3',
            'description': 'Мощный ноутбук для профессионалов с чипом M3 и дисплеем Liquid Retina XDR',
            'tags': 'apple, macbook, ноутбук, m3',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions_count': 4,
            'recipes_count': 3
        },
        {
            'id': 4,
            'name': 'iPad Pro 12.9"',
            'description': 'Профессиональный планшет с чипом M2 и дисплеем Liquid Retina XDR',
            'tags': 'apple, ipad, планшет, m2',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions_count': 2,
            'recipes_count': 1
        }
    ]

def get_mock_model_detail(model_id):
    models = {
        1: {
            'id': 1,
            'name': 'iPhone 15 Pro',
            'description': 'Новейший смартфон от Apple с титановым корпусом и чипом A17 Pro',
            'tags': 'apple, iphone, смартфон, титан',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions': [
                {
                    'id': 1,
                    'title': 'Настройка iPhone 15 Pro',
                    'type': 'pdf',
                    'description': 'Подробная инструкция по настройке нового iPhone'
                },
                {
                    'id': 2,
                    'title': 'Перенос данных на iPhone',
                    'type': 'video',
                    'description': 'Видео-инструкция по переносу данных с предыдущего устройства'
                },
                {
                    'id': 3,
                    'title': 'Настройка Face ID',
                    'type': 'pdf',
                    'description': 'Инструкция по настройке системы распознавания лица'
                }
            ],
            'recipes': [
                {
                    'id': 1,
                    'title': 'Рецепт восстановления iPhone',
                    'type': 'video',
                    'description': 'Пошаговое восстановление iPhone через iTunes'
                },
                {
                    'id': 2,
                    'title': 'Рецепт оптимизации батареи',
                    'type': 'pdf',
                    'description': 'Способы оптимизации работы батареи iPhone'
                }
            ]
        },
        2: {
            'id': 2,
            'name': 'Samsung Galaxy S24',
            'description': 'Флагманский Android смартфон с ИИ функциями и камерой 200MP',
            'tags': 'samsung, android, смартфон, камера',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions': [
                {
                    'id': 4,
                    'title': 'Настройка Samsung Galaxy S24',
                    'type': 'pdf',
                    'description': 'Инструкция по настройке Samsung Galaxy'
                },
                {
                    'id': 5,
                    'title': 'Настройка камеры 200MP',
                    'type': 'video',
                    'description': 'Как использовать профессиональную камеру'
                }
            ],
            'recipes': [
                {
                    'id': 3,
                    'title': 'Рецепт восстановления Samsung',
                    'type': 'pdf',
                    'description': 'Восстановление через Odin'
                }
            ]
        },
        3: {
            'id': 3,
            'name': 'MacBook Pro M3',
            'description': 'Мощный ноутбук для профессионалов с чипом M3 и дисплеем Liquid Retina XDR',
            'tags': 'apple, macbook, ноутбук, m3',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions': [
                {
                    'id': 6,
                    'title': 'Настройка MacBook Pro M3',
                    'type': 'pdf',
                    'description': 'Первоначальная настройка MacBook'
                },
                {
                    'id': 7,
                    'title': 'Оптимизация производительности',
                    'type': 'video',
                    'description': 'Настройка для максимальной производительности'
                },
                {
                    'id': 8,
                    'title': 'Настройка дисплея XDR',
                    'type': 'pdf',
                    'description': 'Калибровка дисплея Liquid Retina XDR'
                },
                {
                    'id': 9,
                    'title': 'Работа с чипом M3',
                    'type': 'video',
                    'description': 'Особенности работы с новым чипом'
                }
            ],
            'recipes': [
                {
                    'id': 4,
                    'title': 'Рецепт оптимизации MacBook',
                    'type': 'pdf',
                    'description': 'Способы оптимизации производительности MacBook'
                },
                {
                    'id': 5,
                    'title': 'Рецепт восстановления macOS',
                    'type': 'video',
                    'description': 'Восстановление системы через Recovery'
                },
                {
                    'id': 6,
                    'title': 'Рецепт очистки системы',
                    'type': 'pdf',
                    'description': 'Очистка кэша и временных файлов'
                }
            ]
        },
        4: {
            'id': 4,
            'name': 'iPad Pro 12.9"',
            'description': 'Профессиональный планшет с чипом M2 и дисплеем Liquid Retina XDR',
            'tags': 'apple, ipad, планшет, m2',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'instructions': [
                {
                    'id': 10,
                    'title': 'Настройка iPad Pro',
                    'type': 'pdf',
                    'description': 'Первоначальная настройка iPad Pro'
                },
                {
                    'id': 11,
                    'title': 'Работа с Apple Pencil',
                    'type': 'video',
                    'description': 'Настройка и использование Apple Pencil'
                }
            ],
            'recipes': [
                {
                    'id': 7,
                    'title': 'Рецепт восстановления iPad',
                    'type': 'pdf',
                    'description': 'Восстановление через iTunes'
                }
            ]
        }
    }
    return models.get(int(model_id), {'error': 'Model not found'})

def get_mock_instructions():
    return [
        {
            'id': 1,
            'title': 'Настройка iPhone 15 Pro',
            'type': 'pdf',
            'description': 'Подробная инструкция по настройке нового iPhone',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        {
            'id': 2,
            'title': 'Перенос данных на iPhone',
            'type': 'video',
            'description': 'Видео-инструкция по переносу данных с предыдущего устройства',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        {
            'id': 3,
            'title': 'Настройка Face ID',
            'type': 'pdf',
            'description': 'Инструкция по настройке системы распознавания лица',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        {
            'id': 4,
            'title': 'Настройка Samsung Galaxy S24',
            'type': 'pdf',
            'description': 'Инструкция по настройке Samsung Galaxy',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 2, 'name': 'Samsung Galaxy S24'}]
        },
        {
            'id': 5,
            'title': 'Настройка камеры 200MP',
            'type': 'video',
            'description': 'Как использовать профессиональную камеру',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 2, 'name': 'Samsung Galaxy S24'}]
        },
        {
            'id': 6,
            'title': 'Настройка MacBook Pro M3',
            'type': 'pdf',
            'description': 'Первоначальная настройка MacBook',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 7,
            'title': 'Оптимизация производительности',
            'type': 'video',
            'description': 'Настройка для максимальной производительности',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 8,
            'title': 'Настройка дисплея XDR',
            'type': 'pdf',
            'description': 'Калибровка дисплея Liquid Retina XDR',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 9,
            'title': 'Работа с чипом M3',
            'type': 'video',
            'description': 'Особенности работы с новым чипом',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 10,
            'title': 'Настройка iPad Pro',
            'type': 'pdf',
            'description': 'Первоначальная настройка iPad Pro',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 4, 'name': 'iPad Pro 12.9"'}]
        },
        {
            'id': 11,
            'title': 'Работа с Apple Pencil',
            'type': 'video',
            'description': 'Настройка и использование Apple Pencil',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 4, 'name': 'iPad Pro 12.9"'}]
        }
    ]

def get_mock_instruction_detail(instruction_id):
    instructions = {
        1: {
            'id': 1,
            'title': 'Настройка iPhone 15 Pro',
            'type': 'pdf',
            'description': 'Подробная инструкция по настройке нового iPhone',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        2: {
            'id': 2,
            'title': 'Перенос данных на iPhone',
            'type': 'video',
            'description': 'Видео-инструкция по переносу данных с предыдущего устройства',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        }
    }
    return instructions.get(int(instruction_id), {'error': 'Instruction not found'})

def get_mock_recipes():
    return [
        {
            'id': 1,
            'title': 'Рецепт восстановления iPhone',
            'type': 'video',
            'description': 'Пошаговое восстановление iPhone через iTunes',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        {
            'id': 2,
            'title': 'Рецепт оптимизации батареи',
            'type': 'pdf',
            'description': 'Способы оптимизации работы батареи iPhone',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        {
            'id': 3,
            'title': 'Рецепт восстановления Samsung',
            'type': 'pdf',
            'description': 'Восстановление через Odin',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 2, 'name': 'Samsung Galaxy S24'}]
        },
        {
            'id': 4,
            'title': 'Рецепт оптимизации MacBook',
            'type': 'pdf',
            'description': 'Способы оптимизации производительности MacBook',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 5,
            'title': 'Рецепт восстановления macOS',
            'type': 'video',
            'description': 'Восстановление системы через Recovery',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 6,
            'title': 'Рецепт очистки системы',
            'type': 'pdf',
            'description': 'Очистка кэша и временных файлов',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        },
        {
            'id': 7,
            'title': 'Рецепт восстановления iPad',
            'type': 'pdf',
            'description': 'Восстановление через iTunes',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 4, 'name': 'iPad Pro 12.9"'}]
        }
    ]

def get_mock_recipe_detail(recipe_id):
    recipes = {
        1: {
            'id': 1,
            'title': 'Рецепт восстановления iPhone',
            'type': 'video',
            'description': 'Пошаговое восстановление iPhone через iTunes',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1, 'name': 'iPhone 15 Pro'}]
        },
        2: {
            'id': 2,
            'title': 'Рецепт оптимизации MacBook',
            'type': 'pdf',
            'description': 'Способы оптимизации производительности MacBook',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
        }
    }
    return recipes.get(int(recipe_id), {'error': 'Recipe not found'})

def get_mock_search_results(query):
    query_lower = query.lower()
    
    # Simple search logic
    models = []
    instructions = []
    recipes = []
    
    if 'iphone' in query_lower or 'apple' in query_lower:
        models = [
            {
                'id': 1,
                'name': 'iPhone 15 Pro',
                'description': 'Новейший смартфон от Apple с титановым корпусом',
                'tags': 'apple, iphone, смартфон'
            }
        ]
        instructions = [
            {
                'id': 1,
                'title': 'Настройка iPhone 15 Pro',
                'type': 'pdf',
                'description': 'Подробная инструкция по настройке нового iPhone'
            }
        ]
        recipes = [
            {
                'id': 1,
                'title': 'Рецепт восстановления iPhone',
                'type': 'video',
                'description': 'Пошаговое восстановление iPhone через iTunes'
            }
        ]
    elif 'samsung' in query_lower or 'galaxy' in query_lower:
        models = [
            {
                'id': 2,
                'name': 'Samsung Galaxy S24',
                'description': 'Флагманский Android смартфон с ИИ функциями',
                'tags': 'samsung, android, смартфон'
            }
        ]
        instructions = [
            {
                'id': 4,
                'title': 'Настройка Samsung Galaxy S24',
                'type': 'pdf',
                'description': 'Инструкция по настройке Samsung Galaxy'
            }
        ]
    elif 'macbook' in query_lower or 'mac' in query_lower:
        models = [
            {
                'id': 3,
                'name': 'MacBook Pro M3',
                'description': 'Мощный ноутбук для профессионалов',
                'tags': 'apple, macbook, ноутбук'
            }
        ]
        instructions = [
            {
                'id': 6,
                'title': 'Настройка MacBook Pro M3',
                'type': 'pdf',
                'description': 'Первоначальная настройка MacBook'
            }
        ]
        recipes = [
            {
                'id': 4,
                'title': 'Рецепт оптимизации MacBook',
                'type': 'pdf',
                'description': 'Способы оптимизации производительности MacBook'
            }
        ]
    elif 'ipad' in query_lower:
        models = [
            {
                'id': 4,
                'name': 'iPad Pro 12.9"',
                'description': 'Профессиональный планшет с чипом M2',
                'tags': 'apple, ipad, планшет'
            }
        ]
        instructions = [
            {
                'id': 10,
                'title': 'Настройка iPad Pro',
                'type': 'pdf',
                'description': 'Первоначальная настройка iPad Pro'
            }
        ]
    
    return {
        'query': query,
        'models': models,
        'instructions': instructions,
        'recipes': recipes
    }

def get_mock_tickets():
    return [
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
        },
        {
            'id': 2,
            'user_id': 123456,
            'username': 'test_user',
            'status': 'closed',
            'subject': 'Вопрос по MacBook',
            'created_at': '2024-01-01T00:00:00Z',
            'closed_at': '2024-01-02T00:00:00Z',
            'messages': [
                {
                    'id': 2,
                    'from_role': 'user',
                    'text': 'Как оптимизировать производительность MacBook?',
                    'created_at': '2024-01-01T00:00:00Z'
                },
                {
                    'id': 3,
                    'from_role': 'admin',
                    'text': 'Рекомендую использовать Activity Monitor для контроля процессов',
                    'created_at': '2024-01-01T12:00:00Z'
                }
            ]
        }
    ]