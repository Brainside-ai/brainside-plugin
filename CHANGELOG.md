# Changelog

All changes to this plugin. Each release bumps `version` in `plugins/brainside/.claude-plugin/plugin.json`. The plugin is text that guides your AI, so read the entry before you update.

## Compatibility

| Plugin | Brainside server | How your AI saves |
|---|---|---|
| **0.5.1** | The release that adds `o_que` and `por_que` to `open_upload_form`, or later | As in 0.5.0, plus: your AI fills the box with what the file is and why keep it, says it offered the box (never that it is open) and gives you the link in the same reply |
| **0.5.0** | The release that adds `open_upload_form` (the upload box in the chat), or later | As in 0.4.0, plus: where a command cannot reach Brainside, or there is no way to run one, it opens an upload box in the chat instead of asking you to allow a domain; if the box does not appear, it gives you the upload page |
| **0.4.0** | The release of the agents v2 (agents waiting for confirmation, the agent catalog in `list_spaces`), or later | As in 0.3.1. Every read starts with a search, even with an App's slug in hand. The agents it creates for you wait for your confirmation on the Brainside screen; it says when it uses an agent, and copies one elsewhere only when you ask |
| **0.3.1** | The release of 2026-10-22 that opens a day's hub (`episodio:YYYY-MM-DD`) and pages `backlinks`, or later | As in 0.3.0. For "what did I do on <date>?", opens that day and lists, page by page, what Brainside recorded in that space that day (notes, not App records or files) |
| **0.3.0** | The release that adds `create_upload` and `get_upload`, or later | As in 0.2.0, plus files: sends them with a one-time upload link, or gives you a Brainside upload page |
| **0.2.0** | The release of 2026-10-21 (the second that day) or later | Proactive saving: saves new items on its own and tells you in one line. Asks before changing or deleting anything, and before saving setup, sensitive, external or client data |
| **0.1.1** | Servers before and after that release | Asks before every save |

Your server is ready for 0.2.0 when your AI's Brainside connector, on a connection that can save, lists the tool `answer_node_questions`, for 0.3.0 when it also lists `create_upload`, for 0.3.1 when its `backlinks` tool also takes `offset`, for 0.4.0 when its `upsert_node` tool also takes `apps`, and for 0.5.0 when it also lists `open_upload_form`. Brainside is hosted, so the server updates for every account at once. The connector address stays `https://api.brainside.ai/mcp` in every version.

## 0.5.1 — 2026-10-23

The upload box, after the first test on claude.ai.

### What changes for you

- **The box tells you what and why.** Your AI fills in what the file is and why keep it; Brainside adds where it will live (the note's name, which only Brainside shows).
- **No false "it's open".** Your AI cannot see the box, so it says it offered one and gives you the upload link in the same reply.
- **If the box does not appear,** reload the app (Ctrl+R or Cmd+R) or reconnect the Brainside connector. In the test of 2026-10-23 the box only showed after one of the two. The link always works.
- **Dismissed is dismissed.** If you tap the box's "Not now" button (in Portuguese, "Agora não"), your AI does not insist.

### What the skill expects from the server

`open_upload_form` taking `o_que` and `por_que`. On a 0.5.0 server the box still works, without those two lines.

## 0.5.0 — 2026-10-23

The upload box in the chat, for the Brainside server release that adds `open_upload_form`, or later.

### What changes for you

- **No domain to allow.** When the upload command is blocked (`403`) or your AI has no way to run commands (claude.ai with code execution off, the Claude mobile app), it opens an upload box in the chat. You pick the file and tap Send; the file goes straight from your device to Brainside, never through the AI.
- **You confirm in the box.** The box shows a notice for sensitive files (exams, invoices, contracts, someone else's files); your tap on Send is the confirmation.
- **If the box does not appear,** tell your AI: it gives you the upload page instead.

### What the skill expects from the server

`open_upload_form` in the tool list. Without it, the skill keeps using the upload page.

## 0.4.0 — 2026-10-22

Agents, for the Brainside server release of the agents v2, or later.

### What changes for you

- **Search first, always.** Your AI starts every read with a search, even when it already knows an App's slug. Opening the App directly missed the agents, rules and notes around it: in a test on 2026-10-22, a financial question went straight to the App and never met the finance agent.
- **Your agents are known up front.** `list_spaces` now brings each space's agent catalog (name, role and Apps). Your AI knows Otto, your Tech Lead or your FinOps agent exist before any search, and still picks them by what the search finds.
- **It tells you when it uses an agent.** "Consultando o Otto…": your AI says so and answers in that agent's role, even if the agent's own text says not to.
- **Agents it creates wait for you.** An agent your AI creates in your own memory is usable right away when you ask for it by name, and becomes automatic once you confirm it on the Brainside screen (text, Apps and origin in view). It never becomes automatic on its own. A copied name, a reserved word, too many in a day from one connection, or a memory that is not yours makes it a draft instead.
- **Taking an agent elsewhere.** When you ask, your AI copies a confirmed agent into another tool (a Claude Code subagent, another harness, another chat), keeps a reference to check for a newer version before using it, and asks before updating either side. It tells you plainly that Brainside cannot see or turn off a copy outside it.

### What the skill expects from the server

- `get_node` of an agent can return `nivel` "sob_pedido" with `aguardando_confirmacao` and `criado_por`, and `como_portar` for confirmed agents.
- `upsert_node` with `forma: "agente"` takes `apps`, and its `recibo` says how the agent came out in `agente` (`sob_pedido`, or `rascunho` with a reason).
- `list_spaces` returns `agentes` per space.

## 0.3.1 — 2026-10-22

The day lookup, for the Brainside server release of 2026-10-22 that opens a day's hub and pages `backlinks`, or later.

### What changes for you

- **"What did I do yesterday?"** Ask your AI what you did on a day and it opens that day in your Brainside instead of searching by text: the day's hub, `episodio:YYYY-MM-DD`, with the day in Brasilia time. What it lists is the day's record in that space: notes saved or changed that day with `upsert_node` or `update_node`, your edits on the Brainside screen and the changes Brainside's Curator applied; from an imported vault, the notes dated that day, the notes linked to or from that day's daily note, and the daily note itself.
- **What the day leaves out.** App records, files and links made with `link` are not in a day's record. When your question may involve them, your AI also looks in your Apps that have a date field.
- **Long days come back whole.** Above 50 items, your AI reads the rest page by page instead of stopping at the first 50.
- **Days before 2026-10-21.** Brainside records each day since 2026-10-21; before that, only imported daily notes got a day. For an earlier day, your AI tells you Brainside does not have that day's record, searches by the date and the month, and says the result is partial.
- **Nothing recorded is not nothing done.** From 2026-10-21 on, when a day has no hub, your AI says nothing was recorded in that space that day, never that you did nothing.

### What the skill expects from the server

- `get_node` with `dedup_key` `"episodio:YYYY-MM-DD"` opens the day's hub, with its first 50 backlinks and `backlinks_total`. The day's record is the backlinks with `relacao` "registrado em", plus the one with `relacao` "sobre" from that day's daily note (kind `evento`).
- `backlinks` takes `offset` and returns `total` and, while there is more, `proximo_offset`.
- If `backlinks` takes no `offset`, the server is older: your AI still opens the day and tells you the list may be incomplete.

### Docs and repository

- Skill: a "What did I do on <date>?" part at the end of section 1 (no section was renumbered), the day in the tools table, and the older-server case.
- Examples: "O que eu fiz ontem?" and a day before 2026-10-21. Troubleshooting: the server this version needs, and a day on an older server.
- README: a row in "What changes in your AI", and compatibility. `INSTALL.md`: the server this version needs.
- ChatGPT custom instructions: the block is unchanged. The field has no room left, so ChatGPT relies on the descriptions of the server's own tools for a day.
- This changelog: 0.3.0 now shows its release date, 2026-10-22.

## 0.3.0 — 2026-10-22

Files, for the Brainside server release that adds `create_upload` and `get_upload`. Update the plugin after that release is live.

### What changes for you

- **Files your AI keeps for you.** Ask your AI to keep a receipt, a PDF or a photo and it goes to Brainside as a file, never as pasted text: to your Brain Node, linked to the item it belongs to, or to a record in one of your Apps. Up to 15 MiB per file.
- **Where your AI can run commands and reach `api.brainside.ai`** (Claude Code, Codex; claude.ai with code execution once that host is allowed, which we haven't confirmed yet), Brainside gives it a one-time upload link for that one file, valid for 10 minutes, and your AI sends the file with a `curl` command. Brainside checks the size, the type and the SHA-256 before keeping anything. Your AI changes only the file's path in that command, never the address or the headers.
- **Where it can't** (ChatGPT, claude.ai until it can reach that host, any app without code execution), your AI gives you a Brainside upload page: you open it, log in and pick the file. The page works only for you, logged in to your own Brainside.
- **Very small files** can still go straight through the connector. Your AI now sends their size and SHA-256 too, measured with a command, and Brainside refuses the file if they don't match.
- **No files with secrets.** Your AI never keeps a file that is or holds a secret (a key or credentials file, a password export), even if you ask: Brainside doesn't look inside files for secrets.
- **Asks first** before keeping a file with health, biometric, identity or bank data, a file that came from someone else (an exam, an invoice, a contract) or a client's file. Brainside itself refuses an external file unless your AI says you agreed.
- **The upload code is not a password of yours.** It works once, for one file, for 10 minutes, and goes only in the upload command. The skill tells your AI never to save it or put it in a link. No password or API key of yours goes through the conversation.
- **Allowing `api.brainside.ai`.** Some AIs block outside hosts. If the upload fails with `host_not_allowed`, your AI offers the upload page and tells you where the host can be allowed: approving the command in Claude Code and Codex, or the Claude Code sandbox's allowed domains. On claude.ai (Settings › Capabilities, or an Owner on Team and Enterprise) we haven't confirmed that allowing it works yet, and users report that the list is not always applied. The README lists, per AI, what to allow and where we read it.

### What the skill expects from the server

- `create_upload` (asks for an upload link, or for the upload page when called without size and hash) and `get_upload` (whether the upload finished), on top of the 0.2.0 tools.
- `upload_attachment` accepts `sha256` and `size_bytes`, and the same destinations as `create_upload`. For an App, the record's attachment field gets the `attachment_url` Brainside returns.
- If the connector lists tools to save but no `create_upload`, the skill sends only small files and tells you larger ones must wait.

### Docs and repository

- Skill: a new "Files" part in section 3 (when to use the upload link, base64 or the upload page; what to do with each response; never a file that holds a secret; run the command and share the page only when they point to Brainside, and never pass them to anyone else), the upload code set apart from secrets, and the tools table.
- Examples and troubleshooting: files in Claude Code and in ChatGPT, a health exam (ask first), `host_not_allowed`, a hash mismatch, a note asking to send a file somewhere, a request to forward the upload link, a credentials file (never), and a new "Sending a file" section with what each client needs and what each upload response means.
- README: a "Sending files" section with what to allow in each AI, its source and the date we checked; privacy notes on the upload command and the one-time code; a new FAQ entry; compatibility.
- `INSTALL.md`: the upload host, and what to allow for files in claude.ai, Claude Code, Codex, ChatGPT and other clients.
- **ChatGPT custom instructions changed:** paste the new block from `chatgpt/custom-instructions.md` (1,492 of 1,500 characters).
- Validator: `api.brainside.ai` may now appear alone, as the host to allow; as an address it may still only be `https://api.brainside.ai/mcp`.

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
