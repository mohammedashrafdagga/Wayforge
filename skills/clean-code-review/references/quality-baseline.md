# Clean-Code and Architecture Quality Baseline

Apply this baseline in the context of the language, framework, codebase size, and documented architecture. The principles are decision aids, not reasons to demand abstractions or personal formatting preferences. A `Pass` requires evidence across all relevant reviewed surfaces; a single representative example cannot establish a repository-wide pass.

## Core areas

### 1. Architecture conformance and boundaries

- Implementation matches the documented or clearly established architecture.
- Responsibilities live in the correct module, feature, package, or layer.
- Dependency direction is intentional and enforced where practical; inner domain or business policy does not depend on UI, transport, persistence, or vendor details.
- Cross-feature access uses deliberate public boundaries rather than internal imports, shared mutable state, or database shortcuts.
- Entrypoints and composition roots assemble dependencies without spreading construction and environment decisions through business code.
- Cycles, layer bypasses, and ambiguous ownership are absent or explicitly justified.

When DDD is intended, also apply the DDD section below. When feature separation is intended, review each important feature vertically across all relevant layers rather than approving its folder structure alone.

### 2. Separation of concerns and cohesion

- Modules, classes, functions, components, and hooks have a coherent responsibility and one primary reason to change.
- Transport, presentation, orchestration, domain policy, persistence, mapping, and infrastructure concerns are not mixed without a framework-supported reason.
- Related behavior and its invariants stay together; unrelated utilities do not accumulate into grab-bag modules.
- Boundary mapping is explicit enough to prevent persistence or wire formats from leaking throughout the system.

### 3. DRY and duplication

- Search for exact, structural, and semantic duplication in business rules, validation, authorization decisions, mappings, queries, error handling, UI behavior, types, and configuration.
- Treat repeated knowledge that must change together as a defect. Consolidate instances under one finding and list every known affected surface.
- Do not flag repetition solely by line count. Small local duplication may be safer than coupling unrelated concepts or introducing a premature abstraction.
- Identify divergent copies separately when duplication has already caused inconsistent behavior.

### 4. SOLID and dependency design

- Single responsibility: units remain cohesive and change for one business or technical concern.
- Open/closed: stable extension points exist where variants are real; conditionals are acceptable when clearer than speculative polymorphism.
- Liskov substitution: implementations honor the promises, error behavior, and invariants of their abstractions.
- Interface segregation: consumers are not forced to depend on operations or data they do not use.
- Dependency inversion: policy depends on stable abstractions at volatile boundaries; abstractions are not added where direct dependency is simpler and equally testable.
- Dependencies are minimal, directionally appropriate, and visible rather than hidden behind service locators or global state.

### 5. Simplicity: KISS and YAGNI

- The solution is no more general, layered, configurable, or indirect than current requirements justify.
- Dead extension points, unused wrappers, speculative flags, duplicate compatibility paths, and abstraction chains are removed or justified.
- Dense cleverness, metaprogramming, and compressed control flow do not obscure intent.
- Simplicity does not excuse duplicated domain knowledge, missing boundaries, or weak correctness guarantees.

### 6. Readability and local design

- Names communicate domain meaning, units, lifecycle, and side effects; misleading generic terms and unexplained abbreviations are avoided.
- Functions and methods operate at a consistent level of abstraction, keep inputs and outputs understandable, and avoid flag-driven multi-purpose behavior.
- Classes, modules, components, and files are sized according to cohesion and navigation cost, not arbitrary line limits.
- Control flow avoids unnecessary nesting, scattered early-exit policy, boolean blindness, and hidden fall-through.
- Comments explain non-obvious intent, constraints, or tradeoffs instead of narrating stale implementation details.
- Formatting and idioms follow configured project conventions. Style-only disagreement is not a reportable defect.

### 7. Domain rules, data, and type integrity

- Business invariants have one authoritative implementation and are protected at appropriate trust boundaries.
- Domain concepts use precise representations; invalid states are difficult to construct where the language permits.
- Nullability, optional values, identifiers, units, money, time, and state transitions are modeled consistently.
- DTOs, view models, persistence models, and domain models are not conflated when their contracts or change pressures differ.
- Mutable state and ownership are explicit; callers cannot unexpectedly corrupt shared data.

### 8. Errors, resources, and asynchronous behavior

- Errors retain actionable context, use consistent categories, and are handled at the layer that can make a meaningful decision.
- Exceptions or result values are not swallowed, converted into false success, used as routine control flow, or logged repeatedly at multiple layers.
- Cleanup, cancellation, timeouts, retries, and transaction boundaries match ownership of the operation.
- Async and concurrent work avoids unawaited operations, race-prone shared state, stale updates, duplicate side effects, and unbounded fan-out.
- User-facing messages, logs, and internal diagnostic details are separated appropriately.

### 9. Testability and test design

- Important domain rules, boundary mappings, failure paths, and regressions have proportionate automated coverage.
- Tests verify observable behavior and contracts rather than mirroring implementation details.
- Tests are deterministic, isolated at the right boundary, clearly arranged, and do not conceal failures with broad mocks or assertions.
- The test distribution fits the system; slow end-to-end tests do not substitute for missing focused coverage.
- Architecture rules with high recurrence risk are enforced by tests or static constraints where practical.
- Production code is not distorted solely to satisfy brittle tests.

### 10. Change safety and repository hygiene

- Public and internal contracts are explicit enough for safe change; compatibility behavior is intentional.
- Dead code, abandoned feature paths, stale TODOs, unused dependencies, and obsolete configuration do not mislead maintainers.
- Constants and configuration have one appropriate source of truth without hiding meaningful local context.
- Logging and observability support diagnosis without scattering infrastructure calls through domain logic.
- Build, type-check, lint, and test configuration are consistent across equivalent packages, or differences are documented.
- Documentation and architecture records describe current decisions that cannot be understood reliably from code alone.

## Conditional frontend areas

Apply when the scope includes a user interface.

- Feature ownership: pages, components, hooks, state, services, and tests follow the intended feature boundaries; shared UI contains genuinely reusable concepts rather than feature leakage.
- Component design: components have coherent responsibilities, predictable inputs and outputs, stable identities, and intentional composition; large components are split by behavior or ownership, not arbitrary line counts.
- State: state has a clear owner and minimal scope; derived state is computed rather than synchronized in duplicate; server state, form state, URL state, and client state are not conflated.
- Effects: effects synchronize with external systems, declare accurate dependencies, clean up resources, and do not replace ordinary derivation or event handling.
- Data access: fetching, caching, loading, empty, error, retry, and stale states are handled consistently at the correct boundary.
- Rendering: expensive work, unstable references, and broad subscriptions are optimized only when evidence or clear scale warrants it; correctness is never traded for memoization.
- UI contracts: reusable components have clear accessibility, interaction, and styling contracts; business rules are not duplicated across presentation variants.

## Conditional backend areas

Apply when the scope includes a server, worker, command-line service, or data-processing application.

- Delivery boundaries: controllers, handlers, resolvers, consumers, and jobs translate input and delegate; they do not become the primary home of business policy.
- Application orchestration: use cases coordinate domain behavior and ports without taking on transport or persistence details.
- Persistence: repositories and queries have clear ownership, avoid leaking ORM behavior across boundaries, and make transaction and loading behavior understandable.
- Integration boundaries: vendor SDKs, messaging, filesystem, clock, randomness, and network concerns are adapted behind appropriately narrow boundaries when volatility or testability justifies it.
- Work processing: retries, idempotency, ordering, partial failure, and duplicate delivery are handled consistently when applicable.
- Runtime lifecycle: connection pools, streams, file handles, background tasks, and shutdown behavior have explicit ownership.

## Conditional DDD and feature-separation areas

Apply when the project claims or clearly implements Domain-Driven Design, bounded contexts, clean or hexagonal architecture, or vertical feature slices.

- Bounded contexts and features have explicit ownership, vocabulary, public contracts, and dependency rules.
- Aggregates protect real consistency boundaries; entities and value objects encode identity and invariants rather than serving as anemic data bags by default.
- Application services orchestrate use cases; domain services contain domain operations that do not naturally belong to one entity or value object.
- Repositories represent domain-oriented collection boundaries rather than generic data-access helpers.
- Domain events represent meaningful completed facts and do not create invisible synchronous coupling.
- Cross-context translation uses explicit contracts or anti-corruption mapping where models differ.
- Shared kernels remain small and deliberately governed. A global `common`, `shared`, or `utils` area is reviewed for hidden coupling and unclear ownership.
- Each feature's presentation, application, domain, infrastructure, and tests follow the project's chosen slicing model; rules are not duplicated between frontend, backend, and data layers without a contract-based reason.
- Framework and persistence annotations in domain code are evaluated by their actual coupling cost and project conventions, not rejected mechanically.

## Evidence and finding rules

For each area, record which surfaces were inspected and cite paths and lines for failures. Useful supporting checks include configured linters, type checkers, test runners, dependency-cycle analyzers, duplicate-code detectors, complexity tools, and architecture tests. Tool output is evidence to investigate, not an automatic finding.

Every finding must state:

1. the violated project rule or baseline principle;
2. the root cause and all known affected surfaces;
3. a concrete correctness, change-cost, testability, or maintainability consequence;
4. the smallest durable remediation, including likely ownership and sequencing;
5. a verification method that can prove the remediation.

Do not report hypothetical future scale, alternative style, or a possible refactor with no credible benefit as a failure. Record worthwhile optional improvements separately from baseline findings.
