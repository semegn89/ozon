def handler(request):
    """Vercel serverless function handler"""
    
    # Mock data
    mock_data = {
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
            }
        ]
    }
    
    # Get request details
    path = request.get('path', '/')
    method = request.get('httpMethod', 'GET')
    
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
        # Test endpoint
        if path == '/api/test':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': '{"message": "API is working!", "status": "ok", "timestamp": "2024-01-01T00:00:00Z"}'
            }
        
        # Health check
        if path == '/api/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': '{"status": "ok", "timestamp": "2024-01-01T00:00:00Z", "storage": {"models": 4, "instructions": 2, "recipes": 1}}'
            }
        
        # Models endpoint
        if path == '/api/models':
            import json
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(mock_data['models'])
            }
        
        # Instructions endpoint
        if path == '/api/instructions':
            import json
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(mock_data['instructions'])
            }
        
        # Recipes endpoint
        if path == '/api/recipes':
            import json
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(mock_data['recipes'])
            }
        
        # Model detail endpoint
        if path.startswith('/api/models/') and method == 'GET':
            import json
            model_id = int(path.split('/')[-1])
            model = next((m for m in mock_data['models'] if m['id'] == model_id), None)
            if model:
                # Add related instructions and recipes
                model['instructions'] = [i for i in mock_data['instructions'] if i['model_id'] == model_id]
                model['recipes'] = [r for r in mock_data['recipes'] if r['model_id'] == model_id]
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(model)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': '{"error": "Model not found"}'
                }
        
        # Search endpoint
        if path == '/api/search' and method == 'POST':
            import json
            body = request.get('body', '')
            data = json.loads(body) if body else {}
            query = data.get('query', '').strip().lower()
            
            if not query:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': '{"error": "Query is required"}'
                }
            
            # Search in all data
            results = {
                'query': query,
                'models': [m for m in mock_data['models'] 
                          if query in m['name'].lower() or 
                             query in m['description'].lower() or 
                             query in m['tags'].lower()],
                'instructions': [i for i in mock_data['instructions'] 
                               if query in i['title'].lower() or 
                                  query in i['description'].lower()],
                'recipes': [r for r in mock_data['recipes'] 
                          if query in r['title'].lower() or 
                             query in r['description'].lower()]
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(results)
            }
        
        # Tickets endpoint
        if path == '/api/tickets':
            import json
            if method == 'GET':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': '[]'
                }
            elif method == 'POST':
                body = request.get('body', '')
                data = json.loads(body) if body else {}
                new_ticket = {
                    'id': 1,
                    'user_id': data.get('user_id'),
                    'username': data.get('username'),
                    'subject': data.get('subject', ''),
                    'status': 'open',
                    'created_at': '2024-01-01T00:00:00Z',
                    'closed_at': None,
                    'messages': [{
                        'id': 1,
                        'from_role': 'user',
                        'text': data.get('message', ''),
                        'created_at': '2024-01-01T00:00:00Z'
                    }]
                }
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps(new_ticket)
                }
        
        # Default response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': '{"message": "API endpoint not found", "path": "' + path + '", "method": "' + method + '"}'
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': '{"error": "' + str(e) + '", "message": "Internal server error"}'
        }