#!/usr/bin/env python3
"""Validate the unified Harness V2 staging candidate without model calls."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
STAGING = ROOT / "staging"
CODEX = STAGING / "global/codex"
SKILL = STAGING / "global/agents/skills/project-bootstrap"
BLUEPRINT = STAGING / "blueprint/project"
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def files(root: Path) -> dict[Path, str]:
    return {path.relative_to(root): hashlib.sha256(path.read_bytes()).hexdigest() for path in root.rglob("*") if path.is_file()}


def run(path: Path, *args: str) -> None:
    result = subprocess.run([sys.executable, "-B", str(path), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        ERRORS.append(f"{path.relative_to(ROOT)} failed:\n{result.stdout}")
    else:
        print(result.stdout.strip())


def main() -> int:
    control = tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))
    luna = tomllib.loads((CODEX / "config.luna-candidate.toml").read_text(encoding="utf-8"))
    check((control.get("model"), control.get("model_reasoning_effort")) == ("gpt-5.6-sol", "medium"), "installable control is not Sol/medium")
    check((luna.get("model"), luna.get("model_reasoning_effort")) == ("gpt-5.6-luna", "medium"), "optional candidate is not Luna/medium")
    check("multi_agent_v2" not in (CODEX / "config.toml").read_text(encoding="utf-8"), "control enables multi_agent_v2")

    expected = {"researcher", "quick-implementer", "implementer", "validator", "planner", "reviewer"}
    actual = {path.stem for path in (CODEX / "agents").glob("*.toml")}
    check(actual == expected, f"agent catalog mismatch: {actual}")
    for path in (CODEX / "agents").glob("*.toml"):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for field in ("name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"):
            check(field in data, f"{path.name} lacks {field}")

    global_words = len((CODEX / "AGENTS.md").read_text(encoding="utf-8").split())
    routing_words = len((CODEX / "routing/MODEL_ROUTING.md").read_text(encoding="utf-8").split())
    project_words = len((BLUEPRINT / ".ai/PROJECT.md.template").read_text(encoding="utf-8").split())
    check(global_words <= 300, f"global AGENTS exceeds budget: {global_words}")
    check(500 <= routing_words <= 750, f"routing outside budget: {routing_words}")
    check(project_words <= 200, f"project router exceeds budget: {project_words}")
    check(files(BLUEPRINT) == files(SKILL / "assets/project"), "blueprint/package parity failure")

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    check(skill_text.startswith("---\nname: project-bootstrap\n"), "invalid skill frontmatter")
    for reference in ("bootstrap-workflow.md", "private-workspace.md", "operating-workflows.md", "tooling.md", "model-routing.md"):
        check((SKILL / "references" / reference).is_file(), f"missing skill reference: {reference}")
        check(reference in skill_text, f"unrouted skill reference: {reference}")

    global_text = (CODEX / "AGENTS.md").read_text(encoding="utf-8")
    check("@" not in global_text, "routing policy is always imported")
    check(global_text.lower().index("correctness") < global_text.lower().index("cost"), "quality does not precede cost globally")

    run(STAGING / "audit/test_v2.py")
    run(STAGING / "audit/quality/materialize_evidence_manifest.py", "--check")
    run(STAGING / "audit/quality/materialize_redteam_results.py", "--check")
    run(STAGING / "audit/quality/validate_quality.py", "--results", str(STAGING / "audit/quality/redteam_results.json"))
    run(STAGING / "audit/quality/validate_quality.py", "--results", str(STAGING / "audit/quality/results.example.json"))
    run(CODEX / "toolbox/_system/test_toolbox.py")
    run(SKILL / "scripts/test_project_privacy.py")

    if ERRORS:
        print("\n".join(f"ERROR: {error}" for error in ERRORS))
        return 1
    print(f"PASS unified V2 staging: global_words={global_words} routing_words={routing_words} project_words={project_words}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
