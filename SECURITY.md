# Segurança / Security

## Como reportar uma vulnerabilidade

Não abra issue pública para falha de segurança.

1. Use o reporte privado do GitHub: aba **Security** › **Report a vulnerability** neste repositório.
2. Ou mande e-mail para **suporte@brainside.ai** com o assunto começando por `[security]`.


Inclua o que for preciso para reproduzir: passos, versão do plugin (`version` em `plugins/brainside/.claude-plugin/plugin.json`), cliente de IA e versão. Não inclua senhas, tokens nem dados pessoais de terceiros. Não acesse, altere nem apague dados de outras pessoas para provar a falha.

Respondemos pelo mesmo canal e avisamos quando a correção sair.

## O que está no escopo

- Este repositório: o texto da skill, os manifestos (`marketplace.json`, `plugin.json`) e o `.mcp.json`.
- O servidor MCP do Brainside (`https://api.brainside.ai/mcp`) e o login OAuth em brainside.ai.

Interessam em especial: texto na skill que leve a IA a agir contra o usuário, troca do endereço do MCP, falha no login ou no consentimento, acesso a dados de outra conta e gravação de segredos.

## Como o plugin se protege

- Só texto e um endereço: sem hooks, agents, comandos ou executáveis. O CI recusa a entrada de qualquer um deles.
- O CI também recusa um `.mcp.json` que aponte para qualquer endereço diferente de `https://api.brainside.ai/mcp`.
- O retorno do Brainside é tratado como dado: a skill manda a IA não seguir instruções encontradas em notas, e-mails ou páginas.
- A skill manda nunca gravar senha, token ou chave.

A branch `main` é protegida e toda mudança passa por PR com review.

## Confira antes de instalar

O endereço do MCP em `plugins/brainside/.mcp.json` tem de ser `https://api.brainside.ai/mcp`, e o repositório tem de ser `brainside-ai/brainside-plugin`. A organização `brainside` no GitHub (sem `-ai`) não é do Brainside.

---

## English

Do not open public issues for security problems. Report privately through the repository's **Security** › **Report a vulnerability** tab, or by email to **suporte@brainside.ai** with a subject starting with `[security]`. Include reproduction steps, the plugin version and your AI client and version; never include passwords, tokens or other people's personal data, and do not access or change other people's data to prove an issue.

In scope: this repository (skill text, manifests, `.mcp.json`) and the Brainside MCP server at `https://api.brainside.ai/mcp`, including its OAuth login. The plugin ships only text and one address, with no hooks, agents, commands or executables, and CI rejects any MCP address other than `https://api.brainside.ai/mcp`.
