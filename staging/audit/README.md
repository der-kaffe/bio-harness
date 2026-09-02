# Adversarial audit harness

This directory contains inert repository fixtures, deterministic staging checks, and an isolated migration simulation. Nothing here targets the real `~/.codex`, `~/.agents`, job-forge, Geometra, MCP, memory, or plugins.

- `fixtures/`: representative repository shapes A–J and expected bootstrap decisions.
- `validate_staging.py`: read-only structural and packaging validation.
- `simulate_migration.py`: creates mock homes only under `audit/simulation/run-001` and exercises preflight, partial failure, install, rollback, drift, and collision behavior.

Repository fixture content is deliberately treated as untrusted input. The tests assert decisions and invariants; they do not run project scripts or bootstrap real repositories.
