# SAG Shop - Telegram Mini App

Веб-приложение для Telegram, которое позволяет пользователям просматривать инструкции и рецепты для различных моделей устройств.

## 🚀 Возможности

- 📱 **Просмотр моделей** - список всех доступных моделей устройств
- 📄 **Инструкции** - пошаговые руководства для каждой модели
- 🍳 **Рецепты** - специальные рецепты и советы
- 🔍 **Поиск** - быстрый поиск по моделям, инструкциям и рецептам
- 🆘 **Поддержка** - система обращений для пользователей
- 📱 **Адаптивный дизайн** - работает на всех устройствах

## 🛠 Технологии

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (PostgreSQL/SQLite)
- **Telegram API**: Telegram WebApp API
- **UI/UX**: Современный дизайн с поддержкой тем Telegram

## 📁 Структура проекта

```
webapp/
├── index.html          # Главная страница
├── style.css           # Стили приложения
├── script.js           # JavaScript логика
├── manifest.json       # Конфигурация PWA
├── api.py              # Flask API сервер
├── requirements.txt    # Python зависимости
└── README.md          # Документация
```

## 🚀 Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
Убедитесь, что база данных настроена и таблицы созданы.

### 3. Запуск API сервера
```bash
python api.py
```

API будет доступен на `http://localhost:5000`

### 4. Настройка веб-сервера
Разместите файлы `index.html`, `style.css`, `script.js` и `manifest.json` на веб-сервере.

## 🔗 Интеграция с ботом

### Добавление кнопки в бот
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_webapp_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть приложение", web_app=WebAppInfo(url="https://your-domain.com/webapp/"))]
    ]
    return InlineKeyboardMarkup(keyboard)
```

### Обработка данных от веб-приложения
```python
def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.effective_message.web_app_data.data)
    # Обработка данных от веб-приложения
```

## 📱 API Endpoints

### GET /api/models
Получить список всех моделей

### GET /api/instructions
Получить список всех инструкций

### GET /api/recipes
Получить список всех рецептов

### GET /api/tickets?user_id={id}
Получить обращения пользователя

### POST /api/tickets
Создать новое обращение

### GET /api/instruction/{id}/download
Скачать файл инструкции

### GET /api/recipe/{id}/download
Скачать файл рецепта

## 🎨 Кастомизация

### Темы Telegram
Приложение автоматически адаптируется под тему Telegram пользователя:
- Светлая тема
- Темная тема
- Системная тема

### Цвета
Основные цвета можно изменить в `style.css`:
```css
:root {
    --primary-color: #2481cc;
    --secondary-color: #f8f9fa;
    --text-color: #000000;
    --hint-color: #999999;
}
```

## 📱 PWA функции

- **Установка на устройство** - пользователи могут установить приложение как нативное
- **Офлайн режим** - базовый функционал работает без интернета
- **Push уведомления** - уведомления о новых инструкциях и рецептах

## 🔒 Безопасность

- Валидация всех входных данных
- Защита от XSS атак
- CORS настройки
- Проверка прав доступа

## 📊 Мониторинг

- Логирование всех API запросов
- Метрики производительности
- Отслеживание ошибок
- Health check endpoint

## 🚀 Деплой

### Railway
1. Подключите репозиторий к Railway
2. Настройте переменные окружения
3. Railway автоматически развернет приложение

### Heroku
1. Создайте Procfile
2. Настройте переменные окружения
3. Деплойте через Git

### VPS
1. Установите Nginx
2. Настройте SSL сертификат
3. Запустите через systemd

## 📝 Лицензия

MIT License

## 🤝 Поддержка

Для вопросов и предложений создайте issue в репозитории или обратитесь в службу поддержки через бот.
