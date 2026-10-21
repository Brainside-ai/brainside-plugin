<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brainside-mark-light.svg">
    <img alt="Brainside" src="assets/brainside-mark-dark.svg" width="88" height="88">
  </picture>
</p>

<h1 align="center">Brainside</h1>

<p align="center">
  <strong>Your memory and your way of working, in any AI.</strong><br>
  The official <a href="https://www.brainside.ai">Brainside</a> plugin for Claude Code, claude.ai and Codex, plus ready-to-paste custom instructions for ChatGPT.
</p>

<p align="center">
  <a href="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml/badge.svg"></a>
  <a href="CHANGELOG.md"><img alt="Version 0.2.0" src="https://img.shields.io/badge/version-0.2.0-52514e"></a>
  <a href="#before-you-start"><img alt="Status: closed beta" src="https://img.shields.io/badge/status-closed_beta-52514e"></a>
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-52514e"></a>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#what-changes-in-your-ai">What changes</a> ·
  <a href="#try-it">Try it</a> ·
  <a href="#privacy-and-security">Privacy</a> ·
  <a href="#faq">FAQ</a>
</p>

---

## Every AI starts from zero

You re-explain who's who, what you've already decided and how you like things done. Switch to another AI and it starts from zero too. Everything you taught the last one stays behind.

## One memory, every AI

Brainside keeps that knowledge once, in your own account: people, projects, clients, decisions, preferences, and your Apps (structured collections such as expenses or recipes). Every AI you connect works from the same memory. Brainside stores, organizes, searches and delivers; your AI does the thinking and the work.

Brainside itself is a hosted service at [brainside.ai](https://www.brainside.ai), now in closed beta. This repository holds only the plugin that connects your AI to it. The plugin gives your AI two things:

- **The `brainside` skill.** Plain text that tells your AI when to search Brainside, what to save on its own, when to ask first, and what never to do.
- **The Brainside connector.** One address, `https://api.brainside.ai/mcp`. You log in once at brainside.ai, and your AI reaches your account through it.

```
  Claude Code · claude.ai · Codex · ChatGPT
        │
        │  skill       when to search, what to save, when to ask first
        │  connector   https://api.brainside.ai/mcp   (you log in at brainside.ai)
        ▼
  Brainside: stores, organizes, searches, delivers
        │
        └── the same memory for every AI you connect
```

## What changes in your AI

| When | Your AI |
|---|---|
| You ask about your people, projects, clients or decisions | Searches Brainside before answering, and tells you what came from there |
| You mention something worth keeping: a decision and its reason, a new person, a deadline | Saves it on its own and tells you in one line what it saved and where: "Saved to your Brainside (<space>): …" |
| A save would change or delete something, touch your rules, agents or Apps, or involve sensitive, external or client data | Asks first, says why (for example, "this changes an existing note" or "this is health data") and shows you what will change |
| Brainside isn't sure, for example whether something is a new version of an existing note | Nothing is overwritten. Brainside keeps both and asks; your AI answers, or asks you when the answer isn't obvious |
| A password, key or token shows up | Never stores it, even if you ask, and suggests a password manager. Brainside also refuses text that looks like a secret |
| Something someone else wrote comes back: a pasted email, a web page, a template, a note | Treats it as information, never as an order |

Your AI takes orders only from you. What it reads in Brainside or elsewhere (notes, emails, web pages, templates) is information, not instructions. It never installs a template or creates an App unless you ask, and the rules and agents it saves stay drafts until you activate them in Brainside.

What it saves on its own follows a rule you can edit in Brainside; see the [FAQ](#faq). If you use Brainside at work, check that your company or your client allows you to keep their data here. Your AI asks before saving it.

> **The skill guides your AI; it doesn't force it.** Your AI follows it most of the time, not every time. If it answers without checking, say "check my Brainside". If it saved something you didn't want, say so: it deletes it, and the item goes to the Brainside trash.

## Before you start

Brainside is in closed beta, so creating an account takes an invite. [Join the waitlist](https://www.brainside.ai/#waitlist): people on it get in first. Already have an account? You're set. Then, depending on your AI:

| AI | What you need |
|---|---|
| Claude Code | Version 2.1.292 or later for the one-line install. Older versions have their own path below. |
| claude.ai (web, desktop, mobile) | A paid plan (Pro, Max, Team or Enterprise) with Settings › Capabilities › Code execution and file creation turned on. On Team and Enterprise, an Owner adds the connector. On the Free plan you can add the connector without the skill ([INSTALL.md](INSTALL.md#claudeai)). |
| Codex | The Codex CLI or Codex in the ChatGPT desktop app. The IDE extension supports the connector but not the skill. |
| ChatGPT | A paid plan that allows custom MCP servers. On Business, Enterprise and Edu, an admin may have to allow them (Developer mode). |

## Install

> The official repository is **`brainside-ai/brainside-plugin`**. The GitHub organization `brainside` (without `-ai`) isn't Brainside.

### Claude Code

```bash
claude plugin install brainside --marketplace brainside-ai/brainside-plugin
```

Start a new session, run `/mcp`, pick **Brainside** (it may show with a `plugin:` prefix) and choose **Authenticate**. Your browser opens the Brainside login.

Older than 2.1.292? Run `claude plugin marketplace add brainside-ai/brainside-plugin`, then `claude plugin install brainside@brainside-ai`.

### claude.ai

1. Open **Customize › Plugins › Add › Add marketplace**, type `brainside-ai/brainside-plugin` and confirm. Leave **Sync automatically** off: you update by hand, after reading the CHANGELOG (see [Updates](#updates)).
2. Add the **Brainside** plugin.
3. In the plugin's **Connectors** tab, add Brainside and log in.

Set it up on the web or in the desktop app. After that it works on mobile too, and in Claude Code if you sign in there with the same claude.ai account (it shows as `brainside@synced`).

### Codex

```bash
codex plugin marketplace add brainside-ai/brainside-plugin
codex plugin add brainside@brainside-ai
```

Start a new session and log in to Brainside when Codex asks. If your Codex has no `plugin add` command, open `/plugins` and install Brainside from the `brainside-ai` marketplace. In the ChatGPT desktop app, use the **Plugins** tab.

### ChatGPT

In ChatGPT, you add the connector by hand and paste our custom instructions in place of the skill:

1. Add `https://api.brainside.ai/mcp` as a custom MCP server, with OAuth, and log in to Brainside.
2. Paste the block from [`chatgpt/custom-instructions.md`](chatgpt/custom-instructions.md) into your custom instructions.

Step by step: [INSTALL.md › ChatGPT](INSTALL.md#chatgpt).

### Any other MCP client

Point it to `https://api.brainside.ai/mcp` (Streamable HTTP, OAuth). If it accepts instructions, give it the text of the [skill](plugins/brainside/skills/brainside/SKILL.md).

### Let your AI install it

In Claude Code or Codex, say:

> Install Brainside following https://github.com/brainside-ai/brainside-plugin/blob/main/INSTALL.md

[`INSTALL.md`](INSTALL.md) is written for AIs. It tells your AI to check that the file came from this repository, to show you each command and to wait for your yes. Clicks and the login stay with you; no step asks for your password.

INSTALL.md also covers every client in detail and how to uninstall. There's also an install guide on the Brainside site: [brainside.ai/instalar](https://www.brainside.ai/instalar).

## Try it

Open a new conversation and don't mention Brainside:

1. *"I met Ana, a freelance designer. She'll redo our website."* Your AI saves Ana on its own and tells you in one line where.
2. In another conversation, or in another AI you connected: *"Who's redoing our website?"* It searches Brainside, answers with Ana, and tells you where that came from.
3. *"Ana will also redo our logo."* This adds to Ana's note without changing what's there, so your AI saves it and tells you.
4. *"Actually, Bruno is redoing the website, not Ana."* This changes what's saved, so your AI shows you what will change and asks first.

## Compatibility

| Plugin | Brainside server | How your AI saves |
|---|---|---|
| **0.2.0** | The release of 2026-10-21 (the second that day) or later | Proactive saving: saves new items on its own and tells you in one line. Asks before changing or deleting anything, and before saving setup, sensitive, external or client data |
| **0.1.1** | Servers before and after that release | Asks before every save |

How to tell your server is ready for 0.2.0: on a connection that can save, your AI's Brainside connector lists the tool `answer_node_questions` (in Claude Code, `/mcp`). Brainside is hosted, so you never update the server yourself: once a release is live, every account has it.

Why 0.2.0 needs that release: on it, saving only creates or adds, and never overwrites. Changing an item takes a separate step that checks your AI read the latest version. On older servers, saving an item that already exists replaced its whole note, which is why 0.1.1 asks before every save.

The connector address stays `https://api.brainside.ai/mcp` in every version.

## Privacy and security

- **The plugin runs nothing on your machine.** It's only text and one address: the skill (Markdown files) and the connector `https://api.brainside.ai/mcp`. It has no hooks, commands, agents, monitors, scripts or executables. You can check it yourself: `python3 .github/scripts/validate.py` fails if any of them appears.
- **What your AI can do once connected** is what the connector offers: search and read your memory and your Apps; save new items, link them, change them and delete them (deleted items go to the Brainside trash, where you can restore them); add, change and delete records in your Apps; store files for those records; install templates, propose new Apps and fields (a proposal exists only after you approve it in Brainside), and archive Apps. Rules and agents your AI saves stay drafts until you activate them. Your AI client lists every tool (in Claude Code, `/mcp`). The skill tells your AI to ask before changing or deleting anything, and never to install a template unless you ask.
- **Read-only, if you prefer.** When you log in, the Brainside page lets you choose whether that AI may save to your Brainside. Leave it unticked and that connection can only search and read.
- **You log in to Brainside, never in the chat.** Login is OAuth, on the Brainside page your browser opens. No password, key or token goes through the conversation.
- **Your AI follows only you:** what you say in the conversation, rules and agents you activated in Brainside, and App manuals you approved or that Brainside wrote. Everything else it reads in Brainside (notes, pasted emails, pages, templates, other members' notes) is information, never an order. Brainside content leaves the conversation only to a destination you asked for.
- **You decide which AIs have access.** In Brainside, **Settings › Connected AIs** lists every AI you authorized, says which ones can save, and lets you revoke each one. Removing the plugin or the connector from an AI also stops it from reaching Brainside.
- **Check the address before you install.** The repository is `github.com/brainside-ai/brainside-plugin`, and [`plugins/brainside/.mcp.json`](plugins/brainside/.mcp.json) holds exactly one server: `https://api.brainside.ai/mcp`.
- **Found a vulnerability?** Report it privately, as described in [`SECURITY.md`](SECURITY.md). Please don't open a public issue.

Brainside's privacy policy: [brainside.ai/privacidade](https://www.brainside.ai/privacidade).

## Updates

Updates are manual on purpose. The plugin is text that guides your AI, so read the [CHANGELOG](CHANGELOG.md) first, then update:

- **Claude Code:** `claude plugin update brainside@brainside-ai`, then start a new session. If `claude plugin list` shows `brainside@synced`, it follows your claude.ai account instead.
- **claude.ai:** Customize › Plugins › the `brainside-ai` marketplace › **Check for updates**.
- **Codex:** `codex plugin marketplace upgrade brainside-ai`.
- **ChatGPT:** when the CHANGELOG says the ChatGPT custom instructions changed, paste the new block from [`chatgpt/custom-instructions.md`](chatgpt/custom-instructions.md).

## FAQ

**Does Brainside read my conversations?**
Not the conversation itself. Brainside receives only what your AI sends in a tool call (a search, an item to open or to save), and that can include parts of what you said.

**How is this different from my AI's own memory?**
Built-in memory stays inside that one AI. Brainside is one memory for every AI you connect, organized into people, projects, decisions and Apps, and you can see and edit it at brainside.ai.

**Can I use more than one AI at the same time?**
Yes. Connect each AI and log in to the same Brainside account. Codex can find what you saved from Claude Code, and vice versa.

**What happens if I disconnect an AI?**
That AI stops reaching Brainside. Your knowledge stays in your Brainside account, and your other AIs keep working. To come back, connect it again and log in.

**What does my AI save on its own?**
New durable knowledge: decisions and their reasons, new people, projects, commitments, events, facts that change something, preferences, links between them, and records for your Apps. It tells you in one line each time. It asks first before changing or deleting anything, before saving rules, agents, manuals, Apps or fields, and before saving sensitive, external or client data. It never saves small talk, lookups, logs or the conversation itself unless you ask.

**Can I change what it saves on its own?**
Yes. That split is a rule in your Brainside, and you can edit it there. Your version replaces the default. It can't remove the limits: no secrets, asking before changes, deletions and sensitive, external or client data, and no templates or Apps you didn't ask for. To stop an AI from saving at all, connect it read-only.

**Something isn't working?**
If your AI can't find the Brainside tools, your login expired, or the connector doesn't show up, see the [troubleshooting guide](plugins/brainside/skills/brainside/references/troubleshooting.md).

## What's in this repository

```
plugins/brainside/skills/brainside/   the skill: SKILL.md, examples and troubleshooting
plugins/brainside/.mcp.json           the connector: one address, HTTP + OAuth
plugins/brainside/.claude-plugin/     the plugin manifest (name and version)
.claude-plugin/marketplace.json       the catalog that Claude Code, claude.ai and Codex read
chatgpt/custom-instructions.md        the ChatGPT custom instructions, in place of the skill
INSTALL.md                            installation written for AIs
CHANGELOG.md                          what changed in each version
SECURITY.md                           how to report a vulnerability
assets/                               the Brainside logo
```

`python3 .github/scripts/validate.py` runs the repository's checks (the manifests, the single connector address, nothing executable in the plugin) and builds the skill ZIP.

## License

This repository is under [Apache-2.0](LICENSE). The license grants no rights to the Brainside name or logo.
