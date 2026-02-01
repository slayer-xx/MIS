import os
"""
Database Initialization Script for Enhanced MIS
Creates all tables for all modules.
"""
from core.database import DatabaseManager
from core.models import Base


def initialize_database(database_path="data/real_estate_mis.db"):
    """
    Initialize the database with all tables.
    
    Args:
        database_path: Path to the SQLite database file
    """
    # Remove existing database if it exists
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"✓ Removed existing database")
        print()
    
    # Create data directory if needed
    import os
    os.makedirs("data", exist_ok=True)
    
    print("=" * 60)
    print("Database Initialization - Real Estate MIS v2.0")
    # Remove existing database if it exists
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"✓ Removed existing database")
        print()
    
    # Create data directory if needed
    import os
    os.makedirs("data", exist_ok=True)
    
    print("=" * 60)
    print()
    
    # Create database manager
    db_manager = DatabaseManager(database_path)
    
    print("Creating database tables...")
    print()
    
    # Create all tables from models
    engine = db_manager.engine
    Base.metadata.create_all(engine)
    
    print("✓ Deals module tables")
    print("  - deals")
    print("  - deal_notes")
    print()
    
    print("✓ Actions module tables")
    print("  - actions")
    print()
    
    print("✓ Commission module tables")
    print("  - commission_structures")
    print("  - commission_payments")
    print("  - builder_payouts")
    print()
    
    print("✓ Clients module tables")
    print("  - clients")
    print("  - client_notes")
    print()
    
    print("✓ Partners module tables")
    print("  - partners")
    print("  - partner_notes")
    print()
    
    print("✓ Expenses module tables")
    print("  - expenses")
    print()
    
    print("✓ System tables")
    print("  - system_settings")
    print()
    
    # Remove existing database if it exists
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"✓ Removed existing database")
        print()
    
    # Create data directory if needed
    import os
    os.makedirs("data", exist_ok=True)
    
    print("=" * 60)
    print("Database initialization complete!")
    # Remove existing database if it exists
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"✓ Removed existing database")
        print()
    
    # Create data directory if needed
    import os
    os.makedirs("data", exist_ok=True)
    
    print("=" * 60)
    print()
    print(f"Database location: {database_path}")
    print()
    
    return db_manager


if __name__ == "__main__":
    initialize_database()
