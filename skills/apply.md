---
name: wayforge-apply
description: This skill should be used when the user asks to "apply the implementation plan", "implement this feature", "run /wayforge-apply", or wants a feature's implementation-plan.md executed task by task. Identical skill installed for Claude Code, Cursor, and Codex — so a plan written by one agent can be applied by whichever agent the user opens next, with no extra handoff step.
---

# /wayforge-apply — Execute an approved implementation plan

Executes `workflow/features/<slug>/implementation-plan.md` task by task. This skill was installed identically into every Wayforge-configured agent (Claude Code, Cursor, Codex) — running it here means picking up a plan that may have been written in a different agent's session, so read everything below fresh rather than relying on any prior conversation.

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
4. If a task turns out to require something the plan didn't anticipate — a genuinely new trade-off, not just an implementation detail — stop and ask the user rather than deciding unilaterally. This mirrors `/wayforge-plan`'s own rule: ambiguity gets surfaced, not silently resolved.

## Step 3 — Do not touch the master docs

Never edit `workflow/data-model.md`, `workflow/api-registry.md`, or `workflow/user-stories.md` during apply. Those only change via `.wayforge/scripts/merge_master_doc.py` at the end of `/wayforge-review`, once the implementation has actually been checked against the plan.

## Step 4 — Report back

Summarize which tasks were completed, which acceptance criteria were verified and how, and flag anything left incomplete or any question raised mid-implementation. Point the user at `/wayforge-review` as the next step.

## Notes

- If the plan's tasks turn out to be poorly scoped once implementation starts (too coarse, missing a dependency between tasks), fixing `implementation-plan.md` itself is out of scope for this skill — flag it to the user and let them decide whether to re-run `/wayforge-plan` or proceed with a manual adjustment.
