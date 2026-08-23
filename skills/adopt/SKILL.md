---
name: adopt
description: This skill should be used when the user asks to "adopt RSW into an existing project", "retrofit the workflow structure", "run /rsw:adopt", "add living docs to an existing codebase", or wants RealSoft Workflow's constitution/data-model/api-registry/user-stories set up for a brownfield project by inspecting the code that's already there.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /rsw:adopt — Retrofit RealSoft Workflow onto an existing project

Retrofits the `workflow/` living-docs tree onto a codebase that already exists, by inspecting it rather than scaffolding a new one. This is the brownfield counterpart to `/rsw:init` — same target structure, no new app created, and a mandatory human-confirmation step before any inferred doc becomes authoritative.

## Step 1 — Ask the same scoping questions as `/rsw:init`, minus scaffolding

1. **Scope** — whole project, backend only, or frontend only?
2. **Framework** — what's actually in use already? (Don't assume FastAPI/React+Vite — detect first, per Step 2, then confirm with the user rather than asking blind.)
3. **Architecture** — is there already a discernible pattern (DDD-ish, layered, something else)? Detect, then confirm.
4. **Git strategy** — mono-repo single branch, split backend/frontend branches, or per-feature branches, going forward from here.

## Step 2 — Inspect the existing codebase

Before asking the framework/architecture questions in detail, do enough inspection to ask informed questions rather than generic ones:

- **Framework detection**: check `pyproject.toml`/`requirements.txt`/`package.json` for FastAPI, Django, Flask, Express, Next.js, etc.
- **Folder pattern**: `Glob` the top 2-3 levels of `src`/`app` to see whether it's feature-based, layer-based (`models/`, `services/`, `controllers/`), or something ad hoc.
- **Entities**: `Grep` for ORM model base classes (SQLAlchemy `Base`, Django `models.Model`, Pydantic-with-table markers, Prisma schema, etc.) to build a first-pass entity list with their fields.
- **Endpoints**: `Grep` for route decorators/registrations (`@app.get`, `@router.post`, Django `urls.py`, Express `app.get(...)`, etc.) to build a first-pass endpoint list with method + path.
- **Existing docs**: check for a README, existing architecture docs, OpenAPI/Swagger output — these are strong signal and should be read fully, not just grepped.

Budget this as a real but bounded pass — enough to draft credible docs, not an exhaustive audit of every file.

## Step 3 — Draft the docs (not yet authoritative)

Using the inspection results, draft:

- `constitution/architecture.md` from `templates/constitution/architecture.md.tmpl`, but with the stack/folder-layout sections rewritten to describe what was *actually found*, not the RSW defaults, unless the defaults genuinely match.
- `constitution/conventions.md` from its template, with `{{GIT_STRATEGY}}` filled from Step 1's answer.
- `data-model.md` from its template, with one `##` entity section per entity found, each with a best-effort field table and, where a clear relationship set was found, a Mermaid `erDiagram` block.
- `api-registry.md` from its template, with endpoints grouped under a best-guess feature grouping (infer from folder/route-prefix structure; if nothing clean presents itself, group under a single `## core` section rather than inventing false feature boundaries).

Leave `user-stories.md` from its template mostly empty — user stories aren't reliably inferable from code; note this to the user rather than fabricating stories to fill the doc.

## Step 4 — Present drafts for correction (mandatory, do not skip)

Show the user the drafted `architecture.md`, `data-model.md`, and `api-registry.md` (or a clear summary with the option to see the full file) and explicitly ask them to confirm or correct before writing them to `workflow/`. State plainly: **a wrong auto-generated constitution is worse than none**, because every later `/rsw:new-feature` and `/rsw:plan` run trusts these docs. Do not write the files as final until the user has responded — this step is not a formality.

Apply the user's corrections, then write the final versions into `workflow/`.

## Step 5 — Create the remaining structure

Same as `/rsw:init` Step 3: create `workflow/features/`, `.claude/`, `.cursor/`, `.codex/` (empty, populated later by `/rsw:plan`/`/rsw:review`).

## Step 6 — Report back

Summarize what was inspected, what was drafted, what the user corrected, and point at `/rsw:new-feature "<description>"` as the next step. Flag explicitly if `user-stories.md` was left empty so the user knows to backfill it or start fresh from the first feature.

## Notes

- If `workflow/` already exists, stop and tell the user `/rsw:adopt` is for a codebase that doesn't have RSW structure yet — point them at editing the existing docs directly, or ask whether they want the inspection re-run to supplement (not overwrite) the existing docs, in which case treat it as a normal additive merge via `${CLAUDE_PLUGIN_ROOT}/scripts/merge_master_doc.py`, not a fresh overwrite.
