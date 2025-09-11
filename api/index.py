#!/usr/bin/env python3
"""
Full API for Telegram Mini App - Vercel deployment
"""
import json
import os
import sys
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models import get_session, InstructionType, TicketStatus, MessageRole
    from services.models_service import ModelsService
    from services.instructions_service import InstructionsService
    from services.recipes_service import RecipesService
    from services.support_service import SupportService
    DB_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    DB_AVAILABLE = False

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
                    'db_available': DB_AVAILABLE
                })
            }
        
        elif path == '/api/models':
            return handle_models(method, body, response_headers)
        
        elif path.startswith('/api/models/'):
            model_id = path.split('/')[-1]
            return handle_model_detail(model_id, response_headers)
        
        elif path == '/api/instructions':
            return handle_instructions(method, body, response_headers)
        
        elif path.startswith('/api/instructions/'):
            instruction_id = path.split('/')[-1]
            return handle_instruction_detail(instruction_id, response_headers)
        
        elif path == '/api/recipes':
            return handle_recipes(method, body, response_headers)
        
        elif path.startswith('/api/recipes/'):
            recipe_id = path.split('/')[-1]
            return handle_recipe_detail(recipe_id, response_headers)
        
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

def handle_models(method, body, headers):
    """Handle models endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_models())
        }
    
    try:
        db = get_session()
        try:
            models_service = ModelsService(db)
            models = models_service.get_models(page=0, limit=100)
            
            result = []
            for model in models:
                model_data = {
                    'id': model.id,
                    'name': model.name,
                    'description': model.description,
                    'tags': model.tags,
                    'created_at': model.created_at.isoformat() if model.created_at else None,
                    'updated_at': model.updated_at.isoformat() if model.updated_at else None,
                    'instructions_count': len(model.instructions) if model.instructions else 0,
                    'recipes_count': len(model.recipes) if model.recipes else 0
                }
                result.append(model_data)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_models())
        }

def handle_model_detail(model_id, headers):
    """Handle model detail endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_model_detail(model_id))
        }
    
    try:
        db = get_session()
        try:
            models_service = ModelsService(db)
            model = models_service.get_model_by_id(int(model_id))
            
            if not model:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Model not found'})
                }
            
            # Get instructions and recipes
            instructions_service = InstructionsService(db)
            recipes_service = RecipesService(db)
            
            instructions = instructions_service.get_instructions_by_model_id(model.id)
            recipes = recipes_service.get_recipes_by_model_id(model.id)
            
            model_data = {
                'id': model.id,
                'name': model.name,
                'description': model.description,
                'tags': model.tags,
                'created_at': model.created_at.isoformat() if model.created_at else None,
                'updated_at': model.updated_at.isoformat() if model.updated_at else None,
                'instructions': [
                    {
                        'id': inst.id,
                        'title': inst.title,
                        'type': inst.type.value if inst.type else None,
                        'description': inst.description
                    } for inst in instructions
                ],
                'recipes': [
                    {
                        'id': recipe.id,
                        'title': recipe.title,
                        'type': recipe.type.value if recipe.type else None,
                        'description': recipe.description
                    } for recipe in recipes
                ]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(model_data)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_model_detail(model_id))
        }

def handle_instructions(method, body, headers):
    """Handle instructions endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_instructions())
        }
    
    try:
        db = get_session()
        try:
            instructions_service = InstructionsService(db)
            instructions = instructions_service.get_instructions(page=0, limit=100)
            
            result = []
            for instruction in instructions:
                instruction_data = {
                    'id': instruction.id,
                    'title': instruction.title,
                    'type': instruction.type.value if instruction.type else None,
                    'description': instruction.description,
                    'tg_file_id': instruction.tg_file_id,
                    'url': instruction.url,
                    'created_at': instruction.created_at.isoformat() if instruction.created_at else None,
                    'updated_at': instruction.updated_at.isoformat() if instruction.updated_at else None,
                    'models': [{'id': model.id, 'name': model.name} for model in instruction.models]
                }
                result.append(instruction_data)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_instructions())
        }

def handle_instruction_detail(instruction_id, headers):
    """Handle instruction detail endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_instruction_detail(instruction_id))
        }
    
    try:
        db = get_session()
        try:
            instructions_service = InstructionsService(db)
            instruction = instructions_service.get_instruction_by_id(int(instruction_id))
            
            if not instruction:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Instruction not found'})
                }
            
            instruction_data = {
                'id': instruction.id,
                'title': instruction.title,
                'type': instruction.type.value if instruction.type else None,
                'description': instruction.description,
                'tg_file_id': instruction.tg_file_id,
                'url': instruction.url,
                'created_at': instruction.created_at.isoformat() if instruction.created_at else None,
                'updated_at': instruction.updated_at.isoformat() if instruction.updated_at else None,
                'models': [{'id': model.id, 'name': model.name} for model in instruction.models]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(instruction_data)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_instruction_detail(instruction_id))
        }

def handle_recipes(method, body, headers):
    """Handle recipes endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_recipes())
        }
    
    try:
        db = get_session()
        try:
            recipes_service = RecipesService(db)
            recipes = recipes_service.get_recipes(page=0, limit=100)
            
            result = []
            for recipe in recipes:
                recipe_data = {
                    'id': recipe.id,
                    'title': recipe.title,
                    'type': recipe.type.value if recipe.type else None,
                    'description': recipe.description,
                    'tg_file_id': recipe.tg_file_id,
                    'url': recipe.url,
                    'created_at': recipe.created_at.isoformat() if recipe.created_at else None,
                    'updated_at': recipe.updated_at.isoformat() if recipe.updated_at else None,
                    'models': [{'id': model.id, 'name': model.name} for model in recipe.models]
                }
                result.append(recipe_data)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_recipes())
        }

def handle_recipe_detail(recipe_id, headers):
    """Handle recipe detail endpoint"""
    if not DB_AVAILABLE:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_recipe_detail(recipe_id))
        }
    
    try:
        db = get_session()
        try:
            recipes_service = RecipesService(db)
            recipe = recipes_service.get_recipe_by_id(int(recipe_id))
            
            if not recipe:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'error': 'Recipe not found'})
                }
            
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'type': recipe.type.value if recipe.type else None,
                'description': recipe.description,
                'tg_file_id': recipe.tg_file_id,
                'url': recipe.url,
                'created_at': recipe.created_at.isoformat() if recipe.created_at else None,
                'updated_at': recipe.updated_at.isoformat() if recipe.updated_at else None,
                'models': [{'id': model.id, 'name': model.name} for model in recipe.models]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(recipe_data)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_recipe_detail(recipe_id))
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
        
        if not DB_AVAILABLE:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(get_mock_search_results(query))
            }
        
        db = get_session()
        try:
            models_service = ModelsService(db)
            instructions_service = InstructionsService(db)
            recipes_service = RecipesService(db)
            
            # Search models
            models = models_service.search_models(query, page=0, limit=10)
            instructions = instructions_service.search_instructions(query, page=0, limit=10)
            recipes = recipes_service.search_recipes(query, page=0, limit=10)
            
            result = {
                'query': query,
                'models': [
                    {
                        'id': model.id,
                        'name': model.name,
                        'description': model.description,
                        'tags': model.tags
                    } for model in models
                ],
                'instructions': [
                    {
                        'id': inst.id,
                        'title': inst.title,
                        'type': inst.type.value if inst.type else None,
                        'description': inst.description
                    } for inst in instructions
                ],
                'recipes': [
                    {
                        'id': recipe.id,
                        'title': recipe.title,
                        'type': recipe.type.value if recipe.type else None,
                        'description': recipe.description
                    } for recipe in recipes
                ]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }
        finally:
            db.close()
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(get_mock_search_results(query if 'query' in locals() else ''))
        }

def handle_tickets(method, body, headers):
    """Handle tickets endpoint"""
    if method == 'GET':
        # Get user tickets
        user_id = request.get('queryStringParameters', {}).get('user_id')
        if not user_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'user_id required'})
            }
        
        if not DB_AVAILABLE:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(get_mock_tickets())
            }
        
        try:
            db = get_session()
            try:
                support_service = SupportService(db)
                tickets = support_service.get_user_tickets(int(user_id), limit=50)
                
                result = []
                for ticket in tickets:
                    messages = support_service.get_ticket_messages(ticket.id)
                    ticket_data = {
                        'id': ticket.id,
                        'user_id': ticket.user_id,
                        'username': ticket.username,
                        'status': ticket.status.value if ticket.status else None,
                        'subject': ticket.subject,
                        'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                        'closed_at': ticket.closed_at.isoformat() if ticket.closed_at else None,
                        'messages': [
                            {
                                'id': msg.id,
                                'from_role': msg.from_role.value if msg.from_role else None,
                                'text': msg.text,
                                'created_at': msg.created_at.isoformat() if msg.created_at else None
                            } for msg in messages
                        ]
                    }
                    result.append(ticket_data)
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(result)
                }
            finally:
                db.close()
        except Exception as e:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(get_mock_tickets())
            }
    
    elif method == 'POST':
        # Create new ticket
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
            
            if not DB_AVAILABLE:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': 1,
                        'status': 'open',
                        'created_at': datetime.now().isoformat()
                    })
                }
            
            db = get_session()
            try:
                support_service = SupportService(db)
                
                # Create ticket
                ticket = support_service.create_ticket(
                    user_id=int(user_id),
                    username=username,
                    subject=subject
                )
                
                # Add first message
                support_service.add_ticket_message(
                    ticket_id=ticket.id,
                    from_role=MessageRole.USER,
                    text=message
                )
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'id': ticket.id,
                        'status': ticket.status.value,
                        'created_at': ticket.created_at.isoformat()
                    })
                }
            finally:
                db.close()
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
            'title': 'Рецепт оптимизации MacBook',
            'type': 'pdf',
            'description': 'Способы оптимизации производительности MacBook',
            'tg_file_id': 'BAADBAADrwADBREAAYag',
            'url': None,
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 3, 'name': 'MacBook Pro M3'}]
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
        }
    }
    return recipes.get(int(recipe_id), {'error': 'Recipe not found'})

def get_mock_search_results(query):
    return {
        'query': query,
        'models': [
            {
                'id': 1,
                'name': 'iPhone 15 Pro',
                'description': 'Новейший смартфон от Apple с титановым корпусом',
                'tags': 'apple, iphone, смартфон'
            }
        ] if 'iphone' in query.lower() else [],
        'instructions': [
            {
                'id': 1,
                'title': 'Настройка iPhone 15 Pro',
                'type': 'pdf',
                'description': 'Подробная инструкция по настройке нового iPhone'
            }
        ] if 'iphone' in query.lower() else [],
        'recipes': []
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
        }
    ]
