from telegram import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from models import Model, Instruction, Ticket, TicketStatus, InstructionType
from texts import get_text
from typing import List, Optional
import math

def main_menu_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    buttons = [
        [InlineKeyboardButton("🌐 Открыть приложение", web_app=WebAppInfo(url="https://gakshop.com/"))],
        [InlineKeyboardButton(get_text('choose_model', lang), callback_data='choose_model')],
        [InlineKeyboardButton(get_text('instructions', lang), callback_data='instructions')],
        [InlineKeyboardButton(get_text('recipes', lang), callback_data='recipes')],
        [InlineKeyboardButton(get_text('support', lang), callback_data='support')],
        [InlineKeyboardButton(get_text('my_tickets', lang), callback_data='my_tickets')],
    ]
    return InlineKeyboardMarkup(buttons)

def models_keyboard(models: List[Model], page: int = 0, total_pages: int = 1, 
                   lang: str = 'ru') -> InlineKeyboardMarkup:
    """Models list keyboard with pagination"""
    buttons = []
    
    # Add models
    for model in models:
        buttons.append([InlineKeyboardButton(
            model.name, 
            callback_data=f'model_{model.id}'
        )])
    
    # Add pagination
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'models_page_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data='current_page'))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'models_page_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add search and back buttons
    buttons.append([
        InlineKeyboardButton(get_text('search_model', lang), callback_data='search_model'),
        InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='main_menu')
    ])
    
    return InlineKeyboardMarkup(buttons)

def model_options_keyboard(model_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Model options keyboard"""
    buttons = [
        [InlineKeyboardButton("📄 Инструкции", callback_data=f'instructions_{model_id}')],
        [InlineKeyboardButton(get_text('download_package', lang), callback_data=f'package_{model_id}')],
        [InlineKeyboardButton("✉️ Написать по этой модели", callback_data=f'support_model_{model_id}')],
        [InlineKeyboardButton(get_text('back_to_models', lang), callback_data='choose_model')],
        [InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(buttons)

def instructions_keyboard(instructions: List[Instruction], model_id: int, 
                         lang: str = 'ru') -> InlineKeyboardMarkup:
    """Instructions list keyboard"""
    buttons = []
    
    for instruction in instructions:
        # Add type emoji
        type_emoji = {
            InstructionType.PDF: "📄",
            InstructionType.VIDEO: "🎥",
            InstructionType.LINK: "🔗"
        }.get(instruction.type, "📄")
        
        buttons.append([InlineKeyboardButton(
            f"{type_emoji} {instruction.title}",
            callback_data=f'instruction_{instruction.id}'
        )])
    
    # Add package download and back buttons
    buttons.append([InlineKeyboardButton(
        get_text('download_package', lang), 
        callback_data=f'package_{model_id}'
    )])
    buttons.append([
        InlineKeyboardButton(get_text('back_to_models', lang), callback_data='choose_model'),
        InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='main_menu')
    ])
    
    return InlineKeyboardMarkup(buttons)

def tickets_keyboard(tickets: List[Ticket], lang: str = 'ru') -> InlineKeyboardMarkup:
    """User tickets keyboard"""
    buttons = []
    
    for ticket in tickets:
        status_emoji = {
            TicketStatus.OPEN: "🟢",
            TicketStatus.IN_PROGRESS: "🟡",
            TicketStatus.CLOSED: "🔴"
        }.get(ticket.status, "🟢")
        
        ticket_text = f"{status_emoji} T-{ticket.id}"
        if ticket.subject:
            ticket_text += f" - {ticket.subject[:30]}..."
        
        buttons.append([InlineKeyboardButton(
            ticket_text,
            callback_data=f'ticket_{ticket.id}'
        )])
    
    buttons.append([InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='main_menu')])
    return InlineKeyboardMarkup(buttons)

def admin_edit_models_keyboard(models: List[Model], page: int = 0, total_pages: int = 1, 
                              lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin edit models keyboard"""
    buttons = []
    
    # Add models with edit buttons
    for model in models:
        buttons.append([InlineKeyboardButton(
            f"✏️ {model.name}", 
            callback_data=f'admin_edit_model_{model.id}'
        )])
    
    # Add pagination
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'admin_edit_models_page_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data='current_page'))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'admin_edit_models_page_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add back button
    buttons.append([InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='admin_models')])
    
    return InlineKeyboardMarkup(buttons)

def admin_delete_models_keyboard(models: List[Model], page: int = 0, total_pages: int = 1, 
                                lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin delete models keyboard"""
    buttons = []
    
    # Add models with delete buttons
    for model in models:
        buttons.append([InlineKeyboardButton(
            f"🗑️ {model.name}", 
            callback_data=f'admin_delete_model_{model.id}'
        )])
    
    # Add pagination
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'admin_delete_models_page_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data='current_page'))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'admin_delete_models_page_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add back button
    buttons.append([InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='admin_models')])
    
    return InlineKeyboardMarkup(buttons)

def confirm_delete_model_keyboard(model_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Confirmation keyboard for model deletion"""
    buttons = [
        [InlineKeyboardButton("✅ Да, удалить", callback_data=f'confirm_delete_model_{model_id}')],
        [InlineKeyboardButton("❌ Отмена", callback_data='admin_delete_model')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_menu_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin menu keyboard"""
    buttons = [
        [InlineKeyboardButton(get_text('admin_models', lang), callback_data='admin_models')],
        [InlineKeyboardButton(get_text('admin_instructions', lang), callback_data='admin_instructions')],
        [InlineKeyboardButton(get_text('admin_recipes', lang), callback_data='admin_recipes')],
        [InlineKeyboardButton(get_text('admin_tickets', lang), callback_data='admin_tickets')],
        [InlineKeyboardButton(get_text('admin_settings', lang), callback_data='admin_settings')],
        [InlineKeyboardButton(get_text('back_to_menu', lang), callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_models_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin models management keyboard"""
    buttons = [
        [InlineKeyboardButton(get_text('add_model', lang), callback_data='admin_add_model')],
        [InlineKeyboardButton(get_text('edit_model', lang), callback_data='admin_edit_model')],
        [InlineKeyboardButton(get_text('delete_model', lang), callback_data='admin_delete_model')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_instructions_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin instructions management keyboard"""
    buttons = [
        [InlineKeyboardButton(get_text('add_instruction', lang), callback_data='admin_add_instruction')],
        [InlineKeyboardButton("📋 Список инструкций", callback_data='admin_list_instructions')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_recipes_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin recipes management keyboard"""
    buttons = [
        [InlineKeyboardButton(get_text('add_recipe', lang), callback_data='admin_add_recipe')],
        [InlineKeyboardButton(get_text('list_recipes', lang), callback_data='admin_list_recipes')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_tickets_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin tickets management keyboard"""
    buttons = [
        [InlineKeyboardButton(get_text('open_tickets', lang), callback_data='admin_open_tickets')],
        [InlineKeyboardButton("📊 Статистика", callback_data='admin_ticket_stats')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin')]
    ]
    return InlineKeyboardMarkup(buttons)

def user_ticket_keyboard(ticket_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """User ticket management keyboard"""
    buttons = [
        [InlineKeyboardButton("✍ Написать сообщение", callback_data=f'user_ticket_message_{ticket_id}')],
        [InlineKeyboardButton("❌ Закрыть тикет", callback_data=f'user_ticket_close_{ticket_id}')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_tickets_list_keyboard(tickets, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin tickets list keyboard with ticket selection"""
    buttons = []
    
    # Add ticket buttons (max 10 tickets per page)
    for ticket in tickets[:10]:
        status_emoji = "🟢" if ticket.status.value == 'open' else "🟡" if ticket.status.value == 'in_progress' else "🔴"
        button_text = f"{status_emoji} T-{ticket.id} @{ticket.username or 'unknown'}"
        buttons.append([InlineKeyboardButton(button_text, callback_data=f'admin_ticket_{ticket.id}')])
    
    # Add navigation buttons
    buttons.append([InlineKeyboardButton("🔄 Обновить", callback_data='admin_open_tickets')])
    buttons.append([InlineKeyboardButton(get_text('back', lang), callback_data='admin_tickets')])
    
    return InlineKeyboardMarkup(buttons)

def admin_ticket_management_keyboard(ticket_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin ticket management keyboard"""
    buttons = [
        [InlineKeyboardButton("✍ Ответить клиенту", callback_data=f'admin_reply_ticket_{ticket_id}')],
        [InlineKeyboardButton("🟡 В работу", callback_data=f'admin_ticket_in_progress_{ticket_id}')],
        [InlineKeyboardButton("🔴 Закрыть тикет", callback_data=f'admin_ticket_close_{ticket_id}')],
        [InlineKeyboardButton("📋 К списку тикетов", callback_data='admin_open_tickets')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin_tickets')]
    ]
    return InlineKeyboardMarkup(buttons)

def instruction_type_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Instruction type selection keyboard"""
    buttons = [
        [InlineKeyboardButton("📄 PDF", callback_data='type_pdf')],
        [InlineKeyboardButton("🎥 Видео", callback_data='type_video')],
        [InlineKeyboardButton("🔗 Ссылка", callback_data='type_link')],
        [InlineKeyboardButton(get_text('cancel', lang), callback_data='admin_instructions')]
    ]
    return InlineKeyboardMarkup(buttons)

def confirmation_keyboard(action: str, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    buttons = [
        [
            InlineKeyboardButton(get_text('yes', lang), callback_data=f'confirm_{action}'),
            InlineKeyboardButton(get_text('no', lang), callback_data=f'cancel_{action}')
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def ticket_actions_keyboard(ticket_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Ticket actions keyboard for admin"""
    buttons = [
        [InlineKeyboardButton(get_text('reply_to_ticket', lang), callback_data=f'admin_reply_{ticket_id}')],
        [InlineKeyboardButton(get_text('close_ticket', lang), callback_data=f'admin_close_{ticket_id}')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin_tickets')]
    ]
    return InlineKeyboardMarkup(buttons)

def language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    buttons = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en')]
    ]
    return InlineKeyboardMarkup(buttons)

def cancel_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Simple cancel keyboard"""
    buttons = [[InlineKeyboardButton(get_text('cancel', lang), callback_data='cancel')]]
    return InlineKeyboardMarkup(buttons)

def back_cancel_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Back and cancel keyboard"""
    buttons = [
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_step')],
        [InlineKeyboardButton(get_text('cancel', lang), callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(buttons)

def admin_instructions_list_keyboard(instructions: List[Instruction], lang: str = 'ru') -> InlineKeyboardMarkup:
    """Admin instructions list keyboard"""
    buttons = []
    
    for instruction in instructions:
        # Add type emoji
        type_emoji = {
            InstructionType.PDF: "📄",
            InstructionType.VIDEO: "🎥",
            InstructionType.LINK: "🔗"
        }.get(instruction.type, "📄")
        
        buttons.append([InlineKeyboardButton(
            f"{type_emoji} {instruction.title}",
            callback_data=f'admin_instruction_{instruction.id}'
        )])
    
    buttons.append([InlineKeyboardButton(get_text('back', lang), callback_data='admin_instructions')])
    return InlineKeyboardMarkup(buttons)

def instruction_management_keyboard(instruction_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Instruction management keyboard for admin"""
    buttons = [
        [InlineKeyboardButton(get_text('bind_to_models', lang), callback_data=f'bind_instruction_{instruction_id}')],
        [InlineKeyboardButton(get_text('unbind_from_models', lang), callback_data=f'unbind_instruction_{instruction_id}')],
        [InlineKeyboardButton("✏️ Редактировать", callback_data=f'edit_instruction_{instruction_id}')],
        [InlineKeyboardButton("🗑 Удалить", callback_data=f'delete_instruction_{instruction_id}')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin_list_instructions')]
    ]
    return InlineKeyboardMarkup(buttons)

def recipe_management_keyboard(recipe_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Recipe management keyboard for admin"""
    buttons = [
        [InlineKeyboardButton(get_text('bind_recipe_to_models', lang), callback_data=f'bind_recipe_{recipe_id}')],
        [InlineKeyboardButton(get_text('unbind_recipe_from_models', lang), callback_data=f'unbind_recipe_{recipe_id}')],
        [InlineKeyboardButton("✏️ Редактировать", callback_data=f'edit_recipe_{recipe_id}')],
        [InlineKeyboardButton("🗑 Удалить", callback_data=f'delete_recipe_{recipe_id}')],
        [InlineKeyboardButton(get_text('back', lang), callback_data='admin_list_recipes')]
    ]
    return InlineKeyboardMarkup(buttons)

def recipes_keyboard(recipes: List, page: int = 0, total_pages: int = 1, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Recipes list keyboard with pagination"""
    buttons = []
    
    # Add recipes
    for recipe in recipes:
        buttons.append([InlineKeyboardButton(
            recipe.title, 
            callback_data=f'recipe_{recipe.id}'
        )])
    
    # Add pagination
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'recipes_page_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data='current_page'))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'recipes_page_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add back button
    buttons.append([InlineKeyboardButton(get_text('back', lang), callback_data='admin_recipes')])
    
    return InlineKeyboardMarkup(buttons)

def model_recipes_keyboard(recipes: List, model_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Model recipes keyboard for user"""
    buttons = []
    
    # Add recipes
    for recipe in recipes:
        if recipe.type.value == 'pdf':
            icon = "📎"
        elif recipe.type.value == 'video':
            icon = "🎬"
        elif recipe.type.value == 'link':
            icon = "🔗"
        else:
            icon = "📄"
        buttons.append([InlineKeyboardButton(
            f"{icon} {recipe.title}",
            callback_data=f'recipe_{recipe.id}'
        )])
    
    # Add download all button
    if recipes:
        buttons.append([InlineKeyboardButton(
            get_text('download_recipes_package', lang),
            callback_data=f'recipes_package_{model_id}'
        )])
    
    # Add back button
    buttons.append([InlineKeyboardButton(get_text('back_to_models', lang), callback_data='choose_model')])
    
    return InlineKeyboardMarkup(buttons)

def models_selection_keyboard(models: List[Model], instruction_id: int, action: str, 
                             selected_models: List[int] = None, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Models selection keyboard for binding/unbinding instructions"""
    if selected_models is None:
        selected_models = []
    
    buttons = []
    
    for model in models:
        # Check if model is selected
        is_selected = model.id in selected_models
        prefix = "✅" if is_selected else "⬜"
        
        buttons.append([InlineKeyboardButton(
            f"{prefix} {model.name}",
            callback_data=f'select_model_{model.id}_{instruction_id}_{action}'
        )])
    
    # Add action buttons
    if selected_models:
        action_text = get_text('bind_instruction_to_models', lang) if action == 'bind' else get_text('unbind_from_models', lang)
        buttons.append([InlineKeyboardButton(
            f"{action_text} ({len(selected_models)})",
            callback_data=f'confirm_{action}_instruction_{instruction_id}'
        )])
    
    buttons.append([InlineKeyboardButton(get_text('cancel', lang), callback_data='admin_list_instructions')])
    return InlineKeyboardMarkup(buttons)

def new_instruction_models_keyboard(models: List[Model], selected_models: List[int] = None, 
                                   page: int = 0, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Models selection keyboard for new instruction creation"""
    if selected_models is None:
        selected_models = []
    
    buttons = []
    
    # Show models with checkboxes
    for model in models:
        is_selected = model.id in selected_models
        prefix = "✅" if is_selected else "⬜"
        
        action = 'unbind_model' if is_selected else 'bind_model'
        buttons.append([InlineKeyboardButton(
            f"{prefix} {model.name}",
            callback_data=f'{action}_{model.id}'
        )])
    
    # Add pagination if needed
    if len(models) >= 10:  # Assuming 10 models per page
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'page_models_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}", callback_data='current_page'))
        if len(models) == 10:  # More pages available
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'page_models_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add action buttons
    if selected_models:
        buttons.append([InlineKeyboardButton(
            f"💾 Продолжить ({len(selected_models)} моделей)",
            callback_data='confirm_create_instruction'
        )])
    
    # Navigation buttons
    buttons.append([
        InlineKeyboardButton("⬅️ Назад", callback_data='back_step'),
        InlineKeyboardButton("❌ Отмена", callback_data='cancel')
    ])
    
    return InlineKeyboardMarkup(buttons)

def new_recipe_models_keyboard(models: List[Model], selected_models: List[int] = None, 
                              page: int = 0, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Models selection keyboard for new recipe creation"""
    if selected_models is None:
        selected_models = []
    
    buttons = []
    
    # Show models with checkboxes
    for model in models:
        is_selected = model.id in selected_models
        prefix = "✅" if is_selected else "⬜"
        
        action = 'unbind_recipe_model' if is_selected else 'bind_recipe_model'
        buttons.append([InlineKeyboardButton(
            f"{prefix} {model.name}",
            callback_data=f'{action}_{model.id}'
        )])
    
    # Add pagination if needed
    if len(models) >= 10:  # Assuming 10 models per page
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f'page_recipe_models_{page-1}'))
        nav_buttons.append(InlineKeyboardButton(f"{page+1}", callback_data='current_page'))
        if len(models) == 10:  # More pages available
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f'page_recipe_models_{page+1}'))
        buttons.append(nav_buttons)
    
    # Add action buttons
    if selected_models:
        buttons.append([InlineKeyboardButton(
            f"💾 Продолжить ({len(selected_models)} моделей)",
            callback_data='confirm_create_recipe'
        )])
    
    # Navigation buttons
    buttons.append([
        InlineKeyboardButton("⬅️ Назад", callback_data='back_step'),
        InlineKeyboardButton("❌ Отмена", callback_data='cancel')
    ])
    
    return InlineKeyboardMarkup(buttons)
