# Harness V2 hybrid active installation audit

- Installation completed: 2026-09-02T23:14:50Z
- Source repository HEAD: `e3c9f83c6f0505263ba9ed7a0b232a5f4a81a925`
- Source state: quality-red-team and installation-audit changes are uncommitted staging source
- Migration tool: `staging/migration/v2_migrate.py`
- Baseline: verified local active-state snapshot; excluded from source control because it inventories machine runtime state
- Backup: verified timestamped local backup; excluded from source control
- Journal: 56/56 actions `COMMITTED`; 12/12 created directories `COMMITTED`
- Pre-existing declared targets were present and hash verified in the excluded backup

## Installed target verification

The 37-file staged candidate map and active installed map both aggregate to SHA-256 `8b8efecedf272eefb1d82068699d8e81e8615602758963449fdd8468aea35a69`. Every active target individually matched its staged source.

| Active target | SHA-256 |
|---|---|
| `~/.codex/AGENTS.md` | `710e953358ebf78ea586cd5cffcdaae679c059e95b7a9bfbdab919fe38950c0c` |
| `~/.codex/routing/MODEL_ROUTING.md` | `1908ca0f1231335f25cdb4776fe4f9343944b11307c25b45be477d12b235c768` |
| `~/.codex/agents/researcher.toml` | `ce6710c14ab7c7d68e08107ce581fc6d4892a8dd9ee0240730cfe1c746aaf74f` |
| `~/.codex/agents/quick-implementer.toml` | `ebefec5297161e4433829a53eac80bff9b46a32c83261f2adcd796878df89912` |
| `~/.codex/agents/implementer.toml` | `6567c8406bd8fe0f8f34e9f42fee6461be6d5e2d74c82f2f87ae721ec7d1a8f8` |
| `~/.codex/agents/validator.toml` | `7eeb0439caf7431033dfb4a3942208a609c1890f431aa732ebc3248838d54d18` |
| `~/.codex/agents/planner.toml` | `4f44a3310a47286a0524147fe25f72d47e914d78fd908b55b32475b2bd358c3a` |
| `~/.codex/agents/reviewer.toml` | `ff25a7dab4a5f48a86b2da1ab96a30182c6110e4c896f72a89c96020065923b1` |
| `~/.codex/toolbox/_system/toolbox.py` | `a31afd3f6571e2e476840261c13c355f1d6123c72f6f8b49a7c54fa2410b5bac` |
| `~/.agents/skills/project-bootstrap/SKILL.md` | `0c4a499f9806ce2e1786f9114b89f97718e90a2bc8a712aa28901dd0955588c9` |

## Configuration and roles

`~/.codex/config.toml` remained byte-for-byte unchanged at SHA-256 `08ef53602a2aa129ed2d24876ad1c6946f6a0ab8135a48c4e6dda9e7e4dccfc6`: parent `gpt-5.6-sol`/medium, `workspace-write`, approval `on-request`, memories disabled, existing `node_repl` MCP unchanged, and no `multi_agent_v2` stanza. The empty custom prefix-rule strategy remained unchanged at rules SHA-256 `2d40abcb9800fa39d3abbd30fb99311b0a16d50357d2099a2ab5a5983c60fbcd`.

Installed roles: researcher Luna/medium read-only; quick-implementer Luna/low workspace-write; implementer Luna/medium workspace-write; validator Luna/low workspace-write; planner Sol/medium read-only; reviewer Sol/low read-only. No duplicate legacy role exists.

## Validation and smoke test

- Unified staging validation: PASS (38 tests; evidence/result freshness; 67 quality fixtures; 3 toolbox tests; 4 privacy tests).
- Installed toolbox suite: PASS (3 tests).
- Installed project-privacy suite: PASS (4 tests).
- Disposable repository: temporary local test directory, removed from the source boundary.
- Private `.ai/PROJECT.md` and project tool were hidden through repository-local `info/exclude`; tracked `AGENTS.md` stayed authoritative.
- Toolbox list/search/validate discovered the manifest without executing `tool.py`.
- Installed policy routes migration/security/durable work predictively to premium reasoning and trivial work directly.
- Validator prompt retained invalid/all-skipped `BLOCKED` and exit-zero tracked-source-mutation `FAIL` behavior.
- Independent installed reviewer: `APPROVE`; no BLOCKER, MAJOR, or MINOR findings.

## Preservation and rollback

All 25 unrelated personal skills retained their preflight per-skill hashes. No real project path or real-project Git exclusion was targeted. Rollback is ready through `v2_migrate.py rollback` with the excluded local backup; it was not run because installation and review passed. The separate parent-model migration was not executed and remains blocked by the quality decision.
