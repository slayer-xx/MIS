"""
Team Member Repository
Handles database operations for team members
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from core.models import TeamMember, TeamMemberNote
from core.base_repository import BaseRepository


class TeamMemberRepository(BaseRepository[TeamMember]):
    """Repository for team member CRUD operations"""
    
    def __init__(self, session: Session):
        super().__init__(session, TeamMember)
    
    def get_by_type(self, member_type: str) -> List[TeamMember]:
        """Get all team members of a specific type"""
        return self.session.query(TeamMember).filter(
            TeamMember.member_type == member_type
        ).all()
    
    def get_active_members(self) -> List[TeamMember]:
        """Get all active team members"""
        return self.session.query(TeamMember).filter(
            TeamMember.employment_status == 'active'
        ).all()
    
    def get_employees(self) -> List[TeamMember]:
        """Get all employees"""
        return self.get_by_type('employee')
    
    def get_revenue_partners(self) -> List[TeamMember]:
        """Get all revenue partners"""
        return self.get_by_type('revenue_partner')
    
    def search_by_name(self, name: str) -> List[TeamMember]:
        """Search team members by name"""
        return self.session.query(TeamMember).filter(
            TeamMember.name.ilike(f"%{name}%")
        ).all()
    
    def update_performance_stats(self, member_id: int, deals_closed: int = 0, commission_earned: float = 0.0):
        """Update team member performance statistics"""
        member = self.get_by_id(member_id)
        if member:
            if deals_closed > 0:
                member.total_deals_closed += deals_closed
            if commission_earned > 0:
                member.total_commission_earned += commission_earned
            self.session.commit()


class TeamMemberNoteRepository(BaseRepository[TeamMemberNote]):
    """Repository for team member notes"""
    
    def __init__(self, session: Session):
        super().__init__(session, TeamMemberNote)
    
    def get_by_team_member(self, team_member_id: int) -> List[TeamMemberNote]:
        """Get all notes for a team member"""
        return self.session.query(TeamMemberNote).filter(
            TeamMemberNote.team_member_id == team_member_id
        ).order_by(TeamMemberNote.created_at.desc()).all()
    
    def get_by_type(self, team_member_id: int, note_type: str) -> List[TeamMemberNote]:
        """Get notes of a specific type for a team member"""
        return self.session.query(TeamMemberNote).filter(
            TeamMemberNote.team_member_id == team_member_id,
            TeamMemberNote.note_type == note_type
        ).order_by(TeamMemberNote.created_at.desc()).all()
