#!/usr/bin/env python3
"""
API endpoints for Telegram Mini App - Vercel deployment
Mock data for quick deployment
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock data - in production, this would be a database
MOCK_DATA = {
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

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test endpoint"""
    return jsonify({
        'message': 'API is working!',
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'storage': {
            'models': len(MOCK_DATA['models']),
            'instructions': len(MOCK_DATA['instructions']),
            'recipes': len(MOCK_DATA['recipes']),
            'tickets': len(MOCK_DATA['tickets'])
        }
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get all models"""
    return jsonify(MOCK_DATA['models'])

@app.route('/api/models/<int:model_id>', methods=['GET'])
def get_model_detail(model_id):
    """Get model with instructions and recipes"""
    model = next((m for m in MOCK_DATA['models'] if m['id'] == model_id), None)
    if not model:
        return jsonify({'error': 'Model not found'}), 404
    
    # Add related instructions and recipes
    model['instructions'] = [i for i in MOCK_DATA['instructions'] if i['model_id'] == model_id]
    model['recipes'] = [r for r in MOCK_DATA['recipes'] if r['model_id'] == model_id]
    
    return jsonify(model)

@app.route('/api/instructions', methods=['GET'])
def get_instructions():
    """Get all instructions"""
    return jsonify(MOCK_DATA['instructions'])

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    return jsonify(MOCK_DATA['recipes'])

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get tickets for user"""
    user_id = request.args.get('user_id')
    if user_id:
        user_tickets = [t for t in MOCK_DATA['tickets'] if t['user_id'] == int(user_id)]
        return jsonify(user_tickets)
    return jsonify(MOCK_DATA['tickets'])

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create new ticket"""
    data = request.json
    new_ticket = {
        'id': max([t['id'] for t in MOCK_DATA['tickets']], default=0) + 1,
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
    MOCK_DATA['tickets'].append(new_ticket)
    return jsonify(new_ticket), 201

@app.route('/api/search', methods=['POST'])
def search():
    """Search in all data"""
    data = request.json
    query = data.get('query', '').strip().lower()
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    results = {
        'query': query,
        'models': [m for m in MOCK_DATA['models'] 
                  if query in m['name'].lower() or 
                     query in m['description'].lower() or 
                     query in m['tags'].lower()],
        'instructions': [i for i in MOCK_DATA['instructions'] 
                       if query in i['title'].lower() or 
                          query in i['description'].lower()],
        'recipes': [r for r in MOCK_DATA['recipes'] 
                  if query in r['title'].lower() or 
                     query in r['description'].lower()]
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)