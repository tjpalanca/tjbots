# Agent Instructions for TJBots

## Overview

TJBots is a project for exploring the capabilities of Large Language Models (LLMs) by building experimental bots and tools. The project emphasizes rapid prototyping, configurability, and sharing findings with the community.

## General guidelines

- Unless explicitly instructed, do NOT write any code until the user permits it. The first step is to understand the requirements, gather ncessary information, and agree on an approach.
- Suggest changes to the Copilot instructions if there are inconsitencies between these instructions and what you were told by the user.
- Check the development log for recently edited files to catch up on progress, if you have questions about what's been done so far.

## Development

- **Devcontainer**: This project runs inside a devcontainer. You'll have to ask the user to first make modifications to the `devcontainer.json` and then rebuild the container in order to make system dependency changes. 
- **uv** - this project uses uv to manage its environment. Remember that you'll need to do `uv run` if running anything inside the terminal.

## Folder structure

- **Bots Application**: Located in `src/tjbots/app/`, the main entry point is `app.py`. This is the test harness application that allows us to test different configurations of bots and tools. 
- **Documentation**: Written in Quarto, located in `docs/`. 
    - `docs/developer` includes any developer documentation
    - `docs/journal` is a development log basically
    - `docs/scenarios` contains use cases that are explored 
- **Tests**: Located in `tests/` mirroring the `src/` structure. 

## Documentation guidelines 

These guidelines cover documenting things in the development journals, but also documenting functions and modules via docstrings.

- **Google-Style**: Use Google-style docstrings for all public modules, functions, and classes.
- **Clarity**: Write clear and concise documentation. Write the high-level intent rather than explaining the code in detail.
- **DRY**: Don't document configuration that is likely to change, instead write a reference to that file.