# Repository layout

This repository versions reproducible harness source and evidence. Active runtime homes and machine backups are not source.

```text
bio-harness/
├── README.md
├── docs/                       # User-facing architecture and operations guides
├── staging/
│   ├── global/
│   │   ├── codex/              # Global AGENTS, agents, routing, config, rules, toolbox
│   │   └── agents/             # Self-contained project-bootstrap skill source
│   ├── blueprint/project/      # Inert, progressively activated private-project menu
│   ├── migration/              # V2 install, rollback, and optional parent migration
│   └── audit/                  # Deterministic tests, fixtures, quality results, provenance
├── migration-execution/        # Historical V1 migration program
└── .gitignore                  # Excludes machine backups and generated residue
```

## Lifecycle classes

| Area | Class | Purpose |
|---|---|---|
| `README.md`, `docs/` | Documentation | Stable entry points for users and maintainers |
| `staging/global/` | Source / staging | Installable global candidate files; inert until migrated |
| `staging/blueprint/` | Blueprint | Optional project-private templates, never wholesale policy |
| `staging/migration/` | Migration source | Hash-aware installation, rollback, and gated model change |
| `staging/audit/test_v2.py` and validators | Test | Deterministic structural and policy validation |
| `staging/audit/fixtures/`, `quality/` | Test / audit | Scenario fixtures, retained trial evidence, and gate outcomes |
| Other `staging/audit/` records | Audit / historical | Baselines, reviews, provenance, and installation evidence |
| `migration-execution/` | Historical | Prior migration source retained for provenance, not V2 guidance |

`backups/`, generated simulation state, Python caches, temporary files, and pre-bootstrap machine snapshots are local-only. Detailed audit evidence may contain historical absolute paths; general documentation avoids depending on them.
