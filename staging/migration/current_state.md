# Current active and staged state

The authoritative V2 preflight is `../audit/v2_preflight_baseline.md`. Active Codex 0.152.0 uses `gpt-5.6-sol` with medium reasoning, workspace-write, on-request approvals, memories disabled, stable multi-agent enabled, and no global toolbox. The active harness remains unchanged during staging.

The unified staged candidate adds private `.ai` project routing, a manifest-driven toolbox, six explicitly pinned roles, an on-demand quality-first routing policy, deterministic infrastructure tests, and a later quality benchmark framework. The installable staged `config.toml` preserves Sol/medium. `config.luna-candidate.toml` is inert and cannot become active through the general V2 migration.

Prior audit and simulation documents remain historical evidence for V1 and must not override this current V2 baseline.
