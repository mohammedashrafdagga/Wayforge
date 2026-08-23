---
name: init
description: This skill should be used when the user asks to "start a new project with RSW", "initialize RealSoft Workflow", "set up the workflow structure", "scaffold a new project with living docs", "run /rsw:init", or wants a new greenfield project bootstrapped with a constitution, data model, API registry, and user-stories doc from day one.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# /rsw:init — Initialize a new RealSoft Workflow project

Bootstraps a brand-new (greenfield) project with the RealSoft Workflow (RSW) structure: a scaffolded FastAPI/React+Vite app (or an overridden stack), the `workflow/` living-docs tree, and the `.claude/`/`.cursor/`/`.codex/` agent folders. This is the only RSW skill that creates a new app from nothing — for an existing codebase, direct the user to `/rsw:adopt` instead.

## Step 1 — Ask the four scoping questions

Never assume these; ask explicitly (use `AskUserQuestion` when available):

1. **Scope** — whole project, backend only, or frontend only? This decides whether `workflow/` and the agent folders live at the repo root or inside `backend/`/`frontend/`.
2. **Framework** — default is FastAPI (backend) + React+Vite (frontend). Confirm, or record an override.
3. **Architecture** — default is DDD, feature-based folders (see `templates/constitution/architecture.md.tmpl`). Confirm, or record an override.
4. **Git strategy** — mono-repo single branch, split backend/frontend branches, or per-feature branches. This gets written into `constitution/conventions.md` and every later `/rsw:plan` run respects it.

Do not proceed past this step with defaults silently assumed — a wrong scope or git strategy is expensive to unwind later.

## Step 2 — Scaffold the app

Determine the target root from the scope answer (repo root, or `backend/`/`frontend/` inside it).

If the framework choices match the defaults (FastAPI and/or React+Vite), run:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/scaffold_project.sh \
  --root <target-root> --scope backend|frontend|both --project-name <project-name>
```

This creates a Python virtualenv, installs FastAPI/uvicorn/SQLAlchemy/pytest, and/or runs `npm create vite@latest` for the frontend, then does a minimal `/health` route as a smoke test. Read the script's stdout/stderr — it exits non-zero and explains itself if a prerequisite (python3, npm) is missing; surface that to the user rather than retrying silently.

If the user picked a **non-default** framework for either side, do not call the script for that side. Scaffold it manually following the user's stated framework, and note the deviation clearly in `constitution/architecture.md` (see Step 3) — the point of that file is to describe what's actually true, not the RSW defaults.

After scaffolding, do a smoke-test run (e.g. `uvicorn src.main:app --reload` briefly, or `npm run dev` briefly) to confirm the app boots before moving on. Stop the process afterward.

## Step 3 — Create the `workflow/` tree and agent folders

Inside the target root, create:

```
workflow/
├── constitution/
│   ├── architecture.md
│   ├── conventions.md
│   └── skills/
├── data-model.md
├── api-registry.md
├── user-stories.md
└── features/
.claude/
.cursor/
.codex/
```

Populate each file from its template under `${CLAUDE_PLUGIN_ROOT}/templates/`:

- `constitution/architecture.md` ← `templates/constitution/architecture.md.tmpl`, filling in `{{PROJECT_NAME}}`, `{{SCOPE}}`, `{{INIT_DATE}}` (today), `{{GIT_STRATEGY}}`, `{{BACKEND_FRAMEWORK}}`, `{{FRONTEND_FRAMEWORK}}`, `{{ARCHITECTURE_STYLE}}`, `{{DATABASE}}`, `{{PACKAGE_MANAGER}}`. Since this template already describes the *default* stack's real conventions, when the user's answers match the defaults this is close to a direct copy; when they diverge, edit the relevant section (e.g. the folder-layout block) to describe what was actually chosen instead of leaving default-stack prose that's now wrong.
- `constitution/conventions.md` ← `templates/constitution/conventions.md.tmpl`, filling in `{{GIT_STRATEGY}}`.
- `data-model.md`, `api-registry.md`, `user-stories.md` ← their respective `templates/*.md.tmpl`, unmodified (they start empty and fill in as features merge).

Leave `.claude/`, `.cursor/`, `.codex/` empty for now — `/rsw:plan` and `/rsw:review` populate the handoff files when the first feature reaches that stage.

## Step 4 — Report back

Summarize what was created (scaffolded app location, workflow tree location, confirmed scope/framework/architecture/git-strategy) and point the user at `/rsw:new-feature "<description>"` as the next step.

## Notes

- If any answer diverges from the default stack, make sure that divergence is reflected concretely in `constitution/architecture.md` — a constitution that still describes FastAPI conventions for a Django project actively misleads every later `/rsw:plan` run.
- This skill never touches an existing `workflow/` directory — if one is found, stop and tell the user `/rsw:init` is for new projects only; point them at `/rsw:adopt` if they meant to retrofit an existing codebase.
