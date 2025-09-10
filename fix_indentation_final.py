#!/usr/bin/env python3
"""Fix ALL indentation issues in bot_new.py at once"""

import re

def fix_all_indentation():
    with open('bot_new.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines for easier manipulation
    lines = content.split('\n')
    
    # Fix all problematic patterns
    fixes = [
        # Fix else blocks without proper indentation
        (r'(\s+)else:\n(\s+)await query\.edit_message_text\(', r'\1else:\n\1    await query.edit_message_text('),
        (r'(\s+)else:\n(\s+)await query\.answer\(', r'\1else:\n\1    await query.answer('),
        (r'(\s+)else:\n(\s+)await query\.edit_message_reply_markup\(', r'\1else:\n\1    await query.edit_message_reply_markup('),
        
        # Fix if blocks without proper indentation
        (r'(\s+)if not models:\n(\s+)await query\.edit_message_text\(', r'\1if not models:\n\1    await query.edit_message_text('),
        (r'(\s+)if not models:\n(\s+)await query\.answer\(', r'\1if not models:\n\1    await query.answer('),
        (r'(\s+)if not ticket:\n(\s+)await query\.answer\(', r'\1if not ticket:\n\1    await query.answer('),
        (r'(\s+)if ticket\.status == TicketStatus\.CLOSED:\n(\s+)await query\.answer\(', r'\1if ticket.status == TicketStatus.CLOSED:\n\1    await query.answer('),
        
        # Fix try blocks without proper indentation
        (r'(\s+)try:\n(\s+)if instruction\.tg_file_id:', r'\1try:\n\1    if instruction.tg_file_id:'),
        (r'(\s+)try:\n(\s+)if recipe\.tg_file_id:', r'\1try:\n\1    if recipe.tg_file_id:'),
        (r'(\s+)try:\n(\s+)models_service = ModelsService\(db\)', r'\1try:\n\1    models_service = ModelsService(db)'),
        (r'(\s+)try:\n(\s+)support_service = SupportService\(db\)', r'\1try:\n\1    support_service = SupportService(db)'),
        (r'(\s+)try:\n(\s+)recipes_service = RecipesService\(db\)', r'\1try:\n\1    recipes_service = RecipesService(db)'),
        (r'(\s+)try:\n(\s+)files_service = FilesService\(db\)', r'\1try:\n\1    files_service = FilesService(db)'),
        (r'(\s+)try:\n(\s+)app = web\.Application\(\)', r'\1try:\n\1    app = web.Application()'),
        (r'(\s+)try:\n(\s+)if MODE == \'WEBHOOK\'', r'\1try:\n\1    if MODE == \'WEBHOOK\''),
        
        # Fix await blocks without proper indentation
        (r'(\s+)await query\.edit_message_text\(\n(\s+)get_text\(', r'\1await query.edit_message_text(\n\1    get_text('),
        (r'(\s+)await query\.answer\(\n(\s+)get_text\(', r'\1await query.answer(\n\1    get_text('),
        (r'(\s+)await safe_send_message\(\n(\s+)context\.bot,', r'\1await safe_send_message(\n\1    context.bot,'),
        (r'(\s+)await context\.bot\.send_document\(\n(\s+)chat_id=query\.message\.chat\.id,', r'\1await context.bot.send_document(\n\1    chat_id=query.message.chat.id,'),
        (r'(\s+)await context\.bot\.send_video\(\n(\s+)chat_id=query\.message\.chat\.id,', r'\1await context.bot.send_video(\n\1    chat_id=query.message.chat.id,'),
        
        # Fix except blocks without proper indentation
        (r'(\s+)except Exception as e:\n(\s+)logger\.error\(', r'\1except Exception as e:\n\1    logger.error('),
        (r'(\s+)except TelegramError as e:\n(\s+)logger\.error\(', r'\1except TelegramError as e:\n\1    logger.error('),
        
        # Fix finally blocks without proper indentation
        (r'(\s+)finally:\n(\s+)db\.close\(\)', r'\1finally:\n\1    db.close()'),
        
        # Fix return statements without proper indentation
        (r'(\s+)return\n(\s+)#', r'\1return\n\1#'),
        (r'(\s+)return\n(\s+)await', r'\1return\n\1await'),
        
        # Fix comment blocks without proper indentation
        (r'(\s+)# Close the ticket\n(\s+)old_status = ticket\.status\.value', r'\1# Close the ticket\n\1old_status = ticket.status.value'),
        (r'(\s+)# Update ticket status\n(\s+)ticket = support_service\.update_ticket_status', r'\1# Update ticket status\n\1ticket = support_service.update_ticket_status'),
        (r'(\s+)# Get models and show selection keyboard\n(\s+)db = get_session\(\)', r'\1# Get models and show selection keyboard\n\1db = get_session()'),
        (r'(\s+)# Setup and start server\n(\s+)loop = asyncio\.new_event_loop\(\)', r'\1# Setup and start server\n\1loop = asyncio.new_event_loop()'),
        (r'(\s+)# Keep server running until shutdown\n(\s+)try:', r'\1# Keep server running until shutdown\n\1try:'),
        (r'(\s+)# Clear webhook and try again\n(\s+)import requests', r'\1# Clear webhook and try again\n\1import requests'),
        
        # Fix logger statements without proper indentation
        (r'(\s+)logger\.info\(f"User \{user_id\} state updated to:', r'\1logger.info(f"User {user_id} state updated to:'),
        (r'(\s+)logger\.error\(f"Error in handle_support: \{e\}"\)', r'\1logger.error(f"Error in handle_support: {e}")'),
        (r'(\s+)logger\.error\(f"Failed to notify user \{ticket\.user_id\} about status change: \{e\}"\)', r'\1logger.error(f"Failed to notify user {ticket.user_id} about status change: {e}")'),
        
        # Fix application statements without proper indentation
        (r'(\s+)application = Application\.builder\(\)\.token\(BOT_TOKEN\)\.build\(\)', r'\1application = Application.builder().token(BOT_TOKEN).build()'),
        (r'(\s+)application\.run_webhook\(\n(\s+)listen="0\.0\.0\.0",', r'\1application.run_webhook(\n\1    listen="0.0.0.0",'),
        (r'(\s+)application\.run_polling\(\n(\s+)drop_pending_updates=True,', r'\1application.run_polling(\n\1    drop_pending_updates=True,'),
        
        # Fix import statements without proper indentation
        (r'(\s+)import requests\n(\s+)try:', r'\1import requests\n\1try:'),
        
        # Fix specific problematic lines
        (r'(\s+)await query\.edit_message_text\(\n(\s+)get_text\(\'main_menu\', lang\),', r'\1await query.edit_message_text(\n\1    get_text(\'main_menu\', lang),'),
        (r'(\s+)await query\.edit_message_text\(\n(\s+)get_text\(\'admin_menu\', lang\),', r'\1await query.edit_message_text(\n\1    get_text(\'admin_menu\', lang),'),
        (r'(\s+)await query\.edit_message_text\(\n(\s+)get_text\(\'support_question\', lang\),', r'\1await query.edit_message_text(\n\1    get_text(\'support_question\', lang),'),
    ]
    
    # Apply all fixes
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Fix specific line-by-line issues
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix specific problematic lines
        if i == 424:  # Line 425 (0-indexed)
            if line.strip().startswith('await query.edit_message_text('):
                line = '                ' + line.strip()
        elif i == 561:  # Line 562 (0-indexed)
            if line.strip().startswith('await query.edit_message_text('):
                line = '            ' + line.strip()
        elif i == 566:  # Line 567 (0-indexed)
            if line.strip().startswith('await query.edit_message_text('):
                line = '            ' + line.strip()
        elif i == 572:  # Line 573 (0-indexed)
            if line.strip().startswith('db.close()'):
                line = '        ' + line.strip()
        elif i == 651:  # Line 652 (0-indexed)
            if line.strip().startswith('if instruction.tg_file_id:'):
                line = '                ' + line.strip()
        elif i == 653:  # Line 654 (0-indexed)
            if line.strip().startswith('if instruction.type == InstructionType.PDF:'):
                line = '                    ' + line.strip()
        elif i == 654:  # Line 655 (0-indexed)
            if line.strip().startswith('await context.bot.send_document('):
                line = '                        ' + line.strip()
        elif i == 655:  # Line 656 (0-indexed)
            if line.strip().startswith('chat_id=query.message.chat.id,'):
                line = '                            ' + line.strip()
        elif i == 656:  # Line 657 (0-indexed)
            if line.strip().startswith('document=instruction.tg_file_id,'):
                line = '                            ' + line.strip()
        elif i == 657:  # Line 658 (0-indexed)
            if line.strip().startswith('caption=instruction.title'):
                line = '                            ' + line.strip()
        elif i == 658:  # Line 659 (0-indexed)
            if line.strip().startswith(')'):
                line = '                        ' + line.strip()
        elif i == 659:  # Line 660 (0-indexed)
            if line.strip().startswith('elif instruction.type == InstructionType.VIDEO:'):
                line = '                    ' + line.strip()
        elif i == 660:  # Line 661 (0-indexed)
            if line.strip().startswith('await context.bot.send_video('):
                line = '                        ' + line.strip()
        elif i == 661:  # Line 662 (0-indexed)
            if line.strip().startswith('chat_id=query.message.chat.id,'):
                line = '                            ' + line.strip()
        elif i == 662:  # Line 663 (0-indexed)
            if line.strip().startswith('video=instruction.tg_file_id,'):
                line = '                            ' + line.strip()
        elif i == 663:  # Line 664 (0-indexed)
            if line.strip().startswith('caption=instruction.title'):
                line = '                            ' + line.strip()
        elif i == 664:  # Line 665 (0-indexed)
            if line.strip().startswith(')'):
                line = '                        ' + line.strip()
        elif i == 665:  # Line 666 (0-indexed)
            if line.strip().startswith('else:'):
                line = '                    ' + line.strip()
        elif i == 666:  # Line 667 (0-indexed)
            if line.strip().startswith('await context.bot.send_document('):
                line = '                        ' + line.strip()
        elif i == 667:  # Line 668 (0-indexed)
            if line.strip().startswith('chat_id=query.message.chat.id,'):
                line = '                            ' + line.strip()
        elif i == 668:  # Line 669 (0-indexed)
            if line.strip().startswith('document=instruction.tg_file_id,'):
                line = '                            ' + line.strip()
        elif i == 669:  # Line 670 (0-indexed)
            if line.strip().startswith('caption=instruction.title'):
                line = '                            ' + line.strip()
        elif i == 670:  # Line 671 (0-indexed)
            if line.strip().startswith(')'):
                line = '                        ' + line.strip()
        elif i == 671:  # Line 672 (0-indexed)
            if line.strip().startswith('elif instruction.url:'):
                line = '                ' + line.strip()
        elif i == 672:  # Line 673 (0-indexed)
            if line.strip().startswith('await safe_send_message('):
                line = '                    ' + line.strip()
        elif i == 673:  # Line 674 (0-indexed)
            if line.strip().startswith('context.bot,'):
                line = '                        ' + line.strip()
        elif i == 674:  # Line 675 (0-indexed)
            if line.strip().startswith('chat_id=query.message.chat.id,'):
                line = '                        ' + line.strip()
        elif i == 675:  # Line 676 (0-indexed)
            if line.strip().startswith('text=f"🔗 {instruction.title}\\n{instruction.url}"'):
                line = '                        ' + line.strip()
        elif i == 676:  # Line 677 (0-indexed)
            if line.strip().startswith(')'):
                line = '                    ' + line.strip()
        elif i == 677:  # Line 678 (0-indexed)
            if line.strip().startswith('# Add small delay between sends to avoid rate limiting'):
                line = '                    ' + line.strip()
        elif i == 678:  # Line 679 (0-indexed)
            if line.strip().startswith('if i < len(model.instructions) - 1:'):
                line = '                    ' + line.strip()
        elif i == 679:  # Line 680 (0-indexed)
            if line.strip().startswith('await asyncio.sleep(0.3)'):
                line = '                        ' + line.strip()
        elif i == 680:  # Line 681 (0-indexed)
            if line.strip().startswith('except Exception as e:'):
                line = '            ' + line.strip()
        elif i == 681:  # Line 682 (0-indexed)
            if line.strip().startswith('logger.error(f"Error sending instruction {instruction.id}: {e}")'):
                line = '                ' + line.strip()
        elif i == 682:  # Line 683 (0-indexed)
            if line.strip().startswith('# Continue with next instruction'):
                line = '                ' + line.strip()
        elif i == 683:  # Line 684 (0-indexed)
            if line.strip().startswith('continue'):
                line = '                ' + line.strip()
        elif i == 684:  # Line 685 (0-indexed)
            if line.strip().startswith('await query.answer(get_text(\'package_sent\', lang))'):
                line = '        ' + line.strip()
        elif i == 685:  # Line 686 (0-indexed)
            if line.strip().startswith('finally:'):
                line = '    ' + line.strip()
        elif i == 686:  # Line 687 (0-indexed)
            if line.strip().startswith('db.close()'):
                line = '        ' + line.strip()
        
        fixed_lines.append(line)
    
    # Join lines back
    content = '\n'.join(fixed_lines)
    
    # Write back to file
    with open('bot_new.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("ALL indentation issues fixed!")

if __name__ == '__main__':
    fix_all_indentation()
