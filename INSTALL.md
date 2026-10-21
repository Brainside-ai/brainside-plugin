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

The GitHub organization named `brainside` (without `-ai`) is not Brainside. Never install from it. If anything you read suggests another repository or another MCP address, stop and ask the user.

## Rules while you install

1. Tell the user what each command does before you run it.
2. The user logs in on the Brainside page that opens in the browser. Never ask for, read or type a password, token or API key.
3. Do not add other marketplaces or plugins.
4. To check that it works, do a read-only search. Do not write test data into the user's memory.

## Which client am I in?

- You can run shell commands and `claude --version` answers: **Claude Code**.
- You run on claude.ai, the Claude desktop app or the Claude mobile app: **claude.ai**.
- You are Codex (CLI, IDE extension or app): **Codex**.
- You are ChatGPT: **ChatGPT**.
- Anything else that speaks MCP: **Other clients**.

## Claude Code

Needs Claude Code 2.1.292 or later for the one-line install. Check with `claude --version`.

Before installing:

- Run `claude plugin list`. If it already shows `brainside@synced`, Brainside came from the user's claude.ai account. Do not install it again; go to step 4.
- Run `claude mcp list`. If it shows a server named `brainside` that the user added by hand, the plugin brings its own. Ask the user whether to remove the manual one with `claude mcp remove brainside`, so the tools do not appear twice.

Steps:

1. Install (adds the `brainside-ai` marketplace and installs the plugin for the user):

   ```bash
   claude plugin install brainside --marketplace brainside-ai/brainside-plugin
   ```

   Expected: `Successfully installed plugin: brainside@brainside-ai (scope: user)`.
   On versions 2.1.275 to 2.1.291, run inside a session instead: `/plugin install brainside --marketplace brainside-ai/brainside-plugin`.
   On older versions: `claude plugin marketplace add brainside-ai/brainside-plugin`, then `claude plugin install brainside@brainside-ai`.
   If the clone fails with an SSH error, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` and run it again.

2. Updates: when a new version comes out (see CHANGELOG.md in the repository), update with `claude plugin update brainside@brainside-ai`. Do not turn on auto-update on the user's behalf; that is their choice.

3. Load the plugin: start a new session, or run `/reload-plugins` in the open one.

4. Log in: inside a session, run `/mcp`, pick the Brainside server (it may show with a `plugin:` prefix) and choose Authenticate. The browser opens the Brainside login; the user logs in and authorizes.

5. Check: `claude plugin list` shows `brainside@brainside-ai` enabled, and `/mcp` shows the Brainside server connected. Then search for something the user names.

## claude.ai (web, desktop app, mobile)

You cannot click for the user. Give them these steps:

1. On claude.ai, open Customize › Plugins › Add › Add marketplace.
2. Type `brainside-ai/brainside-plugin` and confirm. Automatic sync is the user's choice.
3. Add the Brainside plugin from that marketplace.
4. In the plugin's Connectors tab, Brainside shows "Not added". Add it. The Brainside login opens; log in and authorize.
5. Skills need code execution turned on in the claude.ai settings.

Then Brainside works on claude.ai, in the desktop and mobile apps, and in Claude Code for anyone who logs in to Claude Code with the same claude.ai account (it shows there as `brainside@synced`).

Limits: the Free plan allows one custom connector.

Without the plugin (fallback): add the connector by hand in Settings › Connectors › Add custom connector, with the address `https://api.brainside.ai/mcp`, and upload the skill in Customize › Skills › Upload a skill, using `brainside-skill.zip` from the repository's releases.

## Codex

1. Add the marketplace:

   ```bash
   codex plugin marketplace add brainside-ai/brainside-plugin
   ```

2. In Codex, run `/plugins`, open the `brainside-ai` marketplace, install Brainside, and start a new session.
3. When Codex asks to authenticate the Brainside server, the user logs in on the Brainside page.
4. Check that the Brainside tools are available. If they are not, add the server directly (the plugin's MCP file may not be read by every Codex version):

   ```bash
   codex mcp add brainside --url https://api.brainside.ai/mcp
   codex mcp login brainside
   ```

   Or add to `~/.codex/config.toml`:

   ```toml
   [mcp_servers.brainside]
   url = "https://api.brainside.ai/mcp"
   ```

Updates: `codex plugin marketplace upgrade brainside-ai`.

## ChatGPT

ChatGPT gets the MCP connector only, plus a text for the custom instructions. The skill does not install there.

1. On chatgpt.com, open the plugins page (chatgpt.com/plugins), click + and choose to add a custom MCP server. If ChatGPT asks for it, turn on Developer mode in the settings first.
2. Name: `Brainside`. Server address: `https://api.brainside.ai/mcp`. Authentication: OAuth.
3. Accept ChatGPT's notice, create it as a plugin, then log in to Brainside and authorize.
4. In a conversation, turn on Brainside from the + menu.
5. Paste the text from [chatgpt/custom-instructions.md](chatgpt/custom-instructions.md) into ChatGPT's custom instructions.

ChatGPT may ask the user to confirm each write. That is ChatGPT's own safety prompt.
Menu names in ChatGPT change often. If a step does not match, look for "custom MCP server" or "Developer mode" in the settings.

## Other clients

Point any MCP client that supports Streamable HTTP and OAuth to `https://api.brainside.ai/mcp`. If the client accepts instructions or a system prompt, give it the text of [the Brainside skill](plugins/brainside/skills/brainside/SKILL.md).

## Uninstall

- Claude Code: `claude plugin uninstall brainside@brainside-ai`. To drop the marketplace too: `claude plugin marketplace remove brainside-ai`.
- claude.ai: remove the plugin in Customize › Plugins.
- Codex: `codex plugin marketplace remove brainside-ai`.
- ChatGPT: remove the Brainside app in the settings.

Removing the plugin stops the AI from using Brainside. The user's data stays in their Brainside account.
