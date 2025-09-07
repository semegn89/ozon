# DEPRECATED: This file is kept for reference
# Use bot_new.py for the new implementation

from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
)
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
)
import logging

# WARNING: Tokens should be in .env file, not hardcoded!
TOKEN = '7870121478:AAGtGNo-Hrx3Ox4OZsbuqZniexzeR_tl47w'
ADMIN_CHAT_ID = 318073844  # <-- подставь свой chat_id позже

# ---------- Справочники моделей, инструкций и рецептов ----------
MODELS = {
    'lac': {
        'name': "LAC LAICHY L-6707",
        'manual_file_id': 'file_id_инструкции_lac',
        'recipes_file_id': 'file_id_рецептов_lac',
        'manual_text': "Это инструкция для LAC LAICHY L-6707.",
        'recipes_text': "Книга рецептов для LAC LAICHY L-6707.",
    },
    'orv': {
        'name': "ORVIKA ORM-8861",
        'manual_file_id': 'file_id_инструкции_orv',
        'recipes_file_id': 'file_id_рецептов_orv',
        'manual_text': "Это инструкция для ORVIKA ORM-8861.",
        'recipes_text': "Книга рецептов для ORVIKA ORM-8861.",
    },
    # Добавь другие модели по аналогии
}

# -------------- Состояния пользователя ----------------
user_support_state = {}

# -------------- Логгер -----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------- Клавиатуры ----------------
def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("📦 Выбрать модель", callback_data='choose_model')],
        [InlineKeyboardButton("🍽️ Рецепты", callback_data='recipes')],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data='support')],
    ]
    return InlineKeyboardMarkup(buttons)

def models_keyboard():
    buttons = []
    for model_id, data in MODELS.items():
        buttons.append([InlineKeyboardButton(data["name"], callback_data=f'model_{model_id}')])
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')])
    return InlineKeyboardMarkup(buttons)

def model_options_keyboard(model_id):
    buttons = [
        [InlineKeyboardButton("📄 Инструкция", callback_data=f'manual_{model_id}')],
        [InlineKeyboardButton("🍽️ Книга рецептов", callback_data=f'recipes_{model_id}')],
        [InlineKeyboardButton("⬅️ К моделям", callback_data='choose_model')],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(buttons)

# ------------- Хендлеры ----------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"Здравствуйте, {user.first_name}!\nЯ бот-помощник по технике. Выберите действие:",
        reply_markup=main_menu_keyboard()
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == 'main_menu':
        query.edit_message_text("Выберите действие:", reply_markup=main_menu_keyboard())

    elif data == 'choose_model':
        query.edit_message_text("Выберите модель:", reply_markup=models_keyboard())

    elif data.startswith('model_'):
        model_id = data.split('_')[1]
        model = MODELS.get(model_id)
        if model:
            query.edit_message_text(
                f"Вы выбрали модель:\n<b>{model['name']}</b>",
                reply_markup=model_options_keyboard(model_id),
                parse_mode=ParseMode.HTML
            )
        else:
            query.edit_message_text("Модель не найдена!", reply_markup=models_keyboard())

    elif data.startswith('manual_'):
        model_id = data.split('_')[1]
        model = MODELS.get(model_id)
        if model and model.get('manual_file_id'):
            context.bot.send_document(
                chat_id=query.message.chat_id,
                document=model['manual_file_id'],
                caption=model['manual_text']
            )
            query.answer("Инструкция отправлена.")
        else:
            query.answer("Инструкция временно недоступна.", show_alert=True)

    elif data.startswith('recipes_'):
        model_id = data.split('_')[1]
        model = MODELS.get(model_id)
        if model and model.get('recipes_file_id'):
            context.bot.send_document(
                chat_id=query.message.chat_id,
                document=model['recipes_file_id'],
                caption=model['recipes_text']
            )
            query.answer("Книга рецептов отправлена.")
        else:
            query.answer("Книга рецептов временно недоступна.", show_alert=True)

    elif data == 'recipes':
        # Показываем список моделей для выбора рецептов
        query.edit_message_text("Выберите модель для получения книги рецептов:", reply_markup=models_keyboard())

    elif data == 'support':
        user_support_state[user_id] = True
        query.edit_message_text(
            "Опишите ваш вопрос или прикрепите фото/видео. Мы поможем!\n\n"
            "❗️ Пожалуйста, напишите подробно.",
            reply_markup=main_menu_keyboard()
        )

def support_message_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    if user_support_state.get(user_id):
        # Пересылаем админу
        txt = f"❗️Вопрос от @{user.username or 'нет username'} (id: {user.id}):\n"
        if update.message.text:
            context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=txt + update.message.text
            )
        elif update.message.photo:
            context.bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                photo=update.message.photo[-1].file_id,
                caption=txt
            )
        elif update.message.document:
            context.bot.send_document(
                chat_id=ADMIN_CHAT_ID,
                document=update.message.document.file_id,
                caption=txt
            )
        elif update.message.voice:
            context.bot.send_voice(
                chat_id=ADMIN_CHAT_ID,
                voice=update.message.voice.file_id,
                caption=txt
            )
        update.message.reply_text("Ваш вопрос отправлен, мы ответим в ближайшее время!", reply_markup=main_menu_keyboard())
        user_support_state[user_id] = False

def unknown_message(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Пожалуйста, используйте меню для навигации по функциям бота.",
        reply_markup=main_menu_keyboard()
    )

def error_handler(update, context):
    logger.error(f'Ошибка: {context.error}')
    if update and hasattr(update, 'message'):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Произошла ошибка. Пожалуйста, попробуйте позже."
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Вопросы поддержки: текст, фото, документы, голосовые
    dp.add_handler(MessageHandler(
        Filters.text | Filters.photo | Filters.document | Filters.voice,
        support_message_handler
    ))
    # Неизвестные сообщения (не через режим поддержки)
    dp.add_handler(MessageHandler(Filters.all, unknown_message))

    dp.add_error_handler(error_handler)

    updater.start_polling()
    logger.info("Бот запущен!")
    updater.idle()

if __name__ == "__main__":
    main()