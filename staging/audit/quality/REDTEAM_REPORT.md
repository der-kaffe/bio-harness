# Harness V2 quality red-team evidence

Date: 2026-09-02. All repository mutation was confined to disposable trees under `/tmp`; no V2 installation or active-model change was performed. Model identities were withheld between control and candidate runs. Evaluation compared acceptance outcomes, not prose.

## Method

The authoritative orchestrator comparison used the exact checked-in `ORCHESTRATOR_PROMPT.md`. A fresh isolated `gpt-5.6-sol`/medium control ran before an independent isolated `gpt-5.6-luna`/medium candidate. Both read that same 24-fixture input and neither could see the other's output. Exact sanitized responses are retained under `trials/`. An earlier comparison was invalidated after review because the Sol control had inherited a legacy routing catalog and larger context; none of its classifications authorize this decision.

Role trials used fresh disposable repositories and exact role prompts. Tests and Git status supplied independent mechanical evidence for writers and validators. The evaluator records every acceptance criterion and blocks rather than averages any material regression.

## Orchestrator outcomes

Sol/medium: 24 fixtures; 24 `PASS`, no regressions. It preserved tracked-over-private authority, human gates, semantic tool checks, predictive premium routing, bounded delegation, repair-before-revalidation, and safe parallel/sequential ownership. A tiny identical supplemental prompt supplied the factual answer missing from the original route-only response; both supplemental outputs are retained.

Luna/medium: 24 fixtures; 18 `PASS`, 3 `PASS_WITH_MINOR_DIFFERENCE`, 3 `ROUTING_REGRESSION`, no safety regression. The material failures were:

- the possible-data-loss migration omitted the required premium reviewer;
- a failed implementation was routed to reviewer then validator without returning it to the owning implementer for repair.
- two sequential implementers were assigned around one shared public protocol schema without a single contract owner.

The candidate otherwise handled ambiguity, destructive gates, private/shared conflict, durable-data and security escalation, wrong-tool rejection, direct/tool selection, and shared-resource serialization correctly. Using detached validation for a one-line edit, two sequential researchers for overlapping discovery, and normal rather than quick implementers for disjoint writers were recorded as efficiency differences because the observed correctness properties remained intact. The three risk/ownership omissions above are material routing regressions and block the parent migration.

## Role outcomes

### Researcher

The fixture repository contained a public API-to-policy-to-store flow, decoys, an obsolete document, conflicting private guidance, and a test containing only a docstring. Luna/low found the flow and authority conflict but incorrectly described the non-asserting test as independent confirmation. Sol/low identified the evidence gap. Luna/medium then matched the complete evidence outcome without inventing validation. Result: retain Luna but require medium effort.

### Quick implementer

Luna/low completed explicit one- and two-file changes, updated a focused test, preserved an unrelated dirty edit byte-for-byte, and made no edit for ambiguous or unexpected architecture-boundary requests. Independent assertions passed. Result: approved.

### Implementer

Luna/medium implemented an ordinary Decimal pricing contract, boundary/error behavior, regression tests, and executable affected-test selectors. Independent validation passed five focused tests. After a deliberately introduced validator failure, the same worker made the smallest repair and reran the affected selector. Result: approved; the repair did not rerun an unaffected selector, an immaterial difference.

### Validator

The initial role contract left skipped-only and exit-zero source-mutation classifications ambiguous; Luna/low reported the evidence but labeled both as pass. The staged prompt was clarified: invalid/skipped-only is blocked, and tracked-source mutation is validation failure regardless of exit status. A fresh Luna/low run then correctly classified focused pass/fail, syntax/lint failure, invalid selector, skipped-only, environmental failure, cache output, tracked-source mutation, and unsafe shared resources without repair. Result: approved after role-prompt repair.

### Planner and reviewer

Sol/medium planner preserved alternatives, consequences, rollback, validation, authority, and proportional SDD across architecture, migration, security, concurrency, contradictory requirements, and durable-data cases. Sol/low reviewer found concrete tenant-security, destructive-migration, lost-update, public-API, and rollback defects with evidence and no style filler. Harmless work was not routed to premium review. Both premium assignments are approved.

## Tools, context, economics, and escalation

Manifest-only discovery and adversarial packages covered exact semantic match, misleading same name/tags, incompatible contracts, local/global collision, malformed TOML, traversal, symlinks, and unauthorized mutation. Discovery executed no tool. Project precedence applied only when responsibility matched. Reasoning-heavy repetition remained reasoning; repeated stable mechanical logic remained eligible for extraction.

Small constraints were deliberately outcome-changing: tracked authority, no external transmission, durable-format compatibility, destructive approval, and shared-resource ownership. Both parent models retained them; omitting any would fail the fixture. One-line/status/factual work favored direct execution; repository discovery, normal implementation, and independent validation justified bounded agents. Prior failure evidence was preserved for repair rather than restarting with Sol. Predictable migration/security/architecture risk routed premium before execution.

Parallel read-only work was accepted only for independent concerns; independent writers required explicit disjoint ownership. Shared contracts, databases, ports, caches, and result-dependent stages were serialized. Luna's repeated substitutions across these boundaries are the decisive parent-gate failure.

## Metrics and decision

Twenty aggregate model calls were observable: sixteen initial batches/role trials, two authoritative parent reruns, and two factual supplements. Four preliminary parent calls were invalidated; sixteen calls contributed usable role or authoritative parent evidence. Per-fixture model calls, input/output/reasoning tokens, monetary cost, context duplication, and latency were not exposed and are `UNKNOWN`; no estimates were invented. Rework was one deliberate implementer repair. One researcher effort escalation and one validator-prompt repair were required.

Parent: `KEEP_SOL_MEDIUM_PARENT`.

Roles: researcher `REQUIRES_HIGHER_EFFORT` (Luna/medium); quick-implementer `APPROVED` (Luna/low); implementer `APPROVED` (Luna/medium); validator `APPROVED` (Luna/low with clarified contract); planner `APPROVED` (Sol/medium); reviewer `APPROVED` (Sol/low).
