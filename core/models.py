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
    
    V2 Changes:
    - Removed expected_commission and commission_percentage (moved to CommissionStructure)
    - Added commission_paid_by to track source
    - Added business_partner_id for builder deals
    - Added team_member_id for tracking who handled the deal
    - Added total_commission_received for actual amount
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
    
    # Commission tracking (V2)
    commission_paid_by = Column(String(50), nullable=True)  # client/builder
    business_partner_id = Column(Integer, nullable=True)  # ID of builder if builder paid
    team_member_id = Column(Integer, nullable=True)  # ID of team member who handled deal
    total_commission_received = Column(Float, nullable=True)  # Actual total commission amount
    
    # Legacy fields (kept for backward compatibility, will be migrated)
    builder_name = Column(String(200), nullable=True)  # DEPRECATED in V2
    partner_broker_name = Column(String(200), nullable=True)  # DEPRECATED in V2
    expected_commission = Column(Float, nullable=True)  # DEPRECATED in V2
    commission_percentage = Column(Float, nullable=True)  # DEPRECATED in V2
    
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
# TEAM MODULE MODELS (V2)
# ============================================================================

class TeamMember(Base):
    """
    Team member (employees and revenue-sharing partners)
    Module: Team (V2 - replaces Partner partially)
    
    This model tracks internal team members who handle deals and earn commission/salary.
    - Employees: Fixed salary + small commission percentage
    - Revenue Partners: No salary, only revenue share percentage
    - Owner: No salary, no commission split
    """
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    member_type = Column(String(50), nullable=False)  # employee/revenue_partner/owner
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    
    # Employment details
    employment_status = Column(String(50), default="active")  # active/inactive/on_leave
    joining_date = Column(Date, nullable=True)
    exit_date = Column(Date, nullable=True)
    
    # Financial structure for Employees
    monthly_salary = Column(Float, nullable=True)  # Fixed salary (null for revenue partners)
    commission_percentage = Column(Float, nullable=True)  # % of deal commission they get
    
    # Financial structure for Revenue Partners
    revenue_share_percentage = Column(Float, nullable=True)  # % of company profit they get
    
    # Legal/Tax information
    pan_number = Column(String(20), nullable=True)
    aadhar_number = Column(String(20), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_ifsc_code = Column(String(20), nullable=True)
    bank_name = Column(String(100), nullable=True)
    
    # Performance tracking (denormalized for quick access)
    total_deals_closed = Column(Integer, default=0)
    total_commission_earned = Column(Float, default=0.0)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<TeamMember(id={self.id}, name='{self.name}', type='{self.member_type}')>"


class TeamMemberNote(Base):
    """
    Notes and history for team members
    Module: Team (sub-component)
    """
    __tablename__ = "team_member_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_member_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general/performance/issue/achievement
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<TeamMemberNote(id={self.id}, team_member_id={self.team_member_id})>"


# ============================================================================
# BUSINESS PARTNERS MODULE MODELS (V2)
# ============================================================================

class BusinessPartner(Base):
    """
    External business partners (builders, other brokerages)
    Module: Business Partners (V2 - replaces Partner partially)
    
    This model tracks external entities who pay us commission or we collaborate with.
    - Builders: Pay us commission on property sales
    - Brokerage Firms: Other real estate agencies we work with
    - Channel Partners: Other business associates
    """
    __tablename__ = "business_partners"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic info
    name = Column(String(200), nullable=False)
    partner_type = Column(String(50), nullable=False)  # builder/brokerage_firm/channel_partner
    company_name = Column(String(200), nullable=True)
    
    # Contact info
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    
    # Business terms
    default_commission_percentage = Column(Float, nullable=True)  # Default % they pay us
    payment_terms = Column(Text, nullable=True)  # Description of payment terms
    
    # For builders - projects they're working on
    active_projects = Column(Text, nullable=True)  # Comma-separated or JSON
    
    # Legal info
    rera_number = Column(String(100), nullable=True)
    gst_number = Column(String(100), nullable=True)
    pan_number = Column(String(20), nullable=True)
    
    # Relationship quality
    status = Column(String(50), default="active")  # active/inactive
    relationship_quality = Column(String(50), nullable=True)  # excellent/good/average/poor
    
    # Performance tracking (denormalized)
    total_deals_done = Column(Integer, default=0)
    total_commission_paid = Column(Float, default=0.0)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<BusinessPartner(id={self.id}, name='{self.name}', type='{self.partner_type}')>"


class BusinessPartnerNote(Base):
    """
    Notes for business partners
    Module: Business Partners (sub-component)
    """
    __tablename__ = "business_partner_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    business_partner_id = Column(Integer, ForeignKey("business_partners.id"), nullable=False)
    
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general/project/payment/issue
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<BusinessPartnerNote(id={self.id}, business_partner_id={self.business_partner_id})>"


# ============================================================================
# COMMISSION MODULE MODELS (V2 - COMPLETELY REDESIGNED)
# ============================================================================

class CommissionStructure(Base):
    """
    Commission breakdown and distribution for a deal (V2 - Redesigned)
    Module: Commission
    
    This model tracks the complete commission flow:
    1. Who paid the commission (client or builder)
    2. How much was received
    3. Client cashback (if builder paid)
    4. Team member distribution
    5. Company final share
    
    Example flows:
    - Builder pays 5% → 4% to client, 1% retained → split with team member
    - Client pays 2% → split with team member (if applicable)
    """
    __tablename__ = "commission_structures"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, nullable=False)  # No FK - loose coupling
    
    # Commission source
    commission_source = Column(String(50), nullable=False)  # client/builder
    
    # Builder commission details (only if builder paid)
    business_partner_id = Column(Integer, nullable=True)  # ID of builder/business partner
    builder_commission_percentage = Column(Float, nullable=True)  # e.g., 5%
    builder_commission_amount = Column(Float, nullable=True)  # Total from builder
    
    # Client cashback (only if builder paid commission)
    client_cashback_percentage = Column(Float, nullable=True)  # e.g., 4%
    client_cashback_amount = Column(Float, nullable=True)  # Amount given back to client
    client_cashback_paid = Column(Boolean, default=False)
    client_cashback_date = Column(Date, nullable=True)
    
    # Company retention (what company keeps before team distribution)
    company_retention_percentage = Column(Float, nullable=True)  # e.g., 1% or 100%
    company_retention_amount = Column(Float, nullable=False)  # Amount company retains
    
    # Team member distribution
    team_member_id = Column(Integer, nullable=True)  # ID of team member (null if owner handled)
    team_member_type = Column(String(50), nullable=True)  # employee/revenue_partner/owner
    team_member_commission_percentage = Column(Float, nullable=True)  # % of retained amount
    team_member_commission_amount = Column(Float, default=0.0)  # Amount for team member
    
    # Company final share (after all distributions)
    company_final_amount = Column(Float, nullable=False)  # What company actually keeps
    
    # Overall status
    status = Column(String(50), default="pending")  # pending/partially_paid/fully_paid
    
    # Quick reference amounts
    total_commission_received = Column(Float, nullable=False)  # Total received (from client or builder)
    total_commission_paid_out = Column(Float, default=0.0)  # Total paid (cashback + team member)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CommissionStructure(id={self.id}, deal_id={self.deal_id}, total={self.total_commission_received})>"


class CommissionPayment(Base):
    """
    Individual payment transactions in the commission flow (V2 - Enhanced)
    Module: Commission
    
    Tracks each leg of the commission payment:
    1. Builder/Client → Company
    2. Company → Client (cashback, if applicable)
    3. Company → Team Member
    
    This provides a complete audit trail of all money movements.
    """
    __tablename__ = "commission_payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    commission_structure_id = Column(Integer, ForeignKey("commission_structures.id"), nullable=False)
    deal_id = Column(Integer, nullable=False)  # Denormalized for easy querying
    
    # Payment category/direction
    payment_category = Column(String(50), nullable=False)  
    # Values: builder_to_company, client_to_company, company_to_client, company_to_team
    
    # Who is receiving this payment
    recipient_type = Column(String(50), nullable=False)  # company/client/team_member/external
    recipient_id = Column(Integer, nullable=True)  # ID of team member or business partner (if applicable)
    recipient_name = Column(String(200), nullable=True)  # Name for reference
    
    # Payment details
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)  # cash/bank_transfer/cheque/upi/neft/rtgs
    payment_date = Column(Date, nullable=False)
    
    # Additional payment info
    reference_number = Column(String(100), nullable=True)  # Transaction/cheque number
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)  # Last 4 digits for security
    transaction_id = Column(String(100), nullable=True)
    
    # Status
    status = Column(String(50), default="completed")  # pending/completed/failed/cancelled
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CommissionPayment(id={self.id}, category='{self.payment_category}', amount={self.amount})>"


# Legacy model kept for data migration only - will be removed after migration
class BuilderPayout(Base):
    """
    DEPRECATED in V2 - Kept only for data migration
    Tracks builder incentives and payouts separate from broker commission
    Module: Commission
    
    This table will be migrated to CommissionStructure and CommissionPayment
    and then dropped.
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
