# Execpolicy red team

Official Codex 0.152.0 semantics: rules govern commands requested **outside the sandbox**, match exact `argv` prefixes, apply the most restrictive match (`forbidden` > `prompt` > `allow`), and are experimental. Safe simple shell chains are documented as split at runtime; advanced shell syntax is not split and is evaluated as the wrapper argv. `execpolicy check` did not expose runtime shell splitting in these probes, so wrapper protection cannot be claimed from check output alone.

## Observed candidate-before-hardening results

| FAMILY | MATCHED `prompt`/`forbidden` | NO MATCH |
|---|---|---|
| rm | `rm file`, `rm -f`, `rm -rf dir`, `rm -fr`, long flags, `.`, `..`, `/*`; direct `rm -rf /` was forbidden | `/bin/rm`, `/usr/bin/rm`, `command rm`; `sh -c`/`bash -lc` produced no match in `execpolicy check` |
| git | direct `git reset`, `git clean`, `git push`, force variants | `git -C repo reset/push`, `/usr/bin/git push` |
| Terraform | direct `terraform destroy` | `terraform -chdir=infra destroy`, `apply`, `apply -auto-approve`, `plan -destroy` |

Aliases and option reordering are not semantic matches: the engine sees the argv shape it receives. Absolute program resolution requires explicit host-executable policy support; the candidate defined none. These are not obscure attacks—`git -C` and `terraform -chdir` are normal documented command forms.

## Strategy comparison

| OPTION | SECURITY | USABILITY | FALSE POSITIVES | BYPASS / MAINTENANCE | RESULT |
|---|---|---|---|---|---|
| A: six candidate rules | Partial and easily overstated | Prompts for every direct `rm` and normal push | High | Many normal argv forms missed; experimental format | REJECT |
| B: minimal universal danger rules | Slight protection for named spellings | Lower noise | Lower | Still a partial blacklist; no complete portable root-delete pattern | REJECT for now |
| C: zero custom global rules | Honest reliance on native sandbox/approval boundaries plus explicit semantic convention | Least duplicated prompting | Lowest | Destructive writes inside workspace remain convention-only; project/managed deterministic controls needed for demonstrated risks | SELECT |

Terraform illustrates the category error: `destroy` and `apply` can both be consequential, but safe policy depends on backend, workspace, plan, credentials, targets, and organizational process. A global prefix does not know that context. Network/host boundary approvals and project-specific review/checks are more honest than one incomplete global rule.

The hardened `default.rules` is intentionally rule-free. It is retained as an auditable declaration of strategy; it grants nothing. Rule 39 remains untouched in the real HOME and is removed only by a later explicitly authorized whole-file migration.
