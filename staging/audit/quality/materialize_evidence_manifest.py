#!/usr/bin/env python3
"""Create or check the content-addressed red-team evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ARTIFACTS = [
    "ORCHESTRATOR_PROMPT.md",
    "FACTUAL_PROMPT.md",
    "trials/orchestrator_control.json",
    "trials/orchestrator_candidate.json",
    "trials/factual_control.json",
    "trials/factual_candidate.json",
    "TRIAL_ARTIFACTS.md",
    "REDTEAM_REPORT.md",
    "INDEPENDENT_REVIEW.md",
    "../../global/codex/routing/MODEL_ROUTING.md",
    *[f"../../global/codex/agents/{name}.toml" for name in (
        "researcher", "quick-implementer", "implementer", "validator", "planner", "reviewer"
    )],
]
TRIAL_IDS = [
    "ORCH-CONTROL/CANDIDATE", "ORCH-CANDIDATE", "FACTUAL-SUPPLEMENT", "ROLE-R", "ROLE-Q", "ROLE-I", "ROLE-V",
    "ROLE-P/R", "TOOL-T", "REDTEAM_REPORT",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize() -> str:
    artifacts = []
    for relative in ARTIFACTS:
        path = (HERE / relative).resolve()
        if not path.is_file():
            raise FileNotFoundError(relative)
        artifacts.append({"path": relative, "sha256": digest(path)})
    return json.dumps({"version": 1, "trial_ids": TRIAL_IDS, "artifacts": artifacts},
                      sort_keys=True, separators=(",", ":")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = HERE / "evidence_manifest.json"
    content = materialize()
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != content:
            print("ERROR: evidence_manifest.json is stale")
            return 1
        print("PASS red-team evidence freshness")
        return 0
    target.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
