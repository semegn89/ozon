#!/usr/bin/env python3
"""
API endpoints for Telegram Mini App - Vercel deployment
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test API endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'API работает!',
        'timestamp': '2024-01-01T00:00:00Z'
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get all models - mock data"""
    return jsonify([
        {
            'id': 1,
            'name': 'Тестовая модель 1',
            'description': 'Описание модели 1',
            'tags': 'тест, модель',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions': [{'id': 1}]
        },
        {
            'id': 2,
            'name': 'Тестовая модель 2',
            'description': 'Описание модели 2',
            'tags': 'тест, модель',
            'created_at': '2024-01-01T00:00:00Z',
            'instructions': [{'id': 2}]
        }
    ])

@app.route('/api/instructions', methods=['GET'])
def get_instructions():
    """Get all instructions - mock data"""
    return jsonify([
        {
            'id': 1,
            'title': 'Тестовая инструкция 1',
            'type': 'pdf',
            'description': 'Описание инструкции 1',
            'created_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1}]
        }
    ])

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes - mock data"""
    return jsonify([
        {
            'id': 1,
            'title': 'Тестовый рецепт 1',
            'type': 'video',
            'description': 'Описание рецепта 1',
            'created_at': '2024-01-01T00:00:00Z',
            'models': [{'id': 1}]
        }
    ])

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get user tickets - mock data"""
    return jsonify([
        {
            'id': 1,
            'user_id': 123456,
            'username': 'test_user',
            'status': 'open',
            'subject': 'Тестовый тикет',
            'created_at': '2024-01-01T00:00:00Z',
            'messages': [
                {
                    'id': 1,
                    'from_role': 'user',
                    'text': 'Тестовое сообщение',
                    'created_at': '2024-01-01T00:00:00Z'
                }
            ]
        }
    ])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'webapp-api'})

# Vercel entry point
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)