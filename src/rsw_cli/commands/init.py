"""`rsw init` — bootstrap a project with RSW's living docs and agent skills."""
from __future__ import annotations

import shutil
import stat
import subprocess
from datetime import date
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from .. import _assets

console = Console()

AGENT_SKILL_DIRS = {
    "claude": ".claude/skills",
    "cursor": ".cursor/skills",
    "codex": ".agents/skills",
}

SKILL_NAMES = ["new-feature", "plan", "apply", "review", "adopt"]

GIT_STRATEGY_LABELS = {
    "mono": "mono-repo single branch",
    "split": "split backend/frontend branches",
    "per-feature": "per-feature branches",
}

SCOPE_CHOICES = ["backend", "frontend", "both"]
GIT_STRATEGY_CHOICES = list(GIT_STRATEGY_LABELS)


def _resolve_workflow_root(project_path: Path, scope: str) -> Path:
    if scope == "backend":
        return project_path / "backend"
    if scope == "frontend":
        return project_path / "frontend"
    return project_path


def _render(text: str, subs: dict[str, str]) -> str:
    for key, value in subs.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def _copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)


def _make_executable(directory: Path) -> None:
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix in (".sh", ".py"):
            mode = path.stat().st_mode
            path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def init_command(
    project_dir: str = typer.Argument(
        ".", help="Directory to initialize (created if missing). Use '.' for the current directory."
    ),
    scope: Optional[str] = typer.Option(
        None, "--scope", help="backend | frontend | both — where workflow/ and the app live."
    ),
    backend_framework: str = typer.Option("fastapi", "--backend-framework"),
    frontend_framework: str = typer.Option("react-vite", "--frontend-framework"),
    architecture: str = typer.Option("ddd", "--architecture", help="Architecture style (default: DDD, feature-based folders)."),
    git_strategy: Optional[str] = typer.Option(
        None, "--git-strategy", help="mono | split | per-feature"
    ),
    ai: str = typer.Option(
        "claude,cursor,codex", "--ai", help="Comma-separated agents to install /rsw-* skills for: claude,cursor,codex."
    ),
    brownfield: bool = typer.Option(
        False, "--brownfield/--greenfield",
        help="Brownfield: skip app scaffolding, leave the constitution's stack fields for /rsw-adopt to fill in.",
    ),
    project_name: Optional[str] = typer.Option(None, "--project-name"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Accept defaults/flags without interactive prompts."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing workflow/ tree at the target location."),
) -> None:
    """Bootstrap a project with RSW's workflow/ living docs and /rsw-* agent skills."""
    project_path = Path(project_dir).resolve()
    project_path.mkdir(parents=True, exist_ok=True)
    name = project_name or project_path.name

    if scope is None:
        scope = "both" if yes else Prompt.ask("Scope", choices=SCOPE_CHOICES, default="both")
    elif scope not in SCOPE_CHOICES:
        console.print(f"[red]--scope must be one of {SCOPE_CHOICES}, got '{scope}'[/red]")
        raise typer.Exit(1)

    if git_strategy is None:
        git_strategy = "mono" if yes else Prompt.ask(
            "Git strategy", choices=GIT_STRATEGY_CHOICES, default="mono"
        )
    elif git_strategy not in GIT_STRATEGY_CHOICES:
        console.print(f"[red]--git-strategy must be one of {GIT_STRATEGY_CHOICES}, got '{git_strategy}'[/red]")
        raise typer.Exit(1)

    agents = [a.strip() for a in ai.split(",") if a.strip()]
    unknown = [a for a in agents if a not in AGENT_SKILL_DIRS]
    if unknown:
        console.print(f"[red]--ai has unknown agent(s) {unknown}; supported: {list(AGENT_SKILL_DIRS)}[/red]")
        raise typer.Exit(1)
    if not agents:
        console.print("[red]--ai must name at least one agent[/red]")
        raise typer.Exit(1)

    workflow_root = _resolve_workflow_root(project_path, scope)
    workflow_dir = workflow_root / "workflow"

    if workflow_dir.exists() and not force:
        console.print(
            f"[red]{workflow_dir} already exists.[/red] Use --force to overwrite, or run `/rsw-adopt` "
            "inside an already-installed agent to add to it additively instead of re-initializing."
        )
        raise typer.Exit(1)

    templates_src = _assets.templates_dir()
    scripts_src = _assets.scripts_dir()
    skills_src = _assets.skills_dir()

    # --- 1. Scaffold the app (greenfield only) ---
    if not brownfield:
        scaffold_script = scripts_src / "scaffold_project.sh"
        console.print(Panel.fit(f"Scaffolding {scope} (backend_framework={backend_framework}, frontend_framework={frontend_framework})"))
        result = subprocess.run(
            [
                "bash", str(scaffold_script),
                "--root", str(project_path),
                "--scope", scope,
                "--project-name", name,
                "--backend-framework", backend_framework,
                "--frontend-framework", frontend_framework,
            ],
            cwd=str(project_path),
        )
        if result.returncode != 0:
            console.print("[red]Scaffolding failed — see output above. Fix the issue and re-run, or pass --brownfield to skip scaffolding.[/red]")
            raise typer.Exit(result.returncode)
    else:
        console.print("[yellow]--brownfield set: skipping app scaffolding. Run `/rsw-adopt` inside your coding agent after this to infer the stack/data-model/API registry from the existing code.[/yellow]")

    # --- 1b. Write a .gitignore covering what scaffolding/tooling produces ---
    gitignore_path = project_path / ".gitignore"
    gitignore_lines = [
        ".venv/", "__pycache__/", "*.pyc", "node_modules/", ".DS_Store",
    ]
    existing = gitignore_path.read_text().splitlines() if gitignore_path.exists() else []
    merged = existing + [line for line in gitignore_lines if line not in existing]
    gitignore_path.write_text("\n".join(merged) + "\n")

    # --- 2. Create workflow/ tree from templates ---
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "constitution").mkdir(exist_ok=True)
    (workflow_dir / "constitution" / "skills").mkdir(exist_ok=True)
    (workflow_dir / "features").mkdir(exist_ok=True)
    (workflow_dir / "features" / ".gitkeep").touch()

    git_strategy_label = GIT_STRATEGY_LABELS[git_strategy]

    if brownfield:
        stack_subs = {
            "BACKEND_FRAMEWORK": "TBD — run /rsw-adopt to infer from the existing codebase",
            "FRONTEND_FRAMEWORK": "TBD — run /rsw-adopt to infer from the existing codebase",
            "ARCHITECTURE_STYLE": "TBD — run /rsw-adopt to infer from the existing codebase",
            "DATABASE": "TBD — run /rsw-adopt to infer from the existing codebase",
            "PACKAGE_MANAGER": "TBD — run /rsw-adopt to infer from the existing codebase",
        }
    else:
        stack_subs = {
            "BACKEND_FRAMEWORK": backend_framework,
            "FRONTEND_FRAMEWORK": frontend_framework,
            "ARCHITECTURE_STYLE": architecture,
            "DATABASE": "TBD — fill in once a database is chosen",
            "PACKAGE_MANAGER": "pip/venv (backend), npm (frontend)",
        }

    common_subs = {
        "PROJECT_NAME": name,
        "SCOPE": scope,
        "INIT_DATE": date.today().isoformat(),
        "GIT_STRATEGY": git_strategy_label,
        **stack_subs,
    }

    architecture_tmpl = (templates_src / "constitution" / "architecture.md.tmpl").read_text()
    (workflow_dir / "constitution" / "architecture.md").write_text(_render(architecture_tmpl, common_subs))

    conventions_tmpl = (templates_src / "constitution" / "conventions.md.tmpl").read_text()
    (workflow_dir / "constitution" / "conventions.md").write_text(
        _render(conventions_tmpl, {"GIT_STRATEGY": git_strategy_label})
    )

    for doc in ("data-model.md", "api-registry.md", "user-stories.md"):
        (workflow_dir / doc).write_text((templates_src / f"{doc}.tmpl").read_text())

    # --- 3. Copy the .rsw/ tooling bundle (templates + scripts) into the project ---
    rsw_dir = workflow_root / ".rsw"
    _copy_tree(templates_src, rsw_dir / "templates")
    _copy_tree(scripts_src, rsw_dir / "scripts")
    _make_executable(rsw_dir / "scripts")

    # --- 4. Install /rsw-* skills for each selected agent ---
    installed: dict[str, list[str]] = {}
    for agent in agents:
        agent_base = workflow_root / AGENT_SKILL_DIRS[agent]
        installed[agent] = []
        for skill in SKILL_NAMES:
            content = (skills_src / f"{skill}.md").read_text()
            skill_dir = agent_base / f"rsw-{skill}"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(content)
            installed[agent].append(f"rsw-{skill}")

    # --- 5. Report ---
    console.print()
    console.print(Panel.fit(f"[bold green]RSW initialized[/bold green] at {workflow_root}", title="rsw init"))
    console.print(f"  workflow docs: [cyan]{workflow_dir}[/cyan]")
    console.print(f"  tooling bundle: [cyan]{rsw_dir}[/cyan]")
    for agent, skills in installed.items():
        skill_list = ", ".join(f"/{s}" for s in skills)
        console.print(f"  {agent}: [cyan]{workflow_root / AGENT_SKILL_DIRS[agent]}[/cyan] → {skill_list}")

    console.print()
    console.print("Next steps:")
    console.print(f"  cd {workflow_root}")
    if brownfield:
        console.print("  launch your coding agent, then run [bold]/rsw-adopt[/bold]")
    else:
        console.print('  launch your coding agent, then run [bold]/rsw-new-feature "<describe your first feature>"[/bold]')
