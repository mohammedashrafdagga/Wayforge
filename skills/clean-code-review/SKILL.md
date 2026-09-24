---
name: clean-code-review
description: Review frontend, backend, or full-stack code for actionable maintainability and architecture issues, using a full first review and branch-aware incremental reviews thereafter. Use for code-quality audits, DDD or feature-boundary reviews, technical-debt assessments, and clean-code remediation planning; do not use as a substitute for a dedicated security audit.
metadata:
  author: "mohammedashrafdagga"
  version: "1.1.0"
  supported-agents: "codex,claude-code,cursor"
---

# Clean Code Review

Assess the requested codebase as a maintainable system, not as a collection of style violations. Review both frontend and backend when they exist, verify conformance to the project's chosen architecture, and turn confirmed problems and evidence gaps into a practical remediation plan.

A review creates a report. It does not modify application code unless the user also asks to fix or refactor findings.

## Establish scope and architecture

1. Determine the project root from repository and user context. Respect an explicitly narrower scope. A first review of a repository-wide request covers every first-party application, package, service, and shared library.
2. Follow repository instructions. Discover the intended architecture from architecture decision records, documentation, directory conventions, dependency rules, tests, and representative code paths. Treat explicit project rules as authoritative unless they conflict or are demonstrably stale.
3. Inventory the reviewed surfaces: frontend applications and features, backend services and features, domain/application/infrastructure layers, shared packages, entry points, background jobs, data access, integrations, and test suites. Exclude generated code, vendored code, build output, and third-party dependencies from direct quality scoring, while recording harmful generation or integration patterns when relevant.
4. Map important dependency directions and trace representative end-to-end feature paths. For DDD or feature-oriented systems, verify actual boundaries rather than inferring compliance from folder names.
5. Record material unknowns as coverage gaps. In a full review, do not silently reduce the codebase to a convenient sample or one layer. Keep a working coverage ledger, but summarize passing coverage by feature, package, or layer in the report.

## Select full or incremental review

Record the current Git branch and exact reviewed revision on every run. Include staged, unstaged, and untracked application changes in the reviewed state.

- Use `Full` mode when no comparable prior report exists, the user asks for a full review, the earlier checkpoint is unavailable or untrustworthy, or broad architecture/build changes invalidate the prior baseline.
- Otherwise use `Incremental` mode. Prefer the newest comparable reviewed commit that is an ancestor of the current `HEAD`, regardless of whether the current work is on a child branch. Review its committed diff through `HEAD` plus working-tree changes.
- For diverged history, use a trustworthy merge base only when it represents the last shared reviewed state; otherwise use `Full` mode. Explain the fallback.
- Review added, edited, moved, and deleted code. Expand from changed lines to affected feature boundaries, imports/dependents, shared abstractions, contracts, configuration, tests, and end-to-end paths. A shared-layer change can make multiple features part of the incremental scope.
- Do not re-review untouched surfaces only to reproduce a repository inventory. Carry unresolved untouched findings forward by stable ID and prior-report link; reverify them when the changes could affect them or when the user asks.

An incremental pass describes the reviewed change set only. It does not erase inherited findings or establish that untouched code meets the full baseline.

## Review workflow

1. Ensure `<project-root>/docs/clean-code-report/` exists without deleting or overwriting existing content.
2. Read prior `report_*.md` files in that directory. Preserve stable issue IDs when the same root cause remains, and distinguish newly found, recurring, and resolved issues.
3. Read [references/quality-baseline.md](references/quality-baseline.md). Assess every core area and every conditional area that applies to the discovered stack and architecture.
4. Prefer direct evidence: definitions and call sites, import relationships, configuration, architecture tests, focused tests, compiler and linter output, duplication or complexity tools already configured by the project, and version-control-supported observations when available.
5. Use project-native checks when useful. Do not install dependencies, change configuration, or run auto-fix commands merely to complete a review. If a relevant check cannot run safely, record the gap and the command or evidence needed to close it.
6. Consolidate symptoms that share one design cause. Report all known affected surfaces without producing one issue per repeated line. Summarize reviewed clean surfaces by feature rather than listing every file or check. Conversely, do not combine unrelated problems only because they share a principle label.
7. Distinguish an enforceable defect from taste. A finding needs concrete evidence, a maintenance or correctness consequence, and a proportionate remediation. Do not penalize framework conventions, necessary boundary translation, deliberate local duplication, generated code, or simple code that does not yet justify an abstraction.
8. If fixes are requested, remediate in dependency-aware batches, preserve intended behavior and public contracts, add proportionate tests, and rerun relevant checks. Avoid repository-wide rewrites when smaller cohesive changes resolve the root cause.

## Assessment states and severity

Use these states for every baseline area applicable to the active review scope:

- `Pass`: sufficient inspected evidence shows the applicable principle is followed, with no material unresolved finding.
- `Fail`: a concrete violation with credible impact is supported by evidence.
- `Not verified`: inspection or execution evidence is incomplete; state exactly what remains and how to verify it.
- `Not applicable`: the area does not apply to the reviewed system; give the reason.

Rate each finding by consequence and remediation urgency:

- `Critical`: the design defect can plausibly cause widespread incorrect behavior, irreversible data damage, or an inability to operate or change a critical system safely.
- `High`: a systemic boundary, coupling, duplication, or complexity problem creates substantial correctness risk or blocks safe delivery across multiple features.
- `Medium`: a material maintainability or testability problem has bounded impact but should be scheduled.
- `Low`: a localized clarity or consistency problem with a credible cost; purely cosmetic preferences are not findings.

Use the outcome `Does not meet clean-code baseline` when any reviewed or inherited area fails, and `Not ready to approve` when no failure is proven but material scope remains unverified. Use `Meets clean-code baseline` only when the active inventory is complete, all applicable areas pass, and no inherited unresolved findings remain. In incremental mode, describe this as a change-set outcome unless the prior full baseline plus all later deltas establish current whole-project coverage. Severity prioritizes work; it does not change the area state.

## Create the report

Read [references/report-format.md](references/report-format.md) before writing. Create one report on every completed invocation, even when no issues are found or the assessment is incomplete.

Name it `docs/clean-code-report/report_NNN.md`:

- Match only existing filenames of the form `report_` followed by an integer and `.md`.
- Use one greater than the largest number, starting with `report_001.md` and padding to at least three digits.
- Never overwrite, delete, renumber, or rewrite an earlier report. Recalculate if the intended filename already exists before writing.

The report must be understandable with links to earlier detail and include:

1. review mode, current branch, base and reviewed revision, working-tree state, scope, assumptions, and exclusions;
2. a concise outcome and counts by status and severity;
3. actionable new, changed, or reverified findings with stable IDs, exact evidence, impact, root cause, remediation, and verification;
4. resolved findings with current evidence and untouched open findings as a compact ID/link list;
5. feature/package-level coverage for the active review scope, without a file-by-file ledger or repeated passing details;
6. prioritized next actions, checks run or skipped, and residual risk.

Use repository-relative paths and line numbers inside the report. If the project root is not writable, return the intended path and complete report content instead of saving it elsewhere.

In the final response, lead with the outcome, summarize the most important findings and coverage gaps, state whether application code was changed, and link the new report.
