# Security Report Format

Create a concise checkpoint report on every completed review. Group clean coverage by changed feature or trust boundary, and use detailed content only for actionable issues and evidence gaps. Link to prior reports for unchanged issues rather than repeating them.

## Checkpoint and tracking rules

- Record `Review mode` (`Full` or `Incremental`), current branch, base checkpoint, reviewed `HEAD`, and included staged, unstaged, and untracked changes.
- Prefer the newest comparable reviewed commit that is an ancestor of current `HEAD`, even if it was reviewed on a parent branch.
- Give each new root cause the next unused stable ID `SEC-001`, `SEC-002`, and so on. Reuse the ID only for the same root cause.
- Fully describe findings only when new, changed, or reverified. Carry untouched unresolved issues in a compact table with their last detailed report.
- Never infer resolution from absence in a diff. Risk acceptance is not a fix.

## Required structure

```markdown
# Software Security Review — Report NNN

- Date: <YYYY-MM-DD>
- Application: <name and reviewed root>
- Review mode: <Full / Incremental>
- Branch: <branch name, or detached HEAD>
- Base checkpoint: <prior report and commit, merge base, or None>
- Reviewed revision: <HEAD commit plus staged/unstaged/untracked state>
- Review scope: <whole application for Full; changed and transitively affected trust boundaries for Incremental>
- Outcome: <Meets minimum baseline / Does not meet minimum baseline / Not ready to approve>
- Outcome scope: <full reviewed application, or reviewed change set plus inherited issues>
- Release decision: <Block / Conditional / Pass / Not assessed>

## Executive summary

<Most important risk, new/changed issue counts, inherited-open count, and material limitations.>

## Change and coverage summary

| Feature / trust boundary | Change kind | Security behavior reviewed | Result | Evidence or gap |
| --- | --- | --- | --- | --- |
| <cohesive surface> | <Added / Changed / Removed / Full baseline> | <auth, data, dependency, deployment, etc.> | <Pass / Fail / Not verified> | <paths/tests or gap> |

<Do not add one row per file, endpoint, or passing baseline control.>

## Release blockers

<Critical and High issue IDs with concise impact, including inherited blockers; or None.>

## Current issues

### SEC-001 — <specific title>

- Status: <Open / Needs verification / Risk accepted>
- Severity: <Critical / High / Medium / Low>
- Baseline area: <area>
- Affected component: <feature, endpoint, role, tenant, data, or deployment surface>
- Evidence: <repository-relative path:line and/or reproducible observation>
- Impact: <credible abuse and business effect>
- Remediation: <smallest durable fix>
- Verification: <test or evidence that proves resolution>
- Owner / target: <known values or Unassigned / Unscheduled>
- Acceptance: <owner, rationale, compensating controls, expiry; omit unless accepted>

## Inherited unresolved issues

| ID | Status | Severity | Title | Affected feature / boundary | Detailed in |
| --- | --- | --- | --- | --- | --- |
| <ID> | <status> | <severity> | <title> | <surface> | <relative link to prior report> |

## Resolved or reverified

<Issue ID and current verification evidence, or None.>

## Prioritized next actions

### Before release

<Ordered issue IDs and evidence tasks, or None.>

### After release

<Defense-in-depth items, or None.>

## Verification record

- Checks run: <commands/tests/reviews and results>
- Checks not run: <what, why, and how to close the gap>
- Assumptions and exclusions: <material items>
- Residual risk: <including untouched scope in an incremental review>
```

## Content requirements

- Maintain a working checklist for every applicable control in the active scope, but do not paste a complete passing-control matrix into the report.
- Trace incremental changes through consumers and trust boundaries; shared authentication, authorization, parsing, storage, dependency, CI, or deployment changes can widen the scope.
- Use exact evidence for issues, redact secrets and personal data, and distinguish confirmed vulnerabilities from missing evidence.
- Untouched unresolved findings retain their status and affect the release decision. Link to prior detail instead of copying it.
- A clean run should be a short checkpoint containing metadata, grouped reviewed scope, verification, and inherited issues if any.
