<h1 align="center">Brainside</h1>

<p align="center">
  <strong>A sua memória e o seu jeito de trabalhar, em qualquer IA.</strong><br>
  Plugin oficial do <a href="https://www.brainside.ai">Brainside</a> para Claude Code, claude.ai e Codex — e o equivalente para o ChatGPT.
</p>

<p align="center">
  <a href="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/brainside-ai/brainside-plugin/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Licença Apache-2.0" src="https://img.shields.io/badge/licen%C3%A7a-Apache--2.0-blue"></a>
  <img alt="Status: beta" src="https://img.shields.io/badge/status-beta-orange">
</p>

<p align="center"><a href="#english">English below</a></p>

---

## Por que existe

Cada IA nova começa do zero. Você explica de novo quem é quem, o que já decidiu, como gosta das coisas — e, quando troca de ferramenta, perde tudo outra vez.

O Brainside guarda esse conhecimento **uma vez**, na sua conta, e entrega para **qualquer IA que você conectar**. Este plugin é a ponte: ele ensina a sua IA a usar o Brainside sozinha, sem você precisar pedir "salva isso" ou "procura aquilo".

## O que muda na sua IA

| Situação | O que a IA faz |
|---|---|
| Você pergunta algo sobre seus projetos, pessoas, clientes ou decisões | **Busca no Brainside antes de responder** e diz de onde tirou |
| Você conta algo que vale guardar (uma decisão, uma pessoa nova, um prazo) | **Salva sozinha e avisa em uma linha**: "Salvei no seu Brainside: …" |
| A mudança altera ou apaga algo que já existe, mexe nas suas regras, envolve dado sensível ou veio de fonte externa (e-mail, página, arquivo de terceiro) | **Pergunta antes** e só grava com o seu sim |
| Aparece uma senha, chave ou token | **Nunca guarda**, nem se você pedir — e sugere um gerenciador de senhas |

Regras e manuais que **você** escreveu ou aprovou valem como instrução. O que vem de outra pessoa (autor de template, outro membro, conteúdo importado) chega à IA como **informação**, nunca como ordem.

## Como funciona

```
  Sua IA (Claude, Codex, ChatGPT…)
        │   skill "brainside": quando buscar, quando salvar, quando perguntar
        │   conector MCP:      https://api.brainside.ai/mcp   (login OAuth no brainside.ai)
        ▼
  Brainside — guarda, organiza, busca e entrega
        │
        └── a mesma memória em todas as IAs que você conectar
```

O Brainside **guarda, organiza, busca e entrega**. Quem lê, pensa e age é a **sua** IA. O Brainside não roda modelo de linguagem sobre o seu conhecimento para decidir por você.

## Instalação

> O endereço oficial é sempre **`brainside-ai/brainside-plugin`**. A organização `brainside` no GitHub (sem `-ai`) não é do Brainside.

### Claude Code

```bash
claude plugin install brainside --marketplace brainside-ai/brainside-plugin
```

Depois, numa sessão: `/mcp` › **Brainside** › **Authenticate**. O navegador abre o login do Brainside; entre e autorize.

### claude.ai (web, desktop e celular)

1. **Customize › Plugins › Add › Add marketplace** e digite `brainside-ai/brainside-plugin`.
2. Adicione o plugin **Brainside**.
3. Na aba **Connectors** do plugin, adicione o Brainside e entre na sua conta.

Skills precisam da execução de código ligada nas configurações do claude.ai. O plano Free permite um conector personalizado. O que você instala no claude.ai também aparece no Claude Code de quem entra com a mesma conta.

### Codex

```bash
codex plugin marketplace add brainside-ai/brainside-plugin
```

Instale pelo `/plugins`. Se o conector não aparecer: `codex mcp add brainside --url https://api.brainside.ai/mcp` e `codex mcp login brainside`.

### ChatGPT

O ChatGPT não instala plugins de repositório. Adicione o servidor MCP `https://api.brainside.ai/mcp` como app personalizado e cole nas instruções personalizadas o texto de [`chatgpt/instrucoes-personalizadas.md`](chatgpt/instrucoes-personalizadas.md).

### Deixe a sua IA instalar

Em Claude Code ou Codex, dá para pedir à própria IA:

> Instale o Brainside seguindo https://github.com/brainside-ai/brainside-plugin/blob/main/INSTALL.md

O [`INSTALL.md`](INSTALL.md) é escrito para IAs: passos exatos, o que conferir e onde parar para pedir o seu OK.

## Primeiros passos

Depois de conectar, experimente numa conversa nova, sem citar o Brainside:

- "Conheci a Ana, ela é designer na Acme e vai cuidar do nosso site." → a IA salva e avisa.
- "Quem cuida do site mesmo?" → a IA busca e responde com o que você salvou.
- "Decidimos fechar o trimestre sem novas contratações." → vira uma decisão ligada ao projeto.
- "Apaga a nota da Ana." → a IA pede confirmação antes.

Em qualquer IA conectada, a mesma memória.

## Atualizações

Toda mudança neste repositório passa por pull request com CI verde, e cada versão é registrada no [`CHANGELOG.md`](CHANGELOG.md).

- **Claude Code:** `claude plugin update brainside@brainside-ai`
- **Codex:** `codex plugin marketplace upgrade brainside-ai`
- **claude.ai:** ao adicionar o marketplace, você escolhe se ele sincroniza sozinho.

O plugin é só texto, mas é texto que orienta a sua IA. Por isso recomendamos ler o changelog antes de atualizar.

## Privacidade e segurança

- **O dado viaja, o poder não.** O plugin traz apenas a skill (texto) e o endereço do conector. Não traz hooks, comandos, agentes nem executáveis, e não roda código na sua máquina.
- **Login no Brainside, nunca na IA.** A conexão é feita por OAuth na página do Brainside. Nenhuma senha, chave ou token passa pela conversa.
- **Você controla cada conexão.** Em Configurações › IAs conectadas, no Brainside, você vê quais IAs têm acesso, o que cada uma pode fazer e revoga quando quiser.
- **Confira antes de instalar:** o arquivo [`plugins/brainside/.mcp.json`](plugins/brainside/.mcp.json) deve apontar para `https://api.brainside.ai/mcp`.
- **Encontrou uma vulnerabilidade?** Veja o [`SECURITY.md`](SECURITY.md) — o relato é privado.

## Problemas comuns

A IA não acha as ferramentas do Brainside, o login expirou, o conector não aparece: veja o [guia de problemas](plugins/brainside/skills/brainside/references/troubleshooting.md) ou [brainside.ai/instalar](https://www.brainside.ai/instalar).

## Estrutura

```
.claude-plugin/marketplace.json          catálogo (Claude Code, claude.ai e Codex leem o mesmo formato)
plugins/brainside/.claude-plugin/plugin.json
plugins/brainside/.mcp.json              conector MCP (HTTP + OAuth)
plugins/brainside/skills/brainside/      a skill: SKILL.md e referências
chatgpt/instrucoes-personalizadas.md     texto equivalente para o ChatGPT
INSTALL.md                               instalação escrita para IAs
```

## Para quem mantém

- Cada versão sobe o `version` em `plugins/brainside/.claude-plugin/plugin.json` (só lá, nunca também no `marketplace.json`) e ganha uma entrada no `CHANGELOG.md`.
- Validação: `python3 .github/scripts/validate.py` (o mesmo do CI) e, com o Claude Code, `claude plugin validate .`.
- O CI gera `dist/brainside-skill.zip`, o ZIP da skill para upload em claude.ai › Customize › Skills.
- A branch `main` é protegida: só entra por pull request com review e CI verde.

## Licença

[Apache-2.0](LICENSE). A licença não dá direito de uso da marca Brainside.

---

<a id="english"></a>

## English

**Your memory and your way of working, in any AI.** Official [Brainside](https://www.brainside.ai) plugin for Claude Code, claude.ai and Codex, plus an equivalent text for ChatGPT.

Every new AI starts from zero. Brainside keeps what you know **once**, in your account, and hands it to **every AI you connect**. This plugin teaches your AI to use it on its own:

- **Searches Brainside before answering** questions about your people, projects, clients and decisions, and says where the answer came from.
- **Saves durable knowledge on its own and tells you** in one line.
- **Asks first** before changing or deleting anything, touching your rules, saving sensitive data or anything that came from an external source.
- **Never stores secrets**, even if asked.

Brainside stores, organizes, searches and delivers. **Your** AI reads, thinks and acts.

**Install** (the official path is always `brainside-ai/brainside-plugin`; the GitHub org `brainside` without `-ai` is not Brainside):

- **Claude Code:** `claude plugin install brainside --marketplace brainside-ai/brainside-plugin`, then `/mcp` › Brainside › Authenticate.
- **claude.ai:** Customize › Plugins › Add › Add marketplace › `brainside-ai/brainside-plugin`, add the plugin, then add the connector in its Connectors tab.
- **Codex:** `codex plugin marketplace add brainside-ai/brainside-plugin`, then install it from `/plugins`.
- **ChatGPT:** add the MCP server `https://api.brainside.ai/mcp` as a custom app and paste the English block from [`chatgpt/instrucoes-personalizadas.md`](chatgpt/instrucoes-personalizadas.md).
- Or ask your AI: *"Install Brainside following https://github.com/brainside-ai/brainside-plugin/blob/main/INSTALL.md"*.

**Security:** the plugin ships only text (the skill) and the connector address — no hooks, commands, agents or executables. Login happens on brainside.ai via OAuth; you manage and revoke each connected AI in Brainside › Settings › Connected AIs. Updates go through reviewed pull requests and are listed in the [`CHANGELOG.md`](CHANGELOG.md). Vulnerability reports: [`SECURITY.md`](SECURITY.md).

License: [Apache-2.0](LICENSE). The license grants no rights to the Brainside trademark.
