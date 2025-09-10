from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Recipe, Model, InstructionType
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class RecipesService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_recipes(self, page: int = 0, limit: int = 10) -> List[Recipe]:
        """Get paginated list of recipes"""
        offset = page * limit
        return self.db.query(Recipe).order_by(Recipe.created_at.desc(), Recipe.id.desc()).offset(offset).limit(limit).all()
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get recipe by ID"""
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    def get_recipe_by_title(self, title: str) -> Optional[Recipe]:
        """Get recipe by title"""
        return self.db.query(Recipe).filter(Recipe.title == title).first()
    
    def create_recipe(self, title: str, recipe_type: InstructionType, 
                      description: str = None, tg_file_id: str = None, 
                      url: str = None) -> Recipe:
        """Create new recipe"""
        recipe = Recipe(
            title=title,
            type=recipe_type,
            description=description,
            tg_file_id=tg_file_id,
            url=url
        )
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        logger.info(f"Created recipe: {recipe.title} (ID: {recipe.id})")
        return recipe
    
    def update_recipe(self, recipe_id: int, **kwargs) -> Optional[Recipe]:
        """Update recipe"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return None
        
        for key, value in kwargs.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        
        self.db.commit()
        self.db.refresh(recipe)
        logger.info(f"Updated recipe: {recipe.title} (ID: {recipe.id})")
        return recipe
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete recipe"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False
        
        self.db.delete(recipe)
        self.db.commit()
        logger.info(f"Deleted recipe: {recipe.title} (ID: {recipe.id})")
        return True
    
    def get_recipe_models(self, recipe_id: int) -> List[Model]:
        """Get all models for a recipe"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return []
        return recipe.models
    
    def bind_recipe_to_models(self, recipe_id: int, model_ids: List[int]) -> bool:
        """Bind recipe to multiple models"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False
        
        models = self.db.query(Model).filter(Model.id.in_(model_ids)).all()
        if not models:
            return False
        
        # Add models that are not already bound
        new_models = [model for model in models if model not in recipe.models]
        if new_models:
            recipe.models.extend(new_models)
            self.db.commit()
            logger.info(f"Bound recipe {recipe.title} to {len(new_models)} models")
            return True
        return False
    
    def unbind_recipe_from_models(self, recipe_id: int, model_ids: List[int]) -> bool:
        """Unbind recipe from multiple models"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False
        
        models_to_remove = [model for model in recipe.models if model.id in model_ids]
        if models_to_remove:
            for model in models_to_remove:
                recipe.models.remove(model)
            self.db.commit()
            logger.info(f"Unbound recipe {recipe.title} from {len(models_to_remove)} models")
            return True
        return False
    
    def get_recipes_count(self) -> int:
        """Get total count of recipes"""
        return self.db.query(Recipe).count()
    
    def search_recipes(self, query: str, page: int = 0, limit: int = 10) -> List[Recipe]:
        """Search recipes by title or description"""
        offset = page * limit
        search_filter = or_(
            Recipe.title.ilike(f"%{query}%"),
            Recipe.description.ilike(f"%{query}%")
        )
        return self.db.query(Recipe).filter(search_filter).order_by(Recipe.created_at.desc(), Recipe.id.desc()).offset(offset).limit(limit).all()
    
    def get_recipes_by_type(self, recipe_type: InstructionType, 
                            page: int = 0, limit: int = 10) -> List[Recipe]:
        """Get recipes by type"""
        offset = page * limit
        return self.db.query(Recipe).filter(
            Recipe.type == recipe_type
        ).order_by(Recipe.created_at.desc(), Recipe.id.desc()).offset(offset).limit(limit).all()
    
    def get_recipes_by_model_id(self, model_id: int) -> List[Recipe]:
        """Get all recipes for a specific model"""
        model = self.db.query(Model).filter(Model.id == model_id).first()
        if not model:
            return []
        return sorted(model.recipes, key=lambda x: (x.created_at, x.id), reverse=True)
