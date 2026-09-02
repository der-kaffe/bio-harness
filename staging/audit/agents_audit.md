# Global agent adversarial audit

| AGENT | VALUE | ISOLATION BENEFIT | OVERLAP / COST | DECISION |
|---|---|---|---|---|
| researcher | Evidence gathering, docs, root cause, architecture alternatives | Native `read-only` sandbox plus a bounded parent-facing report | Overlaps built-in `explorer`; custom role adds explicit external-doc, secret, contradiction, and no-fix boundaries. Only description is discovery context; full instructions load on spawn | KEEP |
| planner | Converts complex ambiguity into verifiable sequencing and exposes decisions | Native `read-only` prevents implementation creep | Root can plan; role earns its cost only for complex work. Hardened to return trivial work and STOP/ASK on authority-changing unknowns | KEEP |
| reviewer | Independent defect/regression/security/spec review | Native `read-only` prevents silent fixes and preserves independence | Overlaps `/review`; useful for delegated independent review. Hardened against category-filling and style noise | KEEP |

No model or reasoning override is set. Each role inherits the parent unless a spawn/global default overrides it, avoiding hidden cost/model drift.

## Scenario results

- Researcher: read-only inspection commands are allowed; fixes remain prohibited. Contradictions and secrets are reported/redacted. External documentation is evidence, not authority. Architecture output is alternatives/tradeoffs, not a decision.
- Planner: ambiguous critical choices trigger STOP/ASK; non-critical assumptions are labeled. Trivial work receives no document factory. Large work includes dependencies, validation, rollback, and human decisions without autoacceptance.
- Reviewer: a correct diff can return no material findings; subtle bugs, security regressions, breaking APIs, scope creep, and missing tests receive evidence and severity. Style-only issues are omitted or SUGGESTION, never blocker by default.

All three remain optional/on-demand. Root handles ordinary work; keeping the files does not require spawning them.
