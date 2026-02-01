"""
Commission Module - Repository Layer
"""
from typing import List, Optional
from datetime import date
from sqlalchemy import func
from core.base_repository import BaseRepository
from core.models import CommissionStructure, CommissionPayment, BuilderPayout
from core.database import db_manager
from sqlalchemy import or_




class CommissionRepository(BaseRepository):
    """Repository for Commission-related models."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(CommissionStructure, self.session)
    
    def get_by_deal_id(self, deal_id: int) -> List[CommissionStructure]:
        return self.session.query(CommissionStructure).filter(
            CommissionStructure.deal_id == deal_id
        ).all()
    
    def get_pending_commissions(self):
        return self.session.query(CommissionStructure).filter(
            or_(
                CommissionStructure.status == "pending",
                CommissionStructure.status == "partial"
            )
        ).all()

    
    def get_monthly_received(self, month: int, year: int) -> float:
        """Get total commission received in a specific month."""
        payments = self.session.query(func.sum(CommissionPayment.amount)).filter(
            func.extract('month', CommissionPayment.payment_date) == month,
            func.extract('year', CommissionPayment.payment_date) == year
        ).scalar()
        return payments or 0.0
    
    def get_all(self):
        return self.session.query(CommissionStructure).all()
    
    def get_received_commissions(self):
        return self.session.query(CommissionStructure).filter(
            CommissionStructure.status == "received"
        ).all()



class CommissionPaymentRepository(BaseRepository):
    """Repository for Commission Payments."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(CommissionPayment, self.session)
    
    def get_by_commission_id(self, commission_id: int) -> List[CommissionPayment]:
        return self.session.query(CommissionPayment).filter(
            CommissionPayment.commission_structure_id == commission_id
        ).all()


class BuilderPayoutRepository(BaseRepository):
    """Repository for Builder Payouts."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(BuilderPayout, self.session)
    
    def get_by_deal_id(self, deal_id: int) -> List[BuilderPayout]:
        return self.session.query(BuilderPayout).filter(
            BuilderPayout.deal_id == deal_id
        ).all()

