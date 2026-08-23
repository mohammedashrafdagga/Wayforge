# RealSoft Workflow (RSW)

A spec-driven, multi-agent development CLI, installed the same way as [GitHub's spec-kit](https://github.com/github/spec-kit): with `uv tool install`, no marketplace or plugin registration required. It turns "build a feature" into a repeatable pipeline — **scope → plan → implement → review** — backed by living documentation (an architecture constitution, a data model, an API registry, and user stories) that every feature reads before touching code, and updates after.

`rsw init` does the deterministic bootstrapping — scaffolds a FastAPI/React+Vite app (or your override), creates the `workflow/` living-docs tree, and drops the identical `/rsw-new-feature`, `/rsw-plan`, `/rsw-apply`, `/rsw-review`, and `/rsw-adopt` skills straight into whichever coding agents you choose: **Claude Code**, **Cursor**, and/or **Codex**. Because the same skill file lands in every agent, a plan written in one can be applied or reviewed from another with no separate handoff format — `workflow/features/<slug>/implementation-plan.md` and `review.md` *are* the handoff.

## Install

```bash
uv tool install rsw-cli --from git+https://github.com/mohammedashrafdagga/realsoft-workflow.git
```

Or run it once without installing:

```bash
uvx --from git+https://github.com/mohammedashrafdagga/realsoft-workflow.git rsw init my-project
```

To develop against a local checkout:

```bash
pip install -e /path/to/realsoft-workflow
```

## Usage

```bash
rsw init my-project                 # greenfield: scaffolds FastAPI + React/Vite, prompts for scope/git-strategy
cd my-project
```

Launch your coding agent in the project directory, then:

1. **Scope** a feature (`/rsw-new-feature "add a saved-searches feature to the search page"`).
2. **Plan** it (`/rsw-plan`) — reads the constitution and real code patterns, asks about trade-offs instead of guessing, writes `implementation-plan.md`, creates the feature branch.
3. **Implement** it (`/rsw-apply`) — executes the plan task by task. Runnable from any agent RSW was installed for.
4. **Review** it (`/rsw-review`) — checks the implementation against the plan and the constitution, then (on a pass) additively merges the feature's docs into the three master docs.

For an existing codebase:

```bash
rsw init my-existing-project --brownfield
```

then run `/rsw-adopt` inside your coding agent — it inspects the codebase, drafts the constitution/data-model/API-registry, and asks you to confirm or correct before treating them as authoritative.

### `rsw init` flags

| Flag | Default | Does |
|---|---|---|
| `--scope` | prompted | `backend`, `frontend`, or `both` — where `workflow/` and the app live |
| `--backend-framework` | `fastapi` | |
| `--frontend-framework` | `react-vite` | |
| `--architecture` | `ddd` | feature-based folders by default |
| `--git-strategy` | prompted | `mono`, `split` (backend/frontend branches), or `per-feature` branches |
| `--ai` | `claude,cursor,codex` | comma-separated agents to install `/rsw-*` skills for |
| `--brownfield` / `--greenfield` | greenfield | brownfield skips scaffolding and leaves the constitution's stack fields for `/rsw-adopt` to fill in |
| `--yes` / `-y` | off | accept defaults/flags without interactive prompts |
| `--force` | off | overwrite an existing `workflow/` tree at the target location |

## Why "additive-only" master docs

`workflow/data-model.md`, `workflow/api-registry.md`, and `workflow/user-stories.md` are the project's long-lived source of truth. A feature is only ever allowed to *append* to them — never rewrite an existing entry — so they stay trustworthy across dozens of features and multiple agents instead of drifting or getting silently overwritten. This is enforced by `.rsw/scripts/validate_docs.py` (flags likely conflicts before merge — same entity name with different fields, colliding API routes, duplicate stories) and `.rsw/scripts/merge_master_doc.py` (does the actual append, refuses on an unresolved conflict). Both get copied into every RSW-initialized project by `rsw init`. See `workflow/constitution/conventions.md` (generated from `templates/constitution/conventions.md.tmpl`) for the full rule.

## Where agent skills land

| Agent | Skill folder |
|---|---|
| Claude Code | `.claude/skills/rsw-<name>/SKILL.md` |
| Cursor | `.cursor/skills/rsw-<name>/SKILL.md` |
| Codex CLI | `.agents/skills/rsw-<name>/SKILL.md` |

These are plain per-project skills, auto-discovered by each agent — no plugin/marketplace step. Codex's real skill-discovery folder is `.agents/`, not `.codex/`.

## Repo layout (this CLI's own source)

```
realsoft-workflow/
├── pyproject.toml                  # rsw-cli package; entry point `rsw`
├── src/rsw_cli/
│   ├── __init__.py                 # Typer app
│   ├── _assets.py                  # locates the bundled templates/scripts/skills payload
│   └── commands/init.py            # `rsw init`
├── templates/                      # doc templates rsw init renders into workflow/, and copies into .rsw/templates/
│   ├── constitution/architecture.md.tmpl
│   ├── constitution/conventions.md.tmpl
│   ├── data-model.md.tmpl
│   ├── api-registry.md.tmpl
│   ├── user-stories.md.tmpl
│   ├── implementation-plan.md.tmpl
│   └── review.md.tmpl
├── scripts/                        # copied into every initialized project's .rsw/scripts/
│   ├── scaffold_project.sh         # FastAPI / React+Vite scaffolding
│   ├── merge_master_doc.py         # additive-only merge into a master doc
│   └── validate_docs.py            # pre-merge conflict guard
└── skills/                         # canonical /rsw-* skill bodies, installed into every selected agent
    ├── new-feature.md
    ├── plan.md
    ├── apply.md
    ├── review.md
    └── adopt.md
```

`templates/`, `scripts/`, and `skills/` are bundled into the wheel via `pyproject.toml`'s `force-include` rules, so `rsw init` works from an installed CLI with no need for this source repo to be present.

A project initialized with RSW ends up with its own `workflow/` (living docs) and `.rsw/` (the templates/scripts bundle, copied in at init time) — this repo is the CLI that generates and manages those, not the trees themselves.
