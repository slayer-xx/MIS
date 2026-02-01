"""
Expenses Module - Repository Layer
"""
from typing import List
from datetime import date
from sqlalchemy import func
from core.base_repository import BaseRepository
from core.models import Expense
from core.database import db_manager


class ExpenseRepository(BaseRepository):
    """Repository for Expense model."""
    
    def __init__(self):
        self.session = db_manager.get_session()
        super().__init__(Expense, self.session)
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Expense]:
        return self.session.query(Expense).filter(
            Expense.expense_date >= start_date,
            Expense.expense_date <= end_date
        ).order_by(Expense.expense_date.desc()).all()
    
    def get_monthly_total(self, month: int, year: int) -> float:
        total = self.session.query(func.sum(Expense.amount)).filter(
            func.extract('month', Expense.expense_date) == month,
            func.extract('year', Expense.expense_date) == year
        ).scalar()
        return total or 0.0
    
    def get_by_category(self, category: str) -> List[Expense]:
        return self.session.query(Expense).filter(
            Expense.category == category
        ).order_by(Expense.expense_date.desc()).all()
