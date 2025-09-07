import logging
import math
import signal
import sys
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
from telegram.error import TelegramError, Conflict
import asyncio
from datetime import datetime, timedelta
from aiohttp import web
import threading
import time

# Import our modules
from config import BOT_TOKEN, ADMIN_CHAT_IDS, MODE, WEBHOOK_URL
from models import create_tables, get_session, InstructionType, TicketStatus, MessageRole, FileType
from services.models_service import ModelsService
from services.files_service import FilesService
from services.support_service import SupportService
from services.instructions_service import InstructionsService
from keyboards import *
from texts import get_text

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User states for conversation flows
user_states = {}

class UserState:
    def __init__(self, state: str, data: dict = None):
        self.state = state
        self.data = data or {}

# Global variables for graceful shutdown
shutdown_event = threading.Event()
application_instance = None

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_CHAT_IDS

def get_user_lang(user_id: int) -> str:
    """Get user language (default: ru)"""
    # TODO: Implement language preference storage
    return 'ru'

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()
    if application_instance:
        try:
            # Stop the application gracefully
            asyncio.create_task(application_instance.stop())
            asyncio.create_task(application_instance.shutdown())
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    sys.exit(0)

async def handle_conflict_retry(func, max_retries=3, delay=5):
    """Handle conflict errors with retry logic"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Conflict as e:
            if attempt < max_retries - 1:
                logger.warning(f"Conflict detected (attempt {attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                logger.error(f"Max retries reached for conflict: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

# ==================== COMMAND HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    await update.message.reply_text(
        get_text('welcome', lang, name=user.first_name),
        reply_markup=main_menu_keyboard(lang)
    )

async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /models command"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.get_models(page=0, limit=10)
        total_count = models_service.get_models_count()
        total_pages = math.ceil(total_count / 10)
        
        if not models:
            await update.message.reply_text(
                "Модели не найдены. Обратитесь к администратору.",
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        await update.message.reply_text(
            get_text('models_list', lang),
            reply_markup=models_keyboard(models, 0, total_pages, lang)
        )
    finally:
        db.close()

async def my_tickets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /my_tickets command"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    db = get_session()
    try:
        support_service = SupportService(db)
        tickets = support_service.get_user_tickets(user.id, limit=10)
        
        if not tickets:
            await update.message.reply_text(
                get_text('no_tickets', lang),
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        await update.message.reply_text(
            get_text('tickets_list', lang),
            reply_markup=tickets_keyboard(tickets, lang)
        )
    finally:
        db.close()

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    if not is_admin(user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    await update.message.reply_text(
        get_text('admin_menu', lang),
        reply_markup=admin_menu_keyboard(lang)
    )

# ==================== CALLBACK HANDLERS ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    lang = get_user_lang(user.id)
    data = query.data
    
    try:
        logger.info(f"Button callback from user {user.id}: {data}")
        
        # Main menu
        if data == 'main_menu':
            await query.edit_message_text(
                get_text('main_menu', lang),
                reply_markup=main_menu_keyboard(lang)
            )
        
        # Models
        elif data == 'choose_model':
            await handle_choose_model(query, lang)
        elif data.startswith('models_page_'):
            page = int(data.split('_')[2])
            await handle_models_page(query, page, lang)
        elif data.startswith('model_'):
            model_id = int(data.split('_')[1])
            logger.info(f"Model button clicked: callback_data='{data}', model_id={model_id}")
            await handle_model_selected(query, model_id, lang)
        
        # Instructions
        elif data == 'instructions':
            await handle_instructions(query, lang)
        elif data.startswith('instructions_'):
            model_id = int(data.split('_')[1])
            await handle_model_instructions(query, model_id, lang)
        elif data.startswith('instruction_'):
            instruction_id = int(data.split('_')[1])
            await handle_instruction_selected(query, instruction_id, lang)
        elif data.startswith('package_'):
            model_id = int(data.split('_')[1])
            await handle_download_package(query, model_id, lang)
        
        # Support
        elif data == 'support':
            await handle_support(query, lang)
        elif data.startswith('support_model_'):
            model_id = int(data.split('_')[2])
            await handle_support_model(query, model_id, lang)
        elif data == 'my_tickets':
            await handle_my_tickets(query, lang)
        elif data.startswith('ticket_'):
            ticket_id = int(data.split('_')[1])
            await handle_ticket_details(query, ticket_id, lang)
        
        # Search
        elif data == 'search_model':
            await handle_search_model(query, lang)
        
        # Admin
        elif data == 'admin':
            await handle_admin_menu(query, lang)
        elif data == 'admin_models':
            await handle_admin_models(query, lang)
        elif data == 'admin_instructions':
            await handle_admin_instructions(query, lang)
        elif data == 'admin_tickets':
            await handle_admin_tickets(query, lang)
        elif data == 'admin_settings':
            await handle_admin_settings(query, lang)
        
        # Admin - Models
        elif data == 'admin_add_model':
            await handle_admin_add_model(query, lang)
        elif data == 'admin_edit_model':
            await handle_admin_edit_model(query, lang)
        elif data == 'admin_delete_model':
            await handle_admin_delete_model(query, lang)
        
        # Admin - Instructions
        elif data == 'admin_add_instruction':
            await handle_admin_add_instruction(query, lang)
        elif data == 'admin_list_instructions':
            await handle_admin_list_instructions(query, lang)
        elif data.startswith('admin_instruction_'):
            instruction_id = int(data.split('_')[2])
            await handle_admin_instruction_management(query, instruction_id, lang)
        elif data.startswith('bind_instruction_'):
            instruction_id = int(data.split('_')[2])
            await handle_bind_instruction_to_models(query, instruction_id, lang)
        elif data.startswith('unbind_instruction_'):
            instruction_id = int(data.split('_')[2])
            await handle_unbind_instruction_from_models(query, instruction_id, lang)
        elif data.startswith('select_model_'):
            parts = data.split('_')
            model_id = int(parts[2])
            instruction_id = int(parts[3])
            action = parts[4]
            await handle_model_selection_for_instruction(query, model_id, instruction_id, action, lang)
        elif data.startswith('confirm_bind_instruction_'):
            instruction_id = int(data.split('_')[3])
            await handle_confirm_bind_instruction(query, instruction_id, lang)
        elif data.startswith('confirm_unbind_instruction_'):
            instruction_id = int(data.split('_')[3])
            await handle_confirm_unbind_instruction(query, instruction_id, lang)
        
        # Admin - Tickets
        elif data == 'admin_open_tickets':
            await handle_admin_open_tickets(query, lang)
        elif data == 'admin_ticket_stats':
            await handle_admin_ticket_stats(query, lang)
        
        # Instruction type selection
        elif data.startswith('type_'):
            instruction_type = data.split('_')[1]
            await handle_instruction_type_selection(query, instruction_type, lang)
        
        # Confirmation dialogs
        elif data.startswith('confirm_'):
            action = data.split('_', 1)[1]
            await handle_confirmation(query, action, lang)
        elif data.startswith('cancel_'):
            action = data.split('_', 1)[1]
            await handle_cancellation(query, action, lang)
        
        # Cancel
        elif data == 'cancel':
            # Clear user state
            if query.from_user.id in user_states:
                del user_states[query.from_user.id]
            
            # Return to appropriate menu based on user type
            if is_admin(query.from_user.id):
                await query.edit_message_text(
                    get_text('admin_menu', lang),
                    reply_markup=admin_menu_keyboard(lang)
                )
            else:
                await query.edit_message_text(
                    get_text('main_menu', lang),
                    reply_markup=main_menu_keyboard(lang)
                )
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        logger.error(f"User ID: {user.id}")
        logger.error(f"Callback data: {data}")
        logger.error(f"User states: {list(user_states.keys())}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        await query.edit_message_text(
            get_text('error_occurred', lang),
            reply_markup=main_menu_keyboard(lang)
        )

# ==================== MODEL HANDLERS ====================

async def handle_choose_model(query, lang: str):
    """Handle choose model button"""
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.get_models(page=0, limit=10)
        total_count = models_service.get_models_count()
        total_pages = math.ceil(total_count / 10)
        
        # Debug logging
        logger.info(f"Found {len(models)} models, total: {total_count}")
        for model in models:
            logger.info(f"Model: ID={model.id}, name='{model.name}'")
        
        if not models:
            await query.edit_message_text(
                "Модели не найдены. Обратитесь к администратору.",
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        await query.edit_message_text(
            get_text('models_list', lang),
            reply_markup=models_keyboard(models, 0, total_pages, lang)
        )
    finally:
        db.close()

async def handle_models_page(query, page: int, lang: str):
    """Handle models pagination"""
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.get_models(page=page, limit=10)
        total_count = models_service.get_models_count()
        total_pages = math.ceil(total_count / 10)
        
        await query.edit_message_text(
            get_text('models_list', lang),
            reply_markup=models_keyboard(models, page, total_pages, lang)
        )
    finally:
        db.close()

async def handle_model_selected(query, model_id: int, lang: str):
    """Handle model selection"""
    db = get_session()
    try:
        models_service = ModelsService(db)
        
        # Debug logging
        logger.info(f"Looking for model with ID: {model_id}")
        
        model = models_service.get_model_by_id(model_id)
        
        # Debug logging
        if model:
            logger.info(f"Model found: ID={model.id}, name='{model.name}'")
        else:
            logger.warning(f"Model not found with ID: {model_id}")
            # Let's also check what models exist
            all_models = models_service.get_models(page=0, limit=100)
            logger.info(f"Available models: {[(m.id, m.name) for m in all_models]}")
        
        if not model:
            await query.edit_message_text(
                get_text('model_not_found', lang),
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        description = model.description or ""
        tags = f"\n{get_text('model_tags', lang, tags=model.tags)}" if model.tags else ""
        
        await query.edit_message_text(
            get_text('model_selected', lang, name=model.name, description=description) + tags,
            reply_markup=model_options_keyboard(model_id, lang),
            parse_mode='HTML'
        )
    finally:
        db.close()

# ==================== INSTRUCTION HANDLERS ====================

async def handle_instructions(query, lang: str):
    """Handle instructions button"""
    await query.edit_message_text(
        get_text('models_list', lang),
        reply_markup=models_keyboard([], 0, 1, lang)
    )

async def handle_model_instructions(query, model_id: int, lang: str):
    """Handle model instructions"""
    db = get_session()
    try:
        models_service = ModelsService(db)
        model = models_service.get_model_by_id(model_id)
        
        if not model:
            await query.edit_message_text(
                get_text('model_not_found', lang),
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        instructions = model.instructions
        
        if not instructions:
            await query.edit_message_text(
                f"Для модели {model.name} пока нет инструкций.",
                reply_markup=model_options_keyboard(model_id, lang)
            )
            return
        
        await query.edit_message_text(
            get_text('instructions_list', lang, model_name=model.name),
            reply_markup=instructions_keyboard(instructions, model_id, lang),
            parse_mode='HTML'
        )
    finally:
        db.close()

async def handle_instruction_selected(query, instruction_id: int, lang: str):
    """Handle instruction selection"""
    db = get_session()
    try:
        files_service = FilesService(db)
        instruction = files_service.get_instruction_by_id(instruction_id)
        
        if not instruction:
            await query.answer(get_text('instruction_unavailable', lang), show_alert=True)
            return
        
        # Send instruction based on type
        if instruction.tg_file_id:
            if instruction.type == InstructionType.PDF:
                await query.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=instruction.tg_file_id,
                    caption=instruction.description or instruction.title
                )
            elif instruction.type == InstructionType.VIDEO:
                await query.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=instruction.tg_file_id,
                    caption=instruction.description or instruction.title
                )
            else:
                await query.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=instruction.tg_file_id,
                    caption=instruction.description or instruction.title
                )
        elif instruction.url:
            await query.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"🔗 {instruction.title}\n\n{instruction.description or ''}\n\n{instruction.url}"
            )
        
        await query.answer(get_text('instruction_sent', lang))
    finally:
        db.close()

async def handle_download_package(query, model_id: int, lang: str):
    """Handle download package"""
    db = get_session()
    try:
        models_service = ModelsService(db)
        model = models_service.get_model_by_id(model_id)
        
        if not model or not model.instructions:
            await query.answer("Нет инструкций для скачивания.", show_alert=True)
            return
        
        # Send all instructions
        for instruction in model.instructions:
            if instruction.tg_file_id:
                if instruction.type == InstructionType.PDF:
                    await query.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=instruction.tg_file_id,
                        caption=instruction.title
                    )
                elif instruction.type == InstructionType.VIDEO:
                    await query.bot.send_video(
                        chat_id=query.message.chat_id,
                        video=instruction.tg_file_id,
                        caption=instruction.title
                    )
                else:
                    await query.bot.send_document(
                        chat_id=query.message.chat_id,
                        document=instruction.tg_file_id,
                        caption=instruction.title
                    )
            elif instruction.url:
                await query.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"🔗 {instruction.title}\n{instruction.url}"
                )
        
        await query.answer(get_text('package_sent', lang))
    finally:
        db.close()

# ==================== SUPPORT HANDLERS ====================

async def handle_support(query, lang: str):
    """Handle support button"""
    user_id = query.from_user.id
    user_states[user_id] = UserState('support_waiting')
    
    await query.edit_message_text(
        get_text('support_question', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_support_model(query, model_id: int, lang: str):
    """Handle support for specific model"""
    user_id = query.from_user.id
    user_states[user_id] = UserState('support_model_waiting', {'model_id': model_id})
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        model = models_service.get_model_by_id(model_id)
        model_name = model.name if model else f"модели #{model_id}"
    finally:
        db.close()
    
    await query.edit_message_text(
        f"Опишите ваш вопрос по модели {model_name} или прикрепите фото/видео:",
        reply_markup=cancel_keyboard(lang)
    )

async def handle_my_tickets(query, lang: str):
    """Handle my tickets button"""
    user_id = query.from_user.id
    
    db = get_session()
    try:
        support_service = SupportService(db)
        tickets = support_service.get_user_tickets(user_id, limit=10)
        
        if not tickets:
            await query.edit_message_text(
                get_text('no_tickets', lang),
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        await query.edit_message_text(
            get_text('tickets_list', lang),
            reply_markup=tickets_keyboard(tickets, lang)
        )
    finally:
        db.close()

async def handle_ticket_details(query, ticket_id: int, lang: str):
    """Handle ticket details"""
    user_id = query.from_user.id
    
    db = get_session()
    try:
        support_service = SupportService(db)
        ticket = support_service.get_ticket_by_id(ticket_id)
        
        if not ticket or ticket.user_id != user_id:
            await query.answer("Обращение не найдено.", show_alert=True)
            return
        
        status_text = {
            TicketStatus.OPEN: get_text('ticket_status_open', lang),
            TicketStatus.IN_PROGRESS: get_text('ticket_status_in_progress', lang),
            TicketStatus.CLOSED: get_text('ticket_status_closed', lang)
        }.get(ticket.status, get_text('ticket_status_open', lang))
        
        messages = support_service.get_ticket_messages(ticket_id)
        
        text = f"🆔 Обращение T-{ticket.id}\n"
        text += f"📅 Создано: {ticket.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        text += f"📊 Статус: {status_text}\n"
        if ticket.subject:
            text += f"📝 Тема: {ticket.subject}\n"
        text += "\n💬 Сообщения:\n"
        
        for msg in messages:
            role_emoji = "👤" if msg.from_role == MessageRole.USER else "👨‍💼"
            text += f"{role_emoji} {msg.created_at.strftime('%d.%m %H:%M')}\n"
            if msg.text:
                text += f"{msg.text}\n"
            if msg.tg_file_id:
                text += f"📎 Файл прикреплен\n"
            text += "\n"
        
        await query.edit_message_text(
            text,
            reply_markup=main_menu_keyboard(lang)
        )
    finally:
        db.close()

# ==================== SEARCH HANDLERS ====================

async def handle_search_model(query, lang: str):
    """Handle search model button"""
    user_id = query.from_user.id
    user_states[user_id] = UserState('search_waiting')
    
    await query.edit_message_text(
        get_text('search_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

# ==================== ADMIN HANDLERS ====================

async def handle_admin_menu(query, lang: str):
    """Handle admin menu"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        get_text('admin_menu', lang),
        reply_markup=admin_menu_keyboard(lang)
    )

async def handle_admin_models(query, lang: str):
    """Handle admin models"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        "Управление моделями:",
        reply_markup=admin_models_keyboard(lang)
    )

async def handle_admin_instructions(query, lang: str):
    """Handle admin instructions"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        "Управление инструкциями:",
        reply_markup=admin_instructions_keyboard(lang)
    )

async def handle_admin_tickets(query, lang: str):
    """Handle admin tickets"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        "Управление обращениями:",
        reply_markup=admin_tickets_keyboard(lang)
    )

async def handle_admin_settings(query, lang: str):
    """Handle admin settings"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        "⚙️ Настройки бота:\n\n"
        "🔧 Доступные настройки:\n"
        "• Управление админами\n"
        "• Настройки уведомлений\n"
        "• Языковые настройки\n\n"
        "Функция в разработке...",
        reply_markup=admin_menu_keyboard(lang)
    )

# Admin model handlers
async def handle_admin_add_model(query, lang: str):
    """Handle admin add model"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    user_states[user_id] = UserState('admin_add_model_name')
    
    await query.edit_message_text(
        get_text('model_name_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_edit_model(query, lang: str):
    """Handle admin edit model"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    # Show models list for editing
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.get_models(page=0, limit=20)
        total_count = models_service.get_models_count()
        total_pages = math.ceil(total_count / 20)
        
        await query.edit_message_text(
            "Выберите модель для редактирования:",
            reply_markup=models_keyboard(models, 0, total_pages, lang)
        )
    finally:
        db.close()

async def handle_admin_delete_model(query, lang: str):
    """Handle admin delete model"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    # Show models list for deletion
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.get_models(page=0, limit=20)
        total_count = models_service.get_models_count()
        total_pages = math.ceil(total_count / 20)
        
        await query.edit_message_text(
            "Выберите модель для удаления:",
            reply_markup=models_keyboard(models, 0, total_pages, lang)
        )
    finally:
        db.close()

# Admin instruction handlers
async def handle_admin_add_instruction(query, lang: str):
    """Handle admin add instruction"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    user_states[user_id] = UserState('admin_add_instruction_title')
    
    logger.info(f"Admin {user_id} started adding instruction, state set to: admin_add_instruction_title")
    
    await query.edit_message_text(
        get_text('instruction_title_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_list_instructions(query, lang: str):
    """Handle admin list instructions"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        instructions = instructions_service.get_instructions(page=0, limit=20)
        
        if not instructions:
            await query.edit_message_text(
                "Инструкции не найдены.",
                reply_markup=admin_instructions_keyboard(lang)
            )
            return
        
        await query.edit_message_text(
            "📄 Выберите инструкцию для управления:",
            reply_markup=admin_instructions_list_keyboard(instructions, lang)
        )
    finally:
        db.close()


# Admin ticket handlers
async def handle_admin_open_tickets(query, lang: str):
    """Handle admin open tickets"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        support_service = SupportService(db)
        tickets = support_service.get_open_tickets(limit=20)
        
        if not tickets:
            await query.edit_message_text(
                "Открытых обращений нет.",
                reply_markup=admin_tickets_keyboard(lang)
            )
            return
        
        text = "🎫 Открытые обращения:\n\n"
        for ticket in tickets:
            status_emoji = {
                TicketStatus.OPEN: "🟢",
                TicketStatus.IN_PROGRESS: "🟡",
                TicketStatus.CLOSED: "🔴"
            }.get(ticket.status, "🟢")
            
            text += f"{status_emoji} T-{ticket.id} от @{ticket.username or 'unknown'}\n"
            if ticket.subject:
                text += f"   📝 {ticket.subject[:50]}...\n"
            text += f"   📅 {ticket.created_at.strftime('%d.%m %H:%M')}\n\n"
        
        await query.edit_message_text(
            text,
            reply_markup=admin_tickets_keyboard(lang)
        )
    finally:
        db.close()

async def handle_admin_ticket_stats(query, lang: str):
    """Handle admin ticket stats"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        support_service = SupportService(db)
        stats = support_service.get_ticket_stats()
        
        text = "📊 Статистика обращений:\n\n"
        text += f"🟢 Открытых: {stats.get('open', 0)}\n"
        text += f"🟡 В работе: {stats.get('in_progress', 0)}\n"
        text += f"🔴 Закрытых: {stats.get('closed', 0)}\n"
        text += f"📈 Всего: {support_service.get_tickets_count()}"
        
        await query.edit_message_text(
            text,
            reply_markup=admin_tickets_keyboard(lang)
        )
    finally:
        db.close()

# ==================== CONFIRMATION HANDLERS ====================

async def handle_confirmation(query, action: str, lang: str):
    """Handle confirmation actions"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    # TODO: Implement confirmation logic
    await query.edit_message_text(
        f"Подтверждение для действия: {action}",
        reply_markup=admin_menu_keyboard(lang)
    )

async def handle_cancellation(query, action: str, lang: str):
    """Handle cancellation actions"""
    await query.edit_message_text(
        get_text('delete_cancelled', lang),
        reply_markup=admin_menu_keyboard(lang)
    )

async def handle_instruction_type_selection(query, instruction_type: str, lang: str):
    """Handle instruction type selection"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    
    # Check if user has state
    if user_id not in user_states:
        logger.error(f"Admin {user_id} has no state when selecting instruction type")
        await query.edit_message_text(
            "Сессия истекла. Начните добавление инструкции заново.",
            reply_markup=admin_instructions_keyboard(lang)
        )
        return
    
    state = user_states[user_id]
    logger.info(f"Admin {user_id} selected instruction type: '{instruction_type}'")
    logger.info(f"Admin {user_id} current state: {state.state}")
    logger.info(f"Admin {user_id} state data: {state.data}")
    
    # Map type to enum
    type_mapping = {
        'pdf': 'pdf',
        'video': 'video', 
        'link': 'link'
    }
    
    if instruction_type not in type_mapping:
        await query.answer("Неверный тип инструкции", show_alert=True)
        return
    
    # Update state with type
    state.data['type'] = type_mapping[instruction_type]
    user_states[user_id] = UserState('admin_add_instruction_description', state.data)
    
    logger.info(f"Admin {user_id} state updated to: admin_add_instruction_description")
    
    await query.edit_message_text(
        get_text('instruction_description_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

# ==================== MESSAGE HANDLERS ====================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    # Debug logging
    logger.info(f"Message from user {user.id}: {update.message.text if update.message.text else 'Non-text message'}")
    logger.info(f"User states: {list(user_states.keys())}")
    
    # Check if user is admin and has admin state
    if is_admin(user.id) and user.id in user_states:
        state = user_states[user.id]
        logger.info(f"Admin {user.id} state: {state.state}")
        logger.info(f"Admin {user.id} state data: {state.data}")
        
        # Handle admin states first
        try:
            if state.state == 'admin_add_model_name':
                await handle_admin_add_model_name(update, context, lang)
            elif state.state == 'admin_add_model_description':
                await handle_admin_add_model_description(update, context, lang)
            elif state.state == 'admin_add_model_tags':
                await handle_admin_add_model_tags(update, context, lang)
            elif state.state == 'admin_add_instruction_title':
                logger.info(f"Processing admin_add_instruction_title for user {user.id}")
                await handle_admin_add_instruction_title(update, context, lang)
            elif state.state == 'admin_add_instruction_type':
                logger.info(f"Processing admin_add_instruction_type for user {user.id}")
                await handle_admin_add_instruction_type(update, context, lang)
            elif state.state == 'admin_add_instruction_description':
                logger.info(f"Processing admin_add_instruction_description for user {user.id}")
                await handle_admin_add_instruction_description(update, context, lang)
            elif state.state == 'admin_add_instruction_file':
                logger.info(f"Processing admin_add_instruction_file for user {user.id}")
                await handle_admin_add_instruction_file(update, context, lang)
            else:
                # Unknown admin state, clear it
                logger.warning(f"Unknown admin state '{state.state}' for user {user.id}, clearing state")
                del user_states[user.id]
                await update.message.reply_text(
                    "Неизвестное состояние админа. Возвращаемся в админ-меню.",
                    reply_markup=admin_menu_keyboard(lang)
                )
        except Exception as e:
            logger.error(f"Error in admin message handler: {e}")
            logger.error(f"Admin {user.id} state was: {state.state}")
            await update.message.reply_text(
                "Ошибка в админ-панели. Возвращаемся в админ-меню.",
                reply_markup=admin_menu_keyboard(lang)
            )
            if user.id in user_states:
                del user_states[user.id]
        return
    
    # Handle regular user states
    if user.id not in user_states:
        # If admin is trying to enter text but has no state, they might be in the middle of adding instruction
        if is_admin(user.id) and update.message.text:
            logger.info(f"Admin {user.id} has no state but sent text: '{update.message.text}' - assuming instruction title")
            user_states[user.id] = UserState('admin_add_instruction_title')
            await handle_admin_add_instruction_title(update, context, lang)
            return
        else:
            await update.message.reply_text(
                "Пожалуйста, используйте меню для навигации.",
                reply_markup=main_menu_keyboard(lang)
            )
            return
    
    state = user_states[user.id]
    logger.info(f"User {user.id} state: {state.state}")
    
    try:
        if state.state == 'support_waiting':
            await handle_support_message(update, context, lang)
        elif state.state == 'support_model_waiting':
            await handle_support_model_message(update, context, lang)
        elif state.state == 'search_waiting':
            await handle_search_message(update, context, lang)
        # Admin states are handled above in the admin section
        else:
            await update.message.reply_text(
                "Неизвестное состояние. Возвращаемся в главное меню.",
                reply_markup=main_menu_keyboard(lang)
            )
            del user_states[user.id]
    except Exception as e:
        logger.error(f"Error in message_handler: {e}")
        await update.message.reply_text(
            get_text('error_occurred', lang),
            reply_markup=main_menu_keyboard(lang)
        )
        if user.id in user_states:
            del user_states[user.id]

async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle support message"""
    user = update.effective_user
    db = get_session()
    
    try:
        support_service = SupportService(db)
        
        # Create ticket
        ticket = support_service.create_ticket(
            user_id=user.id,
            username=user.username,
            subject=update.message.text[:100] if update.message.text else None
        )
        
        # Add message to ticket
        support_service.add_message_to_ticket(
            ticket_id=ticket.id,
            from_role=MessageRole.USER,
            text=update.message.text
        )
        
        # Send to admins
        admin_text = f"❗️ Новое обращение T-{ticket.id}\n"
        admin_text += f"👤 От: @{user.username or 'нет username'} (ID: {user.id})\n"
        admin_text += f"📝 Текст: {update.message.text}"
        
        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(chat_id=admin_id, text=admin_text)
            except TelegramError as e:
                logger.error(f"Failed to send message to admin {admin_id}: {e}")
        
        await update.message.reply_text(
            get_text('support_sent', lang, ticket_id=ticket.id),
            reply_markup=main_menu_keyboard(lang)
        )
        
    finally:
        db.close()
        if user.id in user_states:
            del user_states[user.id]

async def handle_support_model_message(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle support message for specific model"""
    user = update.effective_user
    state = user_states[user.id]
    model_id = state.data.get('model_id')
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        support_service = SupportService(db)
        
        model = models_service.get_model_by_id(model_id)
        model_name = model.name if model else f"модели #{model_id}"
        
        # Create ticket
        ticket = support_service.create_ticket(
            user_id=user.id,
            username=user.username,
            subject=f"Вопрос по модели {model_name}"
        )
        
        # Add message to ticket
        support_service.add_message_to_ticket(
            ticket_id=ticket.id,
            from_role=MessageRole.USER,
            text=f"Вопрос по модели {model_name}:\n\n{update.message.text}"
        )
        
        # Send to admins
        admin_text = f"❗️ Новое обращение T-{ticket.id}\n"
        admin_text += f"👤 От: @{user.username or 'нет username'} (ID: {user.id})\n"
        admin_text += f"📦 Модель: {model_name}\n"
        admin_text += f"📝 Текст: {update.message.text}"
        
        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(chat_id=admin_id, text=admin_text)
            except TelegramError as e:
                logger.error(f"Failed to send message to admin {admin_id}: {e}")
        
        await update.message.reply_text(
            get_text('support_sent', lang, ticket_id=ticket.id),
            reply_markup=main_menu_keyboard(lang)
        )
        
    finally:
        db.close()
        if user.id in user_states:
            del user_states[user.id]

async def handle_search_message(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle search message"""
    user = update.effective_user
    query_text = update.message.text
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        models = models_service.search_models(query_text, page=0, limit=10)
        total_count = models_service.get_search_models_count(query_text)
        total_pages = math.ceil(total_count / 10)
        
        if not models:
            await update.message.reply_text(
                get_text('no_search_results', lang),
                reply_markup=main_menu_keyboard(lang)
            )
            return
        
        await update.message.reply_text(
            get_text('search_results', lang, query=query_text),
            reply_markup=models_keyboard(models, 0, total_pages, lang)
        )
        
    finally:
        db.close()
        if user.id in user_states:
            del user_states[user.id]

# Admin message handlers
async def handle_admin_add_model_name(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add model name"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    model_name = update.message.text
    
    user_states[user_id] = UserState('admin_add_model_description', {'name': model_name})
    
    await update.message.reply_text(
        get_text('model_description_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_add_model_description(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add model description"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    description = update.message.text if update.message.text != '/skip' else None
    
    user_states[user_id] = UserState('admin_add_model_tags', {
        'name': state.data['name'],
        'description': description
    })
    
    await update.message.reply_text(
        get_text('model_tags_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_add_model_tags(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add model tags"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    tags = update.message.text if update.message.text != '/skip' else None
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        
        # Debug logging
        logger.info(f"Creating model: name='{state.data['name']}', description='{state.data['description']}', tags='{tags}'")
        
        model = models_service.create_model(
            name=state.data['name'],
            description=state.data['description'],
            tags=tags
        )
        
        # Debug logging
        logger.info(f"Model created successfully: ID={model.id}, name='{model.name}'")
        
        await update.message.reply_text(
            get_text('model_created', lang, name=model.name),
            reply_markup=admin_models_keyboard(lang)
        )
        
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        await update.message.reply_text(
            "Ошибка при создании модели. Попробуйте еще раз.",
            reply_markup=admin_models_keyboard(lang)
        )
    finally:
        db.close()
        if user_id in user_states:
            del user_states[user_id]

async def handle_admin_add_instruction_title(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add instruction title"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    title = update.message.text
    
    logger.info(f"Admin {user_id} entered instruction title: '{title}'")
    
    # Always set the state, even if it was lost
    user_states[user_id] = UserState('admin_add_instruction_type', {'title': title})
    
    logger.info(f"Admin {user_id} state updated to: admin_add_instruction_type")
    logger.info(f"User states after update: {list(user_states.keys())}")
    
    await update.message.reply_text(
        get_text('instruction_type_prompt', lang),
        reply_markup=instruction_type_keyboard(lang)
    )

async def handle_admin_add_instruction_type(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add instruction type selection"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    
    # This should be handled by callback, but just in case
    await update.message.reply_text(
        "Пожалуйста, выберите тип инструкции с помощью кнопок выше.",
        reply_markup=instruction_type_keyboard(lang)
    )

async def handle_admin_add_instruction_description(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add instruction description"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    description = update.message.text if update.message.text != '/skip' else None
    
    user_states[user_id] = UserState('admin_add_instruction_file', {
        'title': state.data['title'],
        'type': state.data['type'],
        'description': description
    })
    
    # Different prompts based on type
    if state.data['type'] == 'link':
        prompt = "Введите URL ссылки:"
    else:
        prompt = get_text('instruction_file_prompt', lang)
    
    await update.message.reply_text(
        prompt,
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_add_instruction_file(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add instruction file"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    
    logger.info(f"Admin {user_id} in handle_admin_add_instruction_file")
    logger.info(f"State data: {state.data}")
    
    db = get_session()
    try:
        files_service = FilesService(db)
        
        tg_file_id = None
        url = None
        
        # Handle different types
        if state.data['type'] == 'link':
            # For links, expect URL in text
            if update.message.text and update.message.text.startswith('http'):
                url = update.message.text
            else:
                await update.message.reply_text(
                    "Пожалуйста, отправьте корректный URL (начинающийся с http).",
                    reply_markup=cancel_keyboard(lang)
                )
                return
        else:
            # For files, expect file upload
            if update.message.document:
                tg_file_id = update.message.document.file_id
            elif update.message.video:
                tg_file_id = update.message.video.file_id
            elif update.message.photo:
                tg_file_id = update.message.photo[-1].file_id
            else:
                await update.message.reply_text(
                    "Пожалуйста, отправьте файл.",
                    reply_markup=cancel_keyboard(lang)
                )
                return
        
        instruction = files_service.create_instruction(
            title=state.data['title'],
            instruction_type=InstructionType(state.data['type']),
            description=state.data['description'],
            tg_file_id=tg_file_id,
            url=url
        )
        
        await update.message.reply_text(
            get_text('instruction_created', lang, title=instruction.title),
            reply_markup=admin_instructions_keyboard(lang)
        )
        
    except Exception as e:
        logger.error(f"Error creating instruction: {e}")
        await update.message.reply_text(
            "Ошибка при создании инструкции. Попробуйте еще раз.",
            reply_markup=admin_instructions_keyboard(lang)
        )
    finally:
        db.close()
        if user_id in user_states:
            del user_states[user_id]

# ==================== INSTRUCTION MANAGEMENT HANDLERS ====================

async def handle_admin_instruction_management(query, instruction_id: int, lang: str):
    """Handle instruction management menu"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        instruction = instructions_service.get_instruction_by_id(instruction_id)
        
        if not instruction:
            await query.edit_message_text(
                "Инструкция не найдена.",
                reply_markup=admin_instructions_keyboard(lang)
            )
            return
        
        # Get bound models
        bound_models = instruction.models
        bound_models_text = ""
        if bound_models:
            bound_models_text = f"\n\n🔗 Привязана к моделям:\n"
            for model in bound_models:
                bound_models_text += f"• {model.name}\n"
        
        text = f"📄 {instruction.title}\n"
        text += f"📋 Тип: {instruction.type.value}\n"
        if instruction.description:
            text += f"📝 Описание: {instruction.description}\n"
        text += bound_models_text
        
        await query.edit_message_text(
            text,
            reply_markup=instruction_management_keyboard(instruction_id, lang)
        )
    finally:
        db.close()

async def handle_bind_instruction_to_models(query, instruction_id: int, lang: str):
    """Handle binding instruction to models"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        models_service = ModelsService(db)
        
        instruction = instructions_service.get_instruction_by_id(instruction_id)
        if not instruction:
            await query.edit_message_text(
                "Инструкция не найдена.",
                reply_markup=admin_instructions_keyboard(lang)
            )
            return
        
        # Get all models
        models = models_service.get_models(page=0, limit=100)
        
        if not models:
            await query.edit_message_text(
                "Модели не найдены.",
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
            return
        
        # Get already bound models
        bound_model_ids = [model.id for model in instruction.models]
        
        await query.edit_message_text(
            get_text('select_models_to_bind', lang, title=instruction.title),
            reply_markup=models_selection_keyboard(models, instruction_id, 'bind', bound_model_ids, lang)
        )
    finally:
        db.close()

async def handle_unbind_instruction_from_models(query, instruction_id: int, lang: str):
    """Handle unbinding instruction from models"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        
        instruction = instructions_service.get_instruction_by_id(instruction_id)
        if not instruction:
            await query.edit_message_text(
                "Инструкция не найдена.",
                reply_markup=admin_instructions_keyboard(lang)
            )
            return
        
        # Get bound models
        bound_models = instruction.models
        
        if not bound_models:
            await query.edit_message_text(
                "Инструкция не привязана ни к одной модели.",
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
            return
        
        await query.edit_message_text(
            get_text('select_models_to_unbind', lang, title=instruction.title),
            reply_markup=models_selection_keyboard(bound_models, instruction_id, 'unbind', [], lang)
        )
    finally:
        db.close()

async def handle_model_selection_for_instruction(query, model_id: int, instruction_id: int, action: str, lang: str):
    """Handle model selection for instruction binding/unbinding"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    
    # Initialize or get user state for model selection
    if user_id not in user_states:
        user_states[user_id] = UserState('model_selection', {
            'instruction_id': instruction_id,
            'action': action,
            'selected_models': []
        })
    
    state = user_states[user_id]
    selected_models = state.data.get('selected_models', [])
    
    # Toggle model selection
    if model_id in selected_models:
        selected_models.remove(model_id)
    else:
        selected_models.append(model_id)
    
    state.data['selected_models'] = selected_models
    user_states[user_id] = state
    
    # Update keyboard
    db = get_session()
    try:
        if action == 'bind':
            models_service = ModelsService(db)
            models = models_service.get_models(page=0, limit=100)
        else:  # unbind
            instructions_service = InstructionsService(db)
            instruction = instructions_service.get_instruction_by_id(instruction_id)
            models = instruction.models if instruction else []
        
        await query.edit_message_reply_markup(
            reply_markup=models_selection_keyboard(models, instruction_id, action, selected_models, lang)
        )
    finally:
        db.close()

async def handle_confirm_bind_instruction(query, instruction_id: int, lang: str):
    """Handle confirmation of instruction binding"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    
    if user_id not in user_states or user_states[user_id].state != 'model_selection':
        await query.edit_message_text(
            "Сессия истекла. Попробуйте снова.",
            reply_markup=admin_instructions_keyboard(lang)
        )
        return
    
    state = user_states[user_id]
    selected_models = state.data.get('selected_models', [])
    
    if not selected_models:
        await query.answer("Выберите хотя бы одну модель.", show_alert=True)
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        
        success = instructions_service.bind_instruction_to_models(instruction_id, selected_models)
        
        if success:
            await query.edit_message_text(
                get_text('instruction_bound', lang),
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
        else:
            await query.edit_message_text(
                "Ошибка при привязке инструкции к моделям.",
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
    finally:
        db.close()
        if user_id in user_states:
            del user_states[user_id]

async def handle_confirm_unbind_instruction(query, instruction_id: int, lang: str):
    """Handle confirmation of instruction unbinding"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    user_id = query.from_user.id
    
    if user_id not in user_states or user_states[user_id].state != 'model_selection':
        await query.edit_message_text(
            "Сессия истекла. Попробуйте снова.",
            reply_markup=admin_instructions_keyboard(lang)
        )
        return
    
    state = user_states[user_id]
    selected_models = state.data.get('selected_models', [])
    
    if not selected_models:
        await query.answer("Выберите хотя бы одну модель.", show_alert=True)
        return
    
    db = get_session()
    try:
        instructions_service = InstructionsService(db)
        
        success = instructions_service.unbind_instruction_from_models(instruction_id, selected_models)
        
        if success:
            await query.edit_message_text(
                get_text('instruction_unbound', lang),
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
        else:
            await query.edit_message_text(
                "Ошибка при отвязке инструкции от моделей.",
                reply_markup=instruction_management_keyboard(instruction_id, lang)
            )
    finally:
        db.close()
        if user_id in user_states:
            del user_states[user_id]

# ==================== ERROR HANDLER ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    error = context.error
    
    # Handle conflict errors specifically
    if isinstance(error, Conflict):
        logger.warning(f"Conflict detected: {error}")
        # Don't send conflict errors to admins as they're usually temporary
        return
    
    logger.error(f"Exception while handling an update: {error}")
    
    # Send error to admins (but not for conflicts)
    error_text = f"🚨 Ошибка в боте:\n\n{str(error)}"
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=error_text)
        except:
            pass

# ==================== HEALTHCHECK SERVER ====================

async def healthcheck_handler(request):
    """Simple healthcheck endpoint"""
    return web.Response(text="OK", status=200)

def start_healthcheck_server():
    """Start simple HTTP server for healthcheck"""
    app = web.Application()
    app.router.add_get('/health', healthcheck_handler)
    app.router.add_get('/', healthcheck_handler)
    
    runner = web.AppRunner(app)
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    loop.run_until_complete(site.start())
    
    logger.info("Healthcheck server started on port 8080")
    loop.run_forever()

# ==================== MAIN FUNCTION ====================

def main():
    """Main function"""
    global application_instance
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create database tables
    create_tables()
    
    # Start healthcheck server in background
    healthcheck_thread = threading.Thread(target=start_healthcheck_server, daemon=True)
    healthcheck_thread.start()
    
    # Create application with better error handling
    application = Application.builder().token(BOT_TOKEN).build()
    application_instance = application
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("models", models_command))
    application.add_handler(CommandHandler("my_tickets", my_tickets_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, message_handler))
    application.add_handler(MessageHandler(filters.PHOTO, message_handler))
    application.add_handler(MessageHandler(filters.VIDEO, message_handler))
    application.add_handler(MessageHandler(filters.ALL, message_handler))  # Catch all messages
    
    application.add_error_handler(error_handler)
    
    # Start bot with conflict handling
    try:
        if MODE == 'WEBHOOK' and WEBHOOK_URL:
            logger.info("Starting bot in webhook mode...")
            application.run_webhook(
                listen="0.0.0.0",
                port=8443,
                webhook_url=WEBHOOK_URL
            )
        else:
            logger.info("Starting bot in polling mode...")
            # Add a small delay to avoid immediate conflicts
            time.sleep(2)
            application.run_polling(
                drop_pending_updates=True,  # Drop pending updates to avoid conflicts
                allowed_updates=None,  # Allow all update types
                close_loop=False  # Don't close the event loop on shutdown
            )
    except Conflict as e:
        logger.error(f"Bot conflict detected: {e}")
        logger.info("Attempting to clear webhook and restart...")
        
        # Clear webhook and try again
        import requests
        try:
            clear_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
            response = requests.post(clear_url, json={"drop_pending_updates": True})
            if response.status_code == 200:
                logger.info("Webhook cleared successfully, restarting...")
                time.sleep(5)  # Wait before restarting
                application.run_polling(drop_pending_updates=True)
            else:
                logger.error(f"Failed to clear webhook: {response.text}")
        except Exception as clear_error:
            logger.error(f"Error clearing webhook: {clear_error}")
    except Exception as e:
        logger.error(f"Unexpected error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
