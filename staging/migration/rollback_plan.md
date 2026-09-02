# Harness V2 rollback

Rollback restores exact recorded pre-install bytes, not reconstructed content.

For general V2 installation:

1. Stop and retain failure evidence and the durable state journal.
2. Validate the manifest version, recorded target universe, and exact Codex/agents roots.
3. For each prepared or completed action in reverse order, reconcile the current target with its before/installed hashes.
4. Restore existing files from verified backups and original modes.
5. Remove newly created files only when they still match the candidate hash, then remove installation-created directories only if empty.
6. Restore stale project-bootstrap files only when their recorded target remains absent.
7. Preserve and report any later human edit instead of overwriting it.
8. Verify global AGENTS, routing, agents, toolbox, project-bootstrap, unrelated-skill aggregate hash, and unchanged config.

Rollback never changes a project, Git exclude, `.gitignore`, global Git configuration, auth, memory, or unrelated skill.

The optional Luna-parent migration has its own quality-gate receipt, durable migration journal, and backup. A human approves the exact gate-receipt hash. Apply revalidates its evaluator, fixtures, results, and candidate-config hashes before recording `PREPARED`; rollback handles prepared and committed states and refuses unrelated drift. Failure or rollback of this optional step does not remove Harness V2 workers, tools, routing, or project-bootstrap.
