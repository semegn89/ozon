def handler(request):
    """Vercel serverless function handler - minimal version"""
    
    # Always return success for any request
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message": "API is working!", "status": "ok"}'
    }