OPENAI_MODEL_TASKS: str = "gpt-4-1106-preview"
PROMPT_DEFINE_TASKS: str = "The overall task for this team to comlpete is the following {task_description}. The team is composed of the following agents {agents_description}. Think carefully and define the tasks for each agent. You do not need to use all agents at all steps. You will ask for confirmation for every step of the process.\nYou will answer in JSON."
SYSTEM_PROMPT_DEFINE_TASKS: str = "You are capable of defining tasks for each agent."
