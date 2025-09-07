#!/usr/bin/env python3
"""
Simple test script for the bot
Tests basic functionality without actually running the bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import create_tables, get_session
from services.models_service import ModelsService
from services.files_service import FilesService
from services.support_service import SupportService
from config import BOT_TOKEN, ADMIN_CHAT_IDS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test database operations"""
    logger.info("Testing database operations...")
    
    # Create tables
    create_tables()
    logger.info("✅ Database tables created")
    
    # Test database connection
    db = get_session()
    try:
        models_service = ModelsService(db)
        files_service = FilesService(db)
        support_service = SupportService(db)
        
        # Test models
        models_count = models_service.get_models_count()
        logger.info(f"✅ Models service working, count: {models_count}")
        
        # Test instructions
        instructions_count = files_service.get_instructions_count()
        logger.info(f"✅ Files service working, count: {instructions_count}")
        
        # Test tickets
        tickets_count = support_service.get_tickets_count()
        logger.info(f"✅ Support service working, count: {tickets_count}")
        
        logger.info("✅ All database operations successful")
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False
    finally:
        db.close()
    
    return True

def test_config():
    """Test configuration"""
    logger.info("Testing configuration...")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not configured")
        return False
    
    if not ADMIN_CHAT_IDS:
        logger.error("❌ ADMIN_CHAT_IDS not configured")
        return False
    
    logger.info(f"✅ Bot token configured: {BOT_TOKEN[:10]}...")
    logger.info(f"✅ Admin chat IDs: {ADMIN_CHAT_IDS}")
    
    return True

def test_imports():
    """Test all imports"""
    logger.info("Testing imports...")
    
    try:
        from keyboards import main_menu_keyboard
        from texts import get_text
        logger.info("✅ All imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ Import test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting bot tests...")
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("Database", test_database),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
            logger.info(f"✅ {test_name} test passed")
        else:
            logger.error(f"❌ {test_name} test failed")
    
    logger.info(f"\n🏁 Tests completed: {passed}/{total} passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Bot is ready to run.")
        logger.info("Run 'python bot_new.py' to start the bot.")
    else:
        logger.error("💥 Some tests failed. Please fix the issues before running the bot.")
        sys.exit(1)

if __name__ == "__main__":
    main()
