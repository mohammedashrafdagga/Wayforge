---
name: apply
description: This skill should be used when the user asks to "apply the implementation plan", "implement this feature", "run /rsw:apply", or wants a feature's implementation-plan.md executed task by task. Designed to also be run manually from Cursor via the .cursor/ handoff file that /rsw:plan generates — this Claude Code version is the same workflow run without that handoff.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /rsw:apply — Execute an approved implementation plan

Executes `workflow/features/<slug>/implementation-plan.md` task by task. This skill is intended to also be run manually from Cursor in v1 (via `.cursor/<slug>-apply.md`, written by `/rsw:plan`) — when run from Claude Code, follow the same discipline: read the plan and constitution fully before writing any code, and don't improvise beyond what the plan and acceptance criteria specify.

## Step 1 — Read before writing

Read, in full:

- `workflow/features/<slug>/implementation-plan.md` — the task list and acceptance criteria are the contract
- `workflow/constitution/architecture.md` and `conventions.md` — the plan assumes these; re-confirm rather than relying on memory of them from an earlier step in a long session
- `workflow/features/<slug>/data-model.md` — for exact field names/types when implementing entities

If the plan's branch (per `constitution/conventions.md`'s git strategy) isn't currently checked out, check it out before making changes.

## Step 2 — Work through tasks in order

For each task in `implementation-plan.md`:

1. Implement exactly what the task's "Files" and "Description" specify — no unrelated cleanup, no scope creep into adjacent tasks.
2. Respect the constitution's dependency direction and folder layout even when a shortcut is tempting (e.g. don't import an ORM model into `domain/` because it's convenient).
3. Check the task's acceptance criteria concretely (run the relevant test, hit the endpoint, render the component) rather than asserting completion from reading the code alone.
4. If a task turns out to require something the plan didn't anticipate — a genuinely new trade-off, not just an implementation detail — stop and ask the user rather than deciding unilaterally. This mirrors `/rsw:plan`'s own rule: ambiguity gets surfaced, not silently resolved.

## Step 3 — Do not touch the master docs

Never edit `workflow/data-model.md`, `workflow/api-registry.md`, or `workflow/user-stories.md` during apply. Those only change via `merge_master_doc.py` at the end of `/rsw:review`, once the implementation has actually been checked against the plan.

## Step 4 — Report back

Summarize which tasks were completed, which acceptance criteria were verified and how, and flag anything left incomplete or any question raised mid-implementation. Point the user at `/rsw:review` as the next step — noting it can run from Claude Code directly, or be handed to Codex via `.codex/<slug>-review.md`.

## Notes

- This skill does not create `.codex/` handoff files — that happens in `/rsw:review`, since the review step is what Codex's handoff file points at.
- If the plan's tasks turn out to be poorly scoped once implementation starts (too coarse, missing a dependency between tasks), fix that by editing `implementation-plan.md` directly is out of scope for this skill — flag it to the user and let them decide whether to re-run `/rsw:plan` or proceed with a manual adjustment.
