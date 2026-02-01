"""
Core Module
Central infrastructure components and model exports.
"""
from core.database import db_manager
from core.models import (
    Base, Deal, DealNote, Action,
    CommissionStructure, CommissionPayment, BuilderPayout,
    Client, ClientNote, Partner, PartnerNote,
    Expense, SystemSetting
)
from core.base_repository import BaseRepository

__all__ = [
    'db_manager', 'BaseRepository',
    # Models
    'Base', 'Deal', 'DealNote', 'Action',
    'CommissionStructure', 'CommissionPayment', 'BuilderPayout',
    'Client', 'ClientNote', 'Partner', 'PartnerNote',
    'Expense', 'SystemSetting'
]
