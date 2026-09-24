# API Baseline

Use P01–P09 for every operation. Conditional checks within an area can be `Not applicable` with a reason. Evaluate shared configuration once where appropriate and map it to all affected operations. For non-HTTP APIs, apply equivalent protocol semantics and explain which HTTP-specific checks are inapplicable.

## P01 — Contract and discoverability

Confirm method/operation, effective path/version, purpose, exposure, accepted inputs, successful output, expected errors, and authentication requirements match the implementation. Compare a maintained contract (OpenAPI, schema, or equivalent documentation) with actual routes and serializers. Flag undocumented implemented operations and stale documented routes separately. Preserve established client conventions; do not require a particular naming style, URL version prefix, or response envelope without a project requirement or demonstrated interoperability problem.

## P02 — Request validation

Validate untrusted path, query, header, cookie, and body values on the trusted server before use. Check required versus optional values, null versus absent values, type/coercion behavior, bounds, lengths, enums, formats, nested objects/arrays, and cross-field business constraints. Verify unsupported media types and malformed input produce controlled errors. Confirm unknown or read-only fields cannot change protected properties through mass assignment. Validate pagination, sorting, filtering, and identifiers before query construction; use parameterized data access. Probe representative negative and boundary cases, not just valid input. Client validation and compile-time types do not establish runtime enforcement.

## P03 — Authentication and authorization

Establish intentional public versus protected access. For protected operations, check invalid/expired credentials and enforce operation/role, object ownership, tenant, and property-level permissions on the server. Include identifiers in nested inputs and bulk operations. Verify public and privileged responses expose only permitted fields. Cover alternate route registrations and middleware overrides. Test another user's object or tenant with disposable fixtures when applicable. Apply CSRF defenses to cookie-authenticated state changes where relevant; CORS is not authorization.

## P04 — Protocol and response semantics

Check methods and status codes against actual outcomes and the documented contract. Safe HTTP methods must not request business state changes. Idempotent methods must preserve intended effect across repeats; they need not return identical status codes each time. Check success/error schemas, content types, response headers, and deliberate treatment of absent resources, forbidden actions, conflicts, validation errors, and asynchronous acceptance. Ensure HEAD and no-content responses have appropriate body behavior where applicable. Do not mandate one validation status code for all frameworks; assess protocol correctness and consistent documented behavior.

## P05 — Errors and data exposure

Verify expected validation, domain, dependency, and unexpected failures produce controlled, consistent client responses. Responses must not expose stack traces, secrets, internal queries, or unauthorized fields. Confirm exceptions are handled at the boundary and useful diagnostics are available without sensitive payload logging. Error codes or field details should let callers act appropriately under the existing contract. Do not require a new error format merely for stylistic consistency.

## P06 — Business integrity and retries

Check invariants beyond input shape: valid state transitions, uniqueness, ownership, atomic multi-step writes, rollback, and concurrent updates. For retryable operations where duplicate effects matter (payments, submissions, jobs, webhooks), verify deduplication or equivalent safeguards, including scoping and persistence of idempotency records. Do not require idempotency keys on every POST. Verify retry policies do not amplify non-idempotent side effects; record unavailable dependency failure/concurrency evidence as unverified when needed.

## P07 — Resource limits and reliability

Check bounded request size, collection/page size, query complexity, batch size, uploads, and expensive processing where applicable. Review timeouts, cancellation, connection limits, and bounded retries for dependencies. Assess rate/abuse limits according to exposure and operation cost; do not require a fixed quota on every route. Verify protections cover their intended routes through handler, middleware, gateway, or deployment evidence. Avoid asserting performance thresholds without a defined requirement and measurement. Do not load-test live systems as a routine audit step.

## P08 — Transport, caching, and integrations

Check deployed transport protection and trusted proxy configuration for exposed APIs; local HTTP development alone is not a defect. Confirm caching cannot share private responses across users/tenants and cache keys/invalidation match the contract. Apply origin policy to browser-facing APIs. For inbound webhooks, verify signature checking over the expected payload, replay handling, and duplicate delivery behavior. For uploads, check size/type/content handling and storage access. For user-controlled outbound destinations, check destination restrictions and redirect behavior. Validate upstream responses and handle dependency errors before trusting external data. Mark unavailable deployment evidence explicitly.

## P09 — Verification and operability

Map positive and applicable negative checks to each endpoint. Record which assertions were executed, which came from static review, and which remain unverified. Confirm failures can be diagnosed using appropriate logs, request/correlation IDs, or equivalent telemetry, with sensitive fields redacted. Assess compatibility and deprecation behavior against known clients when contracts change. Health/readiness endpoints should reflect their intended purpose without leaking internals. A missing optional tool is not itself a defect, but missing evidence must not be reported as a pass.

## Sources and interpretation

This is a practical project baseline, not a certification checklist. Use the project's protocol/specification version and documentation. Verify relevant primary documentation when a framework or protocol detail is uncertain or a current standards assessment is requested.

- [HTTP Semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110.html) defines HTTP method and response semantics.
- [OpenAPI: API Endpoints](https://learn.openapis.org/specification/paths.html) and [Parameters and Payload](https://learn.openapis.org/specification/parameters.html) describe operation contracts and inputs; they do not prove runtime enforcement.
- [OWASP API Security Project](https://owasp.org/www-project-api-security/) informs security-specific review areas, including authorization, inventory, resource use, and integrations; it does not cover every API quality requirement.
