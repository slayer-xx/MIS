"""
Dashboard Module - Service Layer
Aggregates data from all modules for dashboard display.
"""
from typing import Dict, Any
from datetime import date, datetime


class DashboardService:
    """
    Service for dashboard data aggregation.
    
    This service reads data from other modules via their services/repositories
    but does not depend on their internal implementation.
    """
    
    def __init__(self, 
                 deal_service=None,
                 action_service=None,
                 commission_service=None,
                 expense_service=None):
        self.deal_service = deal_service
        self.action_service = action_service
        self.commission_service = commission_service
        self.expense_service = expense_service
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Return flat summary matching DashboardPage expectations."""
        
        # ---- DEALS ----
        active_deals = 0
        deals_this_month = 0
        if self.deal_service:
            try:
                active_deals = len(self.deal_service.get_active_deals())
                deals_this_month = len(self.deal_service.get_deals_this_month())
            except:
                pass

        # ---- COMMISSION ----
        total_expected = 0.0
        total_received = 0.0
        received_this_month = 0.0

        if self.commission_service:
            try:
                commissions = self.commission_service.get_all()
                total_expected = sum(c.commission_amount for c in commissions if c.commission_amount)

                from modules.commission.repositories.commission_repository import CommissionPaymentRepository
                payment_repo = CommissionPaymentRepository()
                all_payments = payment_repo.get_all()

                total_received = sum(p.amount for p in all_payments)

                now = datetime.now()
                received_this_month = sum(
                    p.amount for p in all_payments
                    if p.payment_date.month == now.month and p.payment_date.year == now.year
                )
            except:
                pass

        pending_commission = total_expected - total_received

        # ---- EXPENSES ----
        month_expenses = 0.0
        if self.expense_service:
            try:
                now = datetime.now()
                month_expenses = self.expense_service.get_monthly_total(now.year, now.month)
            except:
                pass

        return {
            # Overview section
            'active_deals': active_deals,
            'deals_this_month': deals_this_month,
            'total_expected_commission': total_expected,
            'received_this_month': received_this_month,
            'pending_commission': pending_commission,

            # Money section
            'total_expected': total_expected,
            'total_received': total_received,
            'outstanding': pending_commission,
            'month_expenses': month_expenses,
        }

    
    def _get_deals_summary(self) -> Dict[str, Any]:
        """Get deals summary"""
        if not self.deal_service:
            return {'active': 0, 'this_month': 0}
        
        # This would call deal_service methods
        return {
            'active': 0,  # Placeholder
            'this_month': 0
        }
    
    def _get_actions_summary(self) -> Dict[str, Any]:
        """Get actions summary"""
        if not self.action_service:
            return {'today': 0, 'overdue': 0}
        
        stats = self.action_service.get_dashboard_stats()
        return {
            'today': stats.get('today_count', 0),
            'overdue': stats.get('overdue_count', 0)
        }
    
    def _get_money_summary(self) -> Dict[str, Any]:
        """Get money summary"""
        return {
            'expected': 0.0,
            'received': 0.0,
            'pending': 0.0
        }
    
    def _get_monthly_summary(self) -> Dict[str, Any]:
        """Get current month summary"""
        now = datetime.now()
        month = now.month
        year = now.year
        
        expenses = 0.0
        if self.expense_service:
            expenses = self.expense_service.get_monthly_expenses(month, year)
        
        return {
            'expenses': expenses,
            'commission_received': 0.0,
            'net_profit': 0.0
        }
