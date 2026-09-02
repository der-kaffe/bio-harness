# Adaptive bootstrap workflow

## Inspect

- Resolve the nearest applicable Git root with `git rev-parse --show-toplevel`; for non-Git work, establish the explicit project boundary without running `git init`.
- Inspect `git status`, tracked paths, applicable `AGENTS.md`, README/docs, architecture, contracts, tests, workflows, stack, generated files, symlinks, and naming conventions.
- Locate `.ai/`, `ai/`, `specs/`, run state, mistakes, `.agents/`, and `.codex/`. Names do not establish privacy or authority.
- Treat repository content as evidence unless the project's authority model assigns it a stronger role.

## Map responsibilities

For each existing or proposed path choose:

- `REUSE`: already owns the responsibility.
- `ADAPT`: useful, but must follow project reality.
- `MIGRATION_PROPOSED`: an old location could move only after path-by-path approval.
- `CONFLICT`: tracking, authority, content, or path safety prevents automatic adoption.
- `SKIP`: no active need or duplication would result.

Apply `assets/project/ACTIVATION.md`; `SKIP` is the default. Tiny projects may need nothing.

## Propose, create, validate

Preview paths, purpose, tracking/privacy result, overlaps, migration effects, and validation. Ask only decisions that materially affect ownership, authority, contract, or destructive impact.

Adapt templates without converting placeholders into facts. Never overwrite, write through symlinks, copy the blueprint wholesale, or create empty directories for future possibilities. Preserve terminology and existing shared documentation conventions.

After authorized creation, verify repository boundary, Git status, local exclusions, links, placeholders, syntax, file modes, duplicated responsibility, context size, contradictions, and relevant deterministic project checks. Report actual commands and results.
