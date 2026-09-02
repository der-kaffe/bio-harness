# Candidate config adversarial audit

Validated against Codex CLI 0.152.0, the bundled model catalog, strict app-server parsing, `features list`, and the official configuration reference.

| SETTING | VALUE | EVIDENCE / BEHAVIOR | DECISION |
|---|---|---|---|
| `model` | `gpt-5.6-sol` | Bundled 0.152.0 catalog contains the slug | KEEP: explicit requested default |
| `model_provider` | `openai` | Official key; built-in default is `openai` | KEEP: explicit ownership and no job-forge provider inheritance; one stable line |
| `model_reasoning_effort` | `high` | Official values include `high`; bundled model advertises it | KEEP |
| `sandbox_mode` | `workspace-write` | Official enum includes it; confines ordinary writes to workspace/protected policy | KEEP; not full access |
| `approval_policy` | `on-request` | Official interactive policy; `on-failure` is deprecated | KEEP |
| `features.memories` | `false` | Stable feature, official boolean, current default off | KEEP deliberately: pins a privacy/authority policy if a future default changes; not aesthetic state |

Strict parsing accepted the complete candidate. Configuration precedence remains: CLI/`--config` → trusted project config (closest wins) → selected profile → user config → system config → defaults. Therefore this file is a default, not an unoverrideable policy. Managed `requirements.toml` can also constrain effective choices.

Absent by design: profiles, notices, trusted project paths, MCP, Geometra/job-forge, custom compaction, memory enablement, hooks, additional writable roots, network enablement, and full access. No deprecated key was found.

Residual uncertainty: parsing and bundled availability do not prove account entitlement or that a future CLI preserves the same schema. Revalidate immediately before migration.
