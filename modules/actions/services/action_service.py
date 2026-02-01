"""
Actions Module - Service Layer
Business logic for follow-up actions and reminders.

Module: Actions (independent)
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from core.base_service import BaseService
from modules.actions.repositories.action_repository import ActionRepository


class ActionService(BaseService):
    """
    Service for managing follow-up actions.
    """
    
    def __init__(self, repository: ActionRepository):
        super().__init__(repository)
    
    def create_action(self, data: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
        """
        Create a new action.
        
        Args:
            data: Action data dictionary
            
        Returns:
            Tuple of (success, message, action_object)
        """
        # Validate required fields
        required_fields = ['title', 'action_date', 'action_type']
        is_valid, error = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error, None
        
        # Sanitize inputs
        data['title'] = self.sanitize_string(data['title'])
        data['description'] = self.sanitize_string(data.get('description', ''))
        data['client_name'] = self.sanitize_string(data.get('client_name', ''))
        
        # Set defaults
        if 'priority' not in data or not data['priority']:
            data['priority'] = 'medium'
        
        if 'completed' not in data:
            data['completed'] = False
        
        # Create action
        try:
            action = self.repository.create(**data)   
            return True, "Action created successfully", action
        except Exception as e:
            return False, f"Error creating action: {str(e)}", None
    
    def update_action(self, action_id: int, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Update an existing action.
        
        Args:
            action_id: ID of the action
            data: Updated action data
            
        Returns:
            Tuple of (success, message)
        """
        # Sanitize inputs
        if 'title' in data:
            data['title'] = self.sanitize_string(data['title'])
        if 'description' in data:
            data['description'] = self.sanitize_string(data['description'])
        if 'client_name' in data:
            data['client_name'] = self.sanitize_string(data['client_name'])
        
        try:
            success = self.repository.update(action_id, **data)
            if success:
                return True, "Action updated successfully"
            return False, "Action not found"
        except Exception as e:
            return False, f"Error updating action: {str(e)}"
    
    def get_today_summary(self) -> Dict[str, Any]:
        """
        Get summary of today's actions.
        
        Returns:
            Dictionary with today's action summary
        """
        today_actions = self.repository.get_today_actions()
        
        completed = [a for a in today_actions if a.completed]
        pending = [a for a in today_actions if not a.completed]
        high_priority = [a for a in pending if a.priority == 'high']
        
        return {
            'total': len(today_actions),
            'completed': len(completed),
            'pending': len(pending),
            'high_priority': len(high_priority),
            'actions': today_actions
        }
    
    def get_overdue_summary(self) -> Dict[str, Any]:
        """
        Get summary of overdue actions.
        
        Returns:
            Dictionary with overdue action summary
        """
        overdue_actions = self.repository.get_overdue_actions()
        
        critical = []  # More than 7 days overdue
        today = date.today()
        
        for action in overdue_actions:
            days_overdue = (today - action.action_date).days
            if days_overdue > 7:
                critical.append(action)
        
        return {
            'total': len(overdue_actions),
            'critical': len(critical),
            'actions': overdue_actions
        }
    
    def complete_action(self, action_id: int) -> tuple[bool, str]:
        """
        Mark an action as completed.
        
        Args:
            action_id: ID of the action
            
        Returns:
            Tuple of (success, message)
        """
        try:
            success = self.repository.mark_as_completed(action_id)
            if success:
                return True, "Action marked as completed"
            return False, "Action not found"
        except Exception as e:
            return False, f"Error completing action: {str(e)}"
    
    def reopen_action(self, action_id: int) -> tuple[bool, str]:
        """
        Reopen a completed action.
        
        Args:
            action_id: ID of the action
            
        Returns:
            Tuple of (success, message)
        """
        try:
            success = self.repository.mark_as_pending(action_id)
            if success:
                return True, "Action reopened"
            return False, "Action not found"
        except Exception as e:
            return False, f"Error reopening action: {str(e)}"
    
    def reschedule(self, action_id: int, new_date: date, new_time: Optional[str] = None) -> tuple[bool, str]:
        """
        Reschedule an action.
        
        Args:
            action_id: ID of the action
            new_date: New date
            new_time: New time (optional)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            success = self.repository.reschedule_action(action_id, new_date, new_time)
            if success:
                return True, "Action rescheduled successfully"
            return False, "Action not found"
        except Exception as e:
            return False, f"Error rescheduling action: {str(e)}"
    
    def get_upcoming_week(self) -> List[Any]:
        """
        Get actions for the next 7 days.
        
        Returns:
            List of upcoming actions
        """
        return self.repository.get_upcoming_actions(7)
    
    def get_actions_for_deal(self, deal_id: int) -> List[Any]:
        """
        Get all actions related to a specific deal.
        
        Args:
            deal_id: ID of the deal
            
        Returns:
            List of actions
        """
        return self.repository.get_by_deal_id(deal_id)
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get action statistics for dashboard.
        
        Returns:
            Dictionary with action stats
        """
        today_count = self.repository.count_today_actions()
        overdue_count = self.repository.count_overdue_actions()
        upcoming = self.repository.get_upcoming_actions(7)
        
        return {
            'today_count': today_count,
            'overdue_count': overdue_count,
            'upcoming_week_count': len(upcoming),
            'total_pending': len(self.repository.get_pending_actions())
        }

    # ---------- Methods expected by UI ----------

    def create(self, **data):
        success, msg, action = self.create_action(data)
        if not success:
            raise Exception(msg)
        return action

    def update(self, action_id, data):
        """Update action - wrapper for UI."""
        # If data is a dict, use it directly; otherwise convert
        if not isinstance(data, dict):
            data = vars(data) if hasattr(data, '__dict__') else {}
        success, msg = self.update_action(action_id, data)
        if not success:
            raise Exception(msg)
        return True

    def get_all(self):
        return self.repository.get_all()

    def get_today_actions(self):
        return self.repository.get_today_actions()

    def get_upcoming_week_actions(self):
        return self.repository.get_upcoming_actions(7)

    def get_overdue_actions(self):
        return self.repository.get_overdue_actions()

    def mark_complete(self, action_id):
        success, msg = self.complete_action(action_id)
        if not success:
            raise Exception(msg)

    def mark_pending(self, action_id):
        success, msg = self.reopen_action(action_id)
        if not success:
            raise Exception(msg)

    def get_by_id(self, id):
        """Get action by ID."""
        return self.repository.get_by_id(id)


