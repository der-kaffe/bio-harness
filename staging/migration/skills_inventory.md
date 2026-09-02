# Semantic inventory of existing personal skills

The 25 existing skills are retained in place and are not copied into staging. “Global value” describes reusable value across future projects, not an instruction to load every skill on every turn.

| SKILL | PURPOSE | SOURCE | GLOBAL VALUE | OVERLAPS | RECOMMENDATION |
|---|---|---|---|---|---|
| terraform-skill | Version-aware Terraform/OpenTofu authoring, review, tests, CI, scans, and state-risk diagnosis | antonbabenko/terraform-skill | High when Terraform is detected | Partial with infrastructure safety and audit; domain-specific | Reuse; do not duplicate Terraform methodology |
| ansible-role | Idempotent Ansible role structure, variables, handlers, templates, tags | bagelhole DevOps skills | High when Ansible roles are requested | Ansible operations only | Reuse |
| argocd-gitops | ArgoCD GitOps deployment and progressive delivery | bagelhole | Conditional | Kubernetes/GitOps overlap with kubernetes-ops | Reuse after stack detection |
| dns-management | DNS zones and records across common providers | bagelhole | Conditional | Networking/security family | Reuse |
| docker-compose | Multi-container local environments and Compose orchestration | bagelhole | High when Compose exists | docker-management | Reuse; route Compose-specific work here |
| docker-management | Dockerfiles, images, containers, networking, volumes, troubleshooting | bagelhole | High when Docker exists | docker-compose | Reuse; keep boundary at image/container lifecycle |
| find-skills | Discover installable skills when capability extension is requested | vercel-labs/skills | High | Skill installer discovery | Reuse; not a project bootstrap workflow |
| firewall-config | iptables, nftables, cloud firewall segmentation/filtering | bagelhole | Conditional/high risk | linux-hardening, security | Reuse with explicit scope and approvals |
| git-workflow | Branching, PR, release, GitFlow/trunk/GitHub Flow | bagelhole | Broad | GitHub Actions and resume workflow | Reuse for workflow design; it does not own resumable state |
| github-actions | GitHub Actions CI/CD, runners, secrets, delivery automation | bagelhole | High for GitHub repositories | git-workflow, deployment skills | Reuse after CI/provider detection |
| hashicorp-vault | Vault secrets engines, auth, policies, PKI | bagelhole | Conditional/high risk | Security and TLS | Reuse; never generalize into generic secret mutation |
| helm-charts | Helm chart creation, values, templates, releases | bagelhole | High for Helm projects | kubernetes-ops, ArgoCD | Reuse |
| kubernetes-ops | Kubernetes workloads, services, scaling, troubleshooting | bagelhole | High for Kubernetes projects | Helm, Kustomize, ArgoCD, service mesh | Reuse; select narrower skill when appropriate |
| kustomize | Bases, overlays, declarative patches | bagelhole | Conditional | kubernetes-ops | Reuse |
| linux-administration | Linux packages, services, and system configuration | bagelhole | Broad on Linux | systemd, SSH, hardening | Reuse; choose specialized skill for risky subdomains |
| linux-hardening | CIS-oriented Linux security controls | bagelhole | Conditional/high risk | Linux admin, SSH, firewall | Reuse only for explicit hardening/compliance work |
| load-balancing | Load balancers, health checks, TLS termination | bagelhole | Conditional | reverse-proxy, TLS | Reuse |
| mysql | MySQL/MariaDB administration, replication, performance | bagelhole | Conditional/high risk | No methodological overlap | Reuse after database detection |
| opentelemetry | Vendor-neutral traces, metrics, and logs | bagelhole | Conditional | prometheus-grafana | Reuse for instrumentation |
| prometheus-grafana | Metrics, PromQL, dashboards, alerting | bagelhole | Conditional | OpenTelemetry | Reuse for metrics/visualization |
| reverse-proxy | nginx/Traefik gateways, TLS, routing | bagelhole | Conditional | load balancing, TLS | Reuse |
| service-mesh | Istio/Linkerd mTLS, traffic, observability | bagelhole | Conditional | Kubernetes, networking | Reuse only when a mesh exists or is approved |
| ssh-configuration | SSH servers/clients, keys, tunnels, config | bagelhole | Broad but security-sensitive | Linux hardening | Reuse with human gate for disruptive auth changes |
| ssl-tls-management | Certificates, Let's Encrypt, PKI, renewal, ciphers | bagelhole | Conditional/high risk | Vault, reverse proxy | Reuse |
| systemd-services | systemd services/timers, dependencies, limits | bagelhole | Broad on Linux | Linux administration | Reuse |

## Methodological gap analysis

- **Project bootstrap:** no existing skill inspects an arbitrary repository and adapts a local agent/governance layer. Gap confirmed; create one candidate.
- **Safe edit:** no dedicated generic skill, but the behavior is short and universal. Keep it as global guidance plus a reusable workflow reference, not a separate skill.
- **Resume work:** `git-workflow` helps with Git strategy but does not reconcile run state with repository reality. Keep as a project-bootstrap workflow, not a separate skill yet.
- **Audit:** several technology skills audit their own domain, but none owns a generic expected/current/evidence/gaps method. Keep as a workflow reference until repeated standalone use proves a skill is valuable.
- **Spec-driven development:** no existing skill covers proportional SDD. Embed it in project-bootstrap and project templates rather than auto-loading a separate global skill.

Result: one new candidate skill, no technology duplication.
