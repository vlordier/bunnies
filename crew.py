import logging

import yaml
from crewai import Agent, Task, Crew, Process
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
        Agent(
                role=data["role"],
                goal=data["goal"],
                backstory=data["backstory"],
                verbose=True,
                allow_delegation=True,
                tools=tools,
            ),
    )
    logger.info(f"Created agent with role: {data['role']}")


logger.info(f"Loaded {len(agents_list)} agents.")

tasks_yaml_file = "tasks.yaml"
tasks_list = []
with open(tasks_yaml_file) as file:
    tasks_data = yaml.safe_load(file)
    for data in tasks_data["tasks"]:
        # find in agents_list the agent with the same name as the task in agent_name
        for agent in agents_list:
            if agent.role == data["agent_name"]:
                agent = globals()[data["agent_name"]]
                # data["agent"] = agent
        print(agent)
        # agent = next(agent for agent in agents_list if agent.role == data["agent_name"])
        tasks_list.append(Task(description=data["task"], agent=agent))


# Combine agents and tasks into a Crew
crew = Crew(
    agents=agents_list,
    tasks=tasks_list,  # Add tasks for all agents
    process=Process.sequential,
)

logger.info(f"Created Crew with {len(crew.agents)} agents and {len(crew.tasks)} tasks.")
# Kickoff the crew
logger.info("Starting Crew execution")
try:
    result = crew.kickoff()
    logger.info(f"Result of Crew execution: {result}")
except Exception as e:
    logger.error(f"Crew execution failed with error: {e}")
