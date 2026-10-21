<h1 align="center">Brainside</h1>

<p align="center">
  <strong>Your memory and your way of working, in any AI.</strong><br>
  Official <a href="https://www.brainside.ai">Brainside</a> plugin for Claude Code, claude.ai and Codex — and the equivalent for ChatGPT.
</p>

<p align="center">
  <a href="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue"></a>
  <img alt="Status: beta" src="https://img.shields.io/badge/status-beta-orange">
</p>

---

## Why it exists

Every new AI starts from zero. You explain again who is who, what you already decided, how you like things done — and when you switch tools, you lose it all again.

Brainside keeps that knowledge **once**, in your account, and hands it to **any AI you connect**. This plugin is the bridge: it teaches your AI to use Brainside on its own, without you having to say "save this" or "look that up".

## What changes in your AI

| Situation | What the AI does |
|---|---|
| You ask about your projects, people, clients or decisions | **Searches Brainside before answering** and says where the answer came from |
| You mention something worth keeping (a decision, a new person, a deadline) | **Saves it on its own and tells you in one line**: "Saved to your Brainside: …" |
| The change alters or deletes something that already exists, touches your rules, involves sensitive data or came from an external source (email, web page, someone else's file) | **Asks first** and only writes with your yes |
| A password, key or token shows up | **Never stores it**, even if you ask — and suggests a password manager |

Rules and manuals that **you** wrote or approved count as instructions. What comes from someone else (a template author, another member, imported content) reaches the AI as **information**, never as an order.

## How it works

```
  Your AI (Claude, Codex, ChatGPT…)
        │   "brainside" skill: when to search, when to save, when to ask
        │   MCP connector:     https://api.brainside.ai/mcp   (OAuth login at brainside.ai)
        ▼
  Brainside — stores, organizes, searches and delivers
        │
        └── the same memory in every AI you connect
```

Brainside **stores, organizes, searches and delivers**. **Your** AI reads, thinks and acts. Brainside does not run a language model over your knowledge to decide for you.

## Installation

> The official address is always **`brainside-ai/brainside-plugin`**. The GitHub organization `brainside` (without `-ai`) is not Brainside.

### Claude Code

```bash
claude plugin install brainside --marketplace brainside-ai/brainside-plugin
```

Then, in a session: `/mcp` › **Brainside** › **Authenticate**. Your browser opens the Brainside login; sign in and authorize.

### claude.ai (web, desktop and mobile)

1. **Customize › Plugins › Add › Add marketplace** and type `brainside-ai/brainside-plugin`.
2. Add the **Brainside** plugin.
3. In the plugin's **Connectors** tab, add Brainside and sign in to your account.

Skills need code execution turned on in the claude.ai settings. The Free plan allows one custom connector. What you install in claude.ai also shows up in Claude Code for anyone signed in with the same account.

### Codex

```bash
codex plugin marketplace add brainside-ai/brainside-plugin
```

Install it from `/plugins`. If the connector does not show up: `codex mcp add brainside --url https://api.brainside.ai/mcp` and `codex mcp login brainside`.

### ChatGPT

ChatGPT does not install plugins from a repository. Add the MCP server `https://api.brainside.ai/mcp` as a custom app and paste the text from [`chatgpt/custom-instructions.md`](chatgpt/custom-instructions.md) into the custom instructions.

### Let your AI install it

In Claude Code or Codex, you can ask the AI itself:

> Install Brainside following https://github.com/brainside-ai/brainside-plugin/blob/main/INSTALL.md

[`INSTALL.md`](INSTALL.md) is written for AIs: exact steps, what to check and where to stop and ask for your OK.

## First steps

Once connected, try this in a new conversation, without mentioning Brainside:

- "I met Ana, she's a designer at Acme and will take care of our website." → the AI saves it and tells you.
- "Who's in charge of the website again?" → the AI searches and answers with what you saved.
- "We decided to close the quarter with no new hires." → it becomes a decision linked to the project.
- "Delete Ana's note." → the AI asks for confirmation first.

In every connected AI, the same memory.

## Updates

Every change to this repository goes through a pull request with green CI, and each version is recorded in the [`CHANGELOG.md`](CHANGELOG.md).

- **Claude Code:** `claude plugin update brainside@brainside-ai`
- **Codex:** `codex plugin marketplace upgrade brainside-ai`
- **claude.ai:** when you add the marketplace, you choose whether it syncs on its own.

The plugin is just text, but it is text that guides your AI. That is why we recommend reading the changelog before updating.

## Privacy and security

- **The data travels, the power does not.** The plugin ships only the skill (text) and the connector address. It has no hooks, commands, agents or executables, and it does not run code on your machine.
- **You log in to Brainside, never to the AI.** The connection is made through OAuth on the Brainside page. No password, key or token goes through the conversation.
- **You control each connection.** In Brainside, under Settings › Connected AIs, you see which AIs have access, what each one can do, and you can revoke access at any time.
- **Check before installing:** the file [`plugins/brainside/.mcp.json`](plugins/brainside/.mcp.json) must point to `https://api.brainside.ai/mcp`.
- **Found a vulnerability?** See [`SECURITY.md`](SECURITY.md) — reports are private.

## Troubleshooting

The AI cannot find the Brainside tools, the login expired, the connector does not show up: see the [troubleshooting guide](plugins/brainside/skills/brainside/references/troubleshooting.md) or [brainside.ai/instalar](https://www.brainside.ai/instalar).

## Structure

```
.claude-plugin/marketplace.json          catalog (Claude Code, claude.ai and Codex read the same format)
plugins/brainside/.claude-plugin/plugin.json
plugins/brainside/.mcp.json              MCP connector (HTTP + OAuth)
plugins/brainside/skills/brainside/      the skill: SKILL.md and references
chatgpt/custom-instructions.md           equivalent text for ChatGPT
INSTALL.md                               installation written for AIs
```

## For maintainers

- Each release bumps `version` in `plugins/brainside/.claude-plugin/plugin.json` (only there, never also in `marketplace.json`) and gets an entry in `CHANGELOG.md`.
- Validation: `python3 .github/scripts/validate.py` (the same as CI) and, with Claude Code, `claude plugin validate .`.
- CI builds `dist/brainside-skill.zip`, the skill ZIP for upload at claude.ai › Customize › Skills.
- The `main` branch is protected: changes only land through a pull request with review and green CI.

## License

[Apache-2.0](LICENSE). The license grants no rights to the Brainside trademark.
