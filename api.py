def handler(request):
    """Vercel serverless function handler"""
    
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
        
        # Models endpoint
        if path == '/api/models':
            models = [
                {
                    'id': 1,
                    'name': 'iPhone 15 Pro',
                    'description': 'Новейший смартфон от Apple с титановым корпусом и чипом A17 Pro',
                    'tags': 'apple, iphone, смартфон, титан'
                },
                {
                    'id': 2,
                    'name': 'Samsung Galaxy S24',
                    'description': 'Флагманский Android смартфон с ИИ функциями и камерой 200MP',
                    'tags': 'samsung, android, смартфон, камера'
                },
                {
                    'id': 3,
                    'name': 'MacBook Pro M3',
                    'description': 'Мощный ноутбук для профессионалов с чипом M3 и дисплеем Liquid Retina XDR',
                    'tags': 'apple, macbook, ноутбук, m3'
                }
            ]
            
            import json
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(models)
            }
        
        # Default response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': '{"message": "API endpoint not found", "path": "' + path + '"}'
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': '{"error": "' + str(e) + '"}'
        }
