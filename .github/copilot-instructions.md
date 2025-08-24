# Agent Instructions for TJBots

## Overview

TJBots is a framework designed to explore the capabilities of Large Language Models (LLMs) by building experimental bots and tools. The project emphasizes rapid prototyping, configurability, and sharing findings with the community.

## Development

- **Devcontainer**: This project runs inside a devcontainer. You'll have to ask the user to first make modifications to the `devcontainer.json` and then rebuild the container in order to make system dependency changes. 
- **uv** - this project uses uv to manage its environment. Remember that you'll need to do `uv run` if running anything inside the terminal.

## Folder structure

- **Bots Application**: Located in `src/tjbots/app/`, the main entry point is `app.py`. This is the test harness application that allows us to test different configurations of bots and tools. 
- **Documentation**: Written in Quarto, located in `docs/`. Key files include `index.qmd` and notes under `docs/notes/`.
- **Tests**: Located in `tests/` mirroring the `src/` structure. Uses pytest with shared utilities in `test_utils.py`.

## Testing practices

- **Structure**: Mirror `src/` directory structure in `tests/`
- **Utilities**: Use `tests/tjbots/test_utils.py` for shared constants like `MOCK_ENV`
- **Environment**: Mock API keys with `@patch.dict(os.environ, MOCK_ENV)` for isolation

## General guidelines

- If you encounter something or make a mistake that requires an update to the general or specific Copilot instructions, suggest that change to the user so that you remember the next time. 
- I will generally be logging my development progress in a quarto document in `docs/notes/01-development`. Check the latest file there if you want to know about the progress of development.
