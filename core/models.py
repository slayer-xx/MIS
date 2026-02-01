"""
Enhanced Database Models - Modular Architecture
SQLAlchemy ORM models for all modules in the MIS system.

Design Principle: Each model is independent and uses only IDs for relationships.
This ensures loose coupling and module independence.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# ============================================================================
# DEALS MODULE MODELS
# ============================================================================

class Deal(Base):
    """
    Core Deal model representing a real estate transaction.
    Module: Deals
    """
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    deal_type = Column(String(50), nullable=False)  # Builder/Resale/Rental
    status = Column(String(50), nullable=False)  # Lead/Site Visit/Negotiation/Booking/Closed/Lost
    
    # Client information (can later be replaced with client_id when Clients module is added)
    client_name = Column(String(200), nullable=False)
    client_phone = Column(String(20), nullable=True)
    client_email = Column(String(100), nullable=True)
    
    # Property details
    property_location = Column(String(300), nullable=True)
    property_type = Column(String(100), nullable=True)  # Apartment/Villa/Plot/Commercial
    property_value = Column(Float, nullable=True)
    
    # Deal financial basics
    expected_commission = Column(Float, nullable=True)
    commission_percentage = Column(Float, nullable=True)
    
    # Partner/Builder info (can later be replaced with partner_id)
    builder_name = Column(String(200), nullable=True)
    partner_broker_name = Column(String(200), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_date = Column(Date, nullable=True)
    
    # Relationships (lazy loaded, independent modules access via IDs only)
    notes = relationship("DealNote", back_populates="deal", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Deal(id={self.id}, title='{self.title}', status='{self.status}')>"


class DealNote(Base):
    """
    Timeline notes for deals - internal module of Deals
    Module: Deals (sub-component)
    """
    __tablename__ = "deal_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general/call/meeting/email
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)  # For future multi-user
    
    deal = relationship("Deal", back_populates="notes")
    
    def __repr__(self):
        return f"<DealNote(id={self.id}, deal_id={self.deal_id})>"


# ============================================================================
# ACTIONS (FOLLOW-UP) MODULE MODELS
# ============================================================================

class Action(Base):
    """
    Follow-up actions and reminders
    Module: Actions (independent)
    
    Links to deals via deal_id but doesn't depend on Deal implementation.
    Can also exist independently for general business actions.
    """
    __tablename__ = "actions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Optional link to deal (can be null for general actions)
    deal_id = Column(Integer, nullable=True)  # No FK - loose coupling
    
    # Optional link to client (when clients module exists)
    client_name = Column(String(200), nullable=True)
    
    # Action scheduling
    action_date = Column(Date, nullable=False)
    action_time = Column(String(10), nullable=True)  # "10:30 AM" format
    
    # Action categorization
    action_type = Column(String(50), nullable=False)  # Call/Meeting/SiteVisit/Document/Follow-up
    priority = Column(String(20), default="medium")  # high/medium/low
    
    # Status
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Action(id={self.id}, title='{self.title}', date={self.action_date})>"


# ============================================================================
# COMMISSION MODULE MODELS
# ============================================================================

class CommissionStructure(Base):
    """
    Commission breakdown for a deal
    Module: Commission
    
    Defines who gets what from the total commission.
    Links to deal via deal_id only.
    """
    __tablename__ = "commission_structures"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, nullable=False)  # No FK - loose coupling
    
    # Party receiving commission
    party_type = Column(String(50), nullable=False)  # self/partner/staff/builder
    party_name = Column(String(200), nullable=False)
    
    # Commission details
    commission_percentage = Column(Float, nullable=True)  # % of total deal commission
    commission_amount = Column(Float, nullable=False)  # Actual amount
    
    # Status
    status = Column(String(50), default="pending")  # pending/received/partial
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CommissionStructure(id={self.id}, party='{self.party_name}', amount={self.commission_amount})>"


class CommissionPayment(Base):
    """
    Actual payments received against commissions
    Module: Commission
    
    Tracks when and how commission money came in.
    """
    __tablename__ = "commission_payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    commission_structure_id = Column(Integer, ForeignKey("commission_structures.id"), nullable=False)
    deal_id = Column(Integer, nullable=False)  # Denormalized for easy querying
    
    # Payment details
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)  # cash/bank/cheque/upi
    payment_date = Column(Date, nullable=False)
    
    # Additional info
    reference_number = Column(String(100), nullable=True)  # Transaction/cheque number
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CommissionPayment(id={self.id}, amount={self.amount}, date={self.payment_date})>"


class BuilderPayout(Base):
    """
    Tracks builder incentives and payouts separate from broker commission
    Module: Commission
    """
    __tablename__ = "builder_payouts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, nullable=False)  # No FK - loose coupling
    builder_name = Column(String(200), nullable=False)
    
    # Payout details
    payout_type = Column(String(50), nullable=False)  # incentive/bonus/referral
    payout_amount = Column(Float, nullable=False)
    expected_date = Column(Date, nullable=True)
    
    # Status
    status = Column(String(50), default="pending")  # pending/received/cancelled
    received_date = Column(Date, nullable=True)
    received_amount = Column(Float, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<BuilderPayout(id={self.id}, builder='{self.builder_name}', amount={self.payout_amount})>"


# ============================================================================
# CLIENTS MODULE MODELS
# ============================================================================

class Client(Base):
    """
    Client information repository
    Module: Clients
    
    Independent client database. Deals reference clients by ID.
    """
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    
    # Client categorization
    client_type = Column(String(50), nullable=False)  # Buyer/Seller/Investor/Tenant/Landlord
    source = Column(String(100), nullable=True)  # Referral/Walk-in/Online/Partner
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    
    # Business metadata
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    preferred_locations = Column(Text, nullable=True)  # JSON or comma-separated
    preferred_property_types = Column(Text, nullable=True)  # JSON or comma-separated
    
    # Status
    status = Column(String(50), default="active")  # active/inactive/converted
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', type='{self.client_type}')>"


class ClientNote(Base):
    """
    Notes and history for clients
    Module: Clients (sub-component)
    """
    __tablename__ = "client_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general/call/meeting/preference
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<ClientNote(id={self.id}, client_id={self.client_id})>"


# ============================================================================
# PARTNERS MODULE MODELS
# ============================================================================

class Partner(Base):
    """
    Partner brokers, builders, and channel associates
    Module: Partners
    """
    __tablename__ = "partners"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    partner_type = Column(String(50), nullable=False)  # broker/builder/channel_partner
    company_name = Column(String(200), nullable=True)
    
    # Contact info
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    
    # Business terms
    default_commission_split = Column(Float, nullable=True)  # Default % they get
    rera_number = Column(String(100), nullable=True)
    gst_number = Column(String(100), nullable=True)
    pan_number = Column(String(20), nullable=True)
    
    # Status
    status = Column(String(50), default="active")  # active/inactive
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Partner(id={self.id}, name='{self.name}', type='{self.partner_type}')>"


class PartnerNote(Base):
    """
    Notes for partners
    Module: Partners (sub-component)
    """
    __tablename__ = "partner_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<PartnerNote(id={self.id}, partner_id={self.partner_id})>"


# ============================================================================
# EXPENSES MODULE MODELS
# ============================================================================

class Expense(Base):
    """
    Business expense tracking
    Module: Expenses (fully independent)
    """
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Expense details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    
    # Categorization
    category = Column(String(100), nullable=False)  # Rent/Salary/Marketing/Travel/Utilities/Other
    sub_category = Column(String(100), nullable=True)
    
    # Payment info
    payment_type = Column(String(50), nullable=False)  # cash/bank/card/upi
    expense_date = Column(Date, nullable=False)
    
    # Additional metadata
    vendor_name = Column(String(200), nullable=True)
    invoice_number = Column(String(100), nullable=True)
    is_recurring = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Expense(id={self.id}, title='{self.title}', amount={self.amount})>"


# ============================================================================
# SYSTEM MODELS (for future features)
# ============================================================================

class SystemSetting(Base):
    """
    Application settings and preferences
    Module: System (infrastructure)
    """
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_key = Column(String(100), nullable=False, unique=True)
    setting_value = Column(Text, nullable=True)
    setting_type = Column(String(50), nullable=False)  # string/int/float/bool/json
    
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemSetting(key='{self.setting_key}', value='{self.setting_value}')>"
