from sqlalchemy.orm import Session
from models import Instruction, InstructionType, Model
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class FilesService:
    def __init__(self, db: Session):
        self.db = db
    
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
    
    def get_instruction_by_id(self, instruction_id: int) -> Optional[Instruction]:
        """Get instruction by ID"""
        return self.db.query(Instruction).filter(Instruction.id == instruction_id).first()
    
    def get_instructions(self, page: int = 0, limit: int = 10) -> List[Instruction]:
        """Get paginated list of instructions"""
        offset = page * limit
        return self.db.query(Instruction).offset(offset).limit(limit).all()
    
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
    
    def get_instructions_by_type(self, instruction_type: InstructionType) -> List[Instruction]:
        """Get instructions by type"""
        return self.db.query(Instruction).filter(Instruction.type == instruction_type).all()
    
    def get_instructions_for_model(self, model_id: int) -> List[Instruction]:
        """Get all instructions for a specific model"""
        model = self.db.query(Model).filter(Model.id == model_id).first()
        if not model:
            return []
        return model.instructions
    
    def bind_instruction_to_models(self, instruction_id: int, model_ids: List[int]) -> bool:
        """Bind instruction to multiple models"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return False
        
        models = self.db.query(Model).filter(Model.id.in_(model_ids)).all()
        if not models:
            return False
        
        for model in models:
            if instruction not in model.instructions:
                model.instructions.append(instruction)
        
        self.db.commit()
        logger.info(f"Bound instruction {instruction.title} to {len(models)} models")
        return True
    
    def unbind_instruction_from_model(self, instruction_id: int, model_id: int) -> bool:
        """Unbind instruction from model"""
        instruction = self.get_instruction_by_id(instruction_id)
        model = self.db.query(Model).filter(Model.id == model_id).first()
        
        if not instruction or not model:
            return False
        
        if instruction in model.instructions:
            model.instructions.remove(instruction)
            self.db.commit()
            logger.info(f"Unbound instruction {instruction.title} from model {model.name}")
            return True
        return False
    
    def get_instructions_count(self) -> int:
        """Get total count of instructions"""
        return self.db.query(Instruction).count()
    
    def get_instruction_models(self, instruction_id: int) -> List[Model]:
        """Get all models that have this instruction"""
        instruction = self.get_instruction_by_id(instruction_id)
        if not instruction:
            return []
        return instruction.models
