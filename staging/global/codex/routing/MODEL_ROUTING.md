# Quality-first model routing

## Invariant

Route in this order: correctness, safety, task-required reasoning quality, reliability and reproducibility, then cost, tokens, context, and latency. “Cheapest sufficient” means the least expensive candidate whose demonstrated or strongly justified capability meets the task's quality floor. Price alone never establishes sufficiency.

## Sequence

1. Assess requirements, risk, ambiguity, authority, reversibility, and required quality.
2. If deterministic work has a validated tool with the same semantic contract, use it.
3. If work is truly trivial and reliable for the parent, execute directly.
4. Otherwise assign one bounded responsibility to the appropriate role.
5. Route directly to premium reasoning when predicted capability need or risk warrants it; do not try a weaker tier first when failure could create subtle or hard-to-reverse harm.

## Roles

- `researcher` (Luna/low, read-only): multi-file discovery, tracing, documentation research, and root-cause evidence. No implementation, validation, review, or architecture decisions.
- `quick-implementer` (Luna/low): explicit low-risk, tightly bounded changes, usually around one or two files, with one proportionate focused check.
- `implementer` (Luna/medium): normal features, multi-file fixes, affected tests, and focused repair from validator evidence.
- `validator` (Luna/low): assigned test, build, lint, or type-check scope; no repairs or source edits.
- `planner` (Sol/medium, read-only): consequential architecture, migration, durable data, security, concurrency, public contracts, destructive work, contradictory constraints, and LARGE/RISKY SDD.
- `reviewer` (Sol/low, read-only): independent high-risk review. Skip routine small changes with adequate focused validation.

## Premium routing

Use premium planning or review from the beginning for consequential architecture, security boundaries, migrations, durable-data changes, concurrency, destructive or difficult-to-rollback work, public compatibility, and materially contradictory requirements. Failure-based escalation remains available when complexity was not predictable. Preserve prior evidence and state what stronger reasoning must resolve; do not retry blindly.

## Context and ownership

Default to task-local context, not the entire parent conversation. Supply every critical requirement, constraint, contract or spec link, owned file/module boundary, authority and human-gate boundary, and relevant prior failure. Compression that removes decision-critical meaning is a quality regression. Require compact, decision-ready reports rather than raw search output, logs, files, or diffs.

Parallelize only independent work whose contexts and write surfaces do not overlap. Writers require explicit non-overlapping ownership. Prefer sequential reuse when retained context avoids duplication. Do not parallelize validation sharing mutable databases, fixtures, snapshots, ports, caches, generated outputs, or coverage artifacts unless isolation is proven.

## Validation and review

A trivial change may receive its obvious check directly. A quick implementer may run one narrow check. Normal or substantial implementation should usually receive detached focused validation using a complete affected-test manifest. Use a full suite when the accepted specification requires it, selection is unreliable, or risk warrants it. A validator never silently repairs failures; classify evidence, resume the same implementer when useful, and revalidate.

Premium review is proportionate, not ceremonial. Use it for security, migration, concurrency, architecture, public contracts, durable data, destructive changes, substantial accumulated diffs, or difficult-to-validate behavior.

## Quality gates

Cheaper assignments remain provisional until representative role fixtures pass. Sol/medium is the orchestrator control. Luna/medium may become the parent only after outcome-based comparison shows no safety, material routing, or material quality regression. If it fails, retain Sol/medium and continue with independently validated cheaper workers and tools.

Measure outcome quality, safety, success, rework, escalations, calls, context duplication, tokens and cost when observable, and latency secondarily. Unknown metrics remain unknown.
