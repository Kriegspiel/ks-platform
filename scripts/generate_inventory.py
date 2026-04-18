#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
from collections import OrderedDict
from datetime import datetime, UTC
from pathlib import Path


PLATFORM_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PLATFORM_ROOT / "documentation" / "module-index.md"

REPOS = OrderedDict(
    [
        ("ks-backend", "FastAPI backend, persistence, ratings, transcripts, and technical reports"),
        ("ks-web-app", "Authenticated React frontend for play, review, profiles, and live reports"),
        ("ks-home", "Static public site renderer and build pipeline for kriegspiel.org"),
        ("content", "Source-of-truth blog, changelog, rules, and public copy"),
        ("ks-game", "Python Kriegspiel engine, move/answer objects, and serialization"),
        ("bot-random", "Baseline random bot"),
        ("bot-random-any", "Random bot that asks any-pawn-captures first"),
        ("bot-simple-heuristics", "Heuristic bot with recapture, promotion, and weighted piece-choice rules"),
        ("bot-gpt-nano", "OpenAI-driven conversational bot"),
        ("bot-haiku", "Anthropic-driven conversational bot"),
        ("ks-platform", "Org-level documentation and operations handbook"),
    ]
)

SKIP_DIRS = {
    ".git",
    ".venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
    "coverage",
    ".coverage",
}

RELEVANT_SUFFIXES = {
    ".py",
    ".js",
    ".jsx",
    ".mjs",
    ".json",
    ".md",
    ".service",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
    ".css",
}

SPECIAL_FILES = {"README.md", "AGENTS.md", "LICENSE", ".env.example"}


def find_workspace_root() -> Path:
    sentinels = ("ks-backend", "ks-web-app", "ks-home", "content", "ks-game")
    for candidate in (PLATFORM_ROOT, *PLATFORM_ROOT.parents):
        if all((candidate / name).exists() for name in sentinels):
            return candidate
    raise RuntimeError("Could not locate the Kriegspiel workspace root from this checkout.")


WORKSPACE_ROOT = find_workspace_root()


def iter_repo_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SPECIAL_FILES or path.suffix in RELEVANT_SUFFIXES:
            files.append(path)
    return sorted(files)


def classify(path: Path) -> str:
    if path.name == ".env.example":
        return "env example"
    if path.name in {"README.md", "AGENTS.md"}:
        return "top-level doc"
    if path.name == "LICENSE":
        return "license"
    if path.suffix == ".py":
        return "python module"
    if path.suffix == ".service":
        return "systemd unit"
    if path.suffix == ".sh":
        return "shell script"
    if path.suffix in {".jsx", ".js", ".mjs"}:
        return "js module"
    if path.suffix in {".json", ".toml", ".yaml", ".yml"}:
        return "config/data"
    if path.suffix == ".css":
        return "stylesheet"
    if path.suffix == ".md":
        return "markdown doc/content"
    return "file"


def python_symbols(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - best-effort inventory only
        return [f"parse_error:{type(exc).__name__}"]

    symbols: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            if bases:
                symbols.append(f"class {node.name}({', '.join(bases)})")
            else:
                symbols.append(f"class {node.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            symbols.append(f"{prefix} {node.name}")
        elif isinstance(node, ast.Assign):
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            for name in names:
                if name.isupper():
                    symbols.append(f"const {name}")
    return symbols


EXPORT_PATTERNS = [
    re.compile(r"export\s+default\s+function\s+([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"export\s+default\s+class\s+([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"export\s+function\s+([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"export\s+(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)"),
    re.compile(r"export\s+async\s+function\s+([A-Za-z_][A-Za-z0-9_]*)"),
]


def js_symbols(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    symbols: list[str] = []
    for pattern in EXPORT_PATTERNS:
        symbols.extend(pattern.findall(text))

    for match in re.findall(r"export\s*\{([^}]*)\}", text):
        for raw_name in match.split(","):
            name = raw_name.strip().split(" as ")[0].strip()
            if name:
                symbols.append(name)

    default_name = re.search(r"export\s+default\s+([A-Za-z_][A-Za-z0-9_]*)", text)
    if default_name:
        symbols.append(f"default {default_name.group(1)}")

    return [f"export {name}" for name in dedupe(symbols)]


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def summarize_symbols(path: Path) -> list[str]:
    if path.suffix == ".py":
        return python_symbols(path)
    if path.suffix in {".js", ".jsx", ".mjs"}:
        return js_symbols(path)
    return []


def render_table(repo_root: Path, files: list[Path]) -> list[str]:
    lines = ["| Path | Kind | Symbols |", "| --- | --- | --- |"]
    for path in files:
        rel = path.relative_to(repo_root).as_posix()
        symbols = summarize_symbols(path)
        symbol_text = "<br>".join(f"`{item}`" for item in symbols) if symbols else "—"
        lines.append(f"| `{rel}` | {classify(path)} | {symbol_text} |")
    return lines


def main() -> None:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = [
        "# Module Index",
        "",
        f"Generated from the checked-out repos under `.../kriegspiel/` on {generated_at}.",
        "",
        "This file is exhaustive at the file/module level for the active repos. It is generated by `scripts/generate_inventory.py` and should be regenerated after repo layout changes.",
        "",
    ]

    for repo_name, description in REPOS.items():
        repo_root = WORKSPACE_ROOT / repo_name
        files = iter_repo_files(repo_root)
        lines.extend(
            [
                f"## {repo_name}",
                "",
                description,
                "",
                f"- Repo root: `.../kriegspiel/{repo_name}/`",
                f"- Inventory size: `{len(files)}` files",
                "",
            ]
        )
        lines.extend(render_table(repo_root, files))
        lines.append("")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
