"""
Partners Module - Service Layer
"""
from typing import Dict, Any, Optional
from core.base_service import BaseService
from modules.partners.repositories.partner_repository import PartnerRepository


class PartnerService(BaseService):
    """Service for managing partners."""
    
    def __init__(self, repository: PartnerRepository):
        super().__init__(repository)
    
    def create_partner(self, data: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
        required_fields = ['name', 'partner_type', 'phone']
        is_valid, error = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error, None
        
        try:
            partner = self.repository.create(**data)
            return True, "Partner created successfully", partner
        except Exception as e:
            return False, str(e), None
    
    def create(self, **data):
        success, msg, partner = self.create_partner(data)
        if not success:
            raise Exception(msg)
        return partner
    
    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        """Get partner by ID."""
        return self.repository.get_by_id(id)




    def update(self, partner_id, data):
        """Update partner."""
        return self.repository.update(partner_id, **data)
