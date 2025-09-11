def handler(request):
    """Vercel serverless function handler"""
    import json
    
    # Get the path from the request
    path = request.get('path', '/')
    method = request.get('httpMethod', 'GET')
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    # Set common headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle different routes
    if path == '/api/test':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'ok',
                'message': 'API работает!',
                'path': path,
                'timestamp': '2024-01-01T00:00:00Z'
            })
        }
    
    elif path == '/api/models':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps([
                {
                    'id': 1,
                    'name': 'iPhone 15 Pro',
                    'description': 'Новейший смартфон от Apple с титановым корпусом',
                    'tags': 'apple, iphone, смартфон',
                    'created_at': '2024-01-01T00:00:00Z',
                    'instructions': [{'id': 1}, {'id': 2}]
                },
                {
                    'id': 2,
                    'name': 'Samsung Galaxy S24',
                    'description': 'Флагманский Android смартфон с ИИ функциями',
                    'tags': 'samsung, android, смартфон',
                    'created_at': '2024-01-01T00:00:00Z',
                    'instructions': [{'id': 3}]
                },
                {
                    'id': 3,
                    'name': 'MacBook Pro M3',
                    'description': 'Мощный ноутбук для профессионалов',
                    'tags': 'apple, macbook, ноутбук',
                    'created_at': '2024-01-01T00:00:00Z',
                    'instructions': [{'id': 4}, {'id': 5}]
                }
            ])
        }
    
    elif path == '/api/instructions':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps([
                {
                    'id': 1,
                    'title': 'Настройка iPhone 15 Pro',
                    'type': 'pdf',
                    'description': 'Подробная инструкция по настройке нового iPhone',
                    'created_at': '2024-01-01T00:00:00Z',
                    'models': [{'id': 1}]
                },
                {
                    'id': 2,
                    'title': 'Перенос данных на iPhone',
                    'type': 'video',
                    'description': 'Видео-инструкция по переносу данных',
                    'created_at': '2024-01-01T00:00:00Z',
                    'models': [{'id': 1}]
                },
                {
                    'id': 3,
                    'title': 'Настройка Samsung Galaxy S24',
                    'type': 'pdf',
                    'description': 'Инструкция по настройке Samsung Galaxy',
                    'created_at': '2024-01-01T00:00:00Z',
                    'models': [{'id': 2}]
                }
            ])
        }
    
    elif path == '/api/recipes':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps([
                {
                    'id': 1,
                    'title': 'Рецепт восстановления iPhone',
                    'type': 'video',
                    'description': 'Пошаговое восстановление iPhone через iTunes',
                    'created_at': '2024-01-01T00:00:00Z',
                    'models': [{'id': 1}]
                },
                {
                    'id': 2,
                    'title': 'Рецепт оптимизации MacBook',
                    'type': 'pdf',
                    'description': 'Способы оптимизации производительности MacBook',
                    'created_at': '2024-01-01T00:00:00Z',
                    'models': [{'id': 3}]
                }
            ])
        }
    
    elif path == '/health':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'status': 'ok', 'service': 'webapp-api'})
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not found', 'path': path})
        }