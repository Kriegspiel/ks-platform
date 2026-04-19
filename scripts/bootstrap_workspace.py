#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from workspace_repos import iter_repo_entries, optional_repo_entries, required_repo_entries


PLATFORM_ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap the Kriegspiel multi-repo workspace from a single ks-platform checkout."
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=PLATFORM_ROOT.parent,
        help="Workspace root where sibling repos should live. Defaults to the parent of this ks-platform checkout.",
    )
    parser.add_argument(
        "--include-bots",
        action="store_true",
        help="Clone the optional bot repos too.",
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Fetch existing clones instead of leaving them untouched.",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        help="Clone via HTTPS instead of SSH.",
    )
    return parser.parse_args()


def ensure_workspace_dirs(root: Path) -> None:
    for relative in ("_wroktrees", "_tmp", ".site-refresh"):
        (root / relative).mkdir(parents=True, exist_ok=True)


def repo_url(entry_name: str, use_https: bool) -> str:
    for entry in iter_repo_entries():
        if entry.name == entry_name:
            return entry.https_url if use_https else entry.ssh_url
    raise KeyError(entry_name)


def sync_repo(root: Path, repo_name: str, use_https: bool, update_existing: bool) -> str:
    target = root / repo_name
    if target.exists():
        if not (target / ".git").exists():
            raise RuntimeError(f"Refusing to use existing non-git directory: {target}")
        if update_existing and (target / ".git").exists():
            run("git", "-C", str(target), "fetch", "--all", "--prune")
            return f"updated existing clone: {repo_name}"
        return f"kept existing clone: {repo_name}"

    run("git", "clone", repo_url(repo_name, use_https), str(target))
    return f"cloned: {repo_name}"


def main() -> int:
    args = parse_args()
    workspace_root = args.workspace_root.resolve()
    workspace_root.mkdir(parents=True, exist_ok=True)
    ensure_workspace_dirs(workspace_root)

    wanted = [entry.name for entry in required_repo_entries() if entry.name != "ks-platform"]
    if args.include_bots:
        wanted.extend(entry.name for entry in optional_repo_entries())

    actions: list[str] = []
    for repo_name in wanted:
        actions.append(sync_repo(workspace_root, repo_name, args.https, args.update_existing))

    print(f"Workspace root: {workspace_root}")
    print(f"ks-platform checkout: {PLATFORM_ROOT}")
    print("")
    print("Repo sync results:")
    for action in actions:
        print(f"- {action}")

    print("")
    print("Workspace directories ensured:")
    for relative in ("_wroktrees", "_tmp", ".site-refresh"):
        print(f"- {workspace_root / relative}")

    print("")
    print("Next steps:")
    print(f"- Read {PLATFORM_ROOT / 'README.md'}")
    print(f"- Read {PLATFORM_ROOT / 'AGENTS.md'}")
    print(f"- Read {PLATFORM_ROOT / 'deployment' / 'new-server-bootstrap.md'}")
    print(f"- Read {PLATFORM_ROOT / 'deployment' / 'bootstrap-and-startup.md'}")
    print("- Create the required env files before starting services.")
    print("- Install repo-local dependencies inside each cloned repo as needed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"bootstrap failed while running: {' '.join(exc.cmd)}", file=sys.stderr)
        raise SystemExit(exc.returncode)
    except RuntimeError as exc:
        print(f"bootstrap failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
