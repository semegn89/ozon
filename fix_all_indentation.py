#!/usr/bin/env python3
"""Fix all indentation issues in bot_new.py"""

import re

def fix_indentation():
    with open('bot_new.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix specific problematic lines
    fixes = [
        # Line 426 - fix else block
        (425, "            else:\n"),
        (426, "                await query.edit_message_text(\n"),
        (427, "                    get_text('main_menu', lang),\n"),
        (428, "                    reply_markup=main_menu_keyboard(lang)\n"),
        (429, "                )\n"),
        
        # Line 551 - fix try block
        (550, "    try:\n"),
        (551, "        models_service = ModelsService(db)\n"),
        
        # Line 563 - fix if block
        (562, "        if not models:\n"),
        (563, "            await query.edit_message_text(\n"),
        
        # Line 567 - fix else block
        (566, "        else:\n"),
        (567, "            await query.edit_message_text(\n"),
        
        # Line 573 - fix finally block
        (572, "    finally:\n"),
        (573, "        db.close()\n"),
        
        # Line 653 - fix try block
        (652, "            try:\n"),
        (653, "                if instruction.tg_file_id:\n"),
        
        # Line 654 - fix if block
        (653, "                if instruction.tg_file_id:\n"),
        (654, "                    if instruction.type == InstructionType.PDF:\n"),
        
        # Line 682 - fix elif block
        (681, "                elif instruction.url:\n"),
        (682, "                    await safe_send_message(\n"),
        
        # Line 683 - fix indentation
        (682, "                    await safe_send_message(\n"),
        (683, "                        context.bot,\n"),
        
        # Line 694 - fix try block
        (693, "    try:\n"),
        (694, "        support_service = SupportService(db)\n"),
        
        # Line 715 - fix await block
        (714, "    await query.edit_message_text(\n"),
        (715, "        get_text('support_question', lang),\n"),
        (716, "        reply_markup=cancel_keyboard(lang)\n"),
        (717, "    )\n"),
        
        # Line 721 - fix except block
        (720, "    except Exception as e:\n"),
        (721, "        logger.error(f\"Error in handle_support: {e}\")\n"),
        (722, "        await query.edit_message_text(\n"),
        
        # Line 1619 - fix else block
        (1618, "        else:\n"),
        (1619, "            await query.edit_message_text(\n"),
        
        # Line 2003 - fix try block
        (2002, "    try:\n"),
        (2003, "        support_service = SupportService(db)\n"),
        
        # Line 2007 - fix if block
        (2006, "        if not ticket:\n"),
        (2007, "            await query.answer(\"Тикет не найден!\", show_alert=True)\n"),
        
        # Line 2011 - fix return
        (2010, "            return\n"),
        (2011, "        \n"),
        
        # Line 2014 - fix if block
        (2013, "        if ticket.status == TicketStatus.CLOSED:\n"),
        (2014, "            await query.answer(\"Тикет уже закрыт!\", show_alert=True)\n"),
        
        # Line 2020 - fix return
        (2019, "            return\n"),
        (2020, "        \n"),
        
        # Line 2021 - fix comment
        (2020, "        \n"),
        (2021, "        # Close the ticket\n"),
        
        # Line 2089 - fix indentation
        (2088, "        \n"),
        (2089, "        # Update ticket status\n"),
        
        # Line 2092 - fix indentation
        (2091, "        \n"),
        (2092, "        ticket = support_service.update_ticket_status(ticket_id, TicketStatus.IN_PROGRESS)\n"),
        
        # Line 2097 - fix if block
        (2096, "        if ticket:\n"),
        (2097, "            # Notify user about status change\n"),
        
        # Line 2098 - fix try block
        (2097, "            # Notify user about status change\n"),
        (2098, "            try:\n"),
        
        # Line 2102 - fix await block
        (2101, "                await safe_send_message(\n"),
        (2102, "                    query.bot,\n"),
        
        # Line 2103 - fix await block
        (2102, "                    query.bot,\n"),
        (2103, "                    chat_id=ticket.user_id,\n"),
        
        # Line 2107 - fix await block
        (2106, "                )\n"),
        (2107, "            except TelegramError as e:\n"),
        
        # Line 2109 - fix logger
        (2108, "                logger.error(f\"Failed to notify user {ticket.user_id} about status change: {e}\")\n"),
        (2109, "            \n"),
        
        # Line 2115 - fix await block
        (2114, "            \n"),
        (2115, "            await query.edit_message_text(\n"),
        
        # Line 2178 - fix else block
        (2177, "        else:\n"),
        (2178, "            await query.edit_message_text(\n"),
        
        # Line 2182 - fix indentation
        (2181, "            )\n"),
        (2182, "    finally:\n"),
        
        # Line 2589 - fix indentation
        (2588, "        \n"),
        (2589, "        # Get models and show selection keyboard\n"),
        
        # Line 2896 - fix try block
        (2895, "    try:\n"),
        (2896, "        app = web.Application()\n"),
        
        # Line 2897 - fix app setup
        (2896, "        app = web.Application()\n"),
        (2897, "        app.router.add_get('/health', healthcheck_handler)\n"),
        
        # Line 2901 - fix indentation
        (2900, "        \n"),
        (2901, "        loop = asyncio.new_event_loop()\n"),
        
        # Line 2909 - fix indentation
        (2908, "        \n"),
        (2909, "        # Setup and start server\n"),
        
        # Line 2918 - fix await block
        (2917, "        \n"),
        (2918, "        # Keep server running until shutdown\n"),
        
        # Line 2919 - fix try block
        (2918, "        # Keep server running until shutdown\n"),
        (2919, "        try:\n"),
        
        # Line 3593 - fix try block
        (3592, "    try:\n"),
        (3593, "        if MODE == 'WEBHOOK' and WEBHOOK_URL:\n"),
        
        # Line 3594 - fix if block
        (3593, "        if MODE == 'WEBHOOK' and WEBHOOK_URL:\n"),
        (3594, "            logger.info(\"🌐 Starting bot in webhook mode...\")\n"),
        
        # Line 3596 - fix indentation
        (3595, "            \n"),
        (3596, "            application.run_webhook(\n"),
        
        # Line 3601 - fix else block
        (3600, "        else:\n"),
        (3601, "            logger.info(\"📡 Starting bot in polling mode...\")\n"),
        
        # Line 3602 - fix indentation
        (3601, "            logger.info(\"📡 Starting bot in polling mode...\")\n"),
        (3602, "            # Add a small delay to avoid immediate conflicts\n"),
        
        # Line 3610 - fix await block
        (3609, "            \n"),
        (3610, "            application.run_polling(\n"),
        
        # Line 3611 - fix indentation
        (3610, "            application.run_polling(\n"),
        (3611, "                drop_pending_updates=True,\n"),
        
        # Line 3621 - fix application
        (3620, "        \n"),
        (3621, "        application = Application.builder().token(BOT_TOKEN).build()\n"),
        
        # Line 3626 - fix except block
        (3625, "    except Conflict as e:\n"),
        (3626, "        logger.error(f\"Bot conflict detected: {e}\")\n"),
        
        # Line 3627 - fix indentation
        (3626, "        logger.error(f\"Bot conflict detected: {e}\")\n"),
        (3627, "        logger.info(\"Attempting to clear webhook and restart...\")\n"),
        
        # Line 3629 - fix indentation
        (3628, "        \n"),
        (3629, "        # Clear webhook and try again\n"),
    ]
    
    # Apply fixes
    for line_num, new_content in fixes:
        if line_num < len(lines):
            lines[line_num] = new_content
    
    # Write back to file
    with open('bot_new.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Indentation fixes applied")

if __name__ == '__main__':
    fix_indentation()
