"""
Team Member Service
Handles business logic for team members
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlalchemy.orm import Session
from core.models import TeamMember, TeamMemberNote
from modules.team.repositories.team_repository import TeamMemberRepository, TeamMemberNoteRepository


class TeamMemberService:
    """Service for team member business logic"""
    
    def __init__(self, session: Session):
        self.session = session
        self.repo = TeamMemberRepository(session)
        self.note_repo = TeamMemberNoteRepository(session)
    
    def create_team_member(self, data: Dict[str, Any]) -> TeamMember:
        """Create a new team member"""
        team_member = TeamMember(**data)
        return self.repo.create(team_member)
    
    def update_team_member(self, member_id: int, data: Dict[str, Any]) -> Optional[TeamMember]:
        """Update a team member"""
        return self.repo.update(member_id, data)
    
    def delete_team_member(self, member_id: int) -> bool:
        """Delete a team member"""
        return self.repo.delete(member_id)
    
    def get_team_member(self, member_id: int) -> Optional[TeamMember]:
        """Get a team member by ID"""
        return self.repo.get_by_id(member_id)
    
    def get_all_team_members(self) -> List[TeamMember]:
        """Get all team members"""
        return self.repo.get_all()
    
    def get_active_team_members(self) -> List[TeamMember]:
        """Get all active team members"""
        return self.repo.get_active_members()
    
    def get_employees(self) -> List[TeamMember]:
        """Get all employees"""
        return self.repo.get_employees()
    
    def get_revenue_partners(self) -> List[TeamMember]:
        """Get all revenue partners"""
        return self.repo.get_revenue_partners()
    
    def search_team_members(self, name: str) -> List[TeamMember]:
        """Search team members by name"""
        return self.repo.search_by_name(name)
    
    def add_note(self, team_member_id: int, note_text: str, note_type: str = "general", created_by: str = None) -> TeamMemberNote:
        """Add a note to a team member"""
        note = TeamMemberNote(
            team_member_id=team_member_id,
            note_text=note_text,
            note_type=note_type,
            created_by=created_by
        )
        return self.note_repo.create(note)
    
    def get_member_notes(self, team_member_id: int) -> List[TeamMemberNote]:
        """Get all notes for a team member"""
        return self.note_repo.get_by_team_member(team_member_id)
    
    def calculate_monthly_earnings(self, member_id: int, month: int, year: int) -> Dict[str, float]:
        """Calculate monthly earnings for a team member"""
        member = self.get_team_member(member_id)
        if not member:
            return {"salary": 0.0, "commission": 0.0, "total": 0.0}
        
        # For now, return basic structure
        # This will be enhanced when commission tracking is implemented
        salary = member.monthly_salary or 0.0
        commission = 0.0  # Will be calculated from actual deals/commissions
        
        return {
            "salary": salary,
            "commission": commission,
            "total": salary + commission
        }
    
    def get_member_performance(self, member_id: int) -> Dict[str, Any]:
        """Get performance metrics for a team member"""
        member = self.get_team_member(member_id)
        if not member:
            return {}
        
        return {
            "id": member.id,
            "name": member.name,
            "member_type": member.member_type,
            "total_deals_closed": member.total_deals_closed,
            "total_commission_earned": member.total_commission_earned,
            "employment_status": member.employment_status,
            "joining_date": member.joining_date,
            "monthly_salary": member.monthly_salary,
            "commission_percentage": member.commission_percentage,
            "revenue_share_percentage": member.revenue_share_percentage
        }
    
    def update_performance_stats(self, member_id: int, deals_closed: int = 0, commission_earned: float = 0.0):
        """Update performance statistics for a team member"""
        self.repo.update_performance_stats(member_id, deals_closed, commission_earned)
    
    def get_team_summary(self) -> Dict[str, Any]:
        """Get summary of all team members"""
        all_members = self.get_all_team_members()
        active_members = [m for m in all_members if m.employment_status == 'active']
        
        employees = [m for m in all_members if m.member_type == 'employee']
        revenue_partners = [m for m in all_members if m.member_type == 'revenue_partner']
        owners = [m for m in all_members if m.member_type == 'owner']
        
        total_salary_expense = sum(m.monthly_salary or 0 for m in active_members if m.monthly_salary)
        total_deals = sum(m.total_deals_closed for m in all_members)
        total_commission = sum(m.total_commission_earned for m in all_members)
        
        return {
            "total_members": len(all_members),
            "active_members": len(active_members),
            "employees": len(employees),
            "revenue_partners": len(revenue_partners),
            "owners": len(owners),
            "total_monthly_salary_expense": total_salary_expense,
            "total_deals_closed": total_deals,
            "total_commission_earned": total_commission
        }
