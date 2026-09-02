# Private workspace, authority, and adoption

## Authority

Current explicit human instruction and applicable tracked project/team contracts outrank private `.ai` plans and state. Accepted task-specific private material guides work only where it does not conflict. Implementation evidence proves current reality, not the desired contract. Surface contradictions.

Private findings become shared only through a promotion proposal explaining the team need, identifying the repository's existing tracked destination, and requesting approval when the project/team contract changes.

## Git-local privacy

Run the packaged helper from the skill directory:

```text
python3 scripts/project_privacy.py inspect --path <project>
python3 scripts/project_privacy.py apply --path <project>
```

`apply` is a project write and requires task authority. The helper resolves `git rev-parse --show-toplevel` and `git rev-parse --git-path info/exclude`, rejects tracked `.ai`, `.codex`, or `.agents` conflicts, preserves existing exclude content, and appends only missing anchored patterns. It never edits `.gitignore`, global Git configuration, the index, or history. For non-Git work it reports `NON_GIT` and never initializes a repository.

## Existing layouts

Build a path-by-path adoption map for root `AGENTS.md`, `ai/`, `specs/`, run state, mistakes, `.agents/`, `.codex/`, and `.ai/`. Never infer privacy from a name. Inspect tracking, references, ownership, and authority; require explicit approval before moves or removals.
