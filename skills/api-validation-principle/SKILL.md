---
name: api-validation-principle
description: Audit a system's API endpoints against practical API design, validation, security, and reliability principles, using a full first review and branch-aware incremental reviews thereafter. Use for API best-practice reviews, endpoint change audits, API readiness checks, or remediation against this baseline.
metadata:
  author: "mohammedashrafdagga"
  version: "1.1.0"
  supported-agents: "codex,claude-code,cursor"
---

# API Validation Principle

Review API behavior against an evidence-based baseline. Establish a complete baseline on the first comparable run, then review only API changes and their affected behavior on later runs. Produce a concise, issue-focused report on every invocation. A review identifies gaps; fix application code only when the user asks for implementation or remediation.

## Scope and inventory

1. Determine the target project root from the repository and user context. Default to the whole current project, including all services in a monorepo. Use a narrower application root only when the user scopes the review to it. Reports belong in `<project-root>/docs/api_report/`, never inside the installed skill directory.
2. Create that directory while preserving existing files. Read previous `report_*.md` files for review checkpoints, historical issues, and stable issue IDs. Read [references/report-format.md](references/report-format.md) before writing the new report.
3. Discover endpoints from route registration and mounted routers, controllers, framework-generated routes, API schemas, gateway/reverse-proxy configuration, and tests. Reconcile sources; documentation alone is not a complete inventory. Resolve base paths, versions, hosts, enabled feature flags, and shared middleware. Record unavailable services or runtime route generation as coverage gaps.
4. Include public, authenticated, administrative, internal, health, deprecated-but-active, upload, and inbound webhook endpoints. In a multi-service system, identify the owning service and distinguish gateway aliases from backend routes without losing either exposed surface. Record documented-only operations as discrepancies pending confirmation, and implemented-but-undocumented operations as documentation findings.
5. Assign each HTTP operation a stable identity using service, host/base path where relevant, method, and normalized route template. Different methods on the same path are separate operations. For GraphQL, enumerate schema query/mutation/subscription fields and authorization boundaries; for RPC, enumerate service methods; for WebSockets, enumerate exposed message operations. Do not claim these are covered by reviewing only their HTTP transport route. If they cannot be inspected, record the gap.

On a full review, do not reduce a system-wide request to a sample. Keep a working inventory while reviewing, but do not dump every passing operation into the report. Summarize clean coverage by feature or API surface and give operation-level detail only for findings and evidence gaps.

## Select full or incremental review

Record the current Git branch and exact reviewed revision on every run. Include staged, unstaged, and untracked application changes in the reviewed state.

- Use `Full` mode when no comparable prior report exists, the user requests a full review, the prior checkpoint cannot be resolved safely, or broad routing/framework changes make the earlier inventory unreliable.
- Otherwise use `Incremental` mode. Prefer the newest comparable prior checkpoint whose commit is an ancestor of the current `HEAD`, even when it was recorded on a parent branch. Review the committed diff from that checkpoint through `HEAD` plus current working-tree changes.
- If branches diverged and no reviewed checkpoint is an ancestor, use a trustworthy merge base only when it represents the last shared reviewed state; otherwise fall back to `Full`. State the decision in the report.
- Discover added, edited, moved, and removed operations. Expand beyond changed lines to affected handlers, contracts, middleware, shared validation/authentication, callers, tests, and configuration. A changed shared control brings every operation whose behavior may change into scope.
- Do not re-review untouched operations merely to recreate the old inventory. Carry unresolved untouched findings forward by ID and prior-report link; reverify them only when affected by the diff or explicitly requested.

An incremental result applies to the reviewed change set, not to the untouched repository. Preserve inherited open findings in the project-level decision and never present a clean delta as proof that the whole API now meets the baseline.

## Validate each operation

Read [references/api-baseline.md](references/api-baseline.md) and apply every core principle plus relevant conditional checks to each operation. Follow repository conventions and documented API contracts; distinguish an actual defect from an optional design preference.

- Trace request parsing, validation, authentication, authorization, business logic, persistence/integrations, response serialization, and error handling. Verify middleware is actually mounted on the reviewed route.
- Use code and configuration evidence plus focused local tests where behavior needs execution. Reuse project test tools. Check success, invalid/boundary input, missing or invalid identity, forbidden role/ownership/tenant, not-found/conflict, and applicable retry/failure cases. Mark irrelevant cases with a reason.
- Shared controls may use one evidence record, but enumerate covered operations and verify attachment and overrides. A passing shared middleware test does not prove route-specific ownership rules or business validation.
- Record precise repository-relative paths and lines, test names/commands, results, and environment. Distinguish static review from executed tests. A schema, annotation, successful response, or green general test suite alone is insufficient evidence for an endpoint pass.
- Use local disposable fixtures for operations with side effects. Do not run mutating or load tests against production, third-party services, or real customer data without authorization covering that environment and action. Report checks that could not run as `Not verified`; never silently skip them.
- If fixes are requested, preserve client compatibility where possible, add proportionate regression coverage, and recheck affected behavior. Report the final verified state and remediation evidence without rewriting earlier reports.

## States and decision

Use these states for each principle on each endpoint:

- `Pass`: applicable requirements are satisfied by cited evidence, including focused execution where needed to establish behavior.
- `Fail`: a concrete violation is demonstrated; link a finding.
- `Not verified`: evidence is missing, inconclusive, inaccessible, or a necessary check could not run; state what would resolve it.
- `Not applicable`: this principle does not apply to this operation; give a specific reason. Public access alone does not make authorization review inapplicable: verify that public access is intentional and responses are appropriately limited.

Roll up each endpoint: any `Fail` means `Fail`; otherwise any `Not verified` means `Not verified`; otherwise `Pass`. Conditional `Not applicable` checks do not hide missing core checks. Keep evidence gaps visible even for an endpoint already marked `Fail`.

Set the outcome for the active review scope while also accounting for inherited unresolved findings:

- `Does not meet API baseline` if any endpoint or system-level principle fails.
- `Not ready to approve` if no failure is proven but inventory completeness or any applicable check remains unverified.
- `Meets API baseline` only when the active inventory is complete, all operations and applicable system-level checks in scope pass, and no inherited unresolved failures or evidence gaps remain. In incremental mode, label this as a change-set result unless the prior full baseline plus all later deltas establish current whole-API coverage.
- `No API endpoints found` when inspected sources establish that the scoped project exposes no API. If discovery was blocked, use `Not ready to approve` instead. Neither case means all endpoints passed.

Severity prioritizes remediation; it does not change a failing check into a pass. Use Critical for broad compromise or catastrophic data loss, High for serious authorization/data-integrity failures, Medium for material bounded contract or reliability defects, and Low for limited-impact defects. Optional improvements are recommendations, not failed requirements. An accepted risk remains visible and does not satisfy the baseline.

## Report on every run

Create `docs/api_report/report_NNN.md`, starting with `report_001.md`. Find the largest integer in existing filenames matching `^report_([0-9]+)\.md$`, add one, and pad to at least three digits. Never overwrite, delete, or renumber past reports. Use exclusive file creation and recalculate the number if the path is taken before writing.

Follow the report reference. Include checkpoint metadata, feature-level coverage, detailed current issues, compact inherited issue links, historical changes, and checks not run. Do not include a full endpoint inventory or passing per-principle matrix in the saved report. Always create a report even when no issues are found or verification is blocked. If writing is blocked, return the intended path and complete report content and explicitly state it was not saved; do not substitute a report in another project or claim success.

Before finishing, reconcile the reviewed-operation totals with the feature summaries and findings. Ensure every operation in the active review scope was checked against all applicable principles in the working review, even though clean per-operation results are not copied into the report. Redact credentials, tokens, and personal payloads from evidence.

In the response, state the outcome, endpoints discovered/passed/failed/not verified, important blockers, and the path to the new report. Scope any pass claim to the reviewed project, configuration, revision, and evidence; it is not a guarantee of future behavior.
