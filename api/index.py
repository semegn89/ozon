def handler(request):
    """Vercel serverless function handler"""
    import json
    
    # Get the path from the request
    path = request.get('path', '/')
    
    # Handle different routes
    if path == '/api/test':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'status': 'ok',
                'message': 'API работает!',
                'path': path
            })
        }
    
    elif path == '/api/models':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps([
                {
                    'id': 1,
                    'name': 'Тестовая модель 1',
                    'description': 'Описание модели 1'
                },
                {
                    'id': 2,
                    'name': 'Тестовая модель 2',
                    'description': 'Описание модели 2'
                }
            ])
        }
    
    elif path == '/health':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'status': 'ok', 'service': 'webapp-api'})
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Not found', 'path': path})
        }