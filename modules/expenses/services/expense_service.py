"""
Expenses Module - Service Layer
"""
from typing import Dict, Any, Optional
from datetime import date
from core.base_service import BaseService
from modules.expenses.repositories.expense_repository import ExpenseRepository


class ExpenseService(BaseService):
    """Service for managing expenses."""
    
    def __init__(self, repository: ExpenseRepository):
        super().__init__(repository)
    
    def create_expense(self, data: Dict[str, Any]) -> tuple[bool, str, Optional[Any]]:
        required_fields = ['title', 'amount', 'category', 'payment_type', 'expense_date']
        is_valid, error = self.validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error, None
        
        is_valid, error = self.validate_numeric_field(data['amount'], 'Amount', min_value=0)
        if not is_valid:
            return False, error, None
        
        try:
            expense = self.repository.create(**data)
            return True, "Expense recorded successfully", expense
        except Exception as e:
            return False, str(e), None
    
    def get_monthly_expenses(self, month: int, year: int) -> float:
        return self.repository.get_monthly_total(month, year)
    
    def create(self, **data):
        success, msg, expense = self.create_expense(data)
        if not success:
            raise Exception(msg)
        return expense
    
    def get_all(self):
        return self.repository.get_all()

    def get_by_date_range(self, start_date, end_date):
        return self.repository.get_by_date_range(start_date, end_date)

    def get_monthly_total(self, year: int, month: int):
        return self.repository.get_monthly_total(month, year)

    def get_by_id(self, id):
        """Get expense by ID."""
        return self.repository.get_by_id(id)





    def update(self, expense_id, data):
        """Update expense."""
        return self.repository.update(expense_id, **data)
