# Proportional private operating workflows

## Safe edit and resume

Read → understand → find dependencies → assess impact → check authority → edit → inspect diff → validate. On resume, reconcile private run state with branch, status, diff, relevant commits/files, and current failures; mark/report stale claims.

## Private SDD

- `TRIVIAL`: direct change and focused validation.
- `SMALL`: implementation/tests; brief plan only when useful.
- `MEDIUM`: lightweight private specification when durable reasoning helps.
- `LARGE/RISKY`: proportional requirements, decisions, specification, design, and plan with human gates where authority is needed.

Do not force `tasks.md` or every document. Requirements state needed outcomes; decisions retain provenance; specifications are testable; design explains consequential choices; plans define reviewable execution and validation. Team-facing needs require a promotion proposal into the existing shared convention.

## State, audit, and handoff

Use `run_state.md` only for a genuinely useful resumable checkpoint, `handoff.md` only for a real transfer, `audit/` for evidence-backed gaps, and `progress/` for conclusions not clear from Git/issues. Private artifacts remain non-authoritative against tracked truth.
