#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

from workspace_repos import GITHUB_ORG, REPO_GROUPS

PLATFORM_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PLATFORM_ROOT / "documentation" / "repo-map.md"


def find_workspace_root() -> Path:
    sentinels = ("ks-backend", "ks-web-app", "ks-home", "content", "ks-game")
    for candidate in (PLATFORM_ROOT, *PLATFORM_ROOT.parents):
        if all((candidate / name).exists() for name in sentinels):
            return candidate
    raise RuntimeError("Could not locate the Kriegspiel workspace root from this checkout.")


WORKSPACE_ROOT = find_workspace_root()


def git(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo_root), *args],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def default_branch(repo_root: Path) -> str:
    try:
        remote_head = git(repo_root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
        return remote_head.removeprefix("origin/")
    except subprocess.CalledProcessError:
        return git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")


def commit_sha(repo_root: Path, branch: str) -> str:
    try:
        return git(repo_root, "rev-parse", f"origin/{branch}")
    except subprocess.CalledProcessError:
        return git(repo_root, "rev-parse", "HEAD")


def repo_root_url(repo: str) -> str:
    return f"https://github.com/{GITHUB_ORG}/{repo}"


def tree_url(repo: str, branch: str) -> str:
    return f"{repo_root_url(repo)}/tree/{branch}"


def commit_url(repo: str, sha: str) -> str:
    return f"{repo_root_url(repo)}/commit/{sha}"


def render_group(name: str, entries: list[RepoEntry]) -> list[str]:
    lines = [f"## {name}", "", "| Repo | Purpose | Surface / deployment | Default branch | Current default-branch HEAD |", "| --- | --- | --- | --- | --- |"]
    for entry in entries:
        repo_path = WORKSPACE_ROOT / entry.name
        branch = default_branch(repo_path)
        sha = commit_sha(repo_path, branch)
        short_sha = sha[:7]
        lines.append(
            "| "
            f"[`{entry.name}`]({repo_root_url(entry.name)}) | "
            f"{entry.role} | "
            f"{entry.surface} | "
            f"[`{branch}`]({tree_url(entry.name, branch)}) | "
            f"[`{short_sha}`]({commit_url(entry.name, sha)}) |"
        )
    lines.append("")
    return lines


def main() -> None:
    lines = [
        "# Repo Map",
        "",
        "This file is the quick index for the active Kriegspiel repositories.",
        "",
        "It is grouped by responsibility so `ks-platform` can act as the main entry point for deployment and architecture work.",
        "",
        "## Link policy",
        "",
        "- Repo links go to the repository root for easy browsing.",
        "- Default-branch links go to `main` or `master` and are therefore always the latest branch view.",
        "- HEAD commit links are pinned snapshots of the current default-branch commit at generation time.",
        "- Use branch links for navigation and pinned commit links for rollout notes, audits, and deployment references.",
        "",
        "A single link cannot be both permanently pinned and always-latest. Keeping both link types is the safest pattern.",
        "",
        "## Workspace bootstrap",
        "",
        "Use [`scripts/bootstrap_workspace.py`](../scripts/bootstrap_workspace.py) after cloning `ks-platform` if you want this repo to act as the entry point for a fresh machine.",
        "",
        "That script clones the sibling repos into the same workspace root and creates the shared helper directories.",
        "",
    ]

    for group_name, entries in REPO_GROUPS.items():
        lines.extend(render_group(group_name, entries))

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
