# Wayforge

A spec-driven, multi-agent development CLI, installed the same way as [GitHub's spec-kit](https://github.com/github/spec-kit): with `uv tool install`, no marketplace or plugin registration required. It turns "build a feature" into a repeatable pipeline — **scope → plan → implement → review** — backed by living documentation (an architecture constitution, a data model, an API registry, and user stories) that every feature reads before touching code, and updates after.

`wayforge init` does the deterministic bootstrapping — scaffolds a FastAPI/React+Vite app (or your override), creates the `workflow/` living-docs tree, and drops the identical `/wayforge-new-feature`, `/wayforge-plan`, `/wayforge-apply`, `/wayforge-review`, and `/wayforge-adopt` skills straight into whichever coding agents you choose: **Claude Code**, **Cursor**, and/or **Codex**. Because the same skill file lands in every agent, a plan written in one can be applied or reviewed from another with no separate handoff format — `workflow/features/<slug>/implementation-plan.md` and `review.md` *are* the handoff.

Alongside the pipeline skills, `wayforge init` also installs a standalone set of review skills — `software-security-baseline`, `api-validation-principle`, and `clean-code-review` (ported from [coding-skills](https://github.com/mohammedashrafdagga/coding-skills)) — into the same agents. See [Review skills](#review-skills) below.

## Install

```bash
uv tool install wayforge-cli --from git+https://github.com/mohammedashrafdagga/Wayforge.git
```

Or run it once without installing:

```bash
uvx --from git+https://github.com/mohammedashrafdagga/Wayforge.git wayforge init my-project
```

To develop against a local checkout:

```bash
pip install -e /path/to/Wayforge
```

## Usage

```bash
wayforge init my-project             # greenfield: scaffolds FastAPI + React/Vite, prompts for scope/git-strategy
cd my-project
```

Launch your coding agent in the project directory, then:

1. **Scope** a feature (`/wayforge-new-feature "add a saved-searches feature to the search page"`).
2. **Plan** it (`/wayforge-plan`) — reads the constitution and real code patterns, asks about trade-offs instead of guessing, writes `implementation-plan.md`, creates the feature branch.
3. **Implement** it (`/wayforge-apply`) — executes the plan task by task. Runnable from any agent Wayforge was installed for.
4. **Review** it (`/wayforge-review`) — checks the implementation against the plan and the constitution, then (on a pass) additively merges the feature's docs into the three master docs.

For an existing codebase:

```bash
wayforge init my-existing-project --brownfield
```

then run `/wayforge-adopt` inside your coding agent — it inspects the codebase, drafts the constitution/data-model/API-registry, and asks you to confirm or correct before treating them as authoritative.

### `wayforge init` flags

| Flag | Default | Does |
|---|---|---|
| `--scope` | prompted | `backend`, `frontend`, or `both` — where `workflow/` and the app live |
| `--backend-framework` | `fastapi` | |
| `--frontend-framework` | `react-vite` | |
| `--architecture` | `ddd` | feature-based folders by default |
| `--git-strategy` | prompted | `mono`, `split` (backend/frontend branches), or `per-feature` branches |
| `--ai` | `claude,cursor,codex` | comma-separated agents to install `/wayforge-*` skills for |
| `--brownfield` / `--greenfield` | greenfield | brownfield skips scaffolding and leaves the constitution's stack fields for `/wayforge-adopt` to fill in |
| `--yes` / `-y` | off | accept defaults/flags without interactive prompts |
| `--force` | off | overwrite an existing `workflow/` tree at the target location |

## Why "additive-only" master docs

`workflow/data-model.md`, `workflow/api-registry.md`, and `workflow/user-stories.md` are the project's long-lived source of truth. A feature is only ever allowed to *append* to them — never rewrite an existing entry — so they stay trustworthy across dozens of features and multiple agents instead of drifting or getting silently overwritten. This is enforced by `.wayforge/scripts/validate_docs.py` (flags likely conflicts before merge — same entity name with different fields, colliding API routes, duplicate stories) and `.wayforge/scripts/merge_master_doc.py` (does the actual append, refuses on an unresolved conflict). Both get copied into every Wayforge-initialized project by `wayforge init`. See `workflow/constitution/conventions.md` (generated from `templates/constitution/conventions.md.tmpl`) for the full rule.

## Where agent skills land

| Agent | Pipeline skill folder | Review skill folder |
|---|---|---|
| Claude Code | `.claude/skills/wayforge-<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| Cursor | `.cursor/skills/wayforge-<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` |
| Codex CLI | `.agents/skills/wayforge-<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |

These are plain per-project skills, auto-discovered by each agent — no plugin/marketplace step. Codex's real skill-discovery folder is `.agents/`, not `.codex/`.

## Review skills

Three general-purpose review skills — maintained upstream at [mohammedashrafdagga/coding-skills](https://github.com/mohammedashrafdagga/coding-skills) and vendored here under `skills/` — ride along with every `wayforge init`, independent of the scope→plan→implement→review pipeline:

| Skill | Purpose |
|---|---|
| `software-security-baseline` | Establishes a minimum practical security baseline, then reviews only changed/affected security surfaces on later revisions. Writes `security/report_NNN.md`. |
| `api-validation-principle` | Establishes a full API baseline (routes, auth, validation, reliability), then validates changed/affected operations. Writes `docs/api_report/report_NNN.md`. |
| `clean-code-review` | Establishes a code-quality/architecture baseline, then reviews changed/affected features for maintainability and boundary violations. Writes `docs/clean-code-report/report_NNN.md`. |

Each is a full self-contained skill directory (`SKILL.md` + `references/` + `agents/`) copied as-is into every selected agent — unlike the `wayforge-*` pipeline skills, they aren't renamed or prefixed, and they aren't `wayforge init`-specific: ask any installed agent to "use `software-security-baseline` to review this app" (or the API/clean-code equivalents) and it runs, first-run building a full baseline report, later runs reviewing only what changed since the last recorded Git checkpoint.

## Repo layout (this CLI's own source)

```
Wayforge/
├── pyproject.toml                  # wayforge-cli package; entry point `wayforge`
├── src/wayforge_cli/
│   ├── __init__.py                 # Typer app
│   ├── _assets.py                  # locates the bundled templates/scripts/skills payload
│   └── commands/init.py            # `wayforge init`
├── templates/                      # doc templates wayforge init renders into workflow/, and copies into .wayforge/templates/
│   ├── constitution/architecture.md.tmpl
│   ├── constitution/conventions.md.tmpl
│   ├── data-model.md.tmpl
│   ├── api-registry.md.tmpl
│   ├── user-stories.md.tmpl
│   ├── implementation-plan.md.tmpl
│   └── review.md.tmpl
├── scripts/                        # copied into every initialized project's .wayforge/scripts/
│   ├── scaffold_project.sh         # FastAPI / React+Vite scaffolding
│   ├── merge_master_doc.py         # additive-only merge into a master doc
│   └── validate_docs.py            # pre-merge conflict guard
└── skills/
    ├── new-feature.md              # canonical /wayforge-* skill bodies, installed into every selected agent
    ├── plan.md
    ├── apply.md
    ├── review.md
    ├── adopt.md
    ├── software-security-baseline/ # standalone review skills, vendored from coding-skills and installed as-is
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    ├── api-validation-principle/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    └── clean-code-review/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/
```

`templates/`, `scripts/`, and `skills/` are bundled into the wheel via `pyproject.toml`'s `force-include` rules, so `wayforge init` works from an installed CLI with no need for this source repo to be present.

A project initialized with Wayforge ends up with its own `workflow/` (living docs) and `.wayforge/` (the templates/scripts bundle, copied in at init time) — this repo is the CLI that generates and manages those, not the trees themselves.
