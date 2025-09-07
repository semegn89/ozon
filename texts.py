# Localization texts for the bot

TEXTS = {
    'ru': {
        # Main menu
        'welcome': "Здравствуйте, {name}!\nЯ бот-помощник по технике. Выберите действие:",
        'main_menu': "Выберите действие:",
        
        # Models
        'choose_model': "📦 Выбрать модель",
        'models_list': "Выберите модель:",
        'model_not_found': "Модель не найдена!",
        'model_selected': "Вы выбрали модель:\n<b>{name}</b>\n\n{description}",
        'model_tags': "🏷️ Теги: {tags}",
        
        # Instructions
        'instructions': "🍽️ Рецепты",
        'instructions_list': "Инструкции для модели <b>{model_name}</b>:",
        'instruction_sent': "Инструкция отправлена.",
        'instruction_unavailable': "Инструкция временно недоступна.",
        'download_package': "⬇️ Скачать комплект",
        'package_sent': "Комплект инструкций отправлен.",
        
        # Support
        'support': "❓ Задать вопрос",
        'support_question': "Опишите ваш вопрос или прикрепите фото/видео. Мы поможем!\n\n❗️ Пожалуйста, напишите подробно.",
        'support_sent': "Ваш вопрос отправлен, мы ответим в ближайшее время!\n\n🆔 ID обращения: T-{ticket_id}",
        'my_tickets': "📋 Мои обращения",
        'tickets_list': "Ваши обращения:",
        'ticket_status_open': "🟢 Открыто",
        'ticket_status_in_progress': "🟡 В работе",
        'ticket_status_closed': "🔴 Закрыто",
        'no_tickets': "У вас пока нет обращений.",
        
        # Search
        'search_model': "🔎 Поиск модели",
        'search_prompt': "Введите название модели для поиска:",
        'search_results': "Результаты поиска для '{query}':",
        'no_search_results': "По вашему запросу ничего не найдено.",
        
        # Navigation
        'back': "⬅️ Назад",
        'back_to_models': "⬅️ К моделям",
        'back_to_menu': "⬅️ Главное меню",
        'home': "🏠 В меню",
        
        # Admin
        'admin_menu': "🔧 Админ-панель",
        'admin_models': "📦 Модели",
        'admin_instructions': "📄 Инструкции",
        'admin_tickets': "🎫 Обращения",
        'admin_settings': "⚙️ Настройки",
        
        # Admin - Models
        'add_model': "➕ Добавить модель",
        'edit_model': "✏️ Редактировать",
        'delete_model': "🗑 Удалить",
        'model_name_prompt': "Введите название модели:",
        'model_description_prompt': "Введите описание модели (или /skip для пропуска):",
        'model_tags_prompt': "Введите теги через запятую (или /skip для пропуска):",
        'model_created': "Модель '{name}' создана!",
        'model_updated': "Модель '{name}' обновлена!",
        'model_deleted': "Модель '{name}' удалена!",
        'confirm_delete': "Вы уверены, что хотите удалить модель '{name}'?",
        'delete_confirmed': "Модель удалена.",
        'delete_cancelled': "Удаление отменено.",
        
        # Admin - Instructions
        'add_instruction': "➕ Добавить инструкцию",
        'instruction_title_prompt': "Введите название инструкции:",
        'instruction_type_prompt': "Выберите тип инструкции:",
        'instruction_description_prompt': "Введите описание (или /skip для пропуска):",
        'instruction_file_prompt': "Загрузите файл или отправьте URL:",
        'instruction_created': "Инструкция '{title}' создана!",
        'instruction_updated': "Инструкция '{title}' обновлена!",
        'instruction_deleted': "Инструкция '{title}' удалена!",
        'bind_to_models': "Привязать к моделям",
        'instruction_bound': "Инструкция привязана к моделям!",
        
        # Admin - Tickets
        'open_tickets': "Открытые обращения",
        'ticket_details': "Обращение #{ticket_id}\nПользователь: @{username} (ID: {user_id})\nСтатус: {status}\nСоздано: {created_at}",
        'reply_to_ticket': "✉️ Ответить",
        'close_ticket': "✅ Закрыть",
        'ticket_reply_prompt': "Введите ответ пользователю:",
        'ticket_replied': "Ответ отправлен пользователю.",
        'ticket_closed': "Обращение закрыто.",
        
        # Errors
        'error_occurred': "Произошла ошибка. Пожалуйста, попробуйте позже.",
        'access_denied': "У вас нет прав для выполнения этой команды.",
        'invalid_input': "Неверный ввод. Попробуйте еще раз.",
        'file_too_large': "Файл слишком большой. Максимальный размер: {size}MB",
        'unsupported_file': "Неподдерживаемый тип файла.",
        
        # General
        'processing': "⌛ Обработка...",
        'cancel': "❌ Отмена",
        'skip': "⏭️ Пропустить",
        'confirm': "✅ Подтвердить",
        'yes': "Да",
        'no': "Нет",
        'page': "Страница {current} из {total}",
        'total_items': "Всего: {count}",
    },
    
    'en': {
        # Main menu
        'welcome': "Hello, {name}!\nI'm a technical support bot. Choose an action:",
        'main_menu': "Choose an action:",
        
        # Models
        'choose_model': "📦 Choose Model",
        'models_list': "Choose a model:",
        'model_not_found': "Model not found!",
        'model_selected': "You selected model:\n<b>{name}</b>\n\n{description}",
        'model_tags': "🏷️ Tags: {tags}",
        
        # Instructions
        'instructions': "🍽️ Recipes",
        'instructions_list': "Instructions for model <b>{model_name}</b>:",
        'instruction_sent': "Instruction sent.",
        'instruction_unavailable': "Instruction temporarily unavailable.",
        'download_package': "⬇️ Download Package",
        'package_sent': "Instruction package sent.",
        
        # Support
        'support': "❓ Ask Question",
        'support_question': "Describe your question or attach photo/video. We'll help!\n\n❗️ Please be detailed.",
        'support_sent': "Your question has been sent, we'll respond soon!\n\n🆔 Ticket ID: T-{ticket_id}",
        'my_tickets': "📋 My Tickets",
        'tickets_list': "Your tickets:",
        'ticket_status_open': "🟢 Open",
        'ticket_status_in_progress': "🟡 In Progress",
        'ticket_status_closed': "🔴 Closed",
        'no_tickets': "You have no tickets yet.",
        
        # Search
        'search_model': "🔎 Search Model",
        'search_prompt': "Enter model name to search:",
        'search_results': "Search results for '{query}':",
        'no_search_results': "Nothing found for your query.",
        
        # Navigation
        'back': "⬅️ Back",
        'back_to_models': "⬅️ To Models",
        'back_to_menu': "⬅️ Main Menu",
        'home': "🏠 To Menu",
        
        # Admin
        'admin_menu': "🔧 Admin Panel",
        'admin_models': "📦 Models",
        'admin_instructions': "📄 Instructions",
        'admin_tickets': "🎫 Tickets",
        'admin_settings': "⚙️ Settings",
        
        # Admin - Models
        'add_model': "➕ Add Model",
        'edit_model': "✏️ Edit",
        'delete_model': "🗑 Delete",
        'model_name_prompt': "Enter model name:",
        'model_description_prompt': "Enter model description (or /skip to skip):",
        'model_tags_prompt': "Enter tags separated by commas (or /skip to skip):",
        'model_created': "Model '{name}' created!",
        'model_updated': "Model '{name}' updated!",
        'model_deleted': "Model '{name}' deleted!",
        'confirm_delete': "Are you sure you want to delete model '{name}'?",
        'delete_confirmed': "Model deleted.",
        'delete_cancelled': "Deletion cancelled.",
        
        # Admin - Instructions
        'add_instruction': "➕ Add Instruction",
        'instruction_title_prompt': "Enter instruction title:",
        'instruction_type_prompt': "Choose instruction type:",
        'instruction_description_prompt': "Enter description (or /skip to skip):",
        'instruction_file_prompt': "Upload file or send URL:",
        'instruction_created': "Instruction '{title}' created!",
        'instruction_updated': "Instruction '{title}' updated!",
        'instruction_deleted': "Instruction '{title}' deleted!",
        'bind_to_models': "Bind to Models",
        'instruction_bound': "Instruction bound to models!",
        
        # Admin - Tickets
        'open_tickets': "Open Tickets",
        'ticket_details': "Ticket #{ticket_id}\nUser: @{username} (ID: {user_id})\nStatus: {status}\nCreated: {created_at}",
        'reply_to_ticket': "✉️ Reply",
        'close_ticket': "✅ Close",
        'ticket_reply_prompt': "Enter reply to user:",
        'ticket_replied': "Reply sent to user.",
        'ticket_closed': "Ticket closed.",
        
        # Errors
        'error_occurred': "An error occurred. Please try again later.",
        'access_denied': "You don't have permission to perform this action.",
        'invalid_input': "Invalid input. Please try again.",
        'file_too_large': "File too large. Maximum size: {size}MB",
        'unsupported_file': "Unsupported file type.",
        
        # General
        'processing': "⌛ Processing...",
        'cancel': "❌ Cancel",
        'skip': "⏭️ Skip",
        'confirm': "✅ Confirm",
        'yes': "Yes",
        'no': "No",
        'page': "Page {current} of {total}",
        'total_items': "Total: {count}",
    }
}

def get_text(key: str, lang: str = 'ru', **kwargs) -> str:
    """Get localized text"""
    return TEXTS.get(lang, TEXTS['ru']).get(key, key).format(**kwargs)
