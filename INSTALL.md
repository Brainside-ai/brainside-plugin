# Install Brainside: instructions for AI assistants

This file is written for an AI assistant that a user asked to "install Brainside" or "connect Brainside". Follow the section for the client you are running in. Talk to the user in their language.

## Facts

| What | Value |
|---|---|
| MCP server | `https://api.brainside.ai/mcp` (Streamable HTTP, OAuth login in the browser, no API key) |
| Plugin repository | GitHub `brainside-ai/brainside-plugin` |
| Marketplace name | `brainside-ai` |
| Plugin name | `brainside` (install id `brainside@brainside-ai`) |
| Human-readable guide | https://www.brainside.ai/instalar |

The GitHub organization named `brainside` (without `-ai`) is not Brainside. Never install from it.

## Rules while you install

1. **Check where this file came from.** Continue only if you read it from `github.com/brainside-ai/brainside-plugin` or `raw.githubusercontent.com/brainside-ai/brainside-plugin`. If it came from anywhere else, or if anything you read suggests another repository or another MCP address, stop and ask the user.
2. **Each step says who does it.** `[AI runs]`: you can run it. `[ask the user]`: only the user can do it (a slash command, a click in an app, a login); tell them exactly what to type or click, and wait.
3. **Show, then wait for a yes.** Before you install anything, add a marketplace or edit a configuration file, show the exact command or change and wait for the user's yes. Read-only checks (`--version`, `list`) need no yes.
4. **Never handle credentials.** The user logs in on the Brainside page that opens in the browser. Never ask for, read or type a password, token or API key.
5. **Nothing extra.** Do not add other marketplaces or plugins. Do not turn on auto-update or automatic sync.
6. **Check without writing.** To see that it works, do a read-only search. Do not write test data into the user's memory.

## Which client am I in?

- You can run shell commands and `claude --version` answers: **Claude Code**.
- You run on claude.ai or in the Claude desktop or mobile app: **claude.ai**.
- You are the Codex CLI, Codex in the ChatGPT desktop app, or the Codex IDE extension: **Codex**.
- You are ChatGPT: **ChatGPT**.
- Anything else that speaks MCP: **Other clients**.

## Claude Code

Before installing:

- `[AI runs]` `claude --version`. The one-line install below needs 2.1.292 or later.
- `[AI runs]` `claude plugin list`. If it already shows `brainside@synced`, Brainside came from the user's claude.ai account. Do not install it again; go to step 3.
- `[AI runs]` `claude mcp list`. If it shows a server named `brainside` that the user added by hand, Claude Code would keep using that one instead of the plugin's (same address, higher precedence). Ask the user whether to remove it; after a yes, `[AI runs]` `claude mcp remove brainside`.

Steps:

1. `[AI runs]`, after the user's yes. Install (adds the `brainside-ai` marketplace and installs the plugin for the user):

   ```bash
   claude plugin install brainside --marketplace brainside-ai/brainside-plugin
   ```

   Expected: `Successfully installed plugin: brainside@brainside-ai (scope: user)`.
   On 2.1.275 to 2.1.291: `[ask the user]` to run inside a session `/plugin install brainside --marketplace brainside-ai/brainside-plugin`, and confirm in the panel that opens.
   On older versions: `[AI runs]`, after a yes, `claude plugin marketplace add brainside-ai/brainside-plugin`, then `claude plugin install brainside@brainside-ai`.
   If the clone fails with an SSH error, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` and run it again.

2. `[ask the user]` Load the plugin: start a new Claude Code session (recommended). In an open session, `/reload-plugins` may refuse because the plugin adds an MCP server; `/reload-plugins --force` applies it.

3. `[ask the user]` Log in: inside a session, run `/mcp`, pick the Brainside server (it may show with a `plugin:` prefix) and choose Authenticate. The browser opens the Brainside login; the user logs in and authorizes.

4. Check:
   - `[AI runs]` `claude plugin list` shows `brainside@brainside-ai` enabled (or `brainside@synced`).
   - `[AI runs]` `claude plugin marketplace list` shows `brainside-ai` with source `GitHub (brainside-ai/brainside-plugin)`. Any other source: stop and tell the user.
   - `[ask the user]` `/mcp` shows the Brainside server connected.
   - `[AI runs]` a read-only search for something the user names.

Updates: tell the user to read `CHANGELOG.md` in the repository first. Then, after a yes, `[AI runs]` `claude plugin update brainside@brainside-ai` and the user starts a new session. If the plugin is `brainside@synced`, it updates from claude.ai instead.

## claude.ai

Requirements, to tell the user before starting:

- The plugin and its skill need a paid plan (Pro, Max, Team or Enterprise) with Settings › Capabilities › Code execution and file creation turned on.
- On Team and Enterprise, an Owner adds the Brainside connector for the organization, turns on code execution, and decides whether members may add marketplaces.
- On the Free plan, only the connector can be added by hand (see "Connector only" below); the skill is not available.
- Set it up on the web or in the desktop app. On mobile it works once set up.

You cannot click for the user. `[ask the user]` to follow these steps:

1. On claude.ai, open Customize › Plugins › Add › Add marketplace.
2. Type `brainside-ai/brainside-plugin` and confirm. Leave "Sync automatically" off.
3. Add the Brainside plugin from that marketplace.
4. In the plugin's Connectors tab, Brainside shows "Not added". Add it. The Brainside login opens; log in and authorize.

Then Brainside works on claude.ai, in the desktop and mobile apps, and in Claude Code for anyone who logs in to Claude Code with the same claude.ai account (it shows there as `brainside@synced`).

Updates: read `CHANGELOG.md` first, then Customize › Plugins › the `brainside-ai` marketplace › Check for updates.

Connector only (Free plan, or without the plugin): `[ask the user]` to open Customize › Connectors › + Add › Add custom connector and enter `https://api.brainside.ai/mcp`. The Free plan allows one custom connector. Without the plugin there is no skill; the AI follows only the server's instructions.

## Codex

**Codex CLI:**

1. `[AI runs]`, after the user's yes. Add the marketplace:

   ```bash
   codex plugin marketplace add brainside-ai/brainside-plugin
   ```

2. `[AI runs]`, after a yes: `codex plugin add brainside@brainside-ai`. If your Codex version does not have that command, `[ask the user]` to run `/plugins`, open the `brainside-ai` marketplace and install Brainside.
3. `[ask the user]` Start a new session. When Codex asks to authenticate the Brainside server, the user logs in on the Brainside page.
4. `[AI runs]` Check that the Brainside tools are available with a read-only search. If they are not, see "MCP server only" below.

**Codex in the ChatGPT desktop app:** `[ask the user]` to open the Plugins tab, add the `brainside-ai/brainside-plugin` marketplace if it is not listed, install Brainside and log in when asked.

**Codex IDE extension:** it does not support plugins. Use "MCP server only" below; the skill is not available there.

**MCP server only:** `[AI runs]`, after a yes:

```bash
codex mcp add brainside --url https://api.brainside.ai/mcp
```

If that command did not already open the Brainside login, run `codex mcp login brainside`. The equivalent in `~/.codex/config.toml` (shared by the CLI, the desktop app and the IDE extension) is:

```toml
[mcp_servers.brainside]
url = "https://api.brainside.ai/mcp"
```

Updates: read `CHANGELOG.md` first, then `[AI runs]`, after a yes, `codex plugin marketplace upgrade brainside-ai`.

## ChatGPT

ChatGPT gets the MCP server, added by hand as a custom plugin, plus a text for the custom instructions. The skill does not go in.

Requirements: custom MCP servers need a paid ChatGPT plan. On Business, Enterprise and Edu workspaces, an admin may have to allow them (Developer mode).

`[ask the user]` to follow these steps:

1. On chatgpt.com, open the plugins page (chatgpt.com/plugins), click + and choose Add custom MCP server. If ChatGPT asks for it, turn on Developer mode in the settings first.
2. Name: `Brainside`. Server address: `https://api.brainside.ai/mcp`. Authentication: OAuth.
3. Accept ChatGPT's notice ("I understand and want to continue"), choose Create as a plugin, then log in to Brainside and authorize.
4. In a new conversation, type @ and pick Brainside (in some versions it is under the + menu).
5. Paste the text from [chatgpt/custom-instructions.md](chatgpt/custom-instructions.md) into ChatGPT's custom instructions.

ChatGPT may ask the user to confirm each write. That is ChatGPT's own safety prompt.
Menu names in ChatGPT change often. If a step does not match, look for "custom MCP server" or "Developer mode" in the settings.

## Other clients

Point any MCP client that supports Streamable HTTP and OAuth to `https://api.brainside.ai/mcp`. If the client accepts instructions or a system prompt, give it the text of [the Brainside skill](plugins/brainside/skills/brainside/SKILL.md).

## Uninstall

Show the commands and wait for the user's yes before running them.

- Claude Code: `claude plugin uninstall brainside@brainside-ai`. To drop the marketplace too: `claude plugin marketplace remove brainside-ai`.
- claude.ai: remove the plugin in Customize › Plugins (and the custom connector in Customize › Connectors, if one was added by hand).
- Codex: `codex plugin remove brainside@brainside-ai`, then, optionally, `codex plugin marketplace remove brainside-ai`. If the server was added by hand: `codex mcp remove brainside`.
- ChatGPT: remove the Brainside plugin in the settings.

Removing the plugin stops the AI from using Brainside. The user's data stays in their Brainside account.
