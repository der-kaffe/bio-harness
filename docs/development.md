# Development and testing

Develop against staged source. Do not edit the active `~/.codex` or `~/.agents` installation to prototype a change.

## Common changes

- Global working agreement: edit `staging/global/codex/AGENTS.md` and preserve its small always-loaded budget.
- Agent role: edit the matching file under `staging/global/codex/agents/`; pin model, reasoning effort, and sandbox explicitly.
- Routing: edit `staging/global/codex/routing/MODEL_ROUTING.md`; keep it on demand rather than importing it globally.
- project-bootstrap: edit `staging/global/agents/skills/project-bootstrap/` and keep its assets self-contained and synchronized with the blueprint where validation requires parity.
- Project blueprint: edit `staging/blueprint/project/`; treat it as an activation menu.
- Toolbox system: edit `staging/global/codex/toolbox/_system/`. New reusable tools need narrow semantic contracts, tests, and justified scope; project tools are preferred until global promotion is approved.

## Deterministic validation

Run the repository's unified entry point from the repository root:

```bash
python3 -B staging/audit/validate_staging.py
```

It runs the unified policy/infrastructure tests, quality evidence validation, project-bootstrap validation, toolbox tests, privacy tests, budget checks, candidate parity checks, and migration simulations. It does not run paid model benchmarks or install the harness.

Before review or commit, also run:

```bash
git diff --check
```

Inspect changed paths and the exact staged set. For documentation, verify relative links resolve and Mermaid fences are balanced. Do not install a dependency merely for those lightweight checks.

## Quality and review

Model or prompt changes that affect an approved assignment require representative role fixtures. A proposed parent change requires a Sol/medium control first and cannot pass with a safety regression, unresolved material routing regression, or repeated material quality regression. Outcomes—not prose equality—are compared.

Use a read-only reviewer for architecture, migration, security, public contracts, or accumulated substantial changes. Review source and evidence before installation. Installation itself must use the [transactional migration](installation.md), create verified backups, and undergo a separate post-install review.

Audit outputs belong under `staging/audit/`; stable explanations belong in `docs/`. Never replace retained trial evidence with an unsupported summary.
