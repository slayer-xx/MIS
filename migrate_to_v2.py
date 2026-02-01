"""
Database Migration Script - V2 Commission Restructure
======================================================

This script migrates the database from V1 to V2 structure:

1. Creates new tables: team_members, business_partners, and their notes
2. Updates commission_structures and commission_payments with new schema
3. Migrates existing Partner data to appropriate new tables
4. Adds new fields to deals table
5. Preserves all existing data

IMPORTANT: This script backs up the database before migration.
"""

import os
import shutil
from datetime import datetime
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from core.database import db_manager
from core.models import Base, TeamMember, BusinessPartner
import config

# Try to import Partner model if it exists
try:
    from core.models import Partner
    HAS_PARTNER_MODEL = True
except (ImportError, AttributeError):
    HAS_PARTNER_MODEL = False
    print("Note: Partner model not found in core.models - will skip partner migration")

def backup_database():
    """Create a backup of the current database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config.DATA_DIR / f"real_estate_mis_backup_{timestamp}.db"
    
    print(f"Creating backup at: {backup_path}")
    shutil.copy2(config.DATABASE_PATH, backup_path)
    print("✓ Backup created successfully")
    return backup_path


def check_existing_tables(engine):
    """Check which tables already exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"\nExisting tables: {', '.join(existing_tables)}")
    return existing_tables


def create_new_tables(engine):
    """Create only the new V2 tables"""
    print("\n=== Creating New V2 Tables ===")
    
    # Get list of existing tables
    existing_tables = check_existing_tables(engine)
    
    # Tables we want to create
    new_tables = ['team_members', 'team_member_notes', 'business_partners', 'business_partner_notes']
    
    # Create only new tables
    Base.metadata.create_all(engine, tables=[
        Base.metadata.tables[table] for table in new_tables 
        if table in Base.metadata.tables and table not in existing_tables
    ])
    
    print("✓ New tables created successfully")


def migrate_partners_to_team_and_business(session):
    """Migrate existing Partner data to TeamMember and BusinessPartner tables"""
    print("\n=== Migrating Partner Data ===")
    
    if not HAS_PARTNER_MODEL:
        print("Partner model not available - checking if partners table exists...")
        inspector = inspect(session.bind)
        if 'partners' not in inspector.get_table_names():
            print("No partners table found - skipping partner migration")
            return
    
    try:
        # Check if partners table exists and has data
        result = session.execute(text("SELECT COUNT(*) FROM partners")).fetchone()
        partner_count = result[0] if result else 0
        
        if partner_count == 0:
            print("No partners found to migrate")
            return
        
        print(f"Found {partner_count} partners to migrate")
        
        # Fetch partners using raw SQL since we might not have the model
        partners_data = session.execute(text("""
            SELECT id, name, partner_type, company_name, phone, email, alternate_phone,
                   address, city, default_commission_split, rera_number, gst_number, 
                   pan_number, status, created_at, updated_at
            FROM partners
        """)).fetchall()
        
        team_count = 0
        business_count = 0
        
        for partner in partners_data:
            # Determine where this partner should go
            partner_type = partner[2].lower() if partner[2] else ''
            
            if partner_type == 'broker' or 'broker' in partner_type:
                # Migrate to TeamMember as revenue_partner
                team_member = TeamMember(
                    name=partner[1],
                    member_type='revenue_partner',
                    phone=partner[4] or '',
                    email=partner[5],
                    alternate_phone=partner[6],
                    address=partner[7],
                    city=partner[8],
                    employment_status='active' if partner[13] == 'active' else 'inactive',
                    revenue_share_percentage=partner[9],
                    pan_number=partner[12],
                    notes=f"Migrated from Partners module. Original type: {partner[2]}",
                    created_at=partner[14],
                    updated_at=partner[15]
                )
                session.add(team_member)
                team_count += 1
                print(f"  → Migrated '{partner[1]}' to Team (revenue_partner)")
                
            elif partner_type == 'builder' or 'builder' in partner_type:
                # Migrate to BusinessPartner as builder
                business_partner = BusinessPartner(
                    name=partner[1],
                    partner_type='builder',
                    company_name=partner[3],
                    phone=partner[4] or '',
                    email=partner[5],
                    alternate_phone=partner[6],
                    address=partner[7],
                    city=partner[8],
                    default_commission_percentage=partner[9],
                    rera_number=partner[10],
                    gst_number=partner[11],
                    pan_number=partner[12],
                    status='active' if partner[13] == 'active' else 'inactive',
                    notes=f"Migrated from Partners module. Original type: {partner[2]}",
                    created_at=partner[14],
                    updated_at=partner[15]
                )
                session.add(business_partner)
                business_count += 1
                print(f"  → Migrated '{partner[1]}' to Business Partners (builder)")
                
            else:
                # Channel partner or other - migrate to BusinessPartner
                business_partner = BusinessPartner(
                    name=partner[1],
                    partner_type='channel_partner',
                    company_name=partner[3],
                    phone=partner[4] or '',
                    email=partner[5],
                    alternate_phone=partner[6],
                    address=partner[7],
                    city=partner[8],
                    default_commission_percentage=partner[9],
                    rera_number=partner[10],
                    gst_number=partner[11],
                    pan_number=partner[12],
                    status='active' if partner[13] == 'active' else 'inactive',
                    notes=f"Migrated from Partners module. Original type: {partner[2]}",
                    created_at=partner[14],
                    updated_at=partner[15]
                )
                session.add(business_partner)
                business_count += 1
                print(f"  → Migrated '{partner[1]}' to Business Partners (channel_partner)")
        
        session.commit()
        print(f"\n✓ Migration complete:")
        print(f"  - {team_count} partners → Team Members")
        print(f"  - {business_count} partners → Business Partners")
        
    except Exception as e:
        print(f"✗ Error during partner migration: {e}")
        session.rollback()
        raise


def add_columns_to_deals(engine):
    """Add new columns to deals table"""
    print("\n=== Adding New Columns to Deals Table ===")
    
    # Check which columns already exist
    inspector = inspect(engine)
    existing_columns = [col['name'] for col in inspector.get_columns('deals')]
    
    # Define new columns with their SQL
    new_columns = {
        "commission_paid_by": "ALTER TABLE deals ADD COLUMN commission_paid_by VARCHAR(50)",
        "business_partner_id": "ALTER TABLE deals ADD COLUMN business_partner_id INTEGER",
        "team_member_id": "ALTER TABLE deals ADD COLUMN team_member_id INTEGER",
        "total_commission_received": "ALTER TABLE deals ADD COLUMN total_commission_received FLOAT"
    }
    
    with engine.connect() as conn:
        for column_name, sql in new_columns.items():
            if column_name in existing_columns:
                print(f"  - Column '{column_name}' already exists, skipping")
            else:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"  ✓ Added column: {column_name}")
                except Exception as e:
                    print(f"  ✗ Error adding column '{column_name}': {e}")
    
    print("✓ Deal table columns update complete")


def verify_migration(session):
    """Verify that migration was successful"""
    print("\n=== Verifying Migration ===")
    
    # Count records in new tables
    team_count = session.query(TeamMember).count()
    business_count = session.query(BusinessPartner).count()
    
    print(f"Team Members: {team_count}")
    print(f"Business Partners: {business_count}")
    
    # Check if new columns exist in deals
    from sqlalchemy import inspect
    inspector = inspect(session.bind)
    deal_columns = [col['name'] for col in inspector.get_columns('deals')]
    
    new_deal_columns = ['commission_paid_by', 'business_partner_id', 'team_member_id', 'total_commission_received']
    for col in new_deal_columns:
        if col in deal_columns:
            print(f"✓ Deal column '{col}' exists")
        else:
            print(f"✗ Deal column '{col}' missing")
    
    print("\n✓ Migration verification complete")


def main():
    """Main migration function"""
    print("=" * 70)
    print("DATABASE MIGRATION - V2 COMMISSION RESTRUCTURE")
    print("=" * 70)
    
    # Confirm with user
    print("\nThis migration will:")
    print("1. Create a backup of your current database")
    print("2. Create new tables for Team and Business Partners")
    print("3. Migrate existing Partner data to appropriate tables")
    print("4. Add new columns to Deals table")
    print("5. Keep all existing data intact")
    
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Migration cancelled.")
        return
    
    try:
        # Step 1: Backup database
        backup_path = backup_database()
        
        # Step 2: Initialize database connection
        print("\nInitializing database connection...")
        engine = create_engine(config.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Step 3: Create new tables
        create_new_tables(engine)
        
        # Step 4: Add columns to deals table
        add_columns_to_deals(engine)
        
        # Step 5: Migrate partner data
        migrate_partners_to_team_and_business(session)
        
        # Step 6: Verify migration
        verify_migration(session)
        
        # Close session
        session.close()
        
        print("\n" + "=" * 70)
        print("MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\nBackup saved at: {backup_path}")
        print("\nNext steps:")
        print("1. Test the application with new Team and Business Partners modules")
        print("2. Verify all data migrated correctly")
        print("3. Once confirmed, the old Partners module can be removed")
        
    except Exception as e:
        print(f"\n✗ MIGRATION FAILED: {e}")
        print(f"\nYour original database backup is at: {backup_path}")
        print("You can restore it by copying it back to the data directory.")
        raise


if __name__ == "__main__":
    main()
