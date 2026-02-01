"""
Base Repository
Abstract base class for all repository implementations.
Supports both session-based and self-managed patterns.
"""
from typing import List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from core.database import db_manager

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository providing common CRUD operations.
    All specific repositories should inherit from this.
    
    Supports two initialization patterns:
    1. Self-managed sessions: BaseRepository(model_class)
    2. Injected session: BaseRepository(model_class, session)
    """

    def __init__(self, model_class: type, db_session: Session = None):
        self.model_class = model_class
        self.db_session = db_session  # If provided, use this session
        self.db_manager = db_manager

    def _get_session(self):
        """Get session - either injected or from db_manager"""
        if self.db_session:
            return self.db_session
        return self.db_manager.get_session()

    def get_by_id(self, id: int) -> Optional[T]:
        """Get a single record by ID."""
        if self.db_session:
            return self.db_session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
        else:
            with self.db_manager.session_scope() as session:
                return session.query(self.model_class).filter(
                    self.model_class.id == id
                ).first()

    def get_all(self) -> List[T]:
        """Get all records."""
        if self.db_session:
            return self.db_session.query(self.model_class).all()
        else:
            with self.db_manager.session_scope() as session:
                return session.query(self.model_class).all()

    def create(self, **kwargs) -> T:
        """Create a new record."""
        if self.db_session:
            instance = self.model_class(**kwargs)
            self.db_session.add(instance)
            self.db_session.commit()
            self.db_session.refresh(instance)
            return instance
        else:
            with self.db_manager.session_scope() as session:
                instance = self.model_class(**kwargs)
                session.add(instance)
                session.commit()
                session.refresh(instance)
                return instance

    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update an existing record."""
        if self.db_session:
            instance = self.db_session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
            if instance:
                for key, value in kwargs.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                self.db_session.commit()
                self.db_session.refresh(instance)
            return instance
        else:
            with self.db_manager.session_scope() as session:
                instance = session.query(self.model_class).filter(
                    self.model_class.id == id
                ).first()
                if instance:
                    for key, value in kwargs.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                    session.commit()
                    session.refresh(instance)
                return instance

    def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        if self.db_session:
            instance = self.db_session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
            if instance:
                self.db_session.delete(instance)
                self.db_session.commit()
                return True
            return False
        else:
            with self.db_manager.session_scope() as session:
                instance = session.query(self.model_class).filter(
                    self.model_class.id == id
                ).first()
                if instance:
                    session.delete(instance)
                    session.commit()
                    return True
                return False

    def count(self) -> int:
        """Count total records."""
        if self.db_session:
            return self.db_session.query(self.model_class).count()
        else:
            with self.db_manager.session_scope() as session:
                return session.query(self.model_class).count()
