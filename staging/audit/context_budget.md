# Harness V2 context budget

Measured on 2026-09-02 using whitespace-delimited words and UTF-8 bytes. These are not tokenizer counts.

| Artifact | Loading class | Words | Bytes |
|---|---|---:|---:|
| Global `AGENTS.md` | ALWAYS-LOADED | 294 | 2,310 |
| `routing/MODEL_ROUTING.md` | ON-DEMAND | 549 | 4,316 |
| Private `.ai/PROJECT.md` template | ALWAYS-LOADED only in activated project | 129 | 968 |
| Example `tool.toml` | ON-DEMAND manifest | 26 | 188 |
| project-bootstrap `SKILL.md` | ROLE-LOADED | 323 | 2,671 |
| bootstrap workflow reference | ON-DEMAND | 235 | 1,843 |
| private workspace reference | ON-DEMAND | 194 | 1,517 |
| tooling reference | ON-DEMAND | 170 | 1,359 |
| operating workflows reference | ON-DEMAND | 167 | 1,274 |
| model-routing reference | ON-DEMAND | 132 | 1,040 |
| toolbox implementation | DEBUG-ONLY/source execution | 803 | 8,838 |

Agent instruction payloads load only with their roles:

| Role | Loading class | Instruction words | Instruction bytes |
|---|---|---:|---:|
| researcher | ROLE-LOADED | 98 | 754 |
| quick-implementer | ROLE-LOADED | 107 | 769 |
| implementer | ROLE-LOADED | 126 | 925 |
| validator | ROLE-LOADED | 173 | 1,301 |
| planner | ROLE-LOADED | 108 | 872 |
| reviewer | ROLE-LOADED | 109 | 878 |

The global ceiling is met without importing the routing matrix. Task-critical requirements, constraints, contracts, authority, ownership, and prior evidence are exempt from context minimization: omitting them is a quality regression.
