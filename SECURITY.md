# Security

## How to report a vulnerability

Do not open a public issue for a security problem.

1. Use GitHub's private reporting: the **Security** tab › **Report a vulnerability** in this repository.
2. Or email **suporte@brainside.ai** with a subject starting with `[security]`.

Include what is needed to reproduce it: steps, the plugin version (`version` in `plugins/brainside/.claude-plugin/plugin.json`), the AI client and its version. Do not include passwords, tokens or other people's personal data. Do not access, change or delete other people's data to prove the issue.

We reply through the same channel and let you know when the fix ships.

## What is in scope

- This repository: the skill text, the manifests (`marketplace.json`, `plugin.json`) and `.mcp.json`.
- The Brainside MCP server (`https://api.brainside.ai/mcp`) and the OAuth login at brainside.ai.

Of particular interest: skill text that leads the AI to act against the user, a swapped MCP address, a flaw in login or consent, access to another account's data, and storing of secrets.

## How the plugin protects itself

- Only text and one address: no hooks, agents, commands or executables. CI rejects any of them.
- CI also rejects a `.mcp.json` that points to any address other than `https://api.brainside.ai/mcp`.
- What comes back from Brainside is treated as data: the skill tells the AI not to follow instructions found in notes, emails or pages.
- The skill says never to store a password, token or key.

The `main` branch is protected and every change goes through a PR with review.

## Check before installing

The MCP address in `plugins/brainside/.mcp.json` must be `https://api.brainside.ai/mcp`, and the repository must be `brainside-ai/brainside-plugin`. The GitHub organization `brainside` (without `-ai`) is not Brainside.
