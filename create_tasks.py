import logging
import os

import instructor
import yaml
from dotenv import load_dotenv
from openai import OpenAI

import config
from models import AgentsList, TasksList

load_dotenv()

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# patch OpenAI client with instructor
client = instructor.patch(client)


def get_model_name() -> str:
    if not config.OPENAI_MODEL_TASKS:
        raise ValueError("OPENAI_MODEL_TASKS is not set in config.py")
    model_lst = client.models.list()
    for model_name in model_lst:
        if model_name.id == config.OPENAI_MODEL_TASKS:
            logger.info(f"Selected model for tasks definition: {model_name.id}")
            return config.OPENAI_MODEL_TASKS
    raise ValueError(
        f"{config.OPENAI_MODEL_TASKS} is not a valid model. Valid models are: {model_lst}"
    )


# open agents.yaml to ensure it is valid yaml
with open("agents.yaml") as file:
    agents_data = yaml.safe_load(file)
    agents_description = yaml.dump(agents_data)

agent_list = AgentsList(agents=agents_data["agents"])

logger.info(f"Loaded {len(agents_data['agents'])} agents.")
# task_description = input("Please describe the task: ")

task_description = "We want to define which micro tasks of the gig economy can be replaced, concretely and practically, exploring all aspects of the question, and how to do it concretely and practically."

model = get_model_name()

prompt_define_tasks = config.PROMPT_DEFINE_TASKS.format(
    task_description=task_description, agents_description=agents_description
)
system_define_tasks = config.SYSTEM_PROMPT_DEFINE_TASKS
messages = [
    {"role": "system", "content": system_define_tasks},
    {"role": "user", "content": prompt_define_tasks},
]

logger.info("Sending prompt to OpenAI API...")
results = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=4096,
    n=1,
    response_model=TasksList,
    response_format={"type": "json_object"},
    stop=None,
)

list_of_tasks = TasksList(tasks=results.tasks)

# for n, task in enumerate(list_of_tasks.tasks):
#     logger.info(f"Task %s", n + 1)
#     logger.info("")
#     logger.info(f"Description: %s", task['agent_name'])
#     # logger.info(f"Agent Name: {task.['task']}")
#     logger.info("")

# save tasks to yaml file 'tasks.yaml'
if isinstance(list_of_tasks, TasksList):
    with open("tasks.yaml", "w") as file:
        yaml.dump(list_of_tasks.model_dump(), file)
        logger.info("Saved tasks to tasks.yaml")
else:
    raise ValueError("list_of_tasks is not an instance of TasksList")
