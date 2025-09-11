#!/usr/bin/env python3
"""
API endpoints for Telegram Mini App
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import get_session, InstructionType, TicketStatus, MessageRole
from services.models_service import ModelsService
from services.instructions_service import InstructionsService
from services.recipes_service import RecipesService
from services.support_service import SupportService

app = Flask(__name__)
CORS(app)

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get all models"""
    try:
        db = get_session()
        try:
            models_service = ModelsService(db)
            models = models_service.get_models(page=0, limit=100)
            
            # Convert to JSON-serializable format
            result = []
            for model in models:
                model_data = {
                    'id': model.id,
                    'name': model.name,
                    'description': model.description,
                    'tags': model.tags,
                    'created_at': model.created_at.isoformat() if model.created_at else None,
                    'updated_at': model.updated_at.isoformat() if model.updated_at else None,
                    'instructions': [{'id': inst.id} for inst in model.instructions]
                }
                result.append(model_data)
            
            return jsonify(result)
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/instructions', methods=['GET'])
def get_instructions():
    """Get all instructions"""
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
                    'models': [{'id': model.id} for model in instruction.models]
                }
                result.append(instruction_data)
            
            return jsonify(result)
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
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
                    'models': [{'id': model.id} for model in recipe.models]
                }
                result.append(recipe_data)
            finally:
                db.close()
            
            return jsonify(result)
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get user tickets"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        db = get_session()
        try:
            support_service = SupportService(db)
            tickets = support_service.get_user_tickets(user_id, limit=50)
            
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
            
            return jsonify(result)
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create new ticket"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        user_id = data.get('user_id')
        username = data.get('username')
        subject = data.get('subject', '')
        message = data.get('message', '')
        
        if not user_id or not message:
            return jsonify({'error': 'user_id and message required'}), 400
        
        db = get_session()
        try:
            support_service = SupportService(db)
            
            # Create ticket
            ticket = support_service.create_ticket(
                user_id=user_id,
                username=username,
                subject=subject
            )
            
            # Add first message
            support_service.add_ticket_message(
                ticket_id=ticket.id,
                from_role=MessageRole.USER,
                text=message
            )
            
            return jsonify({
                'id': ticket.id,
                'status': ticket.status.value,
                'created_at': ticket.created_at.isoformat()
            })
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/instruction/<int:instruction_id>/download', methods=['GET'])
def download_instruction(instruction_id):
    """Download instruction file"""
    try:
        db = get_session()
        try:
            instructions_service = InstructionsService(db)
            instruction = instructions_service.get_instruction_by_id(instruction_id)
            
            if not instruction:
                return jsonify({'error': 'Instruction not found'}), 404
            
            if not instruction.tg_file_id:
                return jsonify({'error': 'File not available'}), 404
            
            return jsonify({
                'tg_file_id': instruction.tg_file_id,
                'title': instruction.title,
                'type': instruction.type.value if instruction.type else None
            })
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipe/<int:recipe_id>/download', methods=['GET'])
def download_recipe(recipe_id):
    """Download recipe file"""
    try:
        db = get_session()
        try:
            recipes_service = RecipesService(db)
            recipe = recipes_service.get_recipe_by_id(recipe_id)
            
            if not recipe:
                return jsonify({'error': 'Recipe not found'}), 404
            
            if not recipe.tg_file_id:
                return jsonify({'error': 'File not available'}), 404
            
            return jsonify({
                'tg_file_id': recipe.tg_file_id,
                'title': recipe.title,
                'type': recipe.type.value if recipe.type else None
            })
        finally:
            db.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'webapp-api'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
