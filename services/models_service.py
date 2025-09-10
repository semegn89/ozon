from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Model, Instruction, InstructionType
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ModelsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_models(self, page: int = 0, limit: int = 10) -> List[Model]:
        """Get paginated list of models"""
        offset = page * limit
        return self.db.query(Model).order_by(Model.created_at.desc(), Model.id.desc()).offset(offset).limit(limit).all()
    
    def search_models(self, query: str, page: int = 0, limit: int = 10) -> List[Model]:
        """Search models by name, description or tags"""
        offset = page * limit
        search_filter = or_(
            Model.name.ilike(f"%{query}%"),
            Model.description.ilike(f"%{query}%"),
            Model.tags.ilike(f"%{query}%")
        )
        return self.db.query(Model).filter(search_filter).order_by(Model.created_at.desc(), Model.id.desc()).offset(offset).limit(limit).all()
    
    def get_model_by_id(self, model_id: int) -> Optional[Model]:
        """Get model by ID"""
        return self.db.query(Model).filter(Model.id == model_id).first()
    
    def get_model_by_name(self, name: str) -> Optional[Model]:
        """Get model by name"""
        return self.db.query(Model).filter(Model.name == name).first()
    
    def create_model(self, name: str, description: str = None, tags: str = None) -> Model:
        """Create new model"""
        model = Model(
            name=name,
            description=description,
            tags=tags
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        logger.info(f"Created model: {model.name} (ID: {model.id})")
        return model
    
    def update_model(self, model_id: int, **kwargs) -> Optional[Model]:
        """Update model"""
        model = self.get_model_by_id(model_id)
        if not model:
            return None
        
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        self.db.commit()
        self.db.refresh(model)
        logger.info(f"Updated model: {model.name} (ID: {model.id})")
        return model
    
    def delete_model(self, model_id: int) -> bool:
        """Delete model"""
        model = self.get_model_by_id(model_id)
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        logger.info(f"Deleted model: {model.name} (ID: {model.id})")
        return True
    
    def get_model_instructions(self, model_id: int) -> List[Instruction]:
        """Get all instructions for a model"""
        model = self.get_model_by_id(model_id)
        if not model:
            return []
        return model.instructions
    
    def add_instruction_to_model(self, model_id: int, instruction_id: int) -> bool:
        """Add instruction to model"""
        model = self.get_model_by_id(model_id)
        instruction = self.db.query(Instruction).filter(Instruction.id == instruction_id).first()
        
        if not model or not instruction:
            return False
        
        if instruction not in model.instructions:
            model.instructions.append(instruction)
            self.db.commit()
            logger.info(f"Added instruction {instruction.title} to model {model.name}")
            return True
        return False
    
    def remove_instruction_from_model(self, model_id: int, instruction_id: int) -> bool:
        """Remove instruction from model"""
        model = self.get_model_by_id(model_id)
        instruction = self.db.query(Instruction).filter(Instruction.id == instruction_id).first()
        
        if not model or not instruction:
            return False
        
        if instruction in model.instructions:
            model.instructions.remove(instruction)
            self.db.commit()
            logger.info(f"Removed instruction {instruction.title} from model {model.name}")
            return True
        return False
    
    def get_models_count(self) -> int:
        """Get total count of models"""
        return self.db.query(Model).count()
    
    def get_search_models_count(self, query: str) -> int:
        """Get count of models matching search query"""
        search_filter = or_(
            Model.name.ilike(f"%{query}%"),
            Model.description.ilike(f"%{query}%"),
            Model.tags.ilike(f"%{query}%")
        )
        return self.db.query(Model).filter(search_filter).count()
