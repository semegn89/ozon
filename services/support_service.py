from sqlalchemy.orm import Session
from models import Ticket, TicketMessage, TicketStatus, MessageRole, FileType
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SupportService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_ticket(self, user_id: int, username: str = None, subject: str = None) -> Ticket:
        """Create new support ticket"""
        ticket = Ticket(
            user_id=user_id,
            username=username,
            subject=subject,
            status=TicketStatus.OPEN
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        logger.info(f"Created ticket: {ticket.id} for user {user_id}")
        return ticket
    
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """Get ticket by ID"""
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    def get_user_tickets(self, user_id: int, limit: int = 10) -> List[Ticket]:
        """Get user's tickets"""
        return self.db.query(Ticket).filter(
            Ticket.user_id == user_id
        ).order_by(Ticket.created_at.desc()).limit(limit).all()
    
    def get_open_tickets(self, limit: int = 20) -> List[Ticket]:
        """Get open tickets for admin"""
        return self.db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
        ).order_by(Ticket.created_at.desc()).limit(limit).all()
    
    def update_ticket_status(self, ticket_id: int, status: TicketStatus) -> Optional[Ticket]:
        """Update ticket status"""
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        
        ticket.status = status
        # Set closed_at when closing ticket
        if status == TicketStatus.CLOSED:
            ticket.closed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(ticket)
        logger.info(f"Updated ticket {ticket_id} status to {status.value}")
        return ticket
    
    def add_message_to_ticket(self, ticket_id: int, from_role: MessageRole, 
                             text: str = None, tg_file_id: str = None, 
                             file_type: FileType = None) -> Optional[TicketMessage]:
        """Add message to ticket"""
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        
        message = TicketMessage(
            ticket_id=ticket_id,
            from_role=from_role,
            text=text,
            tg_file_id=tg_file_id,
            file_type=file_type
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        # Update ticket timestamp
        ticket.updated_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"Added message to ticket {ticket_id} from {from_role.value}")
        return message
    
    def get_ticket_messages(self, ticket_id: int) -> List[TicketMessage]:
        """Get all messages for a ticket"""
        return self.db.query(TicketMessage).filter(
            TicketMessage.ticket_id == ticket_id
        ).order_by(TicketMessage.created_at.asc()).all()
    
    def get_ticket_stats(self) -> Dict[str, int]:
        """Get ticket statistics"""
        stats = {}
        for status in TicketStatus:
            count = self.db.query(Ticket).filter(Ticket.status == status).count()
            stats[status.value] = count
        return stats
    
    def close_old_tickets(self, days: int = 90) -> int:
        """Close tickets older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_tickets = self.db.query(Ticket).filter(
            Ticket.status == TicketStatus.CLOSED,
            Ticket.updated_at < cutoff_date
        ).all()
        
        count = len(old_tickets)
        for ticket in old_tickets:
            self.db.delete(ticket)
        
        self.db.commit()
        logger.info(f"Cleaned up {count} old tickets")
        return count
    
    def get_tickets_count(self) -> int:
        """Get total count of tickets"""
        return self.db.query(Ticket).count()
    
    def get_open_tickets_count(self) -> int:
        """Get count of open tickets"""
        return self.db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
        ).count()
    
    def search_tickets(self, query: str, limit: int = 20) -> List[Ticket]:
        """Search tickets by subject or username"""
        return self.db.query(Ticket).filter(
            Ticket.subject.ilike(f"%{query}%") | 
            Ticket.username.ilike(f"%{query}%")
        ).order_by(Ticket.created_at.desc()).limit(limit).all()
