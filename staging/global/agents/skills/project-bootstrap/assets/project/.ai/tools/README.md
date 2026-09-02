# Project-private tools

Search manifests before generating non-trivial deterministic helper code. A tool owns stable mechanical work; it does not replace architecture, requirements interpretation, or other material judgment. Match semantic contracts, not names alone.

Use one package per tool with a tiny `tool.toml`, package-local implementation, and test. Discovery reads manifests only and never executes code. Project tools stay under `.ai/tools/`; global promotion requires explicit human approval.
