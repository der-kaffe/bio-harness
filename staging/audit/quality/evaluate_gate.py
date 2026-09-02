#!/usr/bin/env python3
"""Evaluate classified results; outcome classification remains an evidence task."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import re

import validate_quality

ROLE_ASSIGNMENTS = {
    "researcher": ("gpt-5.6-luna", "low"),
    "quick-implementer": ("gpt-5.6-luna", "low"),
    "implementer": ("gpt-5.6-luna", "medium"),
    "validator": ("gpt-5.6-luna", "low"),
    "planner": ("gpt-5.6-sol", "medium"),
    "reviewer": ("gpt-5.6-sol", "low"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_output_digest(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(r'^model = "gpt-5\.6-sol"$', re.MULTILINE)
    effort = re.compile(r'^model_reasoning_effort = "medium"$', re.MULTILINE)
    if len(pattern.findall(content)) != 1 or len(effort.findall(content)) != 1:
        raise ValueError("control config is not an exact Sol/medium source")
    return hashlib.sha256(pattern.sub('model = "gpt-5.6-luna"', content).encode()).hexdigest()


def evaluate(data: dict[str, object], fixtures: dict[str, dict[str, object]]) -> dict[str, object]:
    validate_quality.validate_results(data, fixtures)
    runs = data["runs"]
    orchestrator_ids = {fixture for fixture, contract in fixtures.items() if contract["role"] == "orchestrator"}
    controls = {run["fixture"]: run for run in runs if run["role"] == "orchestrator" and run["model"] == "gpt-5.6-sol" and run["effort"] == "medium"}
    candidates = {run["fixture"]: run for run in runs if run["role"] == "orchestrator" and run["model"] == "gpt-5.6-luna" and run["effort"] == "medium"}
    missing = sorted(orchestrator_ids - controls.keys()) + sorted(orchestrator_ids - candidates.keys())
    blockers: list[str] = []
    if missing:
        blockers.append("missing control/candidate results")
    invalid_controls = sorted(key for key, run in controls.items() if run["result"] not in {"PASS", "PASS_WITH_MINOR_DIFFERENCE"})
    if invalid_controls:
        blockers.append("control outcome is not passing")
    class_messages = {
        "SAFETY_REGRESSION": "safety regression",
        "ROUTING_REGRESSION": "routing regression",
        "QUALITY_REGRESSION": "material quality regression",
        "INCONCLUSIVE": "inconclusive candidate result",
    }
    for result_class, message in class_messages.items():
        if any(run["result"] == result_class for run in candidates.values()):
            blockers.append(message)
    role_gates: dict[str, object] = {}
    for role, assignment in ROLE_ASSIGNMENTS.items():
        role_fixtures = {fixture for fixture, contract in fixtures.items() if contract["role"] == role}
        role_runs = {run["fixture"]: run for run in runs if run["role"] == role and (run["model"], run["effort"]) == assignment}
        missing_role = sorted(role_fixtures - role_runs.keys())
        regressions = sorted(run["fixture"] for run in role_runs.values() if run["result"] not in {"PASS", "PASS_WITH_MINOR_DIFFERENCE"})
        role_gates[role] = {
            "assignment": f"{assignment[0]}/{assignment[1]}",
            "status": "PASS" if not missing_role and not regressions else "NOT_READY",
            "missing": missing_role,
            "regressions": regressions,
        }
    return {
        "parent_candidate": "gpt-5.6-luna/medium",
        "control": "gpt-5.6-sol/medium",
        "decision": "ELIGIBLE_FOR_HUMAN_APPROVAL" if not blockers else "BLOCKED",
        "blockers": blockers,
        "missing_result_entries": missing,
        "invalid_control_entries": invalid_controls,
        "role_gates": role_gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("fixtures.json"))
    parser.add_argument("--candidate-config", type=Path)
    parser.add_argument("--control-config", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        fixture_data = validate_quality.load(args.fixtures)
        fixtures = validate_quality.validate_fixtures(fixture_data)
        result = evaluate(validate_quality.load(args.results), fixtures)
        if args.receipt:
            if result["decision"] != "ELIGIBLE_FOR_HUMAN_APPROVAL":
                raise ValueError("a gate receipt is emitted only for an eligible comparison")
            if not args.candidate_config or not args.candidate_config.is_file() or not args.control_config or not args.control_config.is_file():
                raise ValueError("receipt requires --control-config and --candidate-config")
            if args.receipt.exists():
                raise ValueError("receipt path already exists")
            receipt = {
                "version": 1,
                "decision": result["decision"],
                "control": result["control"],
                "parent_candidate": result["parent_candidate"],
                "fixtures_sha256": digest(args.fixtures),
                "fixtures_path": str(args.fixtures.resolve()),
                "results_sha256": digest(args.results),
                "results_path": str(args.results.resolve()),
                "evaluator_sha256": digest(Path(__file__)),
                "evaluator_path": str(Path(__file__).resolve()),
                "validator_sha256": digest(Path(validate_quality.__file__)),
                "validator_path": str(Path(validate_quality.__file__).resolve()),
                "control_config_sha256": digest(args.control_config),
                "control_config_path": str(args.control_config.resolve()),
                "candidate_output_sha256": candidate_output_digest(args.control_config),
                "candidate_config_sha256": digest(args.candidate_config),
            }
            args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["decision"] == "ELIGIBLE_FOR_HUMAN_APPROVAL" else 2


if __name__ == "__main__":
    sys.exit(main())
