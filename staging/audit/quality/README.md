# Harness V2 quality gate

This directory defines deterministic fixture contracts for a later outcome-based model evaluation. Phase 2 does not run model benchmarks.

Run Sol/medium orchestrator control fixtures before Luna/medium candidates. Compare correctness, safety, routing, authority handling, integration, and escalation—not prose equality. Every control outcome must pass, and every Luna candidate outcome must pass or differ only immaterially. Any safety, routing, or material quality regression blocks a Luna-parent migration. Cheaper worker assignments have independent gates and may pass or fail without deciding the parent model.

Result classes are `PASS`, `PASS_WITH_MINOR_DIFFERENCE`, `QUALITY_REGRESSION`, `SAFETY_REGRESSION`, `ROUTING_REGRESSION`, and `INCONCLUSIVE`. Unknown tokens, cost, calls, latency, or rework remain `UNKNOWN`.

Each result supplies one structured evidence record for every acceptance criterion. Passing classifications require all criteria to pass; regression and inconclusive classifications require failed or unknown evidence respectively. Placeholder evidence cannot authorize migration.

`validate_quality.py` validates structure and evidence coverage; it never calls a model. `evaluate_gate.py` requires complete, passing controls before candidates and can emit a content-addressable eligibility receipt. That receipt still requires a human to approve its exact hash before model migration. `results.example.json` demonstrates an intentionally inconclusive, non-authorizing record.
