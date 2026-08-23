---
name: rsw-plan
description: This skill should be used when the user asks to "plan this feature", "create an implementation plan", "run /rsw-plan", or wants a task breakdown for a feature that already has user-stories.md and data-model.md from /rsw-new-feature. Produces implementation-plan.md, surfaces trade-offs against the constitution and existing code patterns as explicit questions, and creates the feature branch per the project's git strategy.
---

# /rsw-plan — Turn a scoped feature into an implementation plan

Reads a feature's own docs, the constitution, and a real slice of the existing codebase, then produces `workflow/features/<slug>/implementation-plan.md`: a task breakdown with acceptance criteria, grounded in actual patterns already in the repo — not a generic plan. Creates the feature branch per the project's git strategy.

## Step 1 — Read the full context

- `workflow/features/<slug>/user-stories.md` and `data-model.md` (from `/rsw-new-feature`)
- `workflow/constitution/architecture.md` and `conventions.md`
- `workflow/api-registry.md` (to know what already exists and avoid re-planning it)

If the feature folder doesn't exist yet, stop and point the user at `/rsw-new-feature` first.

## Step 2 — Grep the codebase for comparable patterns (do not skip)

This is the step that makes the plan grounded rather than generic. For each entity/endpoint this feature needs, search the existing codebase for the closest comparable feature slice already implemented (e.g. if adding `saved-searches`, look at how `search` or another similarly-shaped feature structures its `domain/application/infrastructure/api` layers). Note concrete file paths that this plan will follow or deliberately deviate from — these go in the plan's "Existing patterns consulted" section. A plan with no file paths in that section is a sign this step was skipped.

## Step 3 — Surface trade-offs and conflicts as explicit questions

While reading the constitution and existing patterns, actively look for ambiguity: something the user stories don't specify that has more than one reasonable implementation (e.g. "per-user or shared across a team?"), or something that would require deviating from `constitution/architecture.md` (e.g. a sync call where the constitution mandates async). For each one found, ask the user directly — do not guess and move on, and do not bury the question in prose the user might skim past.

Record every question asked and its answer in the plan's "Trade-offs and conflicts surfaced to the user" section, even when the answer was "just use the default" — an empty section there is a signal this step was skipped, not that nothing was ambiguous.

## Step 4 — Write `implementation-plan.md`

Follow `.rsw/templates/implementation-plan.md.tmpl`. Break the feature into independently completable tasks, each with:
- files to be created/modified
- a description concrete enough that a cold-start agent with zero conversation history (i.e. Cursor or Codex, opening only this file) could execute it correctly
- acceptance criteria, traceable back to the acceptance criteria in `user-stories.md` where applicable

List any new data-model entities/endpoints this plan introduces as a pointer to `data-model.md` (the plan doesn't restate them in full).

## Step 4b — Write `workflow/features/<slug>/api-registry.md`

If this feature adds or changes any HTTP endpoint, write `workflow/features/<slug>/api-registry.md` following `.rsw/templates/api-registry.md.tmpl`'s per-feature section shape (a single `## <feature-slug>` heading with a Method/Path/Summary/Auth table). This is the point in the lifecycle where concrete routes are actually decided, so it belongs here, not in `/rsw-new-feature`. `/rsw-review` merges this file into the master `workflow/api-registry.md` — if it's never created, review has nothing to merge and treats the feature as adding no new endpoints. Skip this file entirely (don't create an empty one) for a feature that genuinely adds no endpoints.

## Step 5 — Create the feature branch

Read `workflow/constitution/conventions.md` for the git strategy:
- **mono-repo single branch**: skip branch creation, note in the plan that work happens directly against the default branch (or the user's current branch).
- **split backend/frontend branches**: create `backend/<slug>` and/or `frontend/<slug>` depending on which sides this feature touches.
- **per-feature branches**: create a single `feature/<slug>` branch.

Use `git checkout -b <branch-name>` from the current default branch. If the working tree has uncommitted changes, stop and ask the user before switching branches rather than risking losing work.

## Step 6 — Report back

Summarize the task list, the trade-off questions asked and answered, and the branch created (if any). Point the user at `/rsw-apply` as the next step — runnable from this same agent, or from a different one (Cursor/Codex) since `implementation-plan.md` is self-contained and every RSW-installed agent has the identical `/rsw-apply` skill available.

## Notes

- This skill never edits `constitution/architecture.md` itself. A user-approved deviation from the constitution gets recorded as a scoped exception in this feature's `implementation-plan.md`, not a silent rewrite of the constitution — see `constitution/architecture.md`'s own "Amending this file" section.
