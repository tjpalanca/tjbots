# Copilot Instructions for TJBots

## Overview

TJBots is a framework designed to explore the capabilities of Large Language Models (LLMs) by building experimental bots and tools. The project emphasizes rapid prototyping, configurability, and sharing findings with the community.

## Folder structure

- **Bots Application**: Located in `src/tjbots/app/`, the main entry point is `app.py`. This is the test harness application that allows us to test different configurations of bots and tools. 
- **Documentation**: Written in Quarto, located in `docs/`. Key files include `index.qmd` and notes under `docs/notes/`.
- **Tests**: Located in `tests/` mirroring the `src/` structure. Uses pytest with shared utilities in `test_utils.py`.

## Testing practices

- **Structure**: Mirror `src/` directory structure in `tests/`
- **Utilities**: Use `tests/tjbots/test_utils.py` for shared constants like `MOCK_ENV`
- **Environment**: Mock API keys with `@patch.dict(os.environ, MOCK_ENV)` for isolation

## Ways of working

- If you encounter something or make a mistake that requires an update to the general or specific Copilot instructions, suggest that change to the user so that you remember the next time. 
