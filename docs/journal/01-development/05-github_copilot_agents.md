# GitHub Copilot Agents 

The workflow is similar to how you would interact with a human developer (jokes, banter, and off-topic Slack conversations aside):

1. Create an issue, this should contain a lot more context because that's the prompt to the agent essentially.
2. Assign Copilot the issue and they will raise the pull request.
3. Make comments, do reviews, and then eventually get the PR merged. You can even add in some commits of your own. 

Each request only uses 1 premium request, so it's pretty good value actually.

## Use cases 

GitHub are pretty clear that it should be for _straightforward_ issues on the backlog. Nice to haves, documentation, and other small updates. Code refactors and adding logging are also some things that can be delegated to the coding agent. 

The whole idea is to parallelize yourself and offload these simpler tasks to the agent, freeing you up to focus on more complex and high-value work.

## Security

- Sandboxed environment
- Doesn't have access to all branches 
- Only responds to users with write permissions 
- It's an outside collaborator so GitHub Actions only run with approval, can't mark pull requests as ready for review, cannot approve or merge PRs.
- Tagged to the developer who assigned the issue, so they can't approve the same PR that Copilot Agent raised.
- GitHub has a firewall that is primarily for avoiding exfiltration due to malicious input.
- GitHub also filters out HTML comments in issues to avoid invisible text from being added to the prompt.

## Limitations 

- Only 1 PR and 1 repository at a time, and cannot join existing PRs.
- No commit signing
- Does not work with self-hosted GitHub Actions runners

## MCP Servers for the Coding Agent 

- Basically equips the agent with tools.
- By default, they have access to the GitHub and Playwright (primarily for testing apps on localhost, not for browsing the web).

## Customizations 

- [Adjust the firewall](https://github.com/tjpalanca/tjbots/settings/copilot/coding_agent) to allow the coding agent to access web resources.
- Pre-install environment
    - Copilot can figure it out through trial and error but it can be done
    - No sign of supporting devcontainers
- Add secrets or env vars 
    - Add a github actions variable in the `copilot` environment