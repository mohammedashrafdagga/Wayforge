# Minimum Software Security Baseline

Use this as a risk-based floor for a small-business application, not as proof of security or compliance. Assess every core area. Apply conditional checks only when the feature or exposure exists. A minimum can be implemented differently across stacks, but the security outcome and evidence must be equivalent.

## Core controls

### 1. Ownership, architecture, and data

Minimum outcome:

- The application's deployed components, public entry points, trust boundaries, privileged functions, third parties, and data stores are identifiable.
- Sensitive data is classified at least informally, collected only when needed, and has an owner and retention/deletion expectation.
- High-impact abuse cases are considered: account takeover, privilege escalation, cross-tenant access, bulk export, destructive actions, fraud, and service exhaustion.
- Production security configuration, patching, backups, alerts, and incident handling each have an accountable owner.

Evidence examples: architecture or deployment definitions, route/API inventory, schema, role model, data-flow notes, runbooks, ownership files.

### 2. Authentication and account recovery

Minimum outcome:

- Protected features require authentication. Privileged or administrative accounts for an internet-exposed application require MFA through the application or its identity provider; absence is normally High.
- Passwords, if used, are stored with a maintained adaptive password-hashing implementation and never logged or reversibly encrypted.
- Login, registration, reset, verification, and recovery resist user enumeration, token replay, brute force, and predictable tokens.
- Recovery does not provide a weaker path than normal authentication. Default, shared, and vendor-known passwords are prohibited.
- Authentication failures are rate-limited or otherwise abuse-resistant without enabling trivial account denial of service.

Evidence examples: identity-provider settings, auth handlers, password library configuration, recovery-token generation and expiry, MFA enforcement tests.

### 3. Sessions and credential lifecycle

Minimum outcome:

- Session identifiers and tokens are generated, validated, stored, and transmitted using maintained platform mechanisms.
- Browser session cookies use `Secure`, `HttpOnly`, and an appropriate `SameSite` value; state-changing cookie-authenticated requests have CSRF protection.
- Sessions expire appropriately, rotate after authentication or privilege changes, and can be invalidated on logout, reset, role change, or compromise.
- Long-lived credentials are narrowly scoped, revocable, and not placed in URLs, logs, browser storage without justification, or client code where they cannot remain secret.

Evidence examples: middleware configuration, token claims and validation, logout/revocation paths, cookie tests, CSRF tests.

### 4. Authorization and isolation

Minimum outcome:

- Access is denied by default and enforced server-side for every protected operation and object, including alternate HTTP methods, APIs, exports, background jobs, and administrative functions.
- Object ownership, role, organization, and tenant checks use trusted server-side identity, not caller-supplied ownership claims.
- Sensitive changes require current authorization; highly consequential actions use re-authentication or equivalent step-up protection when appropriate.
- Tests include unauthenticated, wrong-role, wrong-object, and cross-tenant negative cases.

Evidence examples: centralized policies/middleware, query scoping, service-layer checks, authorization matrix, negative integration tests.

### 5. Untrusted input, output, and injection resistance

Minimum outcome:

- Untrusted input is validated for expected type, length, range, structure, and business rules at the trusted boundary.
- Database access uses parameterized queries or safe ORM APIs. OS commands, templates, paths, LDAP, XML, and other interpreters receive context-specific safe handling.
- Output is encoded for its destination context. Rich HTML is sanitized with a maintained sanitizer; ordinary text is not treated as markup.
- Redirects, filenames, archive extraction, and path operations cannot escape an intended allowlisted destination.
- Deserialization uses safe formats and types; untrusted data cannot select arbitrary executable classes or behavior.

Evidence examples: validators, parameter binding, escaping/sanitization calls, adversarial tests, parser configuration.

### 6. Secrets and cryptography

Minimum outcome:

- No production secret, private key, credential, or sensitive token is hardcoded or committed. Secrets come from an appropriate secret store or protected environment mechanism.
- Secrets have least privilege, separate production and non-production values, a rotation path, and prompt revocation after exposure.
- Maintained standard cryptographic libraries and protocols are used; custom cryptography and obsolete algorithms/protocols are absent.
- Security-sensitive comparisons, randomness, encryption modes, nonces, and key handling use library-supported safe patterns.

Evidence examples: secret references with values redacted, repository history scan results, key scopes, rotation procedure, crypto-library configuration.

### 7. Data protection and privacy

Minimum outcome:

- Sensitive data is encrypted in transit using currently supported TLS. Plaintext network paths are removed or tightly isolated and justified.
- Sensitive data at rest is protected according to its threat model, including databases, object storage, exports, backups, and developer copies.
- Logs, analytics, error reports, support tooling, and non-production environments do not expose passwords, tokens, payment data, or unnecessary personal data.
- Access to sensitive data is least-privileged and auditable. Retention and deletion behavior matches stated business and user expectations.

Evidence examples: TLS and datastore settings, log redaction, field inventory, access policies, deletion jobs, backup configuration.

### 8. Secure configuration and deployment

Minimum outcome:

- Production disables debug modes, sample accounts, unsafe diagnostics, directory listing, unnecessary services, verbose errors, and development-only endpoints.
- Security-relevant defaults are safe. Environment separation prevents test data, credentials, and callbacks from crossing into production.
- Infrastructure, database, object storage, queues, and administrative interfaces are not publicly reachable unless required and access-controlled.
- Deployment fails closed when critical security configuration is missing. Production changes are reviewable and attributable.
- Responses do not reveal unnecessary version or infrastructure details.

Evidence examples: environment schema, deployment manifests, network policies, startup validation, production config, change history.

### 9. Dependencies and software supply chain

Minimum outcome:

- Direct and transitive dependencies are reproducible through lockfiles or equivalent controls and come from expected sources.
- Unused dependencies are removed. Known vulnerabilities are scanned, triaged, and patched or explicitly risk-accepted; Critical and realistically exploitable High issues block release.
- Build and release credentials are least-privileged, protected, and separated from untrusted contributions. CI actions/plugins and base images are pinned or otherwise integrity-controlled.
- Released artifacts can be traced to reviewed source and a controlled build. The team can inventory shipped components, using an SBOM when proportionate or customer-required.

Evidence examples: lockfiles, dependency scan, update policy, CI configuration, artifact provenance/signing, component inventory.

### 10. Logging, alerting, and auditability

Minimum outcome:

- Security-significant events are logged: authentication and recovery outcomes, authorization failures, privileged changes, permission changes, secret/config changes, bulk access/export, and destructive actions as applicable.
- Logs identify time, event, actor or correlation identifier, and outcome without storing secrets or excessive personal data.
- Log access is restricted and tamper resistance/centralization is proportionate to risk. Retention is long enough for investigation.
- Actionable alerts have an owner and a tested notification path. Repeated login failures, privilege changes, and suspicious administrative activity are not merely stored and ignored.

Evidence examples: structured logging calls, redaction rules, audit-event schema, alert definitions, sample redacted events, incident runbook.

### 11. Error handling and availability safeguards

Minimum outcome:

- Unexpected failures return generic client errors, preserve useful internal diagnostics safely, and do not leak stacks, queries, secrets, or internal paths.
- Security decisions fail closed. Transactions and partial failures do not leave authorization, money, inventory, or sensitive workflows in an unsafe state.
- Expensive operations and exposed endpoints have proportionate limits for request size, rate, concurrency, timeout, pagination, and resource consumption.
- Health checks, dependency failures, retries, and queues do not create retry storms or expose privileged diagnostics.

Evidence examples: global exception handling, limit configuration, transaction boundaries, timeout/retry policies, failure-path tests.

### 12. Backup, recovery, and incident readiness

Minimum outcome:

- Important data and configuration are backed up with access controls and protection comparable to production.
- Restore has been tested recently enough to support the business recovery need; a backup job reporting success is not sufficient evidence by itself.
- The team can revoke credentials, disable accounts/integrations, preserve relevant logs, deploy a security fix, and communicate during an incident.
- A monitored security contact and a process for receiving, prioritizing, fixing, and disclosing vulnerabilities exist.

Evidence examples: restore-test record, recovery objectives, incident checklist, credential-revocation procedure, security contact, patch workflow.

### 13. Security verification and release discipline

Minimum outcome:

- Security-sensitive changes receive peer review and relevant negative tests. Automated tests cover critical authentication, authorization, validation, and failure paths.
- Secret, dependency, and code/security scanning appropriate to the stack run before release; findings are triaged rather than ignored wholesale.
- Production-like verification confirms configuration and behavior without using production secrets or personal data.
- Accepted risks are documented with an owner, compensating controls, and expiration. Security regressions become repeatable tests when feasible.

Evidence examples: branch protections, review records, CI jobs, test output, scan triage, time-bounded risk register.

## Conditional controls

Apply these when the feature or exposure exists:

| Condition | Minimum additional checks |
| --- | --- |
| Browser UI | Content Security Policy appropriate to the application, clickjacking defense, secure content types, restrictive cross-origin policy, no sensitive caching, CSRF defense, and safe DOM APIs. |
| Public API | Per-object and per-function authorization, schema/content-type validation, bounded pagination and payloads, rate/usage limits, non-leaking errors, replay/idempotency controls where needed, and maintained API documentation/inventory. |
| Multi-tenant application | Tenant scoping at a trusted centralized layer; isolation tests for reads, writes, search, exports, caches, files, jobs, logs, and support/admin tooling. |
| File upload or document processing | File size/count limits, generated storage names, extension/content validation, storage outside executable/public paths, authorization on retrieval, malware/content handling proportionate to risk, safe archive extraction, and isolated parsers. |
| Server-side URL fetching or webhooks | Strict destination validation, redirect revalidation, protection against private/link-local/metadata networks, safe DNS behavior, authentication/signature verification, replay protection, bounded timeouts and response sizes, and secret-safe logs. |
| Payments or valuable transactions | Use a specialized provider where possible; never store prohibited card data; verify provider callbacks; prevent replay/duplicate processing; maintain an auditable ledger; require stronger authorization for refunds, payouts, and destination changes. |
| Email, SMS, invitations, or sharing links | High-entropy, scoped, single-purpose, expiring tokens; revocation or one-time use where appropriate; no sensitive data in URLs; abuse limits; recipient and permission revalidation at redemption. |
| Mobile or desktop client | Treat shipped clients as attacker-controlled; keep authorization and secrets server-side; use platform secure storage; validate updates; minimize local sensitive data; assess deep links/custom protocols and certificate validation. |
| AI/LLM feature | Treat model output and retrieved content as untrusted; isolate tools and tenants; authorize every tool/data action; constrain data disclosure and prompt-injection impact; require confirmation for consequential actions; log decisions without sensitive prompt leakage. |
| Administrative/support tooling | Separate privileged roles, MFA, least privilege, auditable impersonation with clear indication, re-authentication for critical actions, restricted network exposure where practical, and no unaudited direct database edits. |

## Finding quality

For each finding, record:

- a stable identifier and concise title;
- severity and why it has that severity in this application;
- affected component, endpoint, role, tenant, or data;
- evidence with exact paths/lines or a reproducible non-destructive observation;
- a credible abuse path and business impact, without overstating certainty;
- the smallest durable remediation and any relevant compensating control;
- a test that proves the fix and prevents regression.

Do not report speculative scanner output as a confirmed vulnerability. Label it `Needs validation` and explain what evidence would confirm or dismiss it.

## Authoritative basis

- [OWASP Application Security Verification Standard 5.0.0](https://owasp.org/www-project-application-security-verification-standard/) — verification requirements for application technical controls.
- [OWASP Top 10:2025](https://owasp.org/Top10/) — current web-application risk awareness; OWASP explicitly recommends ASVS when a verifiable standard is needed.
- [NIST SP 800-218, Secure Software Development Framework 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) — secure development practices across the software lifecycle.
- [CISA, Shifting the Balance of Cybersecurity Risk](https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_508c.pdf) — secure-by-design and secure-by-default principles.

These sources are broader than this small-business floor. Use their current detailed requirements when the application is high-risk, regulated, contractually constrained, or needs a formal assurance target.
