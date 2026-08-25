---
name: wayforge-adopt
description: This skill should be used when the user asks to "adopt Wayforge into this codebase", "fill in the constitution from the existing code", "run /wayforge-adopt", or has just run `wayforge init --brownfield` and needs the drafted constitution, data model, and API registry inferred from a codebase that already exists. Requires human confirmation before any inferred doc becomes authoritative.
---

# /wayforge-adopt — Infer the living docs from an existing codebase

`wayforge init --brownfield` (run from a terminal, not this skill) already created the `workflow/` skeleton with placeholder docs and installed this skill — it deliberately does not attempt to infer anything about the codebase itself, because that requires reading and reasoning about real code, not just scaffolding folders. That inference is this skill's job.

## Step 0 — Confirm the skeleton exists

Check for `workflow/constitution/architecture.md` with unfilled stack/framework fields (or any other sign `wayforge init --brownfield` already ran). If `workflow/` doesn't exist at all, stop and tell the user to run `wayforge init --brownfield` from a terminal first.

## Step 1 — Inspect the existing codebase

Do enough inspection to draft credible docs — a real but bounded pass, not an exhaustive audit of every file:

- **Framework detection**: check `pyproject.toml`/`requirements.txt`/`package.json` for FastAPI, Django, Flask, Express, Next.js, etc.
- **Folder pattern**: look at the top 2-3 levels of `src`/`app` to see whether it's feature-based, layer-based (`models/`, `services/`, `controllers/`), or ad hoc.
- **Entities**: search for ORM model base classes (SQLAlchemy `Base`, Django `models.Model`, Prisma schema, etc.) to build a first-pass entity list with their fields.
- **Endpoints**: search for route decorators/registrations (`@app.get`, `@router.post`, Django `urls.py`, Express `app.get(...)`, etc.) to build a first-pass endpoint list with method + path.
- **Existing docs**: read any README or architecture docs already in the repo fully — they're stronger signal than inference from code and should shape the draft directly.

## Step 2 — Draft the docs (not yet authoritative)

Using the inspection results:

- Fill in `workflow/constitution/architecture.md`'s stack/folder-layout sections to describe what was *actually found*, not Wayforge's defaults, unless the defaults genuinely match.
- Fill in `workflow/constitution/conventions.md`'s git-strategy line if it wasn't already set by `wayforge init --brownfield`.
- Draft `workflow/data-model.md` following `.wayforge/templates/data-model.md.tmpl`'s per-entity `##` shape, one section per entity found, each with a best-effort field table and, where a clear relationship set was found, a Mermaid `erDiagram` block. Mark each entity's `**Feature:**` as `core` since these predate any Wayforge feature.
- Draft `workflow/api-registry.md` following `.wayforge/templates/api-registry.md.tmpl`'s grouped shape, with endpoints grouped under a best-guess feature grouping (infer from folder/route-prefix structure; if nothing clean presents itself, group under a single `## core` section rather than inventing false feature boundaries).

Leave `workflow/user-stories.md` mostly empty — user stories aren't reliably inferable from code; note this to the user rather than fabricating stories to fill the doc.

## Step 3 — Present drafts for correction (mandatory, do not skip)

Show the user the drafted `architecture.md`, `data-model.md`, and `api-registry.md` (or a clear summary with the option to see the full file) and explicitly ask them to confirm or correct before treating them as final. State plainly: **a wrong auto-generated constitution is worse than none**, because every later `/wayforge-new-feature` and `/wayforge-plan` run trusts these docs. Do not consider the files final until the user has responded — this step is not a formality.

Apply the user's corrections, then write the final versions into `workflow/`.

## Step 4 — Report back

Summarize what was inspected, what was drafted, and what the user corrected. Point the user at `/wayforge-new-feature "<description>"` as the next step. Flag explicitly if `user-stories.md` was left empty so the user knows to backfill it or start fresh from the first feature.

## Notes

- If `workflow/data-model.md` or `workflow/api-registry.md` already contain real entries (this isn't the first `/wayforge-adopt` run — the project has grown organically since), treat new findings as an additive pass: use `.wayforge/scripts/validate_docs.py` and `.wayforge/scripts/merge_master_doc.py` (`--mode entity` for data-model, `--mode group` for api-registry) the same way `/wayforge-review` does, rather than overwriting the files directly.
