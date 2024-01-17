import logging

import yaml
from crewai import Agent, Task, Crew, Process
from langchain.agents import Tool
from langchain.utilities import GoogleSerperAPIWrapper
from tools import code_interpreter_tool, google_search_tool


# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


agent_yaml_file = "agents.yaml"

with open(agent_yaml_file) as file:
    agents_data = yaml.safe_load(file)

tools = [google_search_tool, code_interpreter_tool]

agents_list = []
for data in agents_data["agents"]:
    # Create a variable name by replacing spaces in the role with underscores and prefixing with 'agent_'
    var_name = "agent_" + data["role"].replace(" ", "_").lower()
    # Create the Agent and assign it to the new variable
    agents_list.append(
        {
            "agent_name": var_name,
            "agent": Agent(
                role=data["role"],
                goal=data["goal"],
                backstory=data["backstory"],
                verbose=True,
                allow_delegation=True,
                tools=tools,
            ),
        }
    )
    # globals()[var_name] = Agent(
    #     role=data["role"],
    #     goal=data["goal"],
    #     backstory=data["backstory"],
    #     verbose=True,
    #     allow_delegation=True,
    #     tools=[google_search_tool],
    # )
    logger.info(f"Created {var_name}")


logger.info(f"Loaded {len(agents_list)} agents.")

tasks_yaml_file = "tasks.yaml"
tasks_list = []
with open(tasks_yaml_file) as file:
    tasks_data = yaml.safe_load(file)
    for data in tasks_data["tasks"]:
        # find in agents_list the agent with the same name as the task in agent_name
        agent = next(
            item for item in agents_list if item["agent_name"] == data["agent_name"]
        )  
        tasks_list.append(Task(description=data["task"], agent=agent))


# Combine agents and tasks into a Crew
crew = Crew(
    agents=agents_list,
    tasks=tasks_list,  # Add tasks for all agents
    process=Process.sequential,
)

logger.info(f"Created Crew with {len(crew.agents)} agents and {len(crew.tasks)} tasks.")
# Kickoff the crew
logging.info("Starting Crew execution")
result = crew.kickoff()
logger.info(f"Result of Crew execution: {result}")
