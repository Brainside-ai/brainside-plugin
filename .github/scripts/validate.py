#!/usr/bin/env python3
"""Valida o repositório do plugin do Brainside e gera o ZIP da skill.

Só biblioteca padrão (sem pip install no CI). Uso: python3 .github/scripts/validate.py

Erros fazem o script sair com código 1. Avisos só aparecem na saída.
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_DIR = ROOT / "plugins" / "brainside"
PLUGIN_JSON = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
MCP_JSON = PLUGIN_DIR / ".mcp.json"
SKILLS_DIR = PLUGIN_DIR / "skills"
DIST = ROOT / "dist"
ZIP_NAME = "brainside-skill.zip"

MARKETPLACE_NAME = "brainside-ai"
PLUGIN_NAME = "brainside"
REPO = "brainside-ai/brainside-plugin"
MCP_URL = "https://api.brainside.ai/mcp"
EXPECTED_MCP = {"mcpServers": {"brainside": {"type": "http", "url": MCP_URL}}}

# O que o plugin NÃO pode ter: código que roda na máquina do usuário ou que muda o host.
FORBIDDEN_PLUGIN_PATHS = [
    "bin", "hooks", "agents", "commands", "scripts", "monitors", "output-styles",
    "workflows", "themes", ".lsp.json", "settings.json",
]
FORBIDDEN_PLUGIN_KEYS = [
    "hooks", "agents", "commands", "mcpServers", "lspServers", "outputStyles", "workflows",
    "experimental", "userConfig", "channels", "settings", "dependencies", "skills",
]
ALLOWED_FRONTMATTER = {"name", "description", "license"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URL_RE = re.compile(r"https?://[^\s)\]>`\"'|]+")
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".txt", ".py", ".toml"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"{rel(path)}: arquivo não existe")
    except json.JSONDecodeError as e:
        err(f"{rel(path)}: JSON inválido ({e})")
    return None


def repo_files():
    for p in sorted(ROOT.rglob("*")):
        parts = p.relative_to(ROOT).parts
        if not p.is_file() or parts[0] in {".git", "dist"}:
            continue
        yield p


def check_all_json() -> None:
    for p in repo_files():
        if p.suffix == ".json":
            load_json(p)


def check_marketplace() -> dict | None:
    m = load_json(MARKETPLACE)
    if not isinstance(m, dict):
        return None
    if m.get("name") != MARKETPLACE_NAME:
        err(f"marketplace.json: name deve ser '{MARKETPLACE_NAME}'")
    if not isinstance(m.get("owner"), dict) or not m["owner"].get("name"):
        err("marketplace.json: owner.name é obrigatório")
    plugins = m.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        err("marketplace.json: plugins deve ter exatamente 1 entrada (brainside)")
        return None
    entry = plugins[0]
    if entry.get("name") != PLUGIN_NAME:
        err(f"marketplace.json: a entrada deve se chamar '{PLUGIN_NAME}'")
    if entry.get("source") != f"./plugins/{PLUGIN_NAME}":
        err(f"marketplace.json: source deve ser './plugins/{PLUGIN_NAME}'")
    if "version" in entry:
        err("marketplace.json: não declare version na entrada; o version fica só no plugin.json")
    for key in FORBIDDEN_PLUGIN_KEYS:
        if key in entry:
            err(f"marketplace.json: a entrada não pode declarar '{key}'")
    return entry


def check_plugin_json() -> None:
    p = load_json(PLUGIN_JSON)
    if not isinstance(p, dict):
        return
    if p.get("name") != PLUGIN_NAME:
        err(f"plugin.json: name deve ser '{PLUGIN_NAME}' (igual à entrada do marketplace)")
    if not isinstance(p.get("version"), str) or not p["version"].strip():
        err("plugin.json: version é obrigatório (sem subir o version, quem instalou não recebe a mudança)")
    if p.get("license") != "Apache-2.0":
        err("plugin.json: license deve ser 'Apache-2.0'")
    if REPO not in str(p.get("repository", "")):
        err(f"plugin.json: repository deve apontar para {REPO}")
    for key in FORBIDDEN_PLUGIN_KEYS:
        if key in p:
            err(f"plugin.json: o plugin não pode declarar '{key}'")


def check_mcp_json() -> None:
    m = load_json(MCP_JSON)
    if m is not None and m != EXPECTED_MCP:
        err(f".mcp.json: conteúdo deve ser exatamente {json.dumps(EXPECTED_MCP)}")


def check_forbidden_paths() -> None:
    for name in FORBIDDEN_PLUGIN_PATHS:
        if (PLUGIN_DIR / name).exists():
            err(f"{rel(PLUGIN_DIR / name)}: proibido no plugin (só texto e o .mcp.json)")
    for p in PLUGIN_DIR.rglob("*"):
        if p.is_file() and p.stat().st_mode & 0o111:
            err(f"{rel(p)}: arquivo executável no plugin")
    allowed_top = {".claude-plugin", ".mcp.json", "skills"}
    for p in PLUGIN_DIR.iterdir():
        if p.name not in allowed_top:
            err(f"{rel(p)}: fora do que o plugin pode ter ({', '.join(sorted(allowed_top))})")


def parse_frontmatter(text: str, where: str) -> dict[str, str] | None:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        err(f"{where}: frontmatter deve começar na primeira linha com '---'")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        err(f"{where}: frontmatter sem o '---' de fechamento")
        return None
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            err(f"{where}: frontmatter só aceita 'chave: valor' em uma linha ({line!r})")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in fm:
            err(f"{where}: chave repetida no frontmatter ({key})")
        fm[key] = value.strip('"').strip("'")
    if not "\n".join(lines[end + 1:]).strip():
        err(f"{where}: corpo da skill vazio")
    return fm


def check_skills() -> list[Path]:
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()) if SKILLS_DIR.is_dir() else []
    if [d.name for d in skill_dirs] != [PLUGIN_NAME]:
        err(f"skills/: deve haver exatamente a skill '{PLUGIN_NAME}'")
    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        where = rel(skill_md)
        if not skill_md.is_file():
            err(f"{where}: não existe")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, where)
        if fm is not None:
            extra = set(fm) - ALLOWED_FRONTMATTER
            if extra:
                err(f"{where}: chaves não permitidas no frontmatter: {', '.join(sorted(extra))}")
            name = fm.get("name", "")
            if name != d.name:
                err(f"{where}: name '{name}' deve ser igual ao nome da pasta '{d.name}'")
            if not NAME_RE.match(name) or len(name) > 64:
                err(f"{where}: name deve ser kebab-case com até 64 caracteres")
            desc = fm.get("description", "")
            if not desc:
                err(f"{where}: description é obrigatória")
            elif len(desc) > 1024:
                err(f"{where}: description com {len(desc)} caracteres (máximo 1024)")
        if text.count("\n") >= 500:
            warn(f"{where}: {text.count(chr(10))} linhas; o recomendado é ficar abaixo de 500")
        for p in d.rglob("*"):
            if p.is_file() and p.suffix != ".md":
                err(f"{rel(p)}: a skill só pode ter arquivos .md")
    return skill_dirs


def check_text_references() -> None:
    """Caminho exato brainside-ai/... e o endereço único do MCP em todo texto do repositório."""
    for p in repo_files():
        if p.suffix not in TEXT_SUFFIXES or p.name == "LICENSE" or p == Path(__file__).resolve():
            continue
        text = p.read_text(encoding="utf-8")
        where = rel(p)
        if re.search(r"(?<![\w-])brainside/brainside-plugin", text) or "github.com/brainside/" in text:
            err(f"{where}: cita a org 'brainside' (de terceiros); use 'brainside-ai/...'")
        for m in re.finditer(r"(?:--marketplace|marketplace add)\s+([^\s`]+)", text):
            if m.group(1) not in {REPO, "<source>"}:
                err(f"{where}: marketplace '{m.group(1)}' (esperado {REPO})")
        for url in URL_RE.findall(text):
            url = url.rstrip(".,;:")
            host = re.sub(r"^https?://", "", url).split("/", 1)[0].lower()
            path = "/" + url.split("/", 3)[3] if url.count("/") >= 3 else "/"
            if "brainside" in host:
                if url.startswith("http://"):
                    err(f"{where}: URL do Brainside sem https ({url})")
                if host == "api.brainside.ai" and path != "/mcp":
                    err(f"{where}: api.brainside.ai só aparece como {MCP_URL} ({url})")
                if host not in {"api.brainside.ai", "www.brainside.ai", "brainside.ai"}:
                    err(f"{where}: host do Brainside desconhecido ({url})")
            if host == "github.com" and "brainside" in path.lower() and not path.startswith("/brainside-ai/"):
                err(f"{where}: link do GitHub fora da org brainside-ai ({url})")


def build_zip(skill_dirs: list[Path]) -> None:
    """ZIP determinístico com a pasta da skill no topo (brainside/SKILL.md), como o claude.ai exige."""
    DIST.mkdir(exist_ok=True)
    out = DIST / ZIP_NAME
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for d in skill_dirs:
            for p in sorted(x for x in d.rglob("*") if x.is_file()):
                info = zipfile.ZipInfo(str(p.relative_to(SKILLS_DIR)), date_time=(1980, 1, 1, 0, 0, 0))
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    if f"{PLUGIN_NAME}/SKILL.md" not in names:
        err(f"{rel(out)}: falta {PLUGIN_NAME}/SKILL.md no topo do ZIP")
    print(f"ZIP: {rel(out)} ({len(names)} arquivos: {', '.join(names)})")


def main() -> int:
    check_all_json()
    check_marketplace()
    check_plugin_json()
    check_mcp_json()
    check_forbidden_paths()
    skill_dirs = check_skills()
    check_text_references()
    if (ROOT / "drafts").exists():
        warn("drafts/: rascunhos locais (site e QA); tirar do repositório antes de publicar")
    if not errors:
        build_zip(skill_dirs)
    for w in warnings:
        print(f"AVISO: {w}")
    for e in errors:
        print(f"ERRO: {e}")
    print(f"{len(errors)} erro(s), {len(warnings)} aviso(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
