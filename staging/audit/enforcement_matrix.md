# Enforcement matrix

| CAPABILITY | IMPLEMENTATION | ENFORCEMENT LEVEL | BYPASS / RISK | OWNER | KEEP? |
|---|---|---|---|---|---|
| Workspace confinement | `sandbox_mode=workspace-write` | NATIVE_ENFORCED | Writes inside allowed roots remain possible; runtime overrides/managed policy affect mode | Codex config/runtime | YES |
| Boundary approvals | `approval_policy=on-request` | NATIVE_ENFORCED | Routine in-sandbox actions do not prompt; explicit runtime overrides can change effective policy | Codex config/runtime | YES |
| Memory disabled | `features.memories=false` | NATIVE_ENFORCED for feature toggle | Higher-precedence CLI/project/managed layers may affect effective config | Global config | YES |
| Read-only researcher/planner/reviewer | agent `sandbox_mode=read-only` | NATIVE_ENFORCED default | Parent live runtime overrides are reapplied to children; model instructions still semantic | Agent config/runtime | YES |
| Zero custom command grants | empty candidate rules | EXECPOLICY_ENFORCED absence | Does not block in-sandbox destructive edits | Global rules | YES |
| Human gate | Global/project AGENTS | CONVENTION_ONLY | Model can misunderstand; semantics cannot be expressed completely as argv prefix | Human + agent | YES, explicitly labeled |
| Preserve quality/functionality | Global AGENTS | CONVENTION_ONLY | Semantic and task-dependent | Agent + reviewer | YES |
| Validate before success | Global AGENTS + project commands/tests | CONVENTION_ONLY until a project check exists | Agent can omit/misreport; evidence review needed | Agent/project | YES |
| Stack mechanical validation | Tests/static checks/hooks/CI after stack detection | DETERMINISTIC_PROJECT_CHECK | Only covers encoded invariant | Project | CONDITIONAL |
| Source-of-truth evidence | Register workflow | CONVENTION_ONLY | Evidence can stale; conflicts require audit | Project owner | CONDITIONAL |
| Decision acceptance provenance | Decision register/project process | CONVENTION_ONLY | Cannot prove authority without project process | Human/project | CONDITIONAL |
| Run-state reconciliation | Startup workflow + Git evidence | CONVENTION_ONLY | Stale checkpoint until verified | Project/session | CONDITIONAL |
| Protected content gate | Content register + human approval | CONVENTION_ONLY | Status may stale; no native content semantics | Content owner | CONDITIONAL |
| Project bootstrap path/symlink checks | Skill instructions + diff validation | CONVENTION_ONLY | No implementation script enforces them; human reviews proposal | Skill/root | YES with first-use review |
| Migration collision/hash/rollback checks | staged deterministic simulation and future migration procedure | DETERMINISTIC_PROJECT_CHECK | Simulation is not the real HOME; live races still require preflight | Migration operator | YES |
| Hooks | none | NOT_ENFORCED | No demonstrated global failure warrants automation | Future project/admin | NO for migration |
| Memory truth authority | AGENTS + memory strategy | CONVENTION_ONLY | Recall can conflict; feature remains off | Agent/human | YES as policy |
