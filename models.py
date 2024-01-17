"""
This file contains the models for the data used in the project.
"""

from pydantic import BaseModel


class AgentDefinition(BaseModel):
    """
    This class defines the data model for an agent.
    """

    role: str
    goal: str
    backstory: str
    verbose: bool
    allow_delegation: bool
    tools: list
    agent_name: str


class AgentsList(BaseModel):
    """
    This class defines the data model for a list of agents.
    """

    agents: list[AgentDefinition]


class Task(BaseModel):
    """
    This class defines the data model for a task.
    """

    description: str
    agent: AgentDefinition


class TasksList(BaseModel):
    """
    This class defines the data model for a list of tasks.
    """

    tasks: list[Task]
