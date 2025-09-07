#!/usr/bin/env python3
"""
Database initialization script
Creates tables and adds sample data
"""

from models import create_tables, get_session, InstructionType
from services.models_service import ModelsService
from services.files_service import FilesService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database with sample data"""
    logger.info("Creating database tables...")
    create_tables()
    
    db = get_session()
    try:
        models_service = ModelsService(db)
        files_service = FilesService(db)
        
        # Check if data already exists
        if models_service.get_models_count() > 0:
            logger.info("Database already has data, skipping initialization")
            return
        
        logger.info("Adding sample data...")
        
        # Create sample models
        model1 = models_service.create_model(
            name="LAC LAICHY L-6707",
            description="Многофункциональная кухонная машина с мощным двигателем и множеством насадок",
            tags="кухонная машина, тесто, взбивание, измельчение"
        )
        
        model2 = models_service.create_model(
            name="ORVIKA ORM-8861",
            description="Компактная кухонная машина для домашнего использования",
            tags="кухонная машина, компактная, домашняя"
        )
        
        # Create sample instructions
        instruction1 = files_service.create_instruction(
            title="Руководство пользователя LAC L-6707",
            instruction_type=InstructionType.PDF,
            description="Полное руководство по эксплуатации кухонной машины LAC L-6707",
            tg_file_id="BQACAgIAAxkBAAIBY2Y..."  # Placeholder file ID
        )
        
        instruction2 = files_service.create_instruction(
            title="Книга рецептов LAC L-6707",
            instruction_type=InstructionType.PDF,
            description="Коллекция рецептов для кухонной машины LAC L-6707",
            tg_file_id="BQACAgIAAxkBAAIBY2Y..."  # Placeholder file ID
        )
        
        instruction3 = files_service.create_instruction(
            title="Видео-инструкция по сборке",
            instruction_type=InstructionType.VIDEO,
            description="Пошаговая видео-инструкция по сборке и разборке машины",
            tg_file_id="BAADBAAD..."  # Placeholder file ID
        )
        
        instruction4 = files_service.create_instruction(
            title="Официальный сайт поддержки",
            instruction_type=InstructionType.LINK,
            description="Официальный сайт производителя с дополнительными материалами",
            url="https://example.com/support"
        )
        
        # Bind instructions to models
        models_service.add_instruction_to_model(model1.id, instruction1.id)
        models_service.add_instruction_to_model(model1.id, instruction2.id)
        models_service.add_instruction_to_model(model1.id, instruction3.id)
        models_service.add_instruction_to_model(model1.id, instruction4.id)
        
        models_service.add_instruction_to_model(model2.id, instruction1.id)  # Shared instruction
        models_service.add_instruction_to_model(model2.id, instruction4.id)  # Shared instruction
        
        logger.info("Sample data added successfully!")
        logger.info(f"Created {models_service.get_models_count()} models")
        logger.info(f"Created {files_service.get_instructions_count()} instructions")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
