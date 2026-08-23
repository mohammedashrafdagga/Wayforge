---
name: new-feature
description: This skill should be used when the user asks to "add a feature with RSW", "start a new feature", "run /rsw:new-feature", or describes a new capability to build (e.g. "add a saved-searches feature") in a project that already has a workflow/ tree from /rsw:init or /rsw:adopt. Produces the feature's local user-stories.md and data-model.md after checking them against the existing master docs and constitution.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /rsw:new-feature "<description>" — Scope a new feature against the living docs

Takes a one-line feature description and turns it into `workflow/features/<slug>/user-stories.md` and `workflow/features/<slug>/data-model.md` — checked against the constitution and all three master docs first, so duplication and inconsistency get caught before any code exists.

## Step 0 — Locate the workflow tree

Find `workflow/` (at the repo root, or inside `backend/`/`frontend/` depending on the scope chosen at `/rsw:init`/`/rsw:adopt`). If it doesn't exist, stop and tell the user to run `/rsw:init` or `/rsw:adopt` first — this skill has nothing to check against otherwise.

## Step 1 — Derive the feature slug

Lowercase, hyphen-separated, derived from the description (e.g. "add a saved-searches feature to the search page" → `saved-searches`). Confirm the slug with the user if it's ambiguous. Create `workflow/features/<slug>/`.

## Step 2 — Read before writing (do this fully, not selectively)

Read, in full:

- `workflow/constitution/architecture.md` and `workflow/constitution/conventions.md`
- `workflow/data-model.md` — is there already an entity that overlaps this feature's concept, even under a different name?
- `workflow/api-registry.md` — any existing endpoint that already covers part of this?
- `workflow/user-stories.md` — any related story already recorded, possibly under a different feature?

This is the check that keeps the master docs trustworthy — do not skip straight to writing new content. If something overlapping is found, say so to the user explicitly and ask whether this feature should extend the existing entity/endpoint/story (as a new additive entry referencing it) or is genuinely distinct.

## Step 3 — Write `user-stories.md`

Using `templates/user-stories.md.tmpl`'s per-feature shape (a `## <feature-slug>` heading, `- As a <role>, I want to <action>, so that <benefit>.` entries, each with `**Acceptance criteria:**` checkboxes). Base the stories on the user's description; if the description is thin, ask targeted follow-up questions rather than inventing acceptance criteria from nothing — these criteria become the source of truth `/rsw:plan` and `/rsw:review` both trace back to.

## Step 4 — Write `data-model.md`

Using `templates/data-model.md.tmpl`'s per-entity shape (`## <EntityName>`, `**Feature:** <slug> · **Added:** <date>`, a field table, and a Mermaid `erDiagram` block when there's a real relationship to show — e.g. to an existing master-doc entity). This file records only this feature's *additions* — never restate or re-describe an existing master-doc entity here beyond referencing it by name in a relationship.

If this feature adds no new entities (pure UI change, or reuses an existing entity as-is), write the file with a short note to that effect rather than leaving it as an unfilled template — a later reader needs to know that was a deliberate finding, not an oversight.

## Step 5 — Report back

Summarize the stories and entities drafted, any overlap found in Step 2 and how it was resolved, and point the user at `/rsw:plan` as the next step.

## Notes

- Nothing in this skill touches the master docs (`workflow/data-model.md`, `workflow/api-registry.md`, `workflow/user-stories.md`) directly — those only change via `merge_master_doc.py` at the end of `/rsw:review`. This skill only reads them.
- If the user's description implies work on both backend and frontend, note that in the feature folder but don't split it into two feature slugs unless the git strategy is "split backend/frontend branches" (see `workflow/constitution/conventions.md`) — in that case, flag it so `/rsw:plan` knows to create both branches.
