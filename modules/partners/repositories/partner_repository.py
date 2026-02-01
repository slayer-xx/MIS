"""
Partners Module - Repository Layer
"""
from typing import List
from core.base_repository import BaseRepository
from core.models import Partner, PartnerNote
from core.database import db_manager



class PartnerRepository(BaseRepository):
    """Repository for Partner model."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(Partner, self.session)
        
    
    def get_by_type(self, partner_type: str) -> List[Partner]:
        return self.session.query(Partner).filter(
            Partner.partner_type == partner_type
        ).all()
    
    def get_active_partners(self) -> List[Partner]:
        return self.session.query(Partner).filter(
            Partner.status == "active"
        ).all()
    
    def search(self, query: str) -> List[Partner]:
        search_term = f"%{query}%"
        return self.session.query(Partner).filter(
            (Partner.name.ilike(search_term)) |
            (Partner.company_name.ilike(search_term)) |
            (Partner.phone.ilike(search_term))
        ).all()
