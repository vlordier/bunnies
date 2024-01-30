from typing import List, Optional
from pydantic import BaseModel

# Defining the Pydantic models based on the provided YAML structure

class Success(BaseModel):
    """
    Pydantic model for a success criteria
    """
    name: str
    description: str
    success: Optional[bool] = None
    reason_for_success: Optional[str] = None
    reason_for_failure: Optional[str] = None

class Action(BaseModel):
    """
    Pydantic model for an action
    """
    name: str
    description: str
    success_criteria: list[Success]
    retry: Optional[int] = None

class Step(BaseModel):
    """
    Pydantic model for a step
    """
    name: str
    description: str
    actions: Optional[List[Action]] = []
    success_criteria: list[Success]


class Goal(BaseModel):
    """
    Pydantic model for a goal
    """
    name: str
    description: str
    steps: Optional[List[Step]] = []
    success_criteria: list[Success]

class GoalsModel(BaseModel):
    """
    Pydantic model for the goals.yaml file
    """
    goals: List[Goal]
    success_criteria: list[Success]


class Journey(BaseModel):
    """
    Pydantic model for a journey
    """
    name: str
    description: str
    goals: List[Goal]
    success_criteria: list[Success]

if __name__ == "__main__":
    import yaml
    from pprint import pprint

    with open("goals.yaml") as file:
        goals_data = yaml.safe_load(file)
        goals_model = GoalsModel(goals=goals_data["goals"])
        pprint(goals_model.dict())