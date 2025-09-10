from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

Base = declarative_base()

class InstructionType(enum.Enum):
    PDF = "pdf"
    VIDEO = "video"
    LINK = "link"

class TicketStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class MessageRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class FileType(enum.Enum):
    PHOTO = "photo"
    DOC = "doc"
    VOICE = "voice"
    VIDEO = "video"

# Many-to-many relationship between models and instructions
model_instruction = Table(
    'model_instruction',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('model_id', Integer, ForeignKey('models.id')),
    Column('instruction_id', Integer, ForeignKey('instructions.id'))
)

# Many-to-many relationship between models and recipes
model_recipe = Table(
    'model_recipe',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('model_id', Integer, ForeignKey('models.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)

class Model(Base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    tags = Column(String(500))  # CSV format
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    instructions = relationship("Instruction", secondary=model_instruction, back_populates="models")
    recipes = relationship("Recipe", secondary=model_recipe, back_populates="models")
    
    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}')>"

class Instruction(Base):
    __tablename__ = 'instructions'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(Enum(InstructionType), nullable=False)
    description = Column(Text)
    tg_file_id = Column(String(255))  # Telegram file ID
    url = Column(String(500))  # External URL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    models = relationship("Model", secondary=model_instruction, back_populates="instructions")
    
    def __repr__(self):
        return f"<Instruction(id={self.id}, title='{self.title}', type='{self.type.value}')>"

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(Enum(InstructionType), nullable=False)  # Reuse InstructionType enum
    description = Column(Text)
    tg_file_id = Column(String(255))  # Telegram file ID
    url = Column(String(500))  # External URL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    models = relationship("Model", secondary=model_recipe, back_populates="recipes")
    
    def __repr__(self):
        return f"<Recipe(id={self.id}, title='{self.title}', type='{self.type.value}')>"

class Ticket(Base):
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(255))
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    subject = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, user_id={self.user_id}, status='{self.status.value}')>"

class TicketMessage(Base):
    __tablename__ = 'ticket_messages'
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    from_role = Column(Enum(MessageRole), nullable=False)
    text = Column(Text)
    tg_file_id = Column(String(255))
    file_type = Column(Enum(FileType))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("Ticket", back_populates="messages")
    
    def __repr__(self):
        return f"<TicketMessage(id={self.id}, ticket_id={self.ticket_id}, from_role='{self.from_role.value}')>"

# Database setup
def get_engine():
    from config import DB_URL
    return create_engine(DB_URL, echo=False)

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def create_tables():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
