# Audit and validation evidence

This directory contains deterministic staging checks, inert repository fixtures, retained quality-red-team evidence, independent reviews, provenance, and installation receipts. General readers should start with [`../../docs/README.md`](../../docs/README.md); this area preserves the evidence behind those summaries.

- `fixtures/`: representative repository shapes and expected bootstrap decisions.
- `quality/`: fixture definitions, exact retained trials, outcome results, evidence hashes, and final review.
- `validate_staging.py`: unified structural, policy, packaging, migration, and evidence validation.
- `simulate_migration.py`: creates mock homes only under ignored `audit/simulation/` and exercises preflight, partial failure, install, rollback, drift, and collision behavior.
- `HARNESS_V2_HYBRID_INSTALL_20260902T231047Z.md`: the verified local V2 installation receipt. It records hashes and outcomes, not active runtime data.
- `upstream_provenance.md`: pinned external-reference provenance and adaptation decisions.

Repository fixture content is deliberately treated as untrusted input. Deterministic tests use disposable homes and repositories; they do not run project scripts or bootstrap real repositories. Historical reports describe the state at the time they were written and do not override the current staged source, quality decision, or installation receipt.
