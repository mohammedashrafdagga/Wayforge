"""Locate Wayforge's bundled docs-template / script / skill payload (the "core pack").

When installed from a built wheel (`uv tool install wayforge-cli`, or
`uv tool install wayforge-cli --from git+...`), hatchling's force-include rules
copy the repo's top-level `templates/`, `scripts/`, and `skills/` directories
into `wayforge_cli/core_pack/` inside the wheel — see `pyproject.toml`. At runtime
that lands as a sibling directory of this file.

When running from an unbuilt source checkout (`python -m wayforge_cli`, or an
editable install), no wheel-build step ran, so `core_pack/` won't exist next
to this file. Fall back to walking up from this file to find the repo root
(identified by a sibling `pyproject.toml`) and use its top-level
`templates/`/`scripts/`/`skills/` directly.
"""
from __future__ import annotations

from pathlib import Path


def _wheel_core_pack() -> Path | None:
    candidate = Path(__file__).parent / "core_pack"
    if candidate.is_dir():
        return candidate
    return None


def _dev_repo_root() -> Path | None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").is_file() and (parent / "templates").is_dir():
            return parent
    return None


def templates_dir() -> Path:
    core = _wheel_core_pack()
    if core is not None:
        return core / "templates"
    root = _dev_repo_root()
    if root is not None:
        return root / "templates"
    raise RuntimeError("could not locate Wayforge's bundled templates/ directory")


def scripts_dir() -> Path:
    core = _wheel_core_pack()
    if core is not None:
        return core / "scripts"
    root = _dev_repo_root()
    if root is not None:
        return root / "scripts"
    raise RuntimeError("could not locate Wayforge's bundled scripts/ directory")


def skills_dir() -> Path:
    core = _wheel_core_pack()
    if core is not None:
        return core / "skills"
    root = _dev_repo_root()
    if root is not None:
        return root / "skills"
    raise RuntimeError("could not locate Wayforge's bundled skills/ directory")
