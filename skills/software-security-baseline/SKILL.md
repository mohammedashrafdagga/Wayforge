---
name: software-security-baseline
description: Review or harden a software application against a practical minimum security baseline, using a full first review and branch-aware incremental reviews thereafter. Use for pre-release security checks, security-focused change reviews, minimum-control audits, or remediation of essential safeguards; do not use as a substitute for a penetration test, compliance assessment, or legal advice.
metadata:
  author: "mohammedashrafdagga"
  version: "1.1.0"
  supported-agents: "codex,claude-code,cursor"
---

# Software Security Baseline

Assess whether an application has a defensible minimum level of security for its actual exposure and data. Prioritize exploitable weaknesses and practical remediation over checklist volume.

## Establish scope

Before judging controls, determine from the repository and available context:

- application type, deployment model, environments, and internet exposure;
- users, roles, trust boundaries, administrative paths, and tenant boundaries;
- sensitive data, credentials, payments, regulated data, and retention needs;
- APIs, third-party integrations, webhooks, uploads, background jobs, and outbound requests;
- build, deployment, hosting, database, backups, logging, and update ownership.

Ask only for material facts that cannot be discovered safely. If facts remain unavailable, state assumptions and mark affected controls `Not verified`.

## Review workflow

1. Identify the application root. In a single-application repository, use the repository root. In a monorepo, use the scoped application's root unless the user requested a repository-wide review. Never place application reports inside this skill's directory.
2. Ensure `<application-root>/security/` exists, preserving any existing content. Do not add a placeholder solely to make an empty directory visible to version control.
3. Inspect existing `security/report_*.md` files to understand prior checkpoints and findings, and retain stable issue IDs where the same root cause remains.
4. Inspect architecture, authentication and authorization flows, data paths, configuration, dependencies, deployment files, and tests. Follow repository instructions and use ecosystem-native security checks when available.
5. Read [references/minimum-baseline.md](references/minimum-baseline.md). Assess every core area and each applicable conditional area.
6. Prefer direct evidence: code paths, configuration values with secrets redacted, tests, lockfiles, CI rules, infrastructure definitions, and operational documentation. Do not award a pass from filenames, dependencies, comments, or stated intent alone.
7. Trace security boundaries end to end. For example, confirm that authorization is enforced by the trusted backend on every relevant operation, not only hidden in the UI.
8. When the user requests a review, do not change application code; creating the requested `security/` directory and issue report is allowed. When the user requests hardening or fixes, make the smallest cohesive changes, preserve existing behavior where safe, and add or run proportionate tests.
9. Re-run relevant checks after fixes and report remaining risk and unverified operational controls.

## Select full or incremental review

Record the current Git branch and exact reviewed revision on every run. Include staged, unstaged, and untracked application changes in the reviewed state.

- Use `Full` mode when no comparable prior report exists, the user requests a full review, the prior checkpoint cannot be trusted, or broad dependency, deployment, identity, or trust-boundary changes invalidate it.
- Otherwise use `Incremental` mode. Prefer the newest comparable reviewed commit that is an ancestor of the current `HEAD`, including a checkpoint recorded on a parent branch. Review its committed diff through `HEAD` plus working-tree changes.
- For diverged histories, use a trustworthy merge base only when it is the last shared reviewed state; otherwise use `Full`. Record why.
- Review added, edited, moved, and deleted behavior. Follow changes through affected entry points, trust boundaries, roles/tenants, dependencies, configuration, tests, and deployment behavior. Shared authentication, authorization, parsing, storage, or CI changes bring their consumers into scope.
- Do not repeat the full security audit for untouched code. Carry unresolved untouched findings forward by ID and prior-report link; reverify them only when affected or explicitly requested.

An incremental result applies only to the reviewed change set. Inherited unresolved Critical/High findings still affect the release decision, and a clean delta is not evidence that the whole application meets the baseline.

Use these control states:

- `Pass`: implementation and relevant verification evidence are present.
- `Fail`: absent, ineffective, or bypassable control.
- `Not verified`: evidence is missing or cannot be tested in the current environment.
- `Not applicable`: the exposure or feature does not exist; include the reason.

## Severity and release decision

Rate findings by realistic impact and exploitability, considering internet exposure, privileges, data sensitivity, tenant reach, and compensating controls:

- `Critical`: likely direct compromise, mass sensitive-data exposure, authentication bypass, arbitrary code execution, or equivalent business-threatening impact.
- `High`: plausible account takeover, privilege or tenant-boundary bypass, significant data exposure, or material supply-chain/deployment compromise.
- `Medium`: meaningful weakness that needs pre-release treatment when exposed, but requires stronger preconditions or has limited impact.
- `Low`: defense-in-depth, limited exposure, or hygiene issue with credible security value.

The minimum release gate fails when any reviewed or inherited unresolved Critical or High finding exists. It also remains `Not ready to approve` when a release-critical control cannot be verified. A risk acceptance must name the owner, rationale, compensating controls, and expiration; do not silently convert acceptance into a pass. In incremental mode, a passing change set is not a whole-application approval unless the prior full baseline plus every later delta remains comparable and clear.

## Safety boundaries

- Keep assessment activity read-only unless the user requested changes.
- Do not attack production, third-party systems, or real user accounts without explicit authorization and a defined test scope. Prefer local tests and non-destructive validation.
- Never print, copy, or store live secrets or unnecessary personal data. Report secret locations and identifiers in redacted form.
- Do not claim the application is “secure.” State the reviewed scope, evidence, limitations, and date.
- Flag possible legal, privacy, payment, health, or industry obligations for specialist review; do not declare compliance from this baseline.

## Deliverable

Lead with one outcome: `Meets minimum baseline`, `Does not meet minimum baseline`, or `Not ready to approve`.

Read [references/report-format.md](references/report-format.md) and create a new Markdown report in the application's `security/` directory on every completed review. The report is also the checkpoint for a later incremental run. A `Not verified` control is tracked because it still requires review, evidence, or testing; do not describe it as a confirmed vulnerability.

Name the report `report_NNN.md`:

- Find existing files whose names match `report_` followed by an integer and `.md`.
- Use one greater than the largest existing report number, starting at `report_001.md` and padding to at least three digits.
- Never overwrite, delete, or renumber an earlier report. If the chosen path now exists, recalculate before writing.

When every applicable control in the active scope passes and there are no actionable findings, create a short checkpoint report with the scope and verification summary; do not expand it with repeated passing-control detail.

If the application root is not writable, do not place the report elsewhere. Return the intended path and report content in the response, and state that persistence is blocked by write access.

The response and report must provide:

1. review mode, branch, base and reviewed revision, working-tree state, scope, assumptions, and important exclusions;
2. release blockers first;
3. findings with severity, affected component and evidence location, credible impact, specific remediation, and verification method;
4. compact coverage grouped by changed feature or trust boundary, with detail only for issues and evidence gaps;
5. prioritized next actions split into `before release` and `after release`;
6. checks run, checks not run, and residual risk.

Avoid vague advice. Cite exact file paths and lines when reviewing code. Consolidate repeated instances that share one root cause, but identify all known affected surfaces. Link the newly created report in the response.

## Standards basis

Use the baseline reference as the operational checklist. Treat OWASP ASVS as the verification-oriented source, OWASP Top 10 as risk awareness rather than complete coverage, NIST SSDF as development-process guidance, and CISA Secure by Design as the basis for safe defaults and vendor ownership of customer security outcomes. Re-check current versions when the user requests a formally current or externally cited assessment.
