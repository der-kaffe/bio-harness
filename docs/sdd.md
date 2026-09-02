# Proportional specification-driven development

Specification-driven development (SDD) makes durable reasoning explicit when that improves correctness. It is proportional, not a mandatory document pipeline.

```text
Need → Specification → Design → Plan → Implementation → Validation
```

Any stage may be compressed or omitted when the task does not benefit from it.

| Task class | Typical treatment |
|---|---|
| Trivial | Direct work and an obvious check |
| Small | Implementation and focused tests; brief plan only if useful |
| Medium | Lightweight durable specification for important rules or interfaces |
| Large/risky | Selected requirements, decision, specification, design, and plan artifacts warranted by risk |

There is no mandatory `tasks.md`, and large work does not automatically require every possible file. Durable-data, security, migration, concurrency, public-contract, and consequential architecture work generally needs stronger planning and human decisions than file count alone suggests.

Personal SDD defaults to `.ai/specs/<feature>/`. A small feature might use one `spec.md`; larger work may separate requirements, decision, specification, design, and plan. These private artifacts guide the agent but do not become team requirements automatically.

If a decision or requirement becomes genuinely team-facing, propose promotion into the repository's existing shared documentation convention. Explain why collaborators need it and obtain approval when it changes a project or team contract.
