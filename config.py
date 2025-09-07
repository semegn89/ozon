import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_IDS = [int(x.strip()) for x in os.getenv('ADMIN_CHAT_IDS', '').split(',') if x.strip()]
DB_URL = os.getenv('DB_URL', 'sqlite:///data.db')
MODE = os.getenv('MODE', 'POLLING')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required in .env file")

if not ADMIN_CHAT_IDS:
    raise ValueError("ADMIN_CHAT_IDS is required in .env file")

# Bot settings
PAGINATION_LIMIT = 10
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
TICKET_CLEANUP_DAYS = 90
