# Upstream reference provenance

- Repository: `https://github.com/nsEytgXm/subagents_configs`
- Pinned commit: `65b46e2c6dfbcf31eef362c948d7606d0a438957`
- Consulted on: 2026-09-02
- Files: `README.md`, `agents/*.toml`, `rules/SUBAGENT_ROUTING.md`, `templates/AGENTS.md.template`, `install.sh`
- Role: untrusted external reference only; no runtime dependency and no installer execution.

## Adopted

- Bounded specialist ownership.
- Decision-ready exploration.
- Proportional separation of implementation, validation, and high-risk review.
- Explicit non-overlapping ownership for parallel writers.
- Focused validation and evidence-driven repair.

## Adapted

- Six distinct roles use existing `researcher`, `planner`, and `reviewer` rather than duplicate explorer/reviewer names.
- Quality, safety, and reliability precede cost and token optimization.
- Detailed routing is on demand, not imported globally.
- Every role explicitly pins model, effort, and sandbox.
- Validator uses workspace-write only for build/test artifacts, forbids source/config edits, and reports repository-status deltas.

## Rejected or corrected

- Cost-first routing even when delegation increases aggregate tokens.
- README/TOML effort mismatches: upstream explorer, quick implementer, and implementer claim low/low/medium but configure high/high/high; their progress messages repeat the claims rather than effective values.
- Implicit sandbox inheritance for all roles except commit-pusher.
- Reviewer-after-every-edit wording.
- Commit-pusher as a global role.
- Always-loaded 868-word routing import.
- Automatic `[features.multi_agent_v2]` mutation and incomplete uninstall ownership.
- Reviewer dependency on an external/unpackaged `$code-review` skill.
- Mandatory progress-message noise.
- Generic project-independent TODO/comment injection by the implementer.
