# Reusable deterministic toolbox

A **skill** teaches how to work or reason. A **tool** performs a deterministic mechanical responsibility. Architecture choices, ambiguous interpretation, and domain decisions remain reasoning; inventory, hashing, manifest comparison, validation, and stable transformations may become tools.

## Scopes and package

Project-private tools live under `.ai/tools/<name>/`. Cross-project tools live under `~/.codex/toolbox/<name>/` and require explicit promotion approval.

```text
tool/
├── tool.toml
├── tool.py
└── test_tool.py
```

Python's standard library is the generic default, but a project's existing language may be a better fit. The small manifest declares only discovery-relevant metadata such as name, description, tags, entrypoint, test, determinism, and mutation.

## Discovery and extraction

```text
semantically matching validated tool → reuse
trivial one-off mechanical work       → direct
stable repeated deterministic helper  → consider project extraction
reasoning-heavy responsibility        → keep as reasoning
```

Project manifests are searched before global manifests. Project precedence applies only when semantic responsibility matches; filename or tag similarity is insufficient. Source is read only when modifying, debugging, reviewing, or resolving an insufficient interface.

Extraction considers determinism, recurrence, stable semantics, validation cost, safety, and token benefit. It is not a rigid line-count rule. A second substantially equivalent helper is strong evidence for extraction; repetition never turns judgment into a deterministic tool.

## Security

Discovery parses manifests and never executes entrypoints or tests. Validation rejects unsafe names, absolute or traversing paths, malformed TOML, package/path symlink escapes, and invalid boolean fields. Tests run only when explicitly requested. Mutating tools must declare their surface and have task authority.

A project must never write to the global toolbox silently. Global promotion requires human approval, repeated cross-project evidence, generic stable semantics, tests, dependency review, and collision handling. Mutating global tools require explicit approval.

The system utility supports compact `list`, `search`, `validate`, and safe project-local `scaffold` operations. Its source is [`staging/global/codex/toolbox/_system/toolbox.py`](../staging/global/codex/toolbox/_system/toolbox.py).
