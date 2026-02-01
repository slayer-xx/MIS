"""
Commission Module - Service Layer
"""
from typing import List, Optional, Dict, Any
from core.base_service import BaseService
from modules.commission.repositories.commission_repository import (
    CommissionRepository,
    CommissionPaymentRepository
)


class CommissionService(BaseService):
    """Service for managing commissions."""
    
    def __init__(self, repository: CommissionRepository):
        super().__init__(repository)
    
    def create_commission_structure(self, data: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
        required_fields = ['deal_id', 'party_type', 'party_name', 'commission_amount']
        is_valid, error = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error, None
        
        try:
            commission = self.repository.create(**data)
            return True, "Commission structure created", commission
        except Exception as e:
            return False, str(e), None
    
    def get_deal_commissions(self, deal_id: int) -> List[Any]:
        return self.repository.get_by_deal_id(deal_id)
    
    def calculate_total_expected(self, deal_id: int) -> float:
        commissions = self.repository.get_by_deal_id(deal_id)
        return sum(c.commission_amount for c in commissions)

    # ---------- Methods required by UI ----------

    def get_all(self):
        return self.repository.get_all()

    def get_pending(self):
        return self.repository.get_pending_commissions()

    def get_received(self):
        return self.repository.get_received_commissions()

    def get_summary(self):
        commissions = self.repository.get_all()
        total_expected = sum(c.commission_amount for c in commissions)
        total_received = 0  # until payment aggregation added
        outstanding = total_expected - total_received


        
        return {
            "total_expected": total_expected,
            "total_received": total_received,
            "outstanding": outstanding
        }
    def create(self, **data):
        success, msg, obj = self.create_commission_structure(data)
        if not success:
            raise Exception(msg)
        return obj
    
    def record_payment(self, **data):
        payment_repo = CommissionPaymentRepository()
        payment = payment_repo.create(**data)

        commission_id = data['commission_structure_id']
        commission = self.repository.get_by_id(commission_id)

        payments = payment_repo.get_by_commission_id(commission_id)
        total_received = sum(p.amount for p in payments)

        if total_received >= commission.commission_amount:
            status = "received"
        elif total_received > 0:
            status = "partial"
        else:
            status = "pending"

        # Fix: Use proper update method with dict
        self.repository.update(commission_id, {'status': status})

        return payment

    def get_by_id(self, id):
        """Get commission by ID."""
        return self.repository.get_by_id(id)

    def get_by_deal_id(self, deal_id):
        """Get commission structures for a deal."""
        try:
            return self.repository.get_by_deal_id(deal_id)
        except:
            return []

    def update(self, commission_id, data):
        """Update commission."""
        return self.repository.update(commission_id, **data)





