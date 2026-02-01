"""
Clients Module - Service Layer
"""
from typing import Dict, Any, Optional
from core.base_service import BaseService
from modules.clients.repositories.client_repository import ClientRepository


class ClientService(BaseService):
    """Service for managing clients."""
    
    def __init__(self, repository: ClientRepository):
        super().__init__(repository)
    
    def create_client(self, data: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
        required_fields = ['name', 'phone', 'client_type']
        is_valid, error = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error, None
        
        # Validate phone
        is_valid, error = self.validate_phone_number(data['phone'])
        if not is_valid:
            return False, error, None
        
        # Validate email if provided
        if data.get('email'):
            is_valid, error = self.validate_email(data['email'])
            if not is_valid:
                return False, error, None
        
        try:
            client = self.repository.create(**data)
            return True, "Client created successfully", client
        except Exception as e:
            return False, str(e), None
    
    def search_clients(self, query: str):
        return self.repository.search(query)
    
    def create(self, **data):
        success, msg, client = self.create_client(data)
        if not success:
            raise Exception(msg)
        return client
   
    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        """Get client by ID."""
        return self.repository.get_by_id(id)

    def update(self, client_id, data):
        """Update client."""
        return self.repository.update(client_id, **data)



