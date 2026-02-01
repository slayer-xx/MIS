"""
Actions Module - Repository Layer
Data access for follow-up actions and reminders.

Module: Actions (independent)
"""
from typing import List, Optional
from datetime import date, datetime, timedelta
from core.base_repository import BaseRepository
from core.models import Action
from core.database import db_manager



class ActionRepository(BaseRepository):
    """
    Repository for Action model.
    Handles all database operations for follow-up actions.
    """
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(Action)
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Action]:
        """
        Get actions within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of actions
        """
        return self.session.query(Action).filter(
            Action.action_date >= start_date,
            Action.action_date <= end_date
        ).order_by(Action.action_date, Action.action_time).all()
    
    def get_today_actions(self):
            today = date.today()
            return self.session.query(Action).filter(
                Action.action_date == today,
                Action.completed == False
            ).all()

    def get_overdue_actions(self):
            today = date.today()
            return self.session.query(Action).filter(
                Action.action_date < today,
                Action.completed == False
            ).all()

    
    def get_upcoming_actions(self, days: int = 7) -> List[Action]:
        """
        Get actions scheduled for the next N days.
        
        Args:
            days: Number of days ahead to look
            
        Returns:
            List of upcoming actions
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        return self.session.query(Action).filter(
            Action.action_date >= today,
            Action.action_date <= end_date,
            Action.completed == False
        ).order_by(Action.action_date, Action.action_time).all()
    
    def get_by_deal_id(self, deal_id: int) -> List[Action]:
        """
        Get all actions linked to a specific deal.
        
        Args:
            deal_id: ID of the deal
            
        Returns:
            List of actions for the deal
        """
        return self.session.query(Action).filter(
            Action.deal_id == deal_id
        ).order_by(Action.action_date.desc()).all()
    
    def get_pending_actions(self) -> List[Action]:
        """
        Get all pending (not completed) actions.
        
        Returns:
            List of pending actions
        """
        return self.session.query(Action).filter(
            Action.completed == False
        ).order_by(Action.action_date, Action.priority).all()
    
    def get_completed_actions(self, days: int = 30) -> List[Action]:
        """
        Get recently completed actions.
        
        Args:
            days: Number of days back to look
            
        Returns:
            List of completed actions
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.session.query(Action).filter(
            Action.completed == True,
            Action.completed_at >= cutoff_date
        ).order_by(Action.completed_at.desc()).all()
    
    def mark_as_completed(self, action_id: int) -> bool:
        """
        Mark an action as completed.
        
        Args:
            action_id: ID of the action
            
        Returns:
            True if successful, False otherwise
        """
        action = self.session.get(Action, action_id)
        if action:
            action.completed = True
            action.completed_at = datetime.now()
            self.session.commit()
            return True
        return False
    
    def mark_as_pending(self, action_id: int) -> bool:
        """
        Mark an action as pending (undo completion).
        
        Args:
            action_id: ID of the action
            
        Returns:
            True if successful, False otherwise
        """
        action = self.session.get(Action, action_id)
        if action:
            action.completed = False
            action.completed_at = None
            self.session.commit()
            return True
        return False
    
    def get_by_action_type(self, action_type: str) -> List[Action]:
        """
        Get actions by type.
        
        Args:
            action_type: Type of action
            
        Returns:
            List of actions of that type
        """
        return self.session.query(Action).filter(
            Action.action_type == action_type
        ).order_by(Action.action_date.desc()).all()
    
    def get_by_priority(self, priority: str) -> List[Action]:
        """
        Get actions by priority.
        
        Args:
            priority: Priority level (high/medium/low)
            
        Returns:
            List of actions with that priority
        """
        return self.session.query(Action).filter(
            Action.priority == priority,
            Action.completed == False
        ).order_by(Action.action_date).all()
    
    def count_today_actions(self) -> int:
        """
        Count today's actions.
        
        Returns:
            Number of actions scheduled for today
        """
        today = date.today()
        return self.session.query(Action).filter(
            Action.action_date == today
        ).count()
    
    def count_overdue_actions(self) -> int:
        """
        Count overdue actions.
        
        Returns:
            Number of overdue actions
        """
        today = date.today()
        return self.session.query(Action).filter(
            Action.action_date < today,
            Action.completed == False
        ).count()
    
    def reschedule_action(self, action_id: int, new_date: date, new_time: Optional[str] = None) -> bool:
        """
        Reschedule an action to a new date/time.
        
        Args:
            action_id: ID of the action
            new_date: New date for the action
            new_time: New time (optional)
            
        Returns:
            True if successful, False otherwise
        """
        action = self.session.get(Action, action_id)
        if action:
            action.action_date = new_date
            if new_time:
                action.action_time = new_time
            action.updated_at = datetime.now()
            self.session.commit()
            return True
        return False
    
    def search(self, query: str) -> List[Action]:
        """
        Search actions by title, description, or client name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching actions
        """
        search_term = f"%{query}%"
        return self.session.query(Action).filter(
            (Action.title.ilike(search_term)) |
            (Action.description.ilike(search_term)) |
            (Action.client_name.ilike(search_term))
        ).order_by(Action.action_date.desc()).all()
