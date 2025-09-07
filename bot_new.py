import logging
import math
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
from telegram.error import TelegramError
import asyncio
from datetime import datetime, timedelta

# Import our modules
from config import BOT_TOKEN, ADMIN_CHAT_IDS, MODE, WEBHOOK_URL
from models import create_tables, get_session, InstructionType, TicketStatus, MessageRole, FileType
from services.models_service import ModelsService
from services.files_service import FilesService
from services.support_service import SupportService
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

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_CHAT_IDS

def get_user_lang(user_id: int) -> str:
    """Get user language (default: ru)"""
    # TODO: Implement language preference storage
    return 'ru'

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
        elif data == 'admin_bind_instruction':
            await handle_admin_bind_instruction(query, lang)
        
        # Admin - Tickets
        elif data == 'admin_open_tickets':
            await handle_admin_open_tickets(query, lang)
        elif data == 'admin_ticket_stats':
            await handle_admin_ticket_stats(query, lang)
        
        # Confirmation dialogs
        elif data.startswith('confirm_'):
            action = data.split('_', 1)[1]
            await handle_confirmation(query, action, lang)
        elif data.startswith('cancel_'):
            action = data.split('_', 1)[1]
            await handle_cancellation(query, action, lang)
        
        # Cancel
        elif data == 'cancel':
            await query.edit_message_text(
                get_text('main_menu', lang),
                reply_markup=main_menu_keyboard(lang)
            )
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
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
        model = models_service.get_model_by_id(model_id)
        
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
        files_service = FilesService(db)
        instructions = files_service.get_instructions(page=0, limit=20)
        
        if not instructions:
            await query.edit_message_text(
                "Инструкции не найдены.",
                reply_markup=admin_instructions_keyboard(lang)
            )
            return
        
        text = "📄 Список инструкций:\n\n"
        for instruction in instructions:
            type_emoji = {
                InstructionType.PDF: "📄",
                InstructionType.VIDEO: "🎥",
                InstructionType.LINK: "🔗"
            }.get(instruction.type, "📄")
            text += f"{type_emoji} {instruction.title}\n"
        
        await query.edit_message_text(
            text,
            reply_markup=admin_instructions_keyboard(lang)
        )
    finally:
        db.close()

async def handle_admin_bind_instruction(query, lang: str):
    """Handle admin bind instruction"""
    if not is_admin(query.from_user.id):
        await query.edit_message_text(get_text('access_denied', lang))
        return
    
    await query.edit_message_text(
        "Функция привязки инструкций к моделям будет реализована в следующей версии.",
        reply_markup=admin_instructions_keyboard(lang)
    )

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

# ==================== MESSAGE HANDLERS ====================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user = update.effective_user
    lang = get_user_lang(user.id)
    
    if user.id not in user_states:
        await update.message.reply_text(
            "Пожалуйста, используйте меню для навигации.",
            reply_markup=main_menu_keyboard(lang)
        )
        return
    
    state = user_states[user.id]
    
    try:
        if state.state == 'support_waiting':
            await handle_support_message(update, context, lang)
        elif state.state == 'support_model_waiting':
            await handle_support_model_message(update, context, lang)
        elif state.state == 'search_waiting':
            await handle_search_message(update, context, lang)
        elif state.state == 'admin_add_model_name':
            await handle_admin_add_model_name(update, context, lang)
        elif state.state == 'admin_add_model_description':
            await handle_admin_add_model_description(update, context, lang)
        elif state.state == 'admin_add_model_tags':
            await handle_admin_add_model_tags(update, context, lang)
        elif state.state == 'admin_add_instruction_title':
            await handle_admin_add_instruction_title(update, context, lang)
        elif state.state == 'admin_add_instruction_description':
            await handle_admin_add_instruction_description(update, context, lang)
        elif state.state == 'admin_add_instruction_file':
            await handle_admin_add_instruction_file(update, context, lang)
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
        model = models_service.create_model(
            name=state.data['name'],
            description=state.data['description'],
            tags=tags
        )
        
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
    
    user_states[user_id] = UserState('admin_add_instruction_type', {'title': title})
    
    await update.message.reply_text(
        get_text('instruction_type_prompt', lang),
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
    
    await update.message.reply_text(
        get_text('instruction_file_prompt', lang),
        reply_markup=cancel_keyboard(lang)
    )

async def handle_admin_add_instruction_file(update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """Handle admin add instruction file"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(get_text('access_denied', lang))
        return
    
    user_id = update.effective_user.id
    state = user_states[user_id]
    
    db = get_session()
    try:
        files_service = FilesService(db)
        
        tg_file_id = None
        url = None
        
        if update.message.document:
            tg_file_id = update.message.document.file_id
        elif update.message.video:
            tg_file_id = update.message.video.file_id
        elif update.message.photo:
            tg_file_id = update.message.photo[-1].file_id
        elif update.message.text and update.message.text.startswith('http'):
            url = update.message.text
        else:
            await update.message.reply_text(
                "Пожалуйста, отправьте файл или URL.",
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

# ==================== ERROR HANDLER ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Send error to admins
    error_text = f"🚨 Ошибка в боте:\n\n{str(context.error)}"
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=error_text)
        except:
            pass

# ==================== MAIN FUNCTION ====================

def main():
    """Main function"""
    # Create database tables
    create_tables()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
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
    
    application.add_error_handler(error_handler)
    
    # Start bot
    if MODE == 'WEBHOOK' and WEBHOOK_URL:
        logger.info("Starting bot in webhook mode...")
        application.run_webhook(
            listen="0.0.0.0",
            port=8443,
            webhook_url=WEBHOOK_URL
        )
    else:
        logger.info("Starting bot in polling mode...")
        application.run_polling()

if __name__ == "__main__":
    main()
