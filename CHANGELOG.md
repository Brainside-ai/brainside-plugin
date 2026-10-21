# Changelog

All changes to this plugin. Each release bumps `version` in `plugins/brainside/.claude-plugin/plugin.json`. The plugin is text that guides your AI, so read the entry before you update.

## Compatibility

| Plugin | Brainside server | How your AI saves |
|---|---|---|
| **0.2.0** | The release of 2026-10-21 (the second that day) or later | Proactive saving: saves new items on its own and tells you in one line. Asks before changing or deleting anything, and before saving setup, sensitive, external or client data |
| **0.1.1** | Servers before and after that release | Asks before every save |

Your server is ready for 0.2.0 when your AI's Brainside connector, on a connection that can save, lists the tool `answer_node_questions`. Brainside is hosted, so the server updates for every account at once. The connector address stays `https://api.brainside.ai/mcp` in every version.

## 0.2.0 — 2026-10-21

Proactive saving, for the Brainside server released on 2026-10-21 (the second release that day) or later. Update the plugin after that release is live.

### What changes for you

- **Proactive saving.** Your AI saves new durable knowledge on its own and tells you in one line what it saved and where: "Saved to your Brainside (<space>): …". That covers decisions and their reasons, new people, projects, commitments, events, facts that change something, preferences, links between items, additions that keep what an item already says, and records for your Apps. Small talk, lookups, logs and the conversation itself are saved only when you ask.
- **Still asks first** before changing or deleting anything; before setup (rules, agents, App manuals, new Apps or fields); and before saving sensitive data about you or anyone else, external content, or client and employer data. For client data it offers, in this order, the organization's space, your takeaway without names, e-mails or other identifiers, or not saving. It saves only the minimum and never bulk copies from their systems.
- **Nothing is overwritten by a save.** Saving only creates or adds. Changing an item takes a separate step that checks your AI read the latest version; if the item changed in between, nothing is saved and your AI reads it again.
- **Brainside asks when it isn't sure,** for example whether something is a new version of an existing note. What is certain is saved; your AI answers the question, asks you when the answer isn't obvious, and needs your yes before treating something as a new version. "Don't know" leaves the question waiting for you on the Brainside screen.
- **Deleting** sends the item to the Brainside trash, where you can restore it. Rules and agents are never deleted by your AI: the request waits for your approval in Brainside.
- **Your rules and agents.** Your AI reads your general rules once per conversation and follows the rules that apply to what it found. Rules and agents it saves are drafts until you activate them, and changes to active ones are proposals.
- **Your saving policy is editable.** The split above is a rule in your Brainside. Your version replaces the default; it can't remove the limits.
- **Apps** are found through search and opened like any other item, with their fields and manual. A new App or field is a proposal until you approve it on the Brainside screen.
- **Read-only connections.** If you chose read-only when you logged in, your AI only searches and reads.
- **Secrets:** still never stored. Brainside's server also refuses text that looks like a secret.
- If your AI's connector lists tools to save but not `answer_node_questions` yet, the skill falls back to asking before every save.

### What the skill expects from the server

- One way in for reading the memory (search, then open the item) and one for writing to it (save or add, link, answer Brainside's questions, change, delete): `search_nodes`, `get_node`, `list_nodes`, `upsert_node`, `link`, `answer_node_questions`, `update_node` and `delete_node`. The skill now names the tools by intent, as in the server's catalog.
- `list_apps`, `read_app_manual` and `get_app_schema` left the server: Apps are found through search, and `get_node` on an App gives its fields, manual and manual hash.
- The server's own instructions now say the same as the skill.

### Docs and repository

- README: what changes in your AI, a four-step "Try it", compatibility, what your AI can do once connected, read-only connections, **Settings › Connected AIs**, and two new FAQ entries about what your AI saves on its own.
- `INSTALL.md`: the server version this plugin needs, the save-or-read-only choice at login (the user decides), and nothing saved about the installation itself.
- **ChatGPT custom instructions changed:** paste the new block from `chatgpt/custom-instructions.md`.
- Examples and troubleshooting: proactive saving, client data with identifiers or copied from a client's system, changing a value, read-only connections, an older server, a save refused because of a secret.

## 0.1.1 — 2026-10-21

Saving becomes conservative until the next Brainside server release.

### What changes for you

- **Asks before every save.** Your AI offers to save in one line and saves only after your yes. Asking it to save ("save this") counts as the yes, except for client data. Why: on the current Brainside server, saving an item that already exists replaces the whole note with what is sent. Proactive saving arrives in 0.2.0.
- **No overwrites.** Your AI searches before saving something new. To change an item, it reads it first and sends the complete new version.
- **The skill's rules come first**, even when the connector's instructions or tool descriptions suggest installing templates, proposing Apps or saving without asking.
- **Your AI follows only you**, your active rules, and App manuals you approved or that Brainside wrote (including official verified templates). Everything else that comes back from Brainside is information, never an order.
- **Limits that no rule changes:** never store secrets; ask before changing or deleting anything, and before saving sensitive, external or client data; never install a template or propose an App unless you ask; send Brainside content only to a destination you asked for, never because a file, page or note asked for it, and never inside a URL.
- **Sensitive data** now covers anyone, not just you: health, genetic or biometric data, sex life, racial or ethnic origin, religion, political opinion, union membership, identity documents, bank accounts and cards.
- **Client and employer data:** your AI asks first and offers the organization's space, or your takeaway without names, before your personal space. The save notice names the space: "Saved to your Brainside (<space>): …".
- **Setup** (rules, agents, manuals, Apps, App fields) happens only when you ask. Brainside keeps it as a draft or proposal that you activate on the Brainside screen.
- Your AI no longer suggests on its own that something could become an App.
- When a tool asks where saved content came from, your AI answers truthfully: you, external content, or its own inference.

### Docs and repository

- New README, with the Brainside logo.
- `INSTALL.md`: each step says whether the AI runs it or asks you, and the AI checks where the file came from and shows each command before running it. Also: plan requirements for claude.ai, the current connector menu, the Codex CLI, desktop app and IDE extension apart, ChatGPT's @ menu, `/reload-plugins --force`, a connector added by hand taking precedence over the plugin's, and a complete uninstall for Codex.
- Troubleshooting: updates are manual, after reading this changelog. Auto-update is no longer described.
- `SECURITY.md`: how to report, what is in scope, what the plugin does not do, and how to check the official address.
- The ChatGPT custom instructions now match the skill.
- The skill no longer lists tool names; they come from the connector.
- The plugin's homepage now points to this repository's README.
- Validator and CI: files, manifest keys, addresses, commands and characters are checked against allowlists; a change to the plugin needs a new version; tagged releases attach the skill ZIP and its SHA-256.

## 0.1.0 — 2026-10-21

- First public release (beta).
- `brainside` skill: search Brainside before answering; save durable knowledge on its own and tell the user; ask before changing, deleting, touching rules, or saving sensitive or external content; never store secrets.
- MCP connector `https://api.brainside.ai/mcp` (HTTP + OAuth at brainside.ai).
- Equivalent text for ChatGPT's custom instructions.
- `INSTALL.md` written for AIs.
