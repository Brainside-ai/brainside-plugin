# Security

## How to report a vulnerability

Do not open a public issue for a security problem.

1. Use GitHub's private reporting: the **Security** tab › **Report a vulnerability** in this repository.
2. Or email **suporte@brainside.ai** with a subject starting with `[security]`.

Include what is needed to reproduce it: steps, the plugin version (`version` in `plugins/brainside/.claude-plugin/plugin.json`), the AI client and its version. Do not include passwords, tokens or other people's personal data. Do not access, change or delete other people's data to prove the issue.

## What is in scope

- This repository: the skill and its references, the ChatGPT custom instructions, `INSTALL.md`, the manifests (`marketplace.json`, `plugin.json`) and `.mcp.json`.
- The Brainside MCP server (`https://api.brainside.ai/mcp`), the OAuth login at brainside.ai, and file uploads to `api.brainside.ai` (the one-time upload link and the upload page).
- Copies that pose as this plugin: a repository, page or package that claims to be the official Brainside plugin or points an AI to another Brainside address.

Of particular interest: text that leads the AI to act against the user or to send the user's Brainside content somewhere they did not ask for, a swapped MCP address, a flaw in login or consent, access to another account's data, and storing of secrets.

## What the plugin does not do

The plugin is only text and one address: the `brainside` skill (Markdown files) and the connector address `https://api.brainside.ai/mcp`.

- It has no hooks, commands, agents, monitors, scripts or executables. It runs no code on your machine.
- When you ask your AI to keep a file, the skill asks it to run one command, `curl`, which sends that file to Brainside with a one-time upload code for that file only. Your AI client runs it under its own permissions. The skill tells the AI to change only the file's path in that command, never the address or the headers, and never to save the code or put it in a link.
- It never handles your password. You log in on the Brainside page, through OAuth.
- The skill tells the AI to treat what comes back from Brainside as data, never as orders; to send Brainside content only where you ask; and never to store a password, token or key.

## Check the official address

- The repository is `github.com/brainside-ai/brainside-plugin`. The GitHub organization `brainside` (without `-ai`) is not Brainside.
- `plugins/brainside/.mcp.json` must contain exactly one server, of type `http`, at `https://api.brainside.ai/mcp`.
- In Claude Code, `claude plugin marketplace list` must show the `brainside-ai` marketplace with the source `brainside-ai/brainside-plugin`.
- The install guide on the Brainside site, https://www.brainside.ai/instalar, points to this same repository.
