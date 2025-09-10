#!/usr/bin/env python3
"""
Final indentation fix for bot_new.py
"""

def fix_indentation():
    with open('bot_new.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Fix specific problematic lines
        if line_num == 362:
            # Fix the else block indentation
            if line.strip() == 'await query.edit_message_text(':
                fixed_lines.append('                await query.edit_message_text(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 492:
            # Fix the if not models block
            if line.strip() == 'await query.edit_message_text(':
                fixed_lines.append('            await query.edit_message_text(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 577:
            # Fix the if instruction.tg_file_id block
            if line.strip() == 'if instruction.tg_file_id:':
                fixed_lines.append('                if instruction.tg_file_id:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1124:
            # Fix the else block in message_handler
            if line.strip() == 'await update.message.reply_text(':
                fixed_lines.append('            await update.message.reply_text(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1353:
            # Fix the tg_file_id assignment
            if line.strip() == 'tg_file_id = None':
                fixed_lines.append('    tg_file_id = None\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1356:
            # Fix the if update.message.document block
            if line.strip() == 'if update.message.document:':
                fixed_lines.append('    if update.message.document:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1357:
            # Fix the tg_file_id assignment inside if
            if line.strip() == 'tg_file_id = update.message.document.file_id':
                fixed_lines.append('        tg_file_id = update.message.document.file_id\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1358:
            # Fix the file_size assignment
            if line.strip() == 'file_size = update.message.document.file_size or 0':
                fixed_lines.append('        file_size = update.message.document.file_size or 0\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1359:
            # Fix the file_name assignment
            if line.strip() == 'file_name = update.message.document.file_name or "document"':
                fixed_lines.append('        file_name = update.message.document.file_name or "document"\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1360:
            # Fix the logger.info line
            if line.strip() == 'logger.info(f"Admin {user_id} sent document: {file_name}, size: {file_size}")':
                fixed_lines.append('        logger.info(f"Admin {user_id} sent document: {file_name}, size: {file_size}")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1361:
            # Fix the elif update.message.video block
            if line.strip() == 'elif update.message.video:':
                fixed_lines.append('    elif update.message.video:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1362:
            # Fix the tg_file_id assignment for video
            if line.strip() == 'tg_file_id = update.message.video.file_id':
                fixed_lines.append('        tg_file_id = update.message.video.file_id\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1363:
            # Fix the file_size assignment for video
            if line.strip() == 'file_size = update.message.video.file_size or 0':
                fixed_lines.append('        file_size = update.message.video.file_size or 0\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1364:
            # Fix the file_name assignment for video
            if line.strip() == 'file_name = update.message.video.file_name or "video"':
                fixed_lines.append('        file_name = update.message.video.file_name or "video"\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1365:
            # Fix the logger.info line for video
            if line.strip() == 'logger.info(f"Admin {user_id} sent video: {file_name}, size: {file_size}")':
                fixed_lines.append('        logger.info(f"Admin {user_id} sent video: {file_name}, size: {file_size}")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1366:
            # Fix the elif update.message.photo block
            if line.strip() == 'elif update.message.photo:':
                fixed_lines.append('    elif update.message.photo:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1367:
            # Fix the tg_file_id assignment for photo
            if line.strip() == 'tg_file_id = update.message.photo[-1].file_id':
                fixed_lines.append('        tg_file_id = update.message.photo[-1].file_id\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1368:
            # Fix the file_size assignment for photo
            if line.strip() == 'file_size = update.message.photo[-1].file_size or 0':
                fixed_lines.append('        file_size = update.message.photo[-1].file_size or 0\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1369:
            # Fix the file_name assignment for photo
            if line.strip() == 'file_name = "photo.jpg"  # Photos don\'t have file names':
                fixed_lines.append('        file_name = "photo.jpg"  # Photos don\'t have file names\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1370:
            # Fix the logger.info line for photo
            if line.strip() == 'logger.info(f"Admin {user_id} sent photo, size: {file_size}")':
                fixed_lines.append('        logger.info(f"Admin {user_id} sent photo, size: {file_size}")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1371:
            # Fix the else block
            if line.strip() == 'else:':
                fixed_lines.append('    else:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1373:
            # Fix the await update.message.reply_text line
            if line.strip() == 'await update.message.reply_text(':
                fixed_lines.append('        await update.message.reply_text(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1374:
            # Fix the message text line
            if line.strip() == '"Пожалуйста, пришлите файл. Для отмены — нажмите ❌ Отмена.",':
                fixed_lines.append('            "Пожалуйста, пришлите файл. Для отмены — нажмите ❌ Отмена.",\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1375:
            # Fix the reply_markup line
            if line.strip() == 'reply_markup=back_cancel_keyboard(lang)':
                fixed_lines.append('            reply_markup=back_cancel_keyboard(lang)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1376:
            # Fix the closing parenthesis
            if line.strip() == ')':
                fixed_lines.append('        )\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1377:
            # Fix the return statement
            if line.strip() == 'return':
                fixed_lines.append('        return\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1762:
            # Fix the if user_id in user_states block
            if line.strip() == 'if user_id in user_states:':
                fixed_lines.append('    if user_id in user_states:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 1763:
            # Fix the del user_states[user_id] line
            if line.strip() == 'del user_states[user_id]':
                fixed_lines.append('        del user_states[user_id]\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2066:
            # Fix the app = web.Application() line
            if line.strip() == 'app = web.Application()':
                fixed_lines.append('        app = web.Application()\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2067:
            # Fix the app.router.add_get line
            if line.strip() == 'app.router.add_get(\'/health\', healthcheck_handler)':
                fixed_lines.append('        app.router.add_get(\'/health\', healthcheck_handler)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2068:
            # Fix the second app.router.add_get line
            if line.strip() == 'app.router.add_get(\'/\', healthcheck_handler)':
                fixed_lines.append('        app.router.add_get(\'/\', healthcheck_handler)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2069:
            # Fix the runner = web.AppRunner line
            if line.strip() == 'runner = web.AppRunner(app)':
                fixed_lines.append('        runner = web.AppRunner(app)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2070:
            # Fix the loop = asyncio.new_event_loop line
            if line.strip() == 'loop = asyncio.new_event_loop()':
                fixed_lines.append('        loop = asyncio.new_event_loop()\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2071:
            # Fix the asyncio.set_event_loop line
            if line.strip() == 'asyncio.set_event_loop(loop)':
                fixed_lines.append('        asyncio.set_event_loop(loop)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2073:
            # Fix the loop.run_until_complete line
            if line.strip() == 'loop.run_until_complete(runner.setup())':
                fixed_lines.append('        loop.run_until_complete(runner.setup())\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2074:
            # Fix the site = web.TCPSite line
            if line.strip() == 'site = web.TCPSite(runner, \'0.0.0.0\', 8080)':
                fixed_lines.append('        site = web.TCPSite(runner, \'0.0.0.0\', 8080)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2075:
            # Fix the loop.run_until_complete(site.start()) line
            if line.strip() == 'loop.run_until_complete(site.start())':
                fixed_lines.append('        loop.run_until_complete(site.start())\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2076:
            # Fix the logger.info line
            if line.strip() == 'logger.info("Healthcheck server started on port 8080")':
                fixed_lines.append('        logger.info("Healthcheck server started on port 8080")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2078:
            # Fix the try block
            if line.strip() == 'try:':
                fixed_lines.append('        try:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2079:
            # Fix the while loop
            if line.strip() == 'while not shutdown_event.is_set():':
                fixed_lines.append('            while not shutdown_event.is_set():\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2080:
            # Fix the loop.run_until_complete(asyncio.sleep(1)) line
            if line.strip() == 'loop.run_until_complete(asyncio.sleep(1))':
                fixed_lines.append('                loop.run_until_complete(asyncio.sleep(1))\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2081:
            # Fix the except KeyboardInterrupt block
            if line.strip() == 'except KeyboardInterrupt:':
                fixed_lines.append('        except KeyboardInterrupt:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2082:
            # Fix the logger.info line in except
            if line.strip() == 'logger.info("Healthcheck server stopping...")':
                fixed_lines.append('            logger.info("Healthcheck server stopping...")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2083:
            # Fix the finally block
            if line.strip() == 'finally:':
                fixed_lines.append('        finally:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2084:
            # Fix the loop.run_until_complete(runner.cleanup()) line
            if line.strip() == 'loop.run_until_complete(runner.cleanup())':
                fixed_lines.append('            loop.run_until_complete(runner.cleanup())\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2085:
            # Fix the loop.stop() line
            if line.strip() == 'loop.stop()':
                fixed_lines.append('            loop.stop()\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2086:
            # Fix the logger.info line in finally
            if line.strip() == 'logger.info("Healthcheck server stopped")':
                fixed_lines.append('            logger.info("Healthcheck server stopped")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2087:
            # Fix the except Exception block
            if line.strip() == 'except Exception as e:':
                fixed_lines.append('    except Exception as e:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2088:
            # Fix the logger.error line
            if line.strip() == 'logger.error(f"Healthcheck server error: {e}")':
                fixed_lines.append('        logger.error(f"Healthcheck server error: {e}")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2187:
            # Fix the if MODE == 'WEBHOOK' block
            if line.strip() == 'if MODE == \'WEBHOOK\' and WEBHOOK_URL:':
                fixed_lines.append('        if MODE == \'WEBHOOK\' and WEBHOOK_URL:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2188:
            # Fix the logger.info line
            if line.strip() == 'logger.info("🌐 Starting bot in webhook mode...")':
                fixed_lines.append('            logger.info("🌐 Starting bot in webhook mode...")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2189:
            # Fix the application.run_webhook line
            if line.strip() == 'application.run_webhook(':
                fixed_lines.append('            application.run_webhook(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2190:
            # Fix the listen parameter
            if line.strip() == 'listen="0.0.0.0",':
                fixed_lines.append('                listen="0.0.0.0",\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2191:
            # Fix the port parameter
            if line.strip() == 'port=8443,':
                fixed_lines.append('                port=8443,\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2192:
            # Fix the webhook_url parameter
            if line.strip() == 'webhook_url=WEBHOOK_URL':
                fixed_lines.append('                webhook_url=WEBHOOK_URL\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2193:
            # Fix the closing parenthesis
            if line.strip() == ')':
                fixed_lines.append('            )\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2194:
            # Fix the else block
            if line.strip() == 'else:':
                fixed_lines.append('        else:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2195:
            # Fix the logger.info line in else
            if line.strip() == 'logger.info("📡 Starting bot in polling mode...")':
                fixed_lines.append('            logger.info("📡 Starting bot in polling mode...")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2197:
            # Fix the time.sleep line
            if line.strip() == 'time.sleep(2)':
                fixed_lines.append('            time.sleep(2)\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2198:
            # Fix the application.run_polling line
            if line.strip() == 'application.run_polling(':
                fixed_lines.append('            application.run_polling(\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2199:
            # Fix the drop_pending_updates parameter
            if line.strip() == 'drop_pending_updates=True,':
                fixed_lines.append('                drop_pending_updates=True,\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2200:
            # Fix the allowed_updates parameter
            if line.strip() == 'allowed_updates=["message", "callback_query"]':
                fixed_lines.append('                allowed_updates=["message", "callback_query"]\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2201:
            # Fix the closing parenthesis
            if line.strip() == ')':
                fixed_lines.append('            )\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2202:
            # Fix the except Exception block
            if line.strip() == 'except Exception as e:':
                fixed_lines.append('    except Exception as e:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2203:
            # Fix the logger.error line
            if line.strip() == 'logger.error(f"Bot error: {e}")':
                fixed_lines.append('        logger.error(f"Bot error: {e}")\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2204:
            # Fix the finally block
            if line.strip() == 'finally:':
                fixed_lines.append('    finally:\n')
            else:
                fixed_lines.append(line)
        elif line_num == 2205:
            # Fix the logger.info line in finally
            if line.strip() == 'logger.info("Bot stopped")':
                fixed_lines.append('        logger.info("Bot stopped")\n')
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write the fixed file
    with open('bot_new.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Indentation fixed!")

if __name__ == "__main__":
    fix_indentation()
