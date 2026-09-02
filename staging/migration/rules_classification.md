# Classification of the 38 existing global rules

Source inspected read-only: `~/.codex/rules/default.rules`. Categories describe the strongest relevant concern: `GLOBAL_SAFE`, `PROJECT_SPECIFIC`, `RISKY`, `OBSOLETE`, `AUDIT_SIDE_EFFECT`, or `UNCERTAIN`.

“Keep global” asks whether the existing automatic `allow` belongs in the future global ruleset. A safe command can still be `NO` when it works inside the normal sandbox and needs no elevation.

| ID | PATTERN | CLASS | PROBABLE PURPOSE | SCOPE | RISK | RECOMMENDATION | KEEP GLOBAL |
|---|---|---|---|---|---|---|---|
| R01 | `terraform providers schema -json` | GLOBAL_SAFE | Inspect provider schema | Terraform repos | Executes provider tooling; no infrastructure mutation expected | Use under normal sandbox; no global escalation needed | NO |
| R02 | `terraform init -upgrade -backend=false` | RISKY | Refresh providers without backend | Terraform repos | Network access and dependency/lockfile changes | Run only with repo context and diff review | NO |
| R03 | `terraform fmt -check` | GLOBAL_SAFE | Check formatting | Terraform repos | Low; still stack-specific | Use normally; no escalation rule | NO |
| R04 | `rm -rf /tmp/devstacklibvirt09-schema` | RISKY | Delete a temporary DevStack schema cache | One historical DevStack workflow | Destructive and tied to a stale path | Remove from future global layer; approve target-specific cleanup when needed | NO |
| R05 | `terraform validate` | GLOBAL_SAFE | Validate Terraform configuration | Terraform repos | Provider execution; low direct mutation | Use normally; no escalation rule | NO |
| R06 | `sed -n 1,120p ~/.agents/skills/terraform-skill/SKILL.md` | OBSOLETE | Read installed skill instructions | Local personal skill | Read-only and no elevation needed | Drop | NO |
| R07 | `zsh -lc <libvirt pools + devstack.xml + terraform state inspection>` | PROJECT_SPECIFIC | Inspect DevStack/libvirt/Terraform state | `devstack-main` | Compound wrapper, absolute project path, state exposure | Recreate project-locally only if still needed; prefer individual commands | NO |
| R08 | `zsh -lc <virsh list + devstack domain/interfaces>` | PROJECT_SPECIFIC | Inspect DevStack VM | DevStack/libvirt | Compound exact script; global coupling | Keep out of global rules | NO |
| R09 | `sed -n 1,180p ~/.agents/skills/terraform-skill/SKILL.md` | OBSOLETE | Read installed skill instructions | Local personal skill | Read-only and redundant with skill loading | Drop | NO |
| R10 | `virsh net-define` | RISKY | Define libvirt networks | Any libvirt host | Broad state-changing prefix accepts arbitrary XML path | Require explicit target and human approval | NO |
| R11 | `virsh net-start privada` | RISKY | Start named libvirt network | Historical libvirt project | Host state change | Project-local prompt/approval if needed | NO |
| R12 | `id` | GLOBAL_SAFE | Inspect current identity | General | Harmless, no elevation needed | Drop redundant allow | NO |
| R13 | `zsh -lc <terraform skill + cloudinit volume/state/provider inspection>` | PROJECT_SPECIFIC | Diagnose cloud-init volume lifecycle | DevStack Terraform | Compound project-specific state access | Replace with scoped project workflow if project returns | NO |
| R14 | `terraform plan -out=cloudinit-fix.tfplan` | PROJECT_SPECIFIC | Create a specific plan artifact | DevStack Terraform | Writes project artifact; name is project-specific | Keep project-local | NO |
| R15 | `virsh net-list --all` | PROJECT_SPECIFIC | Inspect libvirt networks | Libvirt work | Read-only but not universal; no global escalation needed | Use normally when relevant | NO |
| R16 | `zsh -lc <devstack VM + cloud-init ISO + templates + ISO tools>` | PROJECT_SPECIFIC | Diagnose VM/cloud-init configuration | DevStack | Large compound script and project files | Replace with documented project diagnostic workflow | NO |
| R17 | `zsh -lc 'terraform state show libvirt_domain.devstack_vm …'` | PROJECT_SPECIFIC | Inspect one Terraform resource | DevStack Terraform | State may expose sensitive values; exact project resource | Project-local only | NO |
| R18 | `isoinfo -i /kvm/pools/homelab/devstack-cloudinit.iso -R -f` | PROJECT_SPECIFIC | Inspect DevStack ISO | Local homelab | Absolute host path | Use without global allow when needed | NO |
| R19 | `virsh vol-download --pool pool devstack-cloudinit.iso /tmp/devstack-cloudinit.iso` | PROJECT_SPECIFIC | Copy a libvirt volume for inspection | DevStack/libvirt | Host access and local artifact write | Require project-specific scope | NO |
| R20 | `zsh -lc <virsh/ip inspection for virbr2, virbr3, 192.168.100.5>` | PROJECT_SPECIFIC | Diagnose DevStack networking | Homelab DevStack | IP/interface-specific compound command | Keep out of global rules | NO |
| R21 | `terraform plan -out=cloudinit-network-fix.tfplan` | PROJECT_SPECIFIC | Create network-fix plan | DevStack Terraform | Writes project artifact | Keep project-local | NO |
| R22 | `git ls-remote https://opendev.org/openstack/devstack refs/heads/stable/2025.2` | PROJECT_SPECIFIC | Verify a DevStack branch | DevStack | Network access; fixed external ref may age | Execute on demand; no permanent allow | NO |
| R23 | `zsh -lc <qemu:///system URI/list/net-list/domifaddr devstack>` | PROJECT_SPECIFIC | Diagnose system libvirt and VM address | DevStack | Host-specific compound access | Keep out of global rules | NO |
| R24 | `ssh -o BatchMode=yes -o ConnectTimeout=8 ubuntu@192.168.100.5` | RISKY | Access DevStack VM | One host/IP | Prefix permits arbitrary trailing remote command | Never retain as global allow; require command-specific approval | NO |
| R25 | `zsh -lc <file/secret scan + terraform state + ansible syntax check>` | PROJECT_SPECIFIC | Audit DevStack repository | `devstackOptimize` | Large compound workflow; state/secrets inspection | Convert to project documentation or a scoped script with tests | NO |
| R26 | `rm -rf <four DevStack tfplans + cached libvirt provider>` | RISKY | Cleanup generated plans/provider cache | `devstackOptimize` | Destructive multi-target deletion including provider binary | Human-gated cleanup only after preview | NO |
| R27 | `printf '%s\n' '--- Terraform ---'` | OBSOLETE | Print a heading | General | No elevation required | Drop | NO |
| R28 | `zsh -lc <virsh devstack interfaces + ip routes + networks>` | PROJECT_SPECIFIC | Diagnose DevStack networking | DevStack | Host/IP-specific compound command | Keep out of global rules | NO |
| R29 | `virsh -c qemu:///system start devstack` | RISKY | Start VM | DevStack | Host state change and resource use | Require target-specific approval | NO |
| R30 | `zsh -lc <devstack state/interfaces + virbr2/netstack + addresses>` | PROJECT_SPECIFIC | Diagnose VM/network state | DevStack | Host-specific compound access | Keep project-local | NO |
| R31 | `zsh -lc <SSH Horizon compress + service restart>` | RISKY | Rebuild Horizon assets and restart service | DevStack VM | Remote sudo and service mutation; compound SSH | Require explicit preview/approval and post-change validation | NO |
| R32 | `cd /home/juanc/Documentos/devstackOptimize/ansible` | OBSOLETE | Change to historical project directory | One project | No standalone permission value; absolute stale coupling | Drop | NO |
| R33 | `ansible-playbook -i inventory.yml site.yml` | RISKY | Apply Ansible site playbook | Inventory-dependent | May mutate multiple hosts; target not visible in prefix | Never global-allow; require inventory/play review and approval | NO |
| R34 | `printf '%s\n' '--- NAT iptables ---'` | OBSOLETE | Print a heading | General | No elevation needed | Drop | NO |
| R35 | `ssh -F /dev/null … StrictHostKeyChecking=accept-new ubuntu@192.168.100.5` | RISKY | Access VM with isolated SSH config | One host/IP | Arbitrary trailing remote command; accepts new host key | Do not retain; use verified host identity and command-specific approval | NO |
| R36 | `zsh -lc <devstack domain/network/route/virbr2 inspection>` | PROJECT_SPECIFIC | Diagnose DevStack connectivity | DevStack | Compound host-specific command | Keep out of global rules | NO |
| R37 | `zsh -lc <Neovim obsolete-reference scan + headless config inspection + tmp cleanup>` | RISKY | Validate personal Neovim configuration | `~/.config/nvim` | Large compound command, embedded Lua, temporary deletion, unrelated globally | Replace with a project-local validation script if still useful | NO |
| R38 | `node ~/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs` | AUDIT_SIDE_EFFECT | Fetch official manual during prior audit | One audit workflow | Network/cache action was persisted unintentionally | Remove during authorized migration; use one-off approval when needed | NO |

## Summary

- `GLOBAL_SAFE`: 4 (`R01`, `R03`, `R05`, `R12`).
- `PROJECT_SPECIFIC`: 17.
- `RISKY`: 11.
- `OBSOLETE`: 5.
- `AUDIT_SIDE_EFFECT`: 1.
- `UNCERTAIN`: 0 after inspection; probable purposes are sufficiently evidenced by command shapes and paths.

No existing automatic `allow` is carried into the candidate. Adversarial testing removed the six proposed `prompt`/`forbidden` rules: execpolicy controls requests outside the sandbox, while the prefix set was bypassable by absolute executables, global options, and wrapper forms and duplicated some sandbox approvals. The hardened candidate contains zero custom global rules.

## Post-baseline rule 39

After the 38-rule classification was completed, cleanup of validation-generated files inside staging unexpectedly caused the permission layer to persist this exact prefix:

```text
rm -rf <explicit list of staging/global/codex generated state paths>
```

Classification: `AUDIT_SIDE_EFFECT`. Purpose: remove only system skills/state databases created by isolated CODEX_HOME validation. Scope: this staging workspace. Risk: destructive but target-specific; more importantly, it was persisted without being requested as a lasting preference. Recommendation: remove during an authorized migration or separately authorized cleanup. Keep global: **NO**.

Migration must identify and hash rule 39, preserve it in the timestamped backup, exclude it from the zero-rule candidate, and remove it only when the human explicitly authorizes replacement of the whole real rules file.
