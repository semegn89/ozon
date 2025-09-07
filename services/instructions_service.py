from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Instruction, Model, InstructionType
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class InstructionsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_instructions(self, page: int = 0, limit: int = 10) -> List[Instruction]:
        """Get paginated list of instructions"""
        offset = page * limit
        return self.db.query(Instruction).offset(offset).limit(limit).all()
    
    def get_instruction_by_id(self, instruction_id: int) -> Optional[Instruction]:
        """Get instruction by ID"""
        return self.db.query(Instruction).filter(Instruction.id == instruction_id).first()
    
    def get_instruction_by_title(self, title: str) -> Optional[Instruction]:
        """Get instruction by title"""
        return self.db.query(Instruction).filter(Instruction.title == title).first()
    
    def create_instruction(self, title: str, instruction_type: InstructionType, 
                          description: str = None, tg_file_id: str = None, 
                          url: str = None) -> Instruction:
        """Create new instruction"""
        instruction = Instruction(
            title=title,
            type=instruction_type,
            description=description,
            tg_file_id=tg_file_id,
            url=url
        )
        self.db.add(instruction)
        self.db.commit()
        self.db.refresh(instruction)
        logger.info(f"Created instruction: {instruction.title} (ID: {instruction.id})")
        return instruction
    
    def update_instruction(self, instruction_id: int, **kwargs) -> Optional[Instruction]:
        """Update instruction"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instruction, key):
                setattr(instruction, key, value)
        
        self.db.commit()
        self.db.refresh(instruction)
        logger.info(f"Updated instruction: {instruction.title} (ID: {instruction.id})")
        return instruction
    
    def delete_instruction(self, instruction_id: int) -> bool:
        """Delete instruction"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return False
        
        self.db.delete(instruction)
        self.db.commit()
        logger.info(f"Deleted instruction: {instruction.title} (ID: {instruction.id})")
        return True
    
    def get_instruction_models(self, instruction_id: int) -> List[Model]:
        """Get all models for an instruction"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return []
        return instruction.models
    
    def bind_instruction_to_models(self, instruction_id: int, model_ids: List[int]) -> bool:
        """Bind instruction to multiple models"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return False
        
        models = self.db.query(Model).filter(Model.id.in_(model_ids)).all()
        if not models:
            return False
        
        # Add models that are not already bound
        new_models = [model for model in models if model not in instruction.models]
        if new_models:
            instruction.models.extend(new_models)
            self.db.commit()
            logger.info(f"Bound instruction {instruction.title} to {len(new_models)} models")
            return True
        return False
    
    def unbind_instruction_from_models(self, instruction_id: int, model_ids: List[int]) -> bool:
        """Unbind instruction from multiple models"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return False
        
        models_to_remove = [model for model in instruction.models if model.id in model_ids]
        if models_to_remove:
            for model in models_to_remove:
                instruction.models.remove(model)
            self.db.commit()
            logger.info(f"Unbound instruction {instruction.title} from {len(models_to_remove)} models")
            return True
        return False
    
    def get_instructions_count(self) -> int:
        """Get total count of instructions"""
        return self.db.query(Instruction).count()
    
    def search_instructions(self, query: str, page: int = 0, limit: int = 10) -> List[Instruction]:
        """Search instructions by title or description"""
        offset = page * limit
        search_filter = or_(
            Instruction.title.ilike(f"%{query}%"),
            Instruction.description.ilike(f"%{query}%")
        )
        return self.db.query(Instruction).filter(search_filter).offset(offset).limit(limit).all()
    
    def get_instructions_by_type(self, instruction_type: InstructionType, 
                                page: int = 0, limit: int = 10) -> List[Instruction]:
        """Get instructions by type"""
        offset = page * limit
        return self.db.query(Instruction).filter(
            Instruction.type == instruction_type
        ).offset(offset).limit(limit).all()
