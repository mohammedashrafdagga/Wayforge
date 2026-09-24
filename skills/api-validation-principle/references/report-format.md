# API Report Format

Every run produces a concise checkpoint report. The review itself must cover every operation in the active scope, but the report groups clean results by feature and gives operation-level detail only for actionable findings or evidence gaps. Keep older reports unchanged and link to them instead of copying their issue text.

## Checkpoint and history

- Record `Review mode` (`Full` or `Incremental`), the current branch, base checkpoint, reviewed `HEAD`, and whether staged, unstaged, or untracked changes were included.
- A comparable prior report targets the same project and materially equivalent API scope. Prefer the newest recorded commit that is an ancestor of `HEAD`; parent-branch checkpoints are valid.
- Assign findings stable IDs `API-001`, `API-002`, and so on. Reuse an ID for the same root cause, including recurrence; unrelated findings get new IDs.
- Fully describe only findings that are new, changed, or reverified in this run. Carry untouched unresolved findings as a compact row containing ID, status, title, affected feature, and prior-report link.
- List added, changed, moved, and removed operations since the base. Group them by feature or API surface; name individual operation keys only when needed to identify a finding or explain scope.

## Required report structure

Never leave template placeholders in a saved report. For empty sections write `None` with a useful explanation.

```markdown
# API Validation — Report NNN

- Reviewed at: <ISO 8601 timestamp with timezone>
- Project: <name and root>
- Review mode: <Full / Incremental>
- Branch: <branch name, or detached HEAD>
- Base checkpoint: <prior report and commit, merge base, or None for first full review>
- Reviewed revision: <HEAD commit plus staged/unstaged/untracked state>
- Scope: <full API or changed features/surfaces and affected shared behavior>
- Outcome: <Meets API baseline / Does not meet API baseline / Not ready to approve / No API endpoints found>
- Outcome scope: <whole reviewed API for Full; reviewed change set plus inherited issues for Incremental>

## Summary

- Reviewed operations: <N in the active scope>
- Results: <P Pass, F Fail, U Not verified; P + F + U = N>
- New or changed findings: <counts by severity; evidence gaps separately>
- Inherited open findings: <count>
- Principal blockers: <IDs and concise impact, or None>

## Change and coverage summary

| Feature / API surface | Added | Changed | Removed | Affected operations reviewed | Result | Evidence or gap |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| <feature or shared control> | <N> | <N> | <N> | <N> | <Pass / Fail / Not verified> | <concise paths/tests or gap> |

<For a Full review, use the same table with operation counts and `—` for change columns. Do not add a row for every passing endpoint.>

## Current issues

### API-001 — <specific defect or evidence gap>

- Status: <Open / Needs verification / Risk accepted>
- Severity: <Critical / High / Medium / Low; use Not assessed for an unqualified evidence gap>
- Principle: <P01–P09>
- Affected operations: <all known stable operation keys>
- Evidence: <repository-relative path:line and observed behavior>
- Expected versus observed: <specific requirement and deviation, or evidence needed>
- Impact: <credible consequence; qualify unconfirmed risk>
- Remediation: <concrete action>
- Verification: <test or evidence that proves resolution>
- Owner / target: <known values or Unassigned / Unscheduled>
- Risk acceptance: <only when already accepted; owner, rationale, scope, expiry>

## Inherited unresolved issues

| ID | Status | Title | Affected feature / surface | Detailed in |
| --- | --- | --- | --- | --- |
| <ID> | <status> | <title> | <feature> | <relative link to prior report> |

## Resolved or reverified

<IDs and current verification evidence, or None.>

## Verification record

| Check / command | Environment and active scope | Result | Limitations |
| --- | --- | --- | --- |
| <actual test or static trace> | <features and operations> | <passed / failed / not run> | <limitations or None> |

## Residual risk and next actions

<Prioritized issue IDs, checks still needed, assumptions, exclusions, and the limits of an incremental review.>
```

## Consistency rules

- Keep a private working ledger while reviewing so every operation in the active scope receives every applicable principle check. Do not paste the per-operation matrix into the report.
- Reconcile reviewed-operation totals with feature rows and affected operations in findings.
- A shared-control finding must identify every known affected operation, even when clean coverage is otherwise summarized.
- In an incremental report, untouched inherited findings remain part of the project-level outcome. Do not mark them resolved through absence from the diff.
- If no operations changed, record a zero-operation incremental checkpoint and any inherited blockers; do not rerun or reproduce the full inventory.
