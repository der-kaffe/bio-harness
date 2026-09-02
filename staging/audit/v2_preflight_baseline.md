# Harness V2 preflight baseline

Observed read-only on 2026-09-02 before staging edits.

## Active Codex

- Version: `codex-cli 0.152.0`
- Model: `gpt-5.6-sol`
- Reasoning effort: `medium`
- Parent sandbox: `workspace-write`
- Approval policy: `on-request`
- Memories: disabled
- `multi_agent`: stable, enabled
- `multi_agent_v2`: stable, disabled
- Global toolbox: absent

| Active target | SHA-256 | Words/bytes where relevant |
|---|---|---|
| `~/.codex/config.toml` | `08ef53602a2aa129ed2d24876ad1c6946f6a0ab8135a48c4e6dda9e7e4dccfc6` | — |
| `~/.codex/AGENTS.md` | `215ddee6248fd889f83deb365ae0dfc954a4fc7809cf116e5361745f1204a4d7` | 236 / 1,773 |
| `~/.codex/agents/planner.toml` | `f032d88b21f245a27c6a89f0d7e08af57af18ac5460db6106fd970f522005da0` | — |
| `~/.codex/agents/researcher.toml` | `fbefc432468108094493fcab1c75179932695045b4a83c72f819c483f8b62fb8` | — |
| `~/.codex/agents/reviewer.toml` | `399719f037a52abc9842399d5bbeb56a88a638469e45e7fe01a89093fb40326b` | — |

Active project-bootstrap aggregate tree hash: `2a37755d145cb40144c0786dd4e1432d33cb0aac14d5bcbd9bf8af62b4be773b`.

Active personal-skill aggregate tree hash: `33583dc46e877b9c073f212fe3588fbb31638e467f8954832c7c18d199d205b6`.

Active skill inventory (26): ansible-role, argocd-gitops, dns-management, docker-compose, docker-management, find-skills, firewall-config, git-workflow, github-actions, hashicorp-vault, helm-charts, kubernetes-ops, kustomize, linux-administration, linux-hardening, load-balancing, mysql, opentelemetry, project-bootstrap, prometheus-grafana, reverse-proxy, service-mesh, ssh-configuration, ssl-tls-management, systemd-services, terraform-skill.

Repository HEAD was `8c61bb28e8d1d00cd7f2fbf932711f0c2e39d30a`; working tree was clean. The staged V1 candidate still used root `AGENTS.md`, `ai/`, root `specs/`, inherited agent models, no toolbox, no on-demand model-routing policy, and Sol/high in the staged config. Active-state reality matched the approved Sol/medium control, so implementation proceeded.
