#!/usr/bin/env python3
"""Validates the Brainside plugin repository and builds the skill ZIP.

Usage: python3 .github/scripts/validate.py [ROOT]

ROOT is the repository to check. It defaults to the repository that contains this script.
On pull requests, CI also runs the copy of this script from main against the pull request's
tree, so a change to these checks only takes effect after it is merged.

Every check is an allowlist: a file, manifest key, address, command or character that is
not listed here fails. Standard library only. Errors exit with code 1; warnings only print.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from fnmatch import fnmatch
from pathlib import Path
from urllib.parse import urlsplit

# CI looks for this exact line before passing ROOT to main's copy of the script.
ACCEPTS_ROOT_ARGUMENT = True

MARKETPLACE_NAME = "brainside-ai"
PLUGIN_NAME = "brainside"
REPO = "brainside-ai/brainside-plugin"
REPO_URL = "https://github.com/brainside-ai/brainside-plugin"
MCP_URL = "https://api.brainside.ai/mcp"
SCHEMA_URL = "https://anthropic.com/claude-code/marketplace.schema.json"
EXPECTED_MCP = {"mcpServers": {"brainside": {"type": "http", "url": MCP_URL}}}
ZIP_NAME = "brainside-skill.zip"

MARKETPLACE = ".claude-plugin/marketplace.json"
PLUGIN_JSON = "plugins/brainside/.claude-plugin/plugin.json"
MCP_JSON = "plugins/brainside/.mcp.json"
SKILL_DIR = "plugins/brainside/skills/brainside/"
SKILLS_ROOT = "plugins/brainside/skills/"
CHANGELOG = "CHANGELOG.md"
SELF = ".github/scripts/validate.py"

# Every file the repository may track. Any other path fails, wherever it is.
ALLOWED_FILES = frozenset({
    ".claude-plugin/marketplace.json",
    ".github/scripts/validate.py",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    ".gitignore",
    "CHANGELOG.md",
    "INSTALL.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "chatgpt/custom-instructions.md",
    "plugins/brainside/.claude-plugin/plugin.json",
    "plugins/brainside/.mcp.json",
    "plugins/brainside/skills/brainside/SKILL.md",
    "plugins/brainside/skills/brainside/references/examples.md",
    "plugins/brainside/skills/brainside/references/troubleshooting.md",
})
ALLOWED_FILE_PATTERNS = (re.compile(r"assets/[a-z0-9]+(?:-[a-z0-9]+)*\.svg"),)

# Manifest keys that may appear. Anything else (hooks, monitors, themes, mcpServers...) fails.
MARKETPLACE_KEYS = {"$schema", "name", "description", "owner", "plugins"}
OWNER_KEYS = {"name", "email"}
ENTRY_KEYS = {"name", "source", "description", "category", "homepage"}
PLUGIN_KEYS = {
    "name", "displayName", "version", "description", "author", "homepage", "repository",
    "license", "keywords", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl",
}
AUTHOR_KEYS = {"name", "email", "url"}
FRONTMATTER_KEYS = {"name", "description", "license"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)

# --- Characters -------------------------------------------------------------------------------
# Outside ASCII, only this visible punctuation (written as escapes so this file stays ASCII):
# middle dot, en and em dash, ellipsis, single angle quotes, arrows, box drawing, down triangle.
ALLOWED_PUNCTUATION = frozenset(
    "\u00b7\u2013\u2014\u2026\u2039\u203a\u2190\u2192\u2194\u2500\u2502\u2514\u251c\u25bc"
)
# Portuguese accented letters, accepted only in examples marked as Portuguese.
ACCENTED_LETTERS = frozenset(
    "\u00e1\u00e0\u00e2\u00e3\u00e9\u00ea\u00ed\u00f3\u00f4\u00f5\u00fa\u00fc\u00e7"
    "\u00c1\u00c0\u00c2\u00c3\u00c9\u00ca\u00cd\u00d3\u00d4\u00d5\u00da\u00dc\u00c7"
)
# Invisible, bidirectional and tag characters (also caught by category, listed for clarity).
INVISIBLE_RANGES = (
    (0xE0000, 0xE007F),  # tags
    (0x200B, 0x200F),    # zero width, LRM, RLM
    (0x202A, 0x202E),    # bidi embeddings and overrides
    (0x2066, 0x2069),    # bidi isolates
    (0xFEFF, 0xFEFF),    # zero width no-break space / BOM
)
INVISIBLE_CATEGORIES = {"Cc", "Cf", "Co", "Cn", "Cs", "Zl", "Zp"}
PORTUGUESE_MARKER = "Portuguese"
PORTUGUESE_TABLE_MARKER = "(Portuguese example)"
MAX_CHAR_ERRORS_PER_FILE = 40  # distinct characters reported per file

# --- Addresses --------------------------------------------------------------------------------
URL_RE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9+.-]*://[^\s<>()\[\]`\"'|]*")
EMAIL_RE = re.compile(r"[\w.+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")
HOST_RE = re.compile(
    r"(?<![\w@.-])((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+([a-z]{2,}))(?![\w-]|\.[a-z0-9])", re.I
)
TAIL_RE = re.compile(r"[^\s<>()\[\]`\"'|,;]*")
# Top-level domains that mark a word as a host name (file extensions such as .md, .py, .zip,
# .sh are left out on purpose, even where they are also domains).
HOST_TLDS = {
    "ai", "com", "net", "org", "io", "dev", "app", "co", "xyz", "example", "cloud", "site",
    "online", "tech", "info", "biz", "us", "br", "uk", "de", "gg", "link", "page", "ly",
    "news", "store", "shop", "live", "pro", "cc", "tv", "ws",
}
# Host names that may be written without a URL. GitHub and api.brainside.ai still have their
# path checked like a URL.
BARE_HOSTS = {
    "brainside.ai", "www.brainside.ai", "api.brainside.ai", "github.com",
    "raw.githubusercontent.com", "claude.ai", "chatgpt.com",
}
EXACT_URLS = {
    MCP_URL,
    SCHEMA_URL,
    "http://www.apache.org/licenses/",            # LICENSE
    "http://www.apache.org/licenses/LICENSE-2.0",  # LICENSE
    "https://www.apache.org/licenses/LICENSE-2.0",
    "http://www.w3.org/2000/svg",                  # SVG namespace
}
EMAIL_DOMAIN = "brainside.ai"
PLUGIN_IDS = {"brainside-ai", "synced"}
REPO_NAMES = {"brainside-plugin", "brainside-plugin.git"}

# --- Commands ---------------------------------------------------------------------------------
MARKETPLACE_ARG_RE = re.compile(r"(?:--marketplace|marketplace\s+add)\s+([^\s`]+)", re.I)
MCP_ADD_RE = re.compile(r"\bmcp\s+add\b([^`\n]*)", re.I)
URL_SETTING_RES = (
    re.compile(r"--url(?:\s+|=)([^\s`]+)", re.I),
    re.compile(r"(?<![\w-])url\s*=\s*([^\s`]+)", re.I),
    re.compile(r"\"url\"\s*:\s*(\"[^\"\n]*\"|[^\s`,}]+)", re.I),
)
STDIO_SEPARATOR_RE = re.compile(r"(?:^|\s)--(?:\s|$)")
FORBIDDEN_COMMANDS = (
    (re.compile(r"\bnpx\b", re.I), "npx"),
    (re.compile(r"\buvx\b", re.I), "uvx"),
    (re.compile(r"\bbunx\b", re.I), "bunx"),
    (re.compile(r"\bpipx\s+run\b", re.I), "pipx run"),
    (re.compile(r"\b(?:curl|wget)\b[^\n]*\|\s*(?:sudo\s+)?(?:ba|z|da|k|fi)?sh\b", re.I),
     "a download piped into a shell"),
    (re.compile(r"--transport\s+stdio\b", re.I), "a stdio MCP server"),
    (re.compile(r"\"(?:type|transport)\"\s*:\s*\"stdio\"", re.I), "a stdio MCP server"),
    (re.compile(r"\"command\"\s*:", re.I), "an MCP server started by a local command"),
)

# --- SVG --------------------------------------------------------------------------------------
SVG_NS = "http://www.w3.org/2000/svg"
SVG_ELEMENTS = {"svg", "g", "path", "circle", "title", "desc"}
LOCAL_URL_REF_RE = re.compile(r"url\(\s*#[\w-]+\s*\)", re.I)

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# --- Files ------------------------------------------------------------------------------------

def git_listing(root: Path) -> dict[str, str] | None:
    """Tracked files and their git modes, or None when ROOT is not the top of a git work tree."""
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=60)
        if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root:
            return None
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-s", "-z"],
                             capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    files: dict[str, str] = {}
    for record in out.stdout.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        files[path.decode("utf-8", "replace")] = meta.split()[0].decode()
    return files


def filesystem_listing(root: Path) -> dict[str, str]:
    """Fallback without git: every file under ROOT except .git/ and simple .gitignore patterns."""
    ignored: list[str] = []
    gitignore = root / ".gitignore"
    if gitignore.is_file():
        for line in gitignore.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().strip("/")
            if line and not line.startswith(("#", "!")):
                ignored.append(line)
    files: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        parts = p.relative_to(root).parts
        if parts[0] == ".git" or any(fnmatch(part, pat) for part in parts for pat in ignored):
            continue
        if p.is_symlink():
            mode = "120000"
        elif p.is_file():
            mode = "100755" if p.stat().st_mode & 0o111 else "100644"
        else:
            continue
        files["/".join(parts)] = mode
    return files


def path_allowed(path: str) -> bool:
    return path in ALLOWED_FILES or any(p.fullmatch(path) for p in ALLOWED_FILE_PATTERNS)


def check_paths(files: dict[str, str]) -> None:
    for path, mode in sorted(files.items()):
        if mode == "120000":
            err(f"{path}: symbolic links are not allowed")
        elif mode == "160000":
            err(f"{path}: submodules are not allowed")
        elif mode == "100755":
            err(f"{path}: executable files are not allowed")
        if not path_allowed(path):
            err(f"{path}: not an allowed path (ALLOWED_FILES in {SELF})")
    for path in sorted(ALLOWED_FILES - set(files)):
        err(f"{path}: required file is missing")


def read_texts(files: dict[str, str]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path, mode in sorted(files.items()):
        if mode not in {"100644", "100755"} or not path_allowed(path):
            continue
        try:
            texts[path] = (ROOT / path).read_bytes().decode("utf-8")
        except FileNotFoundError:
            err(f"{path}: listed by git but missing from the work tree")
        except UnicodeDecodeError as e:
            err(f"{path}: not valid UTF-8 ({e})")
    return texts


# --- Characters -------------------------------------------------------------------------------

def is_invisible(ch: str) -> bool:
    o = ord(ch)
    return (any(lo <= o <= hi for lo, hi in INVISIBLE_RANGES)
            or unicodedata.category(ch) in INVISIBLE_CATEGORIES)


def check_characters(path: str, text: str) -> None:
    """Reports each offending character once per file, at its first position, with a count."""
    found: dict[str, list] = {}
    in_table = portuguese_table = False
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("|"):
            if not in_table:
                in_table, portuguese_table = True, PORTUGUESE_TABLE_MARKER in line
        else:
            in_table = portuguese_table = False
        marked = portuguese_table or PORTUGUESE_MARKER in line
        for col, ch in enumerate(line, 1):
            if ch == "\t" or " " <= ch <= "~":
                continue
            name = unicodedata.name(ch, "unnamed")
            if is_invisible(ch):
                problem = f"invisible, control or bidirectional character U+{ord(ch):04X} ({name})"
            elif ch in ALLOWED_PUNCTUATION:
                continue
            elif ch in ACCENTED_LETTERS:
                if marked:
                    continue
                problem = (f"accented letter '{ch}' outside a marked Portuguese example "
                           f"(mark the line with '{PORTUGUESE_MARKER}')")
            else:
                problem = f"non-ASCII character U+{ord(ch):04X} ({name}) is not on the allowlist"
            if problem in found:
                found[problem][2] += 1
            else:
                found[problem] = [lineno, col, 1]
    for i, (problem, (lineno, col, count)) in enumerate(found.items()):
        if i == MAX_CHAR_ERRORS_PER_FILE:
            err(f"{path}: {len(found) - i} more distinct character error(s) not shown")
            break
        times = f" ({count} times)" if count > 1 else ""
        err(f"{path}:{lineno}:{col}: {problem}{times}")


# --- Addresses --------------------------------------------------------------------------------

def url_problem(url: str) -> str | None:
    """None when the URL is on the allowlist, otherwise the reason it is not."""
    if url in EXACT_URLS:
        return None
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError:
        return "malformed URL"
    host = (parts.hostname or "").lower()
    path = parts.path.lower()
    if not host.isascii() or "xn--" in host:
        return "non-ASCII or punycode host"
    if "@" in parts.netloc or port is not None:
        return "user info or port in the URL"
    if parts.scheme.lower() != "https":
        return "only https URLs are allowed (plus the exact license and SVG namespace URLs)"
    if host == "api.brainside.ai":
        return f"api.brainside.ai may only appear as {MCP_URL}"
    if host in {"www.brainside.ai", "brainside.ai"}:
        return "query strings are not allowed" if parts.query else None
    if host in {"github.com", "raw.githubusercontent.com"}:
        base = "/" + REPO
        if parts.query:
            return "query strings are not allowed"
        if path == base or path == base + ".git" or path.startswith(base + "/"):
            return None
        return f"GitHub address outside {REPO}"
    if host == "img.shields.io":
        return None if path.startswith("/badge/") else "only img.shields.io/badge/ is allowed"
    return "address is not on the allowlist"


def mask(text: str, spans: list[tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in spans:
        chars[start:end] = " " * (end - start)
    return "".join(chars)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def check_addresses(path: str, text: str) -> None:
    spans: list[tuple[int, int]] = []
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(".,;:!?")
        spans.append((m.start(), m.start() + len(url)))
        problem = url_problem(url)
        if problem:
            err(f"{path}:{line_of(text, m.start())}: {problem} ({url})")
    masked = mask(text, spans)

    email_spans: list[tuple[int, int]] = []
    for m in EMAIL_RE.finditer(masked):
        email_spans.append(m.span())
        if m.group(1).lower() != EMAIL_DOMAIN:
            err(f"{path}:{line_of(text, m.start())}: e-mail or SSH address outside "
                f"@{EMAIL_DOMAIN} ({m.group(0)})")
    masked = mask(masked, email_spans)

    for m in HOST_RE.finditer(masked):
        host, tld = m.group(1).lower(), m.group(2).lower()
        if tld not in HOST_TLDS:
            continue
        where = f"{path}:{line_of(text, m.start())}"
        if host not in BARE_HOSTS:
            err(f"{where}: host '{host}' is not on the allowlist")
            continue
        tail = TAIL_RE.match(masked, m.end()).group(0).rstrip(".,;:!?")
        if host == "api.brainside.ai":
            if tail != "/mcp":
                err(f"{where}: api.brainside.ai may only appear as {MCP_URL} ({host}{tail})")
        elif host in {"github.com", "raw.githubusercontent.com"} and tail:
            problem = url_problem(f"https://{host}{tail}")
            if problem:
                err(f"{where}: {problem} ({host}{tail})")

    for m in re.finditer(r"([\w.-]+)/(brainside-plugin[\w.-]*)", text, re.I):
        owner, repo = m.group(1).lower(), m.group(2).lower().rstrip(".")
        if owner != MARKETPLACE_NAME or repo not in REPO_NAMES:
            err(f"{path}:{line_of(text, m.start())}: repository '{m.group(0)}' "
                f"(the only one is {REPO})")
    for m in re.finditer(r"(?<![\w.-])brainside@([\w.-]+)", text, re.I):
        plugin_id = m.group(1).rstrip(".").lower()
        if plugin_id not in PLUGIN_IDS:
            err(f"{path}:{line_of(text, m.start())}: plugin id '{m.group(0)}' "
                f"(expected brainside@{MARKETPLACE_NAME})")
    for m in MARKETPLACE_ARG_RE.finditer(text):
        if m.group(1).lower() != REPO:
            err(f"{path}:{line_of(text, m.start())}: marketplace '{m.group(1)}' (expected {REPO})")


# --- Commands ---------------------------------------------------------------------------------

def check_commands(path: str, text: str) -> None:
    for pattern, what in FORBIDDEN_COMMANDS:
        for m in pattern.finditer(text):
            err(f"{path}:{line_of(text, m.start())}: {what} is not allowed ({m.group(0).strip()})")
    if not path.endswith(".md"):
        return  # JSON manifests are checked key by key; .mcp.json must match exactly.
    for m in MCP_ADD_RE.finditer(text):
        args = m.group(1).strip()
        if not args:
            continue  # the command named in prose, without arguments
        where = f"{path}:{line_of(text, m.start())}"
        if MCP_URL not in args:
            err(f"{where}: an 'mcp add' command must point to {MCP_URL} ({m.group(0).strip()})")
        if STDIO_SEPARATOR_RE.search(args):
            err(f"{where}: 'mcp add <name> --' starts a local stdio server ({m.group(0).strip()})")
        for u in URL_RE.findall(args):
            if u.rstrip(".,;:!?") != MCP_URL:
                err(f"{where}: an 'mcp add' command may only use {MCP_URL} ({u})")
    for pattern in URL_SETTING_RES:
        for m in pattern.finditer(text):
            value = m.group(1).strip("\"'`,;")
            if value != MCP_URL:
                err(f"{path}:{line_of(text, m.start())}: MCP url setting must be exactly "
                    f"{MCP_URL} ({m.group(0).strip()})")


# --- Manifests --------------------------------------------------------------------------------

def load_json(path: str, texts: dict[str, str]):
    if path not in texts:
        return None
    try:
        return json.loads(texts[path])
    except json.JSONDecodeError as e:
        err(f"{path}: invalid JSON ({e})")
        return None


def check_keys(where: str, obj: dict, allowed: set[str]) -> None:
    for key in sorted(set(obj) - allowed):
        err(f"{where}: key '{key}' is not allowed (allowed: {', '.join(sorted(allowed))})")


def check_marketplace(texts: dict[str, str]) -> None:
    m = load_json(MARKETPLACE, texts)
    if not isinstance(m, dict):
        if m is not None:
            err(f"{MARKETPLACE}: must be a JSON object")
        return
    check_keys(MARKETPLACE, m, MARKETPLACE_KEYS)
    if "$schema" in m and m["$schema"] != SCHEMA_URL:
        err(f"{MARKETPLACE}: $schema must be {SCHEMA_URL}")
    if m.get("name") != MARKETPLACE_NAME:
        err(f"{MARKETPLACE}: name must be '{MARKETPLACE_NAME}'")
    owner = m.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        err(f"{MARKETPLACE}: owner.name is required")
    else:
        check_keys(f"{MARKETPLACE} owner", owner, OWNER_KEYS)
    plugins = m.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        err(f"{MARKETPLACE}: plugins must have exactly one entry ({PLUGIN_NAME})")
        return
    entry = plugins[0]
    check_keys(f"{MARKETPLACE} plugins[0]", entry, ENTRY_KEYS)
    if entry.get("name") != PLUGIN_NAME:
        err(f"{MARKETPLACE}: the entry must be named '{PLUGIN_NAME}'")
    if entry.get("source") != f"./plugins/{PLUGIN_NAME}":
        err(f"{MARKETPLACE}: source must be './plugins/{PLUGIN_NAME}'")


def check_plugin_json(texts: dict[str, str]) -> str | None:
    p = load_json(PLUGIN_JSON, texts)
    if not isinstance(p, dict):
        if p is not None:
            err(f"{PLUGIN_JSON}: must be a JSON object")
        return None
    check_keys(PLUGIN_JSON, p, PLUGIN_KEYS)
    if p.get("name") != PLUGIN_NAME:
        err(f"{PLUGIN_JSON}: name must be '{PLUGIN_NAME}' (same as the marketplace entry)")
    if p.get("license") != "Apache-2.0":
        err(f"{PLUGIN_JSON}: license must be 'Apache-2.0'")
    if str(p.get("repository", "")).lower() != REPO_URL:
        err(f"{PLUGIN_JSON}: repository must be exactly {REPO_URL}")
    author = p.get("author")
    if author is not None:
        if isinstance(author, dict):
            check_keys(f"{PLUGIN_JSON} author", author, AUTHOR_KEYS)
        else:
            err(f"{PLUGIN_JSON}: author must be an object")
    keywords = p.get("keywords")
    if keywords is not None and not (isinstance(keywords, list)
                                     and all(isinstance(k, str) for k in keywords)):
        err(f"{PLUGIN_JSON}: keywords must be a list of strings")
    version = p.get("version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        err(f"{PLUGIN_JSON}: version must be semantic (MAJOR.MINOR.PATCH), got {version!r}; "
            "without a new version, people who installed the plugin do not get the change")
        return None
    return version


def check_mcp_json(texts: dict[str, str]) -> None:
    m = load_json(MCP_JSON, texts)
    if m is not None and m != EXPECTED_MCP:
        err(f"{MCP_JSON}: content must be exactly {json.dumps(EXPECTED_MCP)}")


def check_changelog(version: str | None, texts: dict[str, str]) -> None:
    if version is None or CHANGELOG not in texts:
        return
    v = re.escape(version)
    if not re.search(rf"^## (?:\[{v}\]|{v})(?=\s|$)", texts[CHANGELOG], re.M):
        err(f"{CHANGELOG}: no entry for version {version} "
            f"(a heading '## [{version}]' or '## {version}')")


# --- Skill ------------------------------------------------------------------------------------

def parse_frontmatter(text: str, where: str) -> dict[str, str] | None:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        err(f"{where}: frontmatter must start on the first line with '---'")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        err(f"{where}: frontmatter is missing the closing '---'")
        return None
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            err(f"{where}: frontmatter only accepts 'key: value' on a single line ({line!r})")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in fm:
            err(f"{where}: repeated key in frontmatter ({key})")
        fm[key] = value.strip('"').strip("'")
    if not "\n".join(lines[end + 1:]).strip():
        err(f"{where}: skill body is empty")
    return fm


def check_skill(texts: dict[str, str]) -> None:
    where = SKILL_DIR + "SKILL.md"
    if where not in texts:
        return
    text = texts[where]
    fm = parse_frontmatter(text, where)
    if fm is not None:
        check_keys(f"{where} frontmatter", fm, FRONTMATTER_KEYS)
        name = fm.get("name", "")
        if name != PLUGIN_NAME:
            err(f"{where}: name '{name}' must equal the folder name '{PLUGIN_NAME}'")
        if not NAME_RE.match(name) or len(name) > 64:
            err(f"{where}: name must be kebab-case, up to 64 characters")
        desc = fm.get("description", "")
        if not desc:
            err(f"{where}: description is required")
        elif len(desc) > 1024:
            err(f"{where}: description has {len(desc)} characters (maximum 1024)")
    if text.count("\n") >= 500:
        warn(f"{where}: {text.count(chr(10))} lines; staying under 500 is recommended")


# --- SVG --------------------------------------------------------------------------------------

def split_name(name: str) -> tuple[str, str]:
    if name.startswith("{"):
        ns, local = name[1:].split("}", 1)
        return ns, local
    return "", name


def check_svg(path: str, text: str) -> None:
    low = text.lower()
    for marker, what in (("<!doctype", "DOCTYPE"), ("<!entity", "ENTITY"), ("<![cdata[", "CDATA")):
        if marker in low:
            err(f"{path}: {what} is not allowed in SVG")
            return
    for m in re.finditer(r"<\?([^\s?>]*)", text):
        if m.group(1).lower() != "xml" or m.start() != 0:
            err(f"{path}: processing instruction '<?{m.group(1)}' is not allowed in SVG")
    if re.search(r"\son[a-z]+\s*=", text, re.I):
        err(f"{path}: event handler attributes (on*=) are not allowed in SVG")
    if re.search(r"href\s*=", text, re.I):
        err(f"{path}: href and xlink:href are not allowed in SVG")
    for m in re.finditer(r"url\(", text, re.I):
        if not LOCAL_URL_REF_RE.match(text, m.start()):
            err(f"{path}:{line_of(text, m.start())}: only local url(#id) references are allowed")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        err(f"{path}: invalid SVG ({e})")
        return
    if split_name(root.tag) != (SVG_NS, "svg"):
        err(f"{path}: the root element must be <svg> in the SVG namespace")
    for el in root.iter():
        ns, local = split_name(el.tag)
        if ns != SVG_NS or local not in SVG_ELEMENTS:
            err(f"{path}: element <{local}> is not allowed "
                f"(allowed: {', '.join(sorted(SVG_ELEMENTS))})")
        for attr, value in el.attrib.items():
            ans, alocal = split_name(attr)
            if ans:
                err(f"{path}: namespaced attribute '{alocal}' is not allowed")
            if alocal.lower().startswith("on") or alocal.lower() == "href":
                err(f"{path}: attribute '{alocal}' is not allowed")
            if re.search(r"javascript:|data:", value, re.I):
                err(f"{path}: attribute '{alocal}' has a script or data URL")


# --- ZIP --------------------------------------------------------------------------------------

def build_zip(files: dict[str, str]) -> None:
    """Deterministic ZIP with the skill folder at the top (brainside/SKILL.md), as claude.ai needs."""
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / ZIP_NAME
    skill_files = sorted(p for p in files if p.startswith(SKILL_DIR))
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in skill_files:
            info = zipfile.ZipInfo(path[len(SKILLS_ROOT):], date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (ROOT / path).read_bytes())
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    if f"{PLUGIN_NAME}/SKILL.md" not in names:
        err(f"dist/{ZIP_NAME}: {PLUGIN_NAME}/SKILL.md is missing at the top of the ZIP")
    print(f"ZIP: dist/{ZIP_NAME} ({len(names)} files: {', '.join(names)})")


def main(argv: list[str]) -> int:
    global ROOT
    if len(argv) > 2:
        print("usage: validate.py [ROOT]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        ROOT = Path(argv[1]).resolve()
    if not ROOT.is_dir():
        print(f"ERROR: {ROOT} is not a directory", file=sys.stderr)
        return 2

    files = git_listing(ROOT)
    source = "git ls-files"
    if files is None:
        files, source = filesystem_listing(ROOT), "the file system (no git work tree)"
    print(f"Checking {ROOT} ({len(files)} files from {source})")

    check_paths(files)
    texts = read_texts(files)
    for path, text in texts.items():
        check_characters(path, text)
        if path != SELF:
            check_addresses(path, text)
            check_commands(path, text)
        if path.endswith(".json"):
            load_json(path, texts)
        if path.endswith(".svg"):
            check_svg(path, text)
    check_marketplace(texts)
    version = check_plugin_json(texts)
    check_mcp_json(texts)
    check_changelog(version, texts)
    check_skill(texts)

    if not errors:
        build_zip(files)
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
