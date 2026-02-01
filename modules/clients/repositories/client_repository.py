"""
Clients Module - Repository Layer
"""
from typing import List
from core.base_repository import BaseRepository
from core.models import Client, ClientNote
from core.database import db_manager



class ClientRepository(BaseRepository):
    """Repository for Client model."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(Client, self.session)
    
    def get_by_phone(self, phone: str) -> Client:
        return self.session.query(Client).filter(Client.phone == phone).first()
    
    def get_active_clients(self) -> List[Client]:
        return self.session.query(Client).filter(Client.status == "active").all()
    
    def search(self, query: str) -> List[Client]:
        search_term = f"%{query}%"
        return self.session.query(Client).filter(
            (Client.name.ilike(search_term)) |
            (Client.phone.ilike(search_term)) |
            (Client.email.ilike(search_term))
        ).all()


class ClientNoteRepository(BaseRepository):
    """Repository for Client Notes."""
    
    def __init__(self):
        super().__init__(ClientNote, self.session)
    
    def get_by_client_id(self, client_id: int) -> List[ClientNote]:
        return self.session.query(ClientNote).filter(
            ClientNote.client_id == client_id
        ).order_by(ClientNote.created_at.desc()).all()
