# Private workspace activation

Classify existing and proposed paths as `REUSE`, `ADAPT`, `MIGRATION_PROPOSED`, `CONFLICT`, or `SKIP`. Moving or removing an older layout requires explicit approval.

| Artifact | Activate only when |
|---|---|
| `.ai/PROJECT.md` | Private routing materially helps; keep it a small map. |
| `.ai/run_state.md` | Work spans sessions and Git/issues do not provide a sufficient checkpoint. |
| `.ai/handoff.md` | A real transfer is occurring. |
| `.ai/mistakes.md` | A substantially equivalent agent/process failure recurs. |
| `.ai/audit/` | A bounded audit compares expected and current evidence. |
| `.ai/progress/` | Significant conclusions are not already clear from Git/issues. |
| `.ai/specs/<feature>/` | Ambiguity, risk, or durability warrants private SDD. |
| `.ai/state/` | Structured private operational state has a defined owner and lifecycle. |
| `.ai/tools/<name>/` | Reusable deterministic mechanical work passes the extraction heuristic. |

Default to `SKIP`. Existing root `ai/`, `specs/`, `.agents/`, `.codex/`, or `AGENTS.md` may be shared, private, or legacy; inspect tracking and authority before classifying them.
