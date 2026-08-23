# RealSoft Workflow (RSW)

A spec-driven, multi-agent development workflow, distributed as a Claude Code plugin. It turns "build a feature" into a repeatable pipeline — **scope → plan → implement → review** — backed by living documentation (an architecture constitution, a data model, an API registry, and user stories) that every feature reads before touching code, and updates after.

It targets three coding agents from day one: **Claude Code** (the planning/foundation brain), **Cursor** (implementation), and **Codex** (review) — via manual, artifact-based handoff. There's no CLI auto-invocation of Cursor/Codex in v1; RSW writes self-contained instruction files into `.cursor/` and `.codex/` and you open them in that tool yourself.

## Install

```bash
claude plugin marketplace add mohammedashrafdagga/realsoft-workflow
claude plugin install rsw
```

Or, to develop against a local checkout:

```bash
claude --plugin-dir /path/to/realsoft-workflow
```

## Commands

| Command | Does |
|---|---|
| `/rsw:init` | Bootstrap a brand-new project: scaffolds FastAPI/React+Vite (or your override), creates `workflow/` + `.claude/`/`.cursor/`/`.codex/`, writes a constitution pre-filled for the default stack. |
| `/rsw:adopt` | Retrofit RSW onto an existing codebase: inspects it, drafts the constitution/data-model/API-registry, and requires your confirmation before treating them as authoritative. |
| `/rsw:new-feature "<description>"` | Checks a new feature idea against the constitution and all three master docs, then writes the feature's own `user-stories.md` and `data-model.md`. |
| `/rsw:plan` | Reads the feature's docs + the constitution + real patterns already in your codebase; surfaces trade-offs as questions instead of guessing; writes `implementation-plan.md`; creates the feature branch. |
| `/rsw:apply` | Executes the plan task by task. Also runnable from Cursor via the handoff file `/rsw:plan` generates. |
| `/rsw:review` | Checks the implementation against the plan's acceptance criteria and the constitution, writes `review.md`, and — only on a pass — additively merges the feature's docs into the three master docs. Also runnable from Codex via its handoff file. |

## Why "additive-only" master docs

`workflow/data-model.md`, `workflow/api-registry.md`, and `workflow/user-stories.md` are the project's long-lived source of truth. A feature is only ever allowed to *append* to them — never rewrite an existing entry — so they stay trustworthy across dozens of features and multiple agents instead of drifting or getting silently overwritten. This is enforced by `scripts/validate_docs.py` (flags likely conflicts before merge — same entity name with different fields, colliding API routes, duplicate stories) and `scripts/merge_master_doc.py` (does the actual append, refuses on an unresolved conflict). See `templates/constitution/conventions.md.tmpl` for the full rule.

## Repo layout

```
realsoft-workflow/
├── .claude-plugin/plugin.json      # plugin manifest
├── skills/                         # /rsw:init, /rsw:adopt, /rsw:new-feature, /rsw:plan, /rsw:apply, /rsw:review
├── templates/                      # constitution, data-model, api-registry, user-stories,
│                                    # implementation-plan, review, and Cursor/Codex handoff templates
└── scripts/
    ├── scaffold_project.sh         # FastAPI / React+Vite scaffolding for /rsw:init
    ├── merge_master_doc.py         # additive-only merge into a master doc
    └── validate_docs.py            # pre-merge conflict guard
```

A project built with RSW ends up with its own, separate `workflow/` tree — this repo is the plugin that generates and manages it, not the tree itself.

## Status

v1 in progress. See the design notes this was built from for the full phased build plan and open risks (additive-only enforcement, trade-off surfacing quality, handoff-artifact staleness, Mermaid-block merge safety).
