import instructor
from openai import OpenAI

from pydantic import BaseModel
import logging
import os 
from dotenv import load_dotenv

import yaml
import config 

load_dotenv()

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Agent(BaseModel):
    role: str
    goal: str
    backstory: str
    verbose: bool
    allow_delegation: bool
    tools: list
    agent_name: str   

class Task(BaseModel):
    description: str
    agent: Agent

# setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# patch OpenAI client with instructor
client = instructor.patch(client)

def get_model_name():
    if not config.OPENAI_MODEL_TASKS:
        raise ValueError("OPENAI_MODEL_TASKS is not set in config.py")
    model_lst = client.models.list()
    for model_name in model_lst:
        if model_name.id == config.OPENAI_MODEL_TASKS:
            print(f"Selected model for tasks definition: {model_name.id}")
            return config.OPENAI_MODEL_TASKS
    raise ValueError(f"{config.OPENAI_MODEL_TASKS} is not a valid model. Valid models are: {model_lst}")

# open agents.yaml to ensure it is valid yaml
with open("agents.yaml") as file:
    agents_data = yaml.safe_load(file)
    agents_description = yaml.dump(agents_data)

logger.info(f"Loaded {len(agents_data['agents'])} agents.")
# task_description = input("Please describe the task: ")

task_description = " We want to define which micro tasks of the gig economy can be replaced, concretely and practically, exploring all aspects of the question"

model = get_model_name()

prompt_define_tasks = config.PROMPT_DEFINE_TASKS.format(task_description=task_description, agents_description=agents_description)
system_define_tasks = config.SYSTEM_PROMPT_DEFINE_TASKS
messages = [
    {"role": "system", "content": system_define_tasks},
    {"role": "user", "content": prompt_define_tasks},
]

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=4096,
    n=1,
    response_model=Task, 
    response_format={"type": "text"},
    stop=None,
)

print(completion)


