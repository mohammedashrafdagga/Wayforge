# Clean-Code Review Report Format

Create a concise checkpoint report on every review. Report clean coverage by feature, package, or layer; reserve detailed prose for actionable issues and evidence gaps. Link to earlier reports rather than duplicating unchanged findings.

## Checkpoint and tracking rules

- Record `Review mode` (`Full` or `Incremental`), current branch, base checkpoint, reviewed `HEAD`, and included staged, unstaged, and untracked changes.
- A comparable report covers the same project and materially equivalent architecture scope. A reviewed commit on a parent branch is a valid incremental base when it is an ancestor of the current `HEAD`.
- Assign new root causes the next unused stable ID: `CCR-001`, `CCR-002`, and so on. Reuse an ID only for the same root cause.
- Fully describe findings only when they are new, changed, or reverified. Carry untouched unresolved issues in a compact table with a link to the last detailed report.
- Never infer resolution from absence in the current diff or edit older reports to make history appear current.

## Required structure

```markdown
# Clean-Code Review — Report NNN

- Date: <YYYY-MM-DD>
- Project: <name and reviewed root>
- Review mode: <Full / Incremental>
- Branch: <branch name, or detached HEAD>
- Base checkpoint: <prior report and commit, merge base, or None>
- Reviewed revision: <HEAD commit plus staged/unstaged/untracked state>
- Review scope: <whole project for Full; changed and transitively affected features/packages/layers for Incremental>
- Architecture expectation: <documented architecture and evidence source>
- Outcome: <Meets clean-code baseline / Does not meet clean-code baseline / Not ready to approve>
- Outcome scope: <full reviewed project, or reviewed change set plus inherited issues>

## Executive summary

<Most important conclusion, new/changed issue counts by severity, inherited-open count, and material limitations.>

## Change and coverage summary

| Feature / package / layer | Change kind | Affected behavior reviewed | Result | Evidence or gap |
| --- | --- | --- | --- | --- |
| <cohesive surface> | <Added / Changed / Removed / Full baseline> | <concise scope> | <Pass / Fail / Not verified> | <paths, tests, or gap> |

<Group clean results. Do not create a row per file, class, function, or baseline principle.>

## Current findings

### CCR-001 — <specific root-cause title>

- Status: <Open / Needs verification / Accepted debt>
- Severity: <Critical / High / Medium / Low>
- Principle: <baseline area and project rule>
- Affected surfaces: <features, modules, layers, or packages>
- Evidence: <repository-relative path:line plus concise observation>
- Impact: <credible correctness, change-cost, testability, or maintenance consequence>
- Root cause: <why the issue exists across the affected surfaces>
- Remediation: <smallest durable change and important sequencing>
- Verification: <test, static rule, review, or measurable observation>
- Owner / target: <known values or Unassigned / Unscheduled>
- Acceptance: <owner, rationale, guardrails, and revisit date; omit unless accepted>

## Inherited unresolved findings

| ID | Status | Title | Affected feature / surface | Detailed in |
| --- | --- | --- | --- | --- |
| <ID> | <status> | <title> | <surface> | <relative link to prior report> |

## Resolved or reverified

<Finding ID and current verification evidence, or None.>

## Prioritized next actions

<`Fix first`, `Fix next`, and optional `Consider later` items by finding ID; or None.>

## Verification record

- Checks run: <commands, static reviews, and results>
- Checks not run: <check, reason, and how to run it>
- Assumptions and exclusions: <material items>
- Residual risk: <including untouched scope in an incremental review>
```

## Content requirements

- Use repository-relative evidence paths and exact lines for findings when stable line references are available.
- Maintain a working checklist across all applicable baseline areas for the active scope, but do not paste a complete passing matrix into the report.
- Expand incremental review through dependencies and shared abstractions; a small diff can affect several features.
- Separate confirmed failures from evidence gaps. Consolidate repeated symptoms with one root cause while preserving known affected surfaces.
- An untouched finding remains open and affects the project outcome. Its previous detailed report is the source of truth until it is reverified.
- A clean run should be short: checkpoint metadata, grouped reviewed scope, verification, inherited issues if any, and no artificial findings.
