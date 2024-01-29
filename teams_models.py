"""
Models for teams
"""

from typing import List, Optional
from pydantic import BaseModel
from crewai import Agent
from datetime import datetime

class Team(BaseModel):
    """
    Team model
    """
    team_name: str
    team_description: str
    team_members: List[Agent]
    team_owner: Agent
    # add a date for when the team was created
    team_created: datetime
    # add a date for when the team was last updated
    team_updated: datetime

