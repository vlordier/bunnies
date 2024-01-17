# Bunnies
## Let glittery pink bunnies to amazing work

<div align="center">
  <img src="assets/bunnies.png" alt="Bunnies Image" width="300" height="300">
</div>

## Install Aider from git
`python -m pip install git+https://github.com/paul-gauthier/aider.git`

## Use GPT to improve Crew `yaml`

Feed the YAML `agents.yaml` to GPT and prompt it for better definitions for team consistency, tools and more.

##  Use GPT to define and plan first tasks

Set `OPENAI_API_KEY` using a `.env` or `export OPENAI_API_KEY=key`
Run `python create_tasks.py`

## Run your Crew of Bunnies

To use tools like [Google Search from langchain](https://python.langchain.com/docs/integrations/tools/google_serper), set `SERPER_API_KEY` from an account in [https://serper.dev/](https://serper.dev/)

Then run `python crew.py`

##  Maintain and clean

Setup and run `pre-commit` from the `.pre-commit-config.yaml` config
