#!/usr/bin/env python3
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass


GITHUB_ORG = "Kriegspiel"


@dataclass(frozen=True)
class RepoEntry:
    name: str
    role: str
    surface: str
    required: bool = True

    @property
    def ssh_url(self) -> str:
        return f"git@github.com:{GITHUB_ORG}/{self.name}.git"

    @property
    def https_url(self) -> str:
        return f"https://github.com/{GITHUB_ORG}/{self.name}.git"


REPO_GROUPS = OrderedDict(
    [
        (
            "Core services",
            [
                RepoEntry(
                    "ks-backend",
                    "FastAPI backend for API contracts, persistence, ratings, auth, and transcripts",
                    "`api.kriegspiel.org`, `ks-backend.service`",
                ),
                RepoEntry(
                    "ks-web-app",
                    "Authenticated React frontend for lobby, play, review, profiles, and reports",
                    "`app.kriegspiel.org`, `ks-web-app-frontend.service`",
                ),
                RepoEntry(
                    "ks-home",
                    "Static public site renderer and server for the marketing/docs website",
                    "`kriegspiel.org`, `ks-home.service`",
                ),
            ],
        ),
        (
            "Content and shared library",
            [
                RepoEntry(
                    "content",
                    "Source-of-truth content for blog, changelog, rules, and site copy",
                    "Consumed by `ks-home` during refresh/build",
                ),
                RepoEntry(
                    "ks-game",
                    "Python Kriegspiel engine library, move objects, and serialization",
                    "Library dependency, published to PyPI",
                ),
            ],
        ),
        (
            "Bots",
            [
                RepoEntry(
                    "bot-random",
                    "Baseline random bot",
                    "`kriegspiel-random-bot.service`",
                    required=False,
                ),
                RepoEntry(
                    "bot-random-any",
                    "Random bot that asks pawn-capture questions first",
                    "`kriegspiel-random-any-bot.service`",
                    required=False,
                ),
                RepoEntry(
                    "bot-simple-heuristics",
                    "Heuristic bot with recapture, promotion, and weighted choice logic",
                    "`kriegspiel-simple-heuristics-bot.service`",
                    required=False,
                ),
                RepoEntry(
                    "bot-gpt-nano",
                    "OpenAI-driven model bot",
                    "`kriegspiel-gpt-nano-bot.service`",
                    required=False,
                ),
                RepoEntry(
                    "bot-haiku",
                    "Anthropic-driven model bot",
                    "`kriegspiel-haiku-bot.service`",
                    required=False,
                ),
            ],
        ),
        (
            "Platform and operations",
            [
                RepoEntry(
                    "ks-platform",
                    "Org-level documentation, deployment handbook, and operator memory",
                    "Documentation-only handbook repo",
                ),
            ],
        ),
    ]
)


def iter_repo_entries() -> list[RepoEntry]:
    return [entry for group in REPO_GROUPS.values() for entry in group]


def required_repo_entries() -> list[RepoEntry]:
    return [entry for entry in iter_repo_entries() if entry.required]


def optional_repo_entries() -> list[RepoEntry]:
    return [entry for entry in iter_repo_entries() if not entry.required]
