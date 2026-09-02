#!/usr/bin/env python3
"""Validate compact quality fixture/result structure without model calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

RESULTS = {"PASS", "PASS_WITH_MINOR_DIFFERENCE", "QUALITY_REGRESSION", "SAFETY_REGRESSION", "ROUTING_REGRESSION", "INCONCLUSIVE"}
ROLES = {"orchestrator", "researcher", "quick-implementer", "implementer", "validator", "planner", "reviewer", "tools", "routing"}
METRICS = ("rework_count", "escalation_count", "model_calls", "tokens", "cost", "latency")


def load(path: Path) -> object:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate_fixtures(data: object) -> dict[str, dict[str, object]]:
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("fixtures"), list):
        raise ValueError("invalid fixture envelope")
    fixtures: dict[str, dict[str, object]] = {}
    for fixture in data["fixtures"]:
        if not isinstance(fixture, dict) or set(fixture) != {"id", "role", "scenario", "expected_path", "acceptance"}:
            raise ValueError("invalid fixture shape")
        if fixture["id"] in fixtures or fixture["role"] not in ROLES:
            raise ValueError(f"invalid or duplicate fixture: {fixture['id']}")
        if not all(isinstance(fixture[field], str) and fixture[field] for field in ("id", "role", "scenario", "expected_path")):
            raise ValueError("fixture strings must be non-empty")
        if (not isinstance(fixture["acceptance"], list) or not fixture["acceptance"]
                or not all(isinstance(item, str) and item.strip() for item in fixture["acceptance"])
                or len(set(fixture["acceptance"])) != len(fixture["acceptance"])):
            raise ValueError("fixture acceptance must be non-empty")
        fixtures[fixture["id"]] = fixture
    return fixtures


def validate_results(data: object, fixtures: dict[str, dict[str, object]]) -> None:
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("runs"), list):
        raise ValueError("invalid result envelope")
    control_sequence: dict[str, int] = {}
    run_keys: set[tuple[object, ...]] = set()
    sequences: set[int] = set()
    for run in data["runs"]:
        required = {"sequence", "model", "effort", "role", "fixture", "result", "acceptance_evidence", *METRICS}
        if not isinstance(run, dict) or set(run) != required:
            raise ValueError("invalid result shape")
        if run["fixture"] not in fixtures or run["result"] not in RESULTS:
            raise ValueError("unknown fixture or result class")
        if run["role"] != fixtures[run["fixture"]]["role"]:
            raise ValueError("result role does not match fixture role")
        if not isinstance(run["sequence"], int) or run["sequence"] <= 0 or run["sequence"] in sequences:
            raise ValueError("result sequence must be unique and positive")
        sequences.add(run["sequence"])
        run_key = (run["role"], run["model"], run["effort"], run["fixture"])
        if run_key in run_keys:
            raise ValueError("duplicate role/model/effort fixture result")
        run_keys.add(run_key)
        evidence = run["acceptance_evidence"]
        if not isinstance(evidence, list) or not evidence:
            raise ValueError("acceptance evidence is required")
        expected_criteria = fixtures[run["fixture"]]["acceptance"]
        observed: dict[str, str] = {}
        for item in evidence:
            if (not isinstance(item, dict) or set(item) != {"criterion", "status", "evidence"}
                    or item.get("status") not in {"PASS", "FAIL", "UNKNOWN"}
                    or not isinstance(item.get("criterion"), str)
                    or not isinstance(item.get("evidence"), str)
                    or not item["evidence"].strip()
                    or item["evidence"].strip().upper() in {"NOT_RUN", "UNKNOWN", "TBD"}):
                raise ValueError("invalid or placeholder acceptance evidence")
            if item["criterion"] in observed:
                raise ValueError("duplicate acceptance criterion evidence")
            observed[item["criterion"]] = item["status"]
        if set(observed) != set(expected_criteria):
            raise ValueError(f"acceptance evidence does not cover fixture contract: {run['fixture']}")
        if run["result"] in {"PASS", "PASS_WITH_MINOR_DIFFERENCE"} and set(observed.values()) != {"PASS"}:
            raise ValueError("passing result requires every acceptance criterion to pass")
        if run["result"] in {"QUALITY_REGRESSION", "SAFETY_REGRESSION", "ROUTING_REGRESSION"} and "FAIL" not in observed.values():
            raise ValueError("regression result requires failed acceptance evidence")
        if run["result"] == "INCONCLUSIVE" and "UNKNOWN" not in observed.values():
            raise ValueError("inconclusive result requires unknown acceptance evidence")
        for metric in METRICS:
            if run[metric] != "UNKNOWN" and not isinstance(run[metric], (int, float)):
                raise ValueError(f"{metric} must be observed numeric data or UNKNOWN")
        if run["role"] == "orchestrator" and run["model"] == "gpt-5.6-sol" and run["effort"] == "medium":
            control_sequence[run["fixture"]] = run["sequence"]
        if run["role"] == "orchestrator" and run["model"] == "gpt-5.6-luna" and run["effort"] == "medium":
            if run["fixture"] not in control_sequence or control_sequence[run["fixture"]] >= run["sequence"]:
                raise ValueError("Sol/medium control must precede Luna/medium candidate for each orchestrator fixture")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).with_name("fixtures.json"))
    parser.add_argument("--results", type=Path)
    args = parser.parse_args()
    try:
        fixtures = validate_fixtures(load(args.fixtures))
        if args.results:
            validate_results(load(args.results), fixtures)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"PASS fixtures={len(fixtures)} results={'validated' if args.results else 'not supplied'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
