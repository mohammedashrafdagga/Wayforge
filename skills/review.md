---
name: wayforge-review
description: This skill should be used when the user asks to "review this feature", "check the implementation against the plan", "run /wayforge-review", or wants to verify a completed feature's acceptance criteria before merging its docs into the master data-model/api-registry/user-stories. Identical skill installed for Claude Code, Cursor, and Codex — commonly run from a different agent than the one that applied the plan, for an independent check.
---

# /wayforge-review — Verify a feature and merge its docs into the masters

Checks a feature's actual implementation against `implementation-plan.md`'s tasks and acceptance criteria, writes `review.md`, and — only if the review passes — runs the additive-only merge of the feature's local docs into the three master docs. This is the only Wayforge skill that's allowed to change `workflow/data-model.md`, `workflow/api-registry.md`, and `workflow/user-stories.md`, and only via the scripts below, never by hand-editing them.

## Step 1 — Read the plan and diff the implementation

Read `workflow/features/<slug>/implementation-plan.md` in full. Get the diff for the feature's branch against its base (`git diff <base>...<branch>` or equivalent per the git strategy in `constitution/conventions.md`).

## Step 2 — Check every task's acceptance criteria against the actual code

For each task, mark each acceptance criterion pass/fail with a concrete, checkable reference (a file:line, a test that was run, an endpoint that was actually hit) — not an assertion based on reading the plan alone. A criterion that can't be verified this way is a fail with a note explaining what's missing, not a silent pass.

## Step 3 — Check constitution conformance separately from the acceptance criteria

Read `workflow/constitution/architecture.md`. Confirm independently of the task checklist:
- feature code lives inside its own slice (not scattered or bolted onto another feature's folder)
- `domain/` has no framework imports
- dependency direction (`api` → `application` → `domain`) is respected
- no unflagged cross-feature reach into another feature's `infrastructure`/ORM models

A feature can pass every acceptance criterion and still violate the constitution — record that as a separate finding, it doesn't get waived by passing criteria.

## Step 4 — Write `review.md`

Follow `.wayforge/templates/review.md.tmpl`. Set the overall result (PASS / FAIL / PASS WITH NOTES) and list every issue found with enough detail that a follow-up `/wayforge-apply` pass could fix it without re-deriving what's wrong.

## Step 5 — If PASS, run the additive-only merge

Only proceed past this point if the result is PASS or PASS WITH NOTES (issues that don't block merging the docs, e.g. a cosmetic nit). A FAIL stops here — report back and do not merge.

For each of the three master docs, first validate, then merge:

```bash
python3 .wayforge/scripts/validate_docs.py --kind data-model \
  --source workflow/features/<slug>/data-model.md --master workflow/data-model.md

python3 .wayforge/scripts/merge_master_doc.py --mode entity \
  --source workflow/features/<slug>/data-model.md --master workflow/data-model.md
```

```bash
python3 .wayforge/scripts/validate_docs.py --kind api-registry \
  --source workflow/features/<slug>/api-registry.md --master workflow/api-registry.md

python3 .wayforge/scripts/merge_master_doc.py --mode group \
  --source workflow/features/<slug>/api-registry.md --master workflow/api-registry.md
```

```bash
python3 .wayforge/scripts/validate_docs.py --kind user-stories \
  --source workflow/features/<slug>/user-stories.md --master workflow/user-stories.md

python3 .wayforge/scripts/merge_master_doc.py --mode group \
  --source workflow/features/<slug>/user-stories.md --master workflow/user-stories.md
```

(Skip a doc that this feature genuinely has no content for — e.g. no new endpoints — rather than running the scripts against an empty or missing file.)

**If `validate_docs.py` exits non-zero (exit code 2), stop.** Present the reported conflicts to the user verbatim and ask how to resolve each one (rename an entity, adjust a route, or confirm an intentional manual edit to the master doc). Never run the merge script past a validation failure, and never resolve a flagged conflict by guessing which side is right.

If `merge_master_doc.py` reports an entity-mode conflict directly (exit code 2) despite validation passing, that's unexpected — stop and surface the discrepancy to the user rather than forcing it through.

Update `review.md`'s "Merge status" checklist to reflect what actually ran.

## Step 6 — Report back

Summarize the review result, key findings, and whether the master docs were merged. If merged, note what was added to each. If not merged (FAIL, or a validation conflict), state clearly what needs to happen before re-running `/wayforge-review`.
