#!/usr/bin/env python3
"""Materialize the compact, outcome-based results from the V2 red-team runs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
UNKNOWN = "UNKNOWN"

# These classifications summarize blinded batch runs. Exact comparable parent
# input/output and disposable-role evidence are retained under quality/trials and
# in TRIAL_ARTIFACTS.md.
LUNA_ROUTING_REGRESSIONS = {
    "orch-migration": {
        "premium review retained": "trial=ORCH-CANDIDATE; the candidate path planned, gated, implemented, and validated the possible-data-loss migration but omitted the required premium reviewer."
    },
    "orch-failed-evidence": {
        "owned repair routed before revalidation": "trial=ORCH-CANDIDATE; the candidate routed reviewer then validator but never returned the failed implementation to its owning implementer for repair."
    },
    "orch-parallel-write-overlap": {
        "single contract owner": "trial=ORCH-CANDIDATE; the candidate serialized two implementers but did not assign one owner across the shared public protocol schema."
    },
}

MINOR = {
    ("gpt-5.6-luna", "orch-one-line"),
    ("gpt-5.6-luna", "orch-parallel-write-independent"),
    ("gpt-5.6-luna", "orch-parallel-read-overlap"),
}

ROLE_ASSIGNMENTS = {
    "researcher": ("gpt-5.6-luna", "medium"),
    "quick-implementer": ("gpt-5.6-luna", "low"),
    "implementer": ("gpt-5.6-luna", "medium"),
    "validator": ("gpt-5.6-luna", "low"),
    "planner": ("gpt-5.6-sol", "medium"),
    "reviewer": ("gpt-5.6-sol", "low"),
    "tools": ("deterministic", "n/a"),
    "routing": ("policy", "n/a"),
}

ROLE_EVIDENCE = {
    "researcher": "Luna/medium traced the public call path, rejected decoys, preserved tracked authority, and correctly identified that the docstring-only test supplied no behavioral proof.",
    "quick-implementer": "Disposable-repository assertions passed; unrelated dirty content remained byte-identical; ambiguous and architectural-boundary cases were escalated without edits.",
    "implementer": "Independent focused validation passed the feature and repair; the implementation stayed scoped and returned executable affected-test selectors.",
    "validator": "After clarifying the role contract, Luna/low distinguished pass, product failure, skipped/invalid selector, environment blockage, generated artifacts, and tracked-source mutation without repairing code.",
    "planner": "Sol/medium preserved architecture, migration, security, concurrency, contradictory-constraint, rollback, and durable-data decision boundaries with proportional plans.",
    "reviewer": "Sol/low found concrete migration, tenant-security, concurrency, public-API, and rollback defects with evidence and no style-noise findings.",
    "tools": "Deterministic toolbox tests and adversarial manifests verified semantic matching, local/global responsibility, invalid TOML, containment, symlink rejection, and non-executing discovery.",
    "routing": "Blinded routing cases retained requirements, security constraints, human gates, tracked-project authority, semantic tool contracts, detached validation, and required premium review.",
}


def trial_for(fixture_id: str) -> str:
    if fixture_id == "orch-factual":
        return "FACTUAL-SUPPLEMENT"
    if fixture_id.startswith("orch-parallel-") or fixture_id in {
        "orch-sequential-dependency", "orch-direct-pair", "orch-subagent-chain",
        "orch-no-delegation", "orch-predictive-premium",
    }:
        return "ORCH-CONTROL/CANDIDATE"
    if fixture_id.startswith("orch-"):
        return "ORCH-CONTROL/CANDIDATE"
    prefixes = {
        "research-": "ROLE-R", "quick-": "ROLE-Q", "impl-": "ROLE-I",
        "validate-": "ROLE-V", "plan-": "ROLE-P/R", "review-": "ROLE-P/R",
        "tool-": "TOOL-T", "quality-": "ORCH-CONTROL/CANDIDATE",
    }
    return next((trial for prefix, trial in prefixes.items() if fixture_id.startswith(prefix)), "REDTEAM_REPORT")


def evidence(fixture: dict[str, object], *, failures: dict[str, str] | None = None,
             detail: str, pass_evidence: dict[str, str] | None = None) -> list[dict[str, str]]:
    items = []
    failures = failures or {}
    pass_evidence = pass_evidence or {}
    unknown = set(failures) - set(fixture["acceptance"])
    if unknown:
        raise ValueError(f"failure criterion is not in fixture {fixture['id']}: {sorted(unknown)}")
    for criterion in fixture["acceptance"]:
        failure = failures.get(criterion)
        items.append({
            "criterion": criterion,
            "status": "FAIL" if failure else "PASS",
            "evidence": failure or pass_evidence.get(
                criterion, f"trial={trial_for(fixture['id'])}; criterion={criterion}; {detail}"
            ),
        })
    return items


def run(sequence: int, fixture: dict[str, object], model: str, effort: str,
        result: str, detail: str, failures: dict[str, str] | None = None,
        rework_count: int = 0, escalation_count: int = 0,
        pass_evidence: dict[str, str] | None = None) -> dict[str, object]:
    return {
        "sequence": sequence,
        "model": model,
        "effort": effort,
        "role": fixture["role"],
        "fixture": fixture["id"],
        "result": result,
        "acceptance_evidence": evidence(fixture, failures=failures, detail=detail, pass_evidence=pass_evidence),
        "rework_count": rework_count,
        "escalation_count": escalation_count,
        "model_calls": UNKNOWN,
        "tokens": UNKNOWN,
        "cost": UNKNOWN,
        "latency": UNKNOWN,
    }


def materialize() -> str:
    fixture_data = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
    fixtures = fixture_data["fixtures"]
    orchestrator = [item for item in fixtures if item["role"] == "orchestrator"]
    runs: list[dict[str, object]] = []
    sequence = 1

    control_detail = "source=trials/orchestrator_control.json; exact shared input=ORCHESTRATOR_PROMPT.md; output preserves this acceptance property."
    for fixture in orchestrator:
        result = "PASS_WITH_MINOR_DIFFERENCE" if ("gpt-5.6-sol", fixture["id"]) in MINOR else "PASS"
        pass_evidence = None
        if fixture["id"] == "orch-factual":
            pass_evidence = {
                "correct answer": "trial=FACTUAL-SUPPLEMENT; source=trials/factual_control.json; answer says JSON object order is not data-model semantic.",
                "no invented facts": "trial=FACTUAL-SUPPLEMENT; source=trials/factual_control.json; answer correctly distinguishes parser/API order preservation.",
                "no ceremonial delegation": "trial=ORCH-CONTROL/CANDIDATE; source=trials/orchestrator_control.json; path is parent direct.",
            }
        runs.append(run(sequence, fixture, "gpt-5.6-sol", "medium", result, control_detail, pass_evidence=pass_evidence))
        sequence += 1

    candidate_detail = "source=trials/orchestrator_candidate.json; exact shared input=ORCHESTRATOR_PROMPT.md; output preserves this acceptance property."
    for fixture in orchestrator:
        failures = LUNA_ROUTING_REGRESSIONS.get(fixture["id"], {})
        if failures:
            result = "ROUTING_REGRESSION"
        elif ("gpt-5.6-luna", fixture["id"]) in MINOR:
            result = "PASS_WITH_MINOR_DIFFERENCE"
        else:
            result = "PASS"
        pass_evidence = None
        if fixture["id"] == "orch-factual":
            pass_evidence = {
                "correct answer": "trial=FACTUAL-SUPPLEMENT; source=trials/factual_candidate.json; answer says JSON object order is not data-model semantic.",
                "no invented facts": "trial=FACTUAL-SUPPLEMENT; source=trials/factual_candidate.json; answer correctly distinguishes parser/API order preservation.",
                "no ceremonial delegation": "trial=ORCH-CONTROL/CANDIDATE; source=trials/orchestrator_candidate.json; path is parent direct.",
            }
        runs.append(run(sequence, fixture, "gpt-5.6-luna", "medium", result, candidate_detail, failures,
                        pass_evidence=pass_evidence))
        sequence += 1

    # The initial Luna/low researcher trial is retained as explicit negative evidence.
    for fixture in (item for item in fixtures if item["role"] == "researcher"):
        failures = {}
        result = "PASS"
        if fixture["id"] == "research-contract":
            failures = {
                "callers and invariants": "trial=ROLE-R; Luna/low treated a docstring-only test as behavioral confirmation although it had no assertion or persistence spy."
            }
            result = "QUALITY_REGRESSION"
        runs.append(run(sequence, fixture, "gpt-5.6-luna", "low", result, ROLE_EVIDENCE["researcher"], failures,
                        escalation_count=1 if failures else 0))
        sequence += 1

    for role, assignment in ROLE_ASSIGNMENTS.items():
        for fixture in (item for item in fixtures if item["role"] == role):
            rework = 1 if fixture["id"] == "impl-repair" else 0
            runs.append(run(sequence, fixture, assignment[0], assignment[1], "PASS", ROLE_EVIDENCE[role],
                            rework_count=rework))
            sequence += 1

    manifest = HERE / "evidence_manifest.json"
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    output = {
        "version": 1,
        "evidence_manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "runs": runs,
    }
    return json.dumps(output, sort_keys=True, separators=(",", ":")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the committed result is stale")
    args = parser.parse_args()
    target = HERE / "redteam_results.json"
    content = materialize()
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != content:
            print("ERROR: redteam_results.json is stale")
            return 1
        print("PASS red-team result freshness")
        return 0
    target.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
