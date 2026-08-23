"""RealSoft Workflow (RSW) — spec-driven, multi-agent development CLI."""
from __future__ import annotations

import typer

from .commands.init import init_command

__version__ = "0.1.0"

app = typer.Typer(
    name="rsw",
    help="RealSoft Workflow — bootstrap a project with living docs and /rsw-* skills for Claude Code, Cursor, and Codex.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("init")(init_command)


@app.callback(invoke_without_command=False)
def _root() -> None:
    """RealSoft Workflow (RSW)."""


def main() -> None:
    app()


if __name__ == "__main__":
    main()
