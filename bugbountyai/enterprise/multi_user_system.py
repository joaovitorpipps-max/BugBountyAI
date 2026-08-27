"""Multi-User & Team Collaboration System untuk v2"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class UserRole(Enum):
    """User roles definition"""
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User:
    """User class"""

    def __init__(self, user_id: str, username: str, email: str, role: UserRole):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        self.permissions = self._get_permissions_for_role(role)

    @staticmethod
    def _get_permissions_for_role(role: UserRole) -> List[str]:
        """Get permissions based on role"""
        permissions_map = {
            UserRole.ADMIN: [
                "view_all",
                "create",
                "edit",
                "delete",
                "manage_users",
                "manage_settings",
            ],
            UserRole.MANAGER: [
                "view_all",
                "create",
                "edit",
                "manage_team",
            ],
            UserRole.ANALYST: [
                "view_assigned",
                "create",
                "edit_own",
            ],
            UserRole.VIEWER: [
                "view_assigned",
            ],
        }
        return permissions_map.get(role, [])


class Team:
    """Team class untuk collaboration"""

    def __init__(self, team_id: str, team_name: str, owner_id: str):
        self.team_id = team_id
        self.team_name = team_name
        self.owner_id = owner_id
        self.members: List[User] = []
        self.projects: List[str] = []
        self.created_at = datetime.now()

    def add_member(self, user: User) -> bool:
        """Add member ke team"""
        if user not in self.members:
            self.members.append(user)
            logger.info(f"Added {user.username} to team {self.team_name}")
            return True
        return False

    def remove_member(self, user_id: str) -> bool:
        """Remove member dari team"""
        for i, member in enumerate(self.members):
            if member.user_id == user_id:
                self.members.pop(i)
                logger.info(f"Removed user {user_id} from team {self.team_name}")
                return True
        return False

    def get_members(self) -> List[User]:
        """Get all team members"""
        return self.members


class MultiUserSystem:
    """Multi-user system management"""

    def __init__(self):
        """Initialize multi-user system"""
        self.users: Dict[str, User] = {}
        self.teams: Dict[str, Team] = {}
        logger.info("MultiUserSystem initialized")

    def create_user(self, username: str, email: str, role: UserRole) -> User:
        """Create new user
        
        Args:
            username: Username
            email: Email address
            role: User role
            
        Returns:
            Created User object
        """
        user_id = f"user_{len(self.users) + 1}"
        user = User(user_id, username, email, role)
        self.users[user_id] = user
        logger.info(f"Created user: {username}")
        return user

    def create_team(self, team_name: str, owner_id: str) -> Team:
        """Create new team
        
        Args:
            team_name: Team name
            owner_id: Owner user ID
            
        Returns:
            Created Team object
        """
        team_id = f"team_{len(self.teams) + 1}"
        team = Team(team_id, team_name, owner_id)
        self.teams[team_id] = team
        logger.info(f"Created team: {team_name}")
        return team

    def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get personalized dashboard untuk user
        
        Args:
            user_id: User ID
            
        Returns:
            User dashboard data
        """
        user = self.users.get(user_id)
        if not user:
            return {"error": "User not found"}
        
        return {
            "user": {
                "id": user.user_id,
                "username": user.username,
                "role": user.role.value,
            },
            "permissions": user.permissions,
            "recent_activity": [],
            "assigned_projects": [],
        }

    def can_user_access(self, user_id: str, resource_id: str, action: str) -> bool:
        """Check if user can access resource
        
        Args:
            user_id: User ID
            resource_id: Resource ID
            action: Action to perform
            
        Returns:
            True if user can access
        """
        user = self.users.get(user_id)
        if not user:
            return False
        
        return action in user.permissions
