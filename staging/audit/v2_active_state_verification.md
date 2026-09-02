# Harness V2 active-state verification

Final read-only verification: 2026-09-02.

| Active target | Preflight SHA-256 | Final SHA-256 | Result |
|---|---|---|---|
| `~/.codex/config.toml` | `08ef53602a2aa129ed2d24876ad1c6946f6a0ab8135a48c4e6dda9e7e4dccfc6` | same | UNCHANGED |
| `~/.codex/AGENTS.md` | `215ddee6248fd889f83deb365ae0dfc954a4fc7809cf116e5361745f1204a4d7` | same | UNCHANGED |
| active planner | `f032d88b21f245a27c6a89f0d7e08af57af18ac5460db6106fd970f522005da0` | same | UNCHANGED |
| active researcher | `fbefc432468108094493fcab1c75179932695045b4a83c72f819c483f8b62fb8` | same | UNCHANGED |
| active reviewer | `399719f037a52abc9842399d5bbeb56a88a638469e45e7fe01a89093fb40326b` | same | UNCHANGED |
| active project-bootstrap aggregate | `2a37755d145cb40144c0786dd4e1432d33cb0aac14d5bcbd9bf8af62b4be773b` | same | UNCHANGED |
| all active personal skills aggregate | `33583dc46e877b9c073f212fe3588fbb31638e467f8954832c7c18d199d205b6` | same | UNCHANGED |

The active global toolbox remains absent. The repository-local `.git/info/exclude` final hash is `6671fe83b7a07c8932ee89164d1f2793b2318058eb8b98dc5c06ee0a5a3b0ec1`; no command opened it for write, and all privacy-helper executions targeted temporary test repositories. `git diff --name-only -- . ':!staging'` returned no path. No active config, active agent, active skill, real project file, Git configuration, or real-project exclude was modified.
