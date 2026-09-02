# Private tool policy

## Discovery and extraction

Search `.ai/tools/*/tool.toml`, then `~/.codex/toolbox/*/tool.toml`, reading manifests rather than source. Match semantic responsibility, input/output behavior, determinism, and mutation—not filename alone. Project semantics take precedence for the same exact responsibility.

Reuse a suitable validated tool. Keep trivial one-off mechanical work direct. Consider project-local extraction when deterministic logic is non-trivial, stable, plausibly reusable, or substantially equivalent logic is needed again. Reasoning-heavy interpretation and decisions remain model/human work. Use judgment based on determinism, repeatability, stability, semantic reuse, validation cost, safety, and token benefit; line count is not a law.

## Package and execution

A package contains a tiny `tool.toml`, package-local implementation, and normally a test. Discovery never executes code. Validate before executing non-trivial or mutating tools. Default output is compact; verbose logs, trees, contents, and diffs are opt-in or failure-driven.

Project tools remain under `.ai/tools/`. Never write or promote into the global toolbox from a project without human approval, cross-project evidence, generic stable semantics, tests, dependency review, and collision handling. Mutating global tools require explicit approval.
