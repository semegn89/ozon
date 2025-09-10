#!/usr/bin/env python3
"""Simple fix for indentation issues"""

import re

def fix_simple():
    with open('bot_new.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the most common patterns
    patterns = [
        # Fix else blocks
        (r'(\s+)else:\n(\s+)await query\.edit_message_text\(', r'\1else:\n\1    await query.edit_message_text('),
        (r'(\s+)else:\n(\s+)await query\.answer\(', r'\1else:\n\1    await query.answer('),
        
        # Fix if blocks
        (r'(\s+)if not models:\n(\s+)await query\.edit_message_text\(', r'\1if not models:\n\1    await query.edit_message_text('),
        (r'(\s+)if not ticket:\n(\s+)await query\.answer\(', r'\1if not ticket:\n\1    await query.answer('),
        
        # Fix try blocks
        (r'(\s+)try:\n(\s+)if instruction\.tg_file_id:', r'\1try:\n\1    if instruction.tg_file_id:'),
        (r'(\s+)try:\n(\s+)models_service = ModelsService\(db\)', r'\1try:\n\1    models_service = ModelsService(db)'),
        
        # Fix await blocks
        (r'(\s+)await query\.edit_message_text\(\n(\s+)get_text\(', r'\1await query.edit_message_text(\n\1    get_text('),
        (r'(\s+)await query\.answer\(\n(\s+)get_text\(', r'\1await query.answer(\n\1    get_text('),
        
        # Fix except blocks
        (r'(\s+)except Exception as e:\n(\s+)logger\.error\(', r'\1except Exception as e:\n\1    logger.error('),
        
        # Fix finally blocks
        (r'(\s+)finally:\n(\s+)db\.close\(\)', r'\1finally:\n\1    db.close()'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    with open('bot_new.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Simple fixes applied")

if __name__ == '__main__':
    fix_simple()
