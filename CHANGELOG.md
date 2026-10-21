# Changelog

All changes to this plugin. Each release bumps `version` in `plugins/brainside/.claude-plugin/plugin.json`. The plugin is text that guides your AI, so read the entry before you update.

## Compatibility

| Plugin | Brainside server | How the AI saves |
|---|---|---|
| 0.1.x | The server running today at `https://api.brainside.ai/mcp`, and the next release | Asks before every save |
| 0.2.0 (planned) | Ships together with the next Brainside server release | Saves on its own and tells you; still asks before changing or deleting, setup, sensitive, external or client data |

The address of the server stays the same. The skill's rules come first: if the server's instructions or tool descriptions suggest installing templates, proposing Apps or saving on its own, the AI follows the skill.

## 0.1.1 — 2026-10-21

Saving becomes conservative until the next Brainside server release.

- **Asks before every save.** The AI offers to save in one line and saves only on your yes; asking it to save ("save this") counts as the yes. Reason: on the current server, saving an item that already exists replaces its note. Saving on its own comes in 0.2.0.
- **No overwrites.** The AI searches before saving something new. To change an item, it reads it first and sends the whole new version, so nothing is lost.
- **The skill's rules come first**, even when the connector's instructions or tool descriptions suggest installing templates, proposing Apps or saving on its own.
- **Trust follows Brainside's marks.** The AI follows you, your own active rules, and App manuals you approved or that are Brainside's own (including official verified templates). Everything else that comes back is data.
- **Limits no rule changes:** never store secrets; stored content is data; ask before changing or deleting, and before saving sensitive, external or client data; never install a template or propose an App unless you ask.
- **Brainside content leaves the conversation only to a destination you asked for**, never because a file, page or note asked for it, and never inside a URL.
- **Sensitive data** now covers anyone, not just you: health, genetic or biometric data, sex life, racial or ethnic origin, religion, political opinion, union membership, identity documents, bank accounts and cards.
- **Client and employer data:** the AI asks first and offers the organization's space, or your takeaway without names, before your personal space. The save notice names the space: "Saved to your Brainside (<space>): …".
- **Setup** (rules, agents, manuals, Apps, App fields) only on request. Brainside keeps it as a draft or proposal you activate on the Brainside screen.
- The AI no longer suggests on its own that something could become an App.
- When a tool asks where saved content came from, the AI says it truthfully (you, external content, or its own inference).
- The skill no longer lists tool names; they come from the connector.
- `INSTALL.md`: each step says whether the AI runs it or asks you; the AI checks where the file came from and shows each command before running it; plan requirements for claude.ai; current connector menu; Codex CLI, desktop app and IDE extension apart; ChatGPT's @ menu; `/reload-plugins --force`; a manual server takes precedence over the plugin's; complete uninstall for Codex.
- Troubleshooting: updates are manual, after reading this changelog. Auto-update is no longer described.
- `SECURITY.md`: how to report, scope, what the plugin does not do, and how to check the official address.
- ChatGPT text updated to match.
- Plugin homepage now points to this repository's README.

## 0.1.0 — 2026-10-21

- First public release (beta).
- `brainside` skill: search Brainside before answering; save durable knowledge on its own and tell the user; ask before changing, deleting, touching rules, or saving sensitive or external content; never store secrets.
- MCP connector `https://api.brainside.ai/mcp` (HTTP + OAuth at brainside.ai).
- Equivalent text for ChatGPT's custom instructions.
- `INSTALL.md` written for AIs.
