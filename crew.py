import logging

from crewai import Agent, Crew, Process, Task

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define tools
from tools import code_interpreter_tool

# Define the Data Analyst agent
data_analyst = Agent(
    role="Data Analyst",
    goal="Analyze trends in gig economy data to identify in-demand skills on platforms like Fiverr",
    tools=[code_interpreter_tool],
    allow_delegation=True,
)

# Define other agents with their respective roles, goals, and tools
# ...

# Define tasks for each agent
task_for_data_analyst = Task(
    description="Analyze gig economy data to identify trends and in-demand skills on Fiverr",
    agent=data_analyst,
)

# Define tasks for other agents
# ...

# Combine agents and tasks into a Crew
crew = Crew(
    agents=[data_analyst, ...],  # Add all agents
    tasks=[task_for_data_analyst, ...],  # Add tasks for all agents
    process=Process.sequential,
)

# Kickoff the crew
result = crew.kickoff()
logging.info(f"Result of Crew execution: {result}")
