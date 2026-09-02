# Harness V2 migration preview

This is preparation, not authorization. Do not run against active homes until the exact targets and baseline are approved.

## General V2 installation

`v2_migrate.py` snapshots, previews, installs, and rolls back:

- global `AGENTS.md`;
- on-demand routing policy;
- six explicit agent definitions;
- toolbox system utility and tests;
- self-contained project-bootstrap skill, references, helper, and assets.

It intentionally excludes `config.toml`, unrelated skills, Git configuration, projects, and authentication/state. Snapshot records target hashes, modes, absences, the complete existing project-bootstrap file set, and candidate hashes. Plan/install stop on candidate, target, root, or target-universe drift. Install durably backs up targets and records a `PREPARED` intent before every file mutation, then records `COMMITTED` after atomic replacement or removal. Recovery reconciles current hashes with prepared/committed states, refuses later drift, and removes only installation-created directories when they remain empty.

Use a mock home first. For active installation, capture an approved baseline immediately before the exclusive migration window and review the plan before `install`.

## Separate optional parent migration

`migrate_parent_model.py` is a distinct operation. It accepts only the expected Sol/medium control and exact config hash. It validates a content-addressed quality-gate receipt, reruns its pinned evaluator against the exact hashed fixtures/results, and requires the human-approved receipt hash. It durably writes the backup and `PREPARED` journal before changing only the model to Luna, then records `COMMITTED`; rollback also recovers a prepared transaction and refuses later drift.

Never bundle this optional step with general V2 installation. Run it only after Sol/medium control fixtures precede and support a non-regressing Luna/medium outcome and a human approves the result.
