# Пример админ-панели в Telegram боте
# Добавить в bot_new.py

async def handle_admin_webapp_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление веб-приложением через бота"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    keyboard = [
        [InlineKeyboardButton("📱 Добавить модель", callback_data='admin_add_model')],
        [InlineKeyboardButton("📋 Добавить инструкцию", callback_data='admin_add_instruction')],
        [InlineKeyboardButton("🍳 Добавить рецепт", callback_data='admin_add_recipe')],
        [InlineKeyboardButton("📊 Статистика веб-приложения", callback_data='admin_webapp_stats')],
        [InlineKeyboardButton("🔄 Обновить кэш", callback_data='admin_refresh_cache')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='admin_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔧 **Управление веб-приложением**\n\n"
        "Здесь вы можете управлять контентом веб-приложения:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_admin_add_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление новой модели через бота"""
    query = update.callback_query
    await query.answer()
    
    # Устанавливаем состояние для добавления модели
    user_states[query.from_user.id] = UserState(
        state='admin_add_model_name',
        data={}
    )
    
    await query.edit_message_text(
        "📱 **Добавление новой модели**\n\n"
        "Введите название модели:",
        parse_mode='Markdown'
    )

async def handle_admin_add_model_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка названия модели"""
    user_id = update.effective_user.id
    user_state = user_states.get(user_id)
    
    if not user_state or user_state.state != 'admin_add_model_name':
        return
    
    model_name = update.message.text
    user_state.data['name'] = model_name
    user_state.state = 'admin_add_model_description'
    
    await update.message.reply_text(
        "📝 Введите описание модели:"
    )

async def handle_admin_add_model_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка описания модели"""
    user_id = update.effective_user.id
    user_state = user_states.get(user_id)
    
    if not user_state or user_state.state != 'admin_add_model_description':
        return
    
    description = update.message.text
    user_state.data['description'] = description
    user_state.state = 'admin_add_model_tags'
    
    await update.message.reply_text(
        "🏷️ Введите теги через запятую:"
    )

async def handle_admin_add_model_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка тегов модели и сохранение"""
    user_id = update.effective_user.id
    user_state = user_states.get(user_id)
    
    if not user_state or user_state.state != 'admin_add_model_tags':
        return
    
    tags = update.message.text
    
    # Сохраняем модель в базу данных
    db = get_session()
    try:
        models_service = ModelsService(db)
        new_model = models_service.create_model(
            name=user_state.data['name'],
            description=user_state.data['description'],
            tags=tags
        )
        
        # Отправляем в веб-приложение через API
        await send_to_webapp_api('POST', '/api/models', {
            'name': new_model.name,
            'description': new_model.description,
            'tags': new_model.tags
        })
        
        await update.message.reply_text(
            f"✅ **Модель добавлена!**\n\n"
            f"📱 {new_model.name}\n"
            f"📝 {new_model.description}\n"
            f"🏷️ {new_model.tags}\n\n"
            f"Модель доступна в веб-приложении!",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()
        # Очищаем состояние
        if user_id in user_states:
            del user_states[user_id]

async def send_to_webapp_api(method: str, endpoint: str, data: dict = None):
    """Отправка данных в веб-приложение через API"""
    import aiohttp
    
    url = f"https://gakshop.com{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        if method == 'GET':
            async with session.get(url) as response:
                return await response.json()
        elif method == 'POST':
            async with session.post(url, json=data) as response:
                return await response.json()
        elif method == 'PUT':
            async with session.put(url, json=data) as response:
                return await response.json()
        elif method == 'DELETE':
            async with session.delete(url) as response:
                return await response.json()
