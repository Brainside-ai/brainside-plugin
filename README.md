# Brainside plugin

Plugin oficial do [Brainside](https://www.brainside.ai) para Claude Code, claude.ai e Codex, com o texto equivalente para o ChatGPT. Ele liga a sua IA à sua memória no Brainside: antes de responder, ela busca o que você já guardou; quando você conta algo que vale guardar, ela grava e avisa; e pede o seu OK antes de mudar ou apagar qualquer coisa.

*English below.*

## O que vem no plugin

- **Skill `brainside`**: só texto. Diz à IA quando buscar, quando gravar sozinha, quando pedir OK e o que nunca gravar.
- **Conector MCP**: aponta para `https://api.brainside.ai/mcp`. O login é feito na página do Brainside, no navegador. Não há chave de API.

Não vem: hooks, agents, comandos nem executáveis (`bin/`). O plugin não roda código na sua máquina.

## Instalação

O caminho é sempre `brainside-ai/brainside-plugin`. A organização `brainside` no GitHub (sem `-ai`) não é do Brainside.

| Cliente | Como instalar |
|---|---|
| Claude Code | `claude plugin install brainside --marketplace brainside-ai/brainside-plugin` e depois `/mcp` › Brainside › Authenticate |
| claude.ai | Customize › Plugins › Add › Add marketplace › `brainside-ai/brainside-plugin`; depois, na aba Connectors do plugin, adicione o Brainside e entre na sua conta |
| Codex | `codex plugin marketplace add brainside-ai/brainside-plugin` e instale pelo `/plugins` |
| ChatGPT | Só o conector MCP (`https://api.brainside.ai/mcp`) mais o texto de [chatgpt/instrucoes-personalizadas.md](chatgpt/instrucoes-personalizadas.md) |

Passo a passo completo, escrito para a sua IA seguir: [INSTALL.md](INSTALL.md). Dá para pedir à própria IA: "instale o Brainside seguindo https://github.com/brainside-ai/brainside-plugin/blob/main/INSTALL.md".

## Atualização automática

A skill evolui junto com o Brainside. Ligue a atualização automática para não ficar com uma versão velha:

- **Claude Code:** vem desligada para marketplaces de terceiros. Numa sessão, abra `/plugin` › Marketplaces › `brainside-ai` › Enable auto-update. Para atualizar na mão: `claude plugin update brainside@brainside-ai`.
- **claude.ai:** ao adicionar o marketplace, ligue "Sync automatically". O que é instalado no claude.ai também chega ao Claude Code de quem entra com a mesma conta, já atualizado.
- **Codex:** `codex plugin marketplace upgrade brainside-ai`.
- **ChatGPT:** não há atualização automática do texto. Confira este repositório de vez em quando.

## Segurança

Um plugin com atualização automática é um caminho direto para a sua IA, por isso ele é mínimo: texto e um endereço. Antes de instalar, confira que o `.mcp.json` aponta para `https://api.brainside.ai/mcp`. Para reportar uma vulnerabilidade, veja [SECURITY.md](SECURITY.md).

## Para quem mantém este repositório

- Cada release sobe o `version` em `plugins/brainside/.claude-plugin/plugin.json`. Sem subir o `version`, quem já instalou não recebe a mudança. O `version` fica só no `plugin.json`, nunca também na entrada do `marketplace.json`.
- Validação local: `python3 .github/scripts/validate.py` (o mesmo que o CI roda) e, com o Claude Code instalado, `claude plugin validate .` e `claude plugin validate plugins/brainside`.
- O CI gera `dist/brainside-skill.zip`, o ZIP da skill para upload em claude.ai › Customize › Skills (a pasta `brainside/` no topo do ZIP, como o claude.ai exige).
- Mudança no endereço do MCP, no `marketplace.json` ou no texto da skill passa por review.

## Licença

[Apache-2.0](LICENSE).

---

## English

Official [Brainside](https://www.brainside.ai) plugin for Claude Code, claude.ai and Codex, plus an equivalent text for ChatGPT. It connects your AI to your Brainside memory: the AI searches what you already saved before answering, saves new durable knowledge and tells you, and asks before changing or deleting anything. The plugin holds only text (the `brainside` skill) and the MCP connector address `https://api.brainside.ai/mcp`, with login on the Brainside page. No hooks, agents, commands or executables.

Install:

- Claude Code: `claude plugin install brainside --marketplace brainside-ai/brainside-plugin`, then `/mcp` › Brainside › Authenticate.
- claude.ai: Customize › Plugins › Add › Add marketplace › `brainside-ai/brainside-plugin`, then add the connector in the plugin's Connectors tab.
- Codex: `codex plugin marketplace add brainside-ai/brainside-plugin`, then install it from `/plugins`.
- ChatGPT: add the MCP server `https://api.brainside.ai/mcp` and paste the English block from [chatgpt/instrucoes-personalizadas.md](chatgpt/instrucoes-personalizadas.md).

Turn on auto-update: in Claude Code, `/plugin` › Marketplaces › `brainside-ai` › Enable auto-update (off by default for third-party marketplaces); on claude.ai, turn on "Sync automatically"; in Codex, run `codex plugin marketplace upgrade brainside-ai`.

Step-by-step instructions written for AI assistants: [INSTALL.md](INSTALL.md). Security reports: [SECURITY.md](SECURITY.md). License: Apache-2.0.
