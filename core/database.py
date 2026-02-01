"""
Database Management
Handles database connection, initialization, and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import config
from core.models import Base


class DatabaseManager:
    """
    Singleton database manager for the application.
    Handles connection lifecycle and session management.
    """
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Initialize database connection and create tables."""
        if self._engine is None:
            self._engine = create_engine(
                config.DATABASE_URL,
                echo=False,  # Set to True for SQL query debugging
                connect_args={"check_same_thread": False}  # For SQLite
            )
            self._session_factory = scoped_session(
                sessionmaker(bind=self._engine, expire_on_commit=False)
            )
            # Create all tables
            Base.metadata.create_all(self._engine)
            print(f"Database initialized at: {config.DATABASE_PATH}")

    def get_session(self):
        """Get a new database session."""
        if self._session_factory is None:
            self.initialize()
        return self._session_factory()

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope for database operations.
        Usage:
            with db_manager.session_scope() as session:
                session.add(obj)
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def close(self):
        """Close database connections."""
        if self._session_factory:
            self._session_factory.remove()
        if self._engine:
            self._engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()
