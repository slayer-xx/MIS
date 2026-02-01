"""
Deal Service
Business logic layer for Deal operations.
"""
from typing import List, Optional, Dict
from datetime import datetime
from modules.deals.repositories.deal_repository import DealRepository
from core.models import Deal


class DealService:
    """
    Service layer for Deal-related business operations.
    UI should interact with this service, not directly with repositories.
    """

    def __init__(self, deal_repo):
        self.deal_repo = deal_repo

    def create_deal(
        self,
        title: str,
        deal_type: str,
        status: str,
        client_name: str,
        property_value: Optional[float] = None,
        expected_commission: Optional[float] = None
    ) -> Deal:
        """
        Create a new deal with validation.
        
        Args:
            title: Deal title
            deal_type: Type of deal (Builder/Resale/Rental)
            status: Current status
            client_name: Name of the client
            property_value: Property value (optional)
            expected_commission: Expected commission amount (optional)
            
        Returns:
            Created Deal object
            
        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not title or not title.strip():
            raise ValueError("Deal title is required")
        
        if not client_name or not client_name.strip():
            raise ValueError("Client name is required")
        
        if property_value is not None and property_value < 0:
            raise ValueError("Property value cannot be negative")
        
        if expected_commission is not None and expected_commission < 0:
            raise ValueError("Expected commission cannot be negative")

        # Create deal
        return self.deal_repo.create(
            title=title.strip(),
            deal_type=deal_type,
            status=status,
            client_name=client_name.strip(),
            property_value=property_value,
            expected_commission=expected_commission
        )

    def update_deal(
        self,
        deal_id: int,
        **kwargs
    ) -> Optional[Deal]:
        """
        Update an existing deal.
        
        Args:
            deal_id: ID of the deal to update
            **kwargs: Fields to update
            
        Returns:
            Updated Deal object or None if not found
        """
        # Validation for specific fields
        if 'property_value' in kwargs and kwargs['property_value'] is not None:
            if kwargs['property_value'] < 0:
                raise ValueError("Property value cannot be negative")
        
        if 'expected_commission' in kwargs and kwargs['expected_commission'] is not None:
            if kwargs['expected_commission'] < 0:
                raise ValueError("Expected commission cannot be negative")

        return self.deal_repo.update(deal_id, **kwargs)

    def delete_deal(self, deal_id: int) -> bool:
        """
        Delete a deal.
        
        Args:
            deal_id: ID of the deal to delete
            
        Returns:
            True if deleted, False if not found
        """
        return self.deal_repo.delete(deal_id)

    def get_deal_by_id(self, deal_id: int) -> Optional[Deal]:
        """Get a deal by its ID."""
        return self.deal_repo.get_by_id(deal_id)

    def get_all_deals(self, sort_by: str = "created_at", ascending: bool = False) -> List[Deal]:
        """
        Get all deals, optionally sorted.
        
        Args:
            sort_by: Field to sort by
            ascending: Sort order
            
        Returns:
            List of Deal objects
        """
        return self.deal_repo.get_all_sorted(sort_by, ascending)

    def get_deals_by_status(self, status: str) -> List[Deal]:
        """Get all deals with a specific status."""
        return self.deal_repo.get_by_status(status)

    def get_deals_by_type(self, deal_type: str) -> List[Deal]:
        """Get all deals of a specific type."""
        return self.deal_repo.get_by_deal_type(deal_type)

    def search_deals(self, search_term: str) -> List[Deal]:
        """
        Search deals by title or client name.
        
        Args:
            search_term: Search term
            
        Returns:
            List of matching Deal objects
        """
        if not search_term or not search_term.strip():
            return self.get_all_deals()
        
        # Search in both title and client name
        title_results = self.deal_repo.search_by_title(search_term)
        client_results = self.deal_repo.search_by_client(search_term)
        
        # Combine and deduplicate results
        all_results = {deal.id: deal for deal in title_results + client_results}
        return list(all_results.values())

    def get_dashboard_stats(self) -> Dict:
        """
        Get statistics for dashboard.
        
        Returns:
            Dictionary with various statistics
        """
        all_deals = self.deal_repo.get_all()
        
        return {
            'total_deals': len(all_deals),
            'active_deals': len([d for d in all_deals if d.status not in ['Closed', 'Lost']]),
            'closed_deals': len([d for d in all_deals if d.status == 'Closed']),
            'total_property_value': self.deal_repo.get_total_property_value(),
            'total_expected_commission': self.deal_repo.get_total_expected_commission(),
        }

    def format_currency(self, amount: Optional[float]) -> str:
        """Format amount as currency string."""
        if amount is None:
            return "₹0"
        return f"₹{amount:,.2f}"
    
    def get_active_deals(self):
        """Get all active deals (not closed or cancelled)."""
        return [d for d in self.deal_repo.get_all() if d.status not in ["Closed", "Lost", "Cancelled"]]

    def get_deals_this_month(self):
        """Get deals created this month."""
        now = datetime.now()
        return [
            d for d in self.deal_repo.get_all()
            if d.created_at and d.created_at.month == now.month and d.created_at.year == now.year
        ]

    def get_by_id(self, deal_id):
        """Get deal by ID."""
        return self.deal_repo.get_by_id(deal_id)

    def update(self, deal_id, data):
        """Update deal."""
        return self.repository.update(deal_id, **data)

