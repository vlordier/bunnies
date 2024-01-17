import logging

import yaml
from crewai import Agent

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Define tools

agent_yaml_file = "agents.yaml"

with open(agent_yaml_file) as file:
    agents_data = yaml.safe_load(file)

for data in agents_data["agents"]:
    # Create a variable name by replacing spaces in the role with underscores and prefixing with 'agent_'
    var_name = "agent_" + data["role"].replace(" ", "_").lower()
    # Create the Agent and assign it to the new variable
    globals()[var_name] = Agent(role=data["role"], goal=data["goal"])
    logger.info(f"Created agent: {var_name}")


# Define tasks for other agents
# ...

# # Combine agents and tasks into a Crew
# crew = Crew(
#     agents=[data_analyst, ...],  # Add all agents
#     tasks=[task_for_data_analyst, ...],  # Add tasks for all agents
#     process=Process.sequential,
# )

# # Kickoff the crew
# result = crew.kickoff()
# logging.info(f"Result of Crew execution: {result}")
