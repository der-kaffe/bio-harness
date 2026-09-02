# ADVERSARIAL AUDIT

Audit date: 2026-09-01. Target: Codex CLI 0.152.0. Scope: `staging/` only. No migration or real global mutation was performed.

## Critical findings

None found after hardening. No test justifies treating convention-only semantic safeguards as technical guarantees.

## High findings

1. **Partial execpolicy blacklist created false assurance.** Normal argv forms bypassed the six candidate prefixes, and rules govern outside-sandbox execution rather than destructive edits generally. **Fixed:** selected zero custom global rules.
2. **Project-bootstrap was not self-contained.** It depended on a staging-relative blueprint path. **Fixed:** packaged byte-identical `assets/project` and removed fallback dependency.
3. **Blueprint activation was underspecified.** A naïve bootstrap could create empty registers/theme/handoff/SDD in every repo. **Fixed:** added an explicit activation matrix with `SKIP` default.
4. **Authority order could turn stale implementation into requirement.** **Fixed:** repository evidence now proves current state and raises drift; it does not silently override approved targets.
5. **Migration/rollback lacked a complete race and ownership protocol.** **Fixed:** added hashes, symlink identity, all-target preflight, journal, atomic staging guidance, collision aborts, and preservation of later human edits; simulated partial and delayed rollback.

## Medium findings

- Human gate was broad enough to prompt for normal requested deletions/renames; narrowed to material impact lacking sufficient current authority.
- Researcher lacked untrusted-content/secret handling; planner lacked proportional STOP/ASK rules; reviewer encouraged potentially noisy category coverage. All hardened.
- Source-of-truth drift, missing evidence, contradictory active facts, decision provenance, stale run state, and ADR/register conflict needed explicit handling. Added.
- Mistake counts lacked lifecycle statuses and normalization rules. Added `MITIGATED`/`RESOLVED`/`ACCEPTED_RISK`; automate prevention, not danger.
- SDD categories were too abstract. Added concrete risk/ambiguity criteria.
- Skill/repository supply-chain and path/symlink threats were underdocumented. Added boundaries and a supply-chain policy.
- Progress, handoff, content register, and theme activation could duplicate existing systems. Made conditional.

## Low findings

- `model_provider="openai"` repeats the built-in default, but deliberately makes ownership explicit and prevents ambiguity when leaving job-forge; retained.
- Three agents overlap root/built-ins, but their native read-only isolation and bounded on-demand context justify retention.
- Blueprint exists in review and packaged copies; parity validation controls the drift cost.

## False assumptions discovered

- Execpolicy is not a universal destructive-command firewall.
- Prefixes do not understand semantic subcommands after global options.
- `execpolicy check` did not demonstrate the documented safe-wrapper runtime splitting; it cannot prove wrapper coverage here.
- Repository reality is evidence, not automatically project authority.
- Template availability is not activation.
- A structural fixture test is not an end-to-end behavioral guarantee.
- `features.memories=false` matches today's default, but explicit pinning can still express a deliberate future policy.

## Changes made in staging

- Hardened config documentation, global AGENTS, all three agents, project-bootstrap, blueprint governance/runtime/SDD templates, migration/rollback plans, memory/hooks docs, README, and validation record.
- Added packaged assets, activation matrix, supply-chain policy, A–J fixtures, deterministic staging validator, isolated migration simulator, enforcement matrix, and detailed audit reports.
- Removed all six custom candidate prefix rules; real rules were untouched.

## Components removed

- Six candidate execpolicy entries: `rm -rf /`, broad `rm`, `git reset`, `git clean`, `git push`, and `terraform destroy`.
- No agent, blueprint responsibility, existing skill, integration, or real file was removed.

## Components simplified

- Global AGENTS: 2,136 bytes/286 words → 1,773 bytes/236 words; command catalog collapsed into material-impact semantics.
- Rules: six incomplete controls → an explicit zero-rule policy.
- Bootstrap: one canonical install path (`assets/project`) and conditional activation.

## Config audit

All six keys are official and strict-parse under 0.152.0. Model slug and `high` effort are in the bundled catalog. No legacy profile, trust path, MCP, job-forge/Geometra, compaction override, full access, or deprecated key remains. `memories=false` stays as a deliberate policy pin. See `config_audit.md`.

## AGENTS audit

The 236-word constitution contains only global authority/scope, preservation, validation/uncertainty, deterministic-check preference, and a narrowly scoped human gate. Semantic rules are explicitly convention-only. See `global_agents_classification.md`.

## Agents audit

Researcher, planner, and reviewer remain. They inherit model/effort, default to native read-only, load only when spawned, and now cover secrets/untrusted evidence, proportional planning, real human decisions, severity, and anti-nitpicking. See `agents_audit.md`.

## Rules red-team results

Direct prefixes worked; `/bin`/`/usr/bin`, `command`, `git -C`, and `terraform -chdir` shapes did not. Most-restrictive precedence worked for direct root deletion. Rules apply outside sandbox and remain experimental. See `rules_red_team.md`.

## Selected global rules strategy

Selected C: zero custom global rules. A was noisy and bypassable; B remained an incomplete portable blacklist. Native workspace isolation/interactive boundary approval stays, while semantic destructive review is honestly convention-only until a concrete deterministic project/managed control exists.

## Project-bootstrap packaging

`assets/project` now contains all 21 blueprint files, including activation policy, and matches the review tree byte-for-byte. Skill validation passes and no external staging path remains.

## Project-bootstrap scenario results

A–J decision fixtures pass structural validation: minimal empty repo, existing AGENTS reuse, existing methodology reuse, dirty-tree preservation, conditional frontend theme, backend theme skip, tiny-script no-op, monorepo scoping, existing SOT reuse, and conflicting untrusted methodology stop/report. See `bootstrap_scenarios.md`.

## Blueprint proportionality

Every artifact now has CREATE/SKIP/MERGE criteria. Empty placeholders are prohibited as output. Theme/content/handoff/progress/registers/specs activate only for a demonstrated owner and recurring question.

## Governance audit

SOT requires stable relevant evidence and handles drift/conflicts; decisions record proposer/acceptor provenance and ADR inconsistency; gaps remain observations; content protection is conditional; run state reconciles with Git reality and becomes STALE on conflict.

## SDD audit

Typo: direct. Bounded bug: brief plan/regression check. Endpoint: lightweight spec/plan. Database migration or major architecture rewrite: full SDD plus impact/authority gates. Documents never authorize destructive work by themselves.

## Mistake-loop audit

Counts normalize one equivalent cause/pattern; unrelated failures do not combine. At count ≥3, evaluate deterministic prevention/detection. Dangerous actions are never automated because of count. CI-backed closure can be `MITIGATED` then `RESOLVED` with evidence.

## Context-budget audit

- Always global: AGENTS 1,773 bytes/236 words.
- Agent discovery: concise descriptions; full files (124/122/132 words) only on spawn.
- Skill discovery: frontmatter; SKILL 341 words only when selected; references 367/311 words on demand; assets are output, not instructions.
- Project AGENTS: 2,422 bytes/334 words only in bootstrapped projects.
- Blueprint README/registers/specs: on demand.

Repeated human-gate text remains only at global and future project boundaries; detailed skill references point back instead of restating it. Packaged asset duplication is disk packaging, not duplicate model context.

## Security audit

Bootstrap now rejects path escape/output symlink following, overwrites, implicit executable-bit changes, arbitrary script execution, secret recording, and automatic trust in repository text or installed skills. These are convention-only because the skill contains no mutation script; every proposed write remains diff/human reviewed. No auth/secret was copied. The migration simulator bounds all paths to staging and uses no shell input.

## Supply-chain observations

The 25 personal skills remain unchanged but are instruction/executable supply-chain surfaces. Relevance, provenance, dependencies, scripts, permissions, and updates require review; existence is not trust or authority. See `migration/supply_chain.md`.

## Enforcement matrix

See `enforcement_matrix.md`. Native enforcement covers sandbox, approval boundaries, feature toggle, and default subagent sandbox. Semantic quality, authority, human gates, and state/register discipline remain convention-only. Project tests/hooks/CI become deterministic only when a concrete invariant exists.

## Migration simulation

An isolated mock reproduced a legacy config symlink, job-forge content, 39 rules (including two audit side effects), personal skills, and collision possibility. Collision and post-backup target drift aborted before mutation. Complete install produced a regular candidate config, three agents, zero rules, and packaged skill.

## Rollback simulation

Rollback succeeded after failure immediately after config and after rules. A delayed rollback preserved a human-edited AGENTS, restored legacy rules by hash, and restored backed-up legacy config as a regular 0600 file when the job-forge target disappeared. See `simulation/run-001/report.json`.

## Validation rerun

| COMMAND | RESULT | STATUS |
|---|---|---|
| `codex --version` | 0.152.0 | PASS |
| strict app-server with isolated config/state | complete config + agents accepted | PASS |
| `codex debug prompt-input` isolated | global AGENTS present | PASS |
| `codex debug models --bundled` | `gpt-5.6-sol`, `high` supported | PASS |
| `validate_staging.py` | config/assets/links/fixtures/rules/credentials | PASS |
| `quick_validate.py project-bootstrap` | valid | PASS |
| `diff -qr` blueprint vs assets | identical | PASS |
| `execpolicy check` empty candidate | parses; no match | PASS |
| adversarial checks on old six rules | normal bypass shapes observed | FAIL old design / FIXED |
| `simulate_migration.py` | install/partial/delayed rollback assertions | PASS |
| real rules read-only count | 39 | PASS unchanged this phase |

## Real global side effects still present

Rule 39 remains in real `~/.codex/rules/default.rules`: the exact staging cleanup allow persisted during the prior phase. It was not removed or changed. Rule 38 (manual fetch) and rule 39 are both excluded from the candidate and backed up/removed only during a later human-authorized whole-rules migration.

## Remaining human decisions

1. Accept or reject the zero-custom-global-rules strategy.
2. Accept or reject installation of each optional global agent (researcher/planner/reviewer).
3. Choose the migration window and backup retention period.
4. Authorize or reject the future migration itself. No authorization is inferred from this audit.

## Migration readiness

The candidate is coherent, self-contained, proportional, strict-parseable, explicit about enforcement gaps, and rollbackable in the tested mock. The remaining decisions are policy acceptance and authorization, not unresolved technical defects. First project bootstrap must still be previewed because behavioral correctness is not deterministically guaranteed.

READY_TO_MIGRATE
