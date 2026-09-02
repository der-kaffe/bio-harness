# Harness V2 staging validation

Validated on 2026-09-02 with Codex CLI 0.152.0. The quality red-team and local hybrid installation are complete. No project adoption, real-project Git-exclude change, or parent-model migration was performed.

| Check | Result |
|---|---|
| `python3 -B staging/audit/validate_staging.py` | PASS |
| Unified infrastructure/policy tests | 38/38 PASS |
| Toolbox standalone tests | 3/3 PASS |
| Git-privacy standalone tests | 4/4 PASS |
| Quality fixture/result schema | 67 fixtures PASS |
| project-bootstrap skill validator | PASS |
| Blueprint/installed-copy asset parity | PASS |
| Global AGENTS budget | 294 words; PASS |
| Routing policy budget | 549 words; PASS |
| Private project router budget | 129 words; PASS |
| Independent Sol/low quality review | APPROVE after remediation |

The suite exercises normal and linked worktrees, paths with spaces, tracked private-looking paths, dirty/non-Git/malformed repositories, idempotent excludes, read-only and symlink failures, local/global tool discovery and precedence, malformed/traversing/symlinked packages, non-executing discovery, project-only scaffolding, catalog/config invariants, quality-first ordering, outcome evidence, Sol-before-Luna control, general install/rollback, root mismatch, true interrupted PREPARED-journal recovery, exact evidence-bound parent migration, and drift rejection.

The first reviewer pass found non-durable mutation journals, a boolean-only Luna gate, weak result evidence, rollback root ambiguity, and created-directory residue. These were corrected. A second pass found partial-prefix recovery and exact control/candidate binding gaps; these were corrected and the final closure review reported no BLOCKER or MAJOR finding.

## Quality decision

- Sol/medium parent control: 24 PASS, 0 regressions.
- Luna/medium parent candidate: 18 PASS, 3 PASS_WITH_MINOR_DIFFERENCE, 3 ROUTING_REGRESSION, 0 safety regressions.
- Parent decision: `KEEP_SOL_MEDIUM_PARENT`.
- Researcher: Luna/medium after Luna/low missed material evidence.
- Validator: Luna/low after the skipped-only/source-mutation contract was corrected and re-tested.
- The V2 hybrid was installed locally through the validated migration; no real-project bootstrap was exercised.
- Account-level model availability was not re-probed with paid workloads; current local Codex configuration/capabilities and active Sol use are the available evidence.
