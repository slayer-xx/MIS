"""
Deal Repository
Data access layer for Deal operations.
"""
from typing import List, Optional
from core.base_repository import BaseRepository
from core.models import Deal
from core.database import db_manager


class DealRepository(BaseRepository[Deal]):
    """
    Repository for managing Deal data operations.
    Inherits common CRUD from BaseRepository.
    """

    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(Deal)

    def get_by_status(self, status: str) -> List[Deal]:
        """Get all deals with a specific status."""
        with self.db_manager.session_scope() as session:
            return session.query(Deal).filter(Deal.status == status).all()

    def get_by_deal_type(self, deal_type: str) -> List[Deal]:
        """Get all deals of a specific type."""
        with self.db_manager.session_scope() as session:
            return session.query(Deal).filter(Deal.deal_type == deal_type).all()

    def search_by_title(self, search_term: str) -> List[Deal]:
        """Search deals by title (case-insensitive)."""
        with self.db_manager.session_scope() as session:
            return session.query(Deal).filter(
                Deal.title.ilike(f"%{search_term}%")
            ).all()

    def search_by_client(self, search_term: str) -> List[Deal]:
        """Search deals by client name (case-insensitive)."""
        with self.db_manager.session_scope() as session:
            return session.query(Deal).filter(
                Deal.client_name.ilike(f"%{search_term}%")
            ).all()

    def get_all_sorted(self, sort_by: str = "created_at", ascending: bool = False) -> List[Deal]:
        """
        Get all deals sorted by a specific field.
        
        Args:
            sort_by: Field name to sort by
            ascending: Sort order (True for ascending, False for descending)
        """
        with self.db_manager.session_scope() as session:
            query = session.query(Deal)
            
            if hasattr(Deal, sort_by):
                order_column = getattr(Deal, sort_by)
                if ascending:
                    query = query.order_by(order_column.asc())
                else:
                    query = query.order_by(order_column.desc())
            
            return query.all()

    def get_total_property_value(self) -> float:
        """Calculate total property value across all deals."""
        with self.db_manager.session_scope() as session:
            result = session.query(Deal).all()
            return sum(deal.property_value or 0 for deal in result)

    def get_total_expected_commission(self) -> float:
        """Calculate total expected commission across all deals."""
        with self.db_manager.session_scope() as session:
            result = session.query(Deal).all()
            return sum(deal.expected_commission or 0 for deal in result)
