#!/usr/bin/env python3
"""Separate, evidence-bound Sol/medium to Luna/medium parent migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import subprocess
import tempfile

STAGING = Path(__file__).resolve().parents[1]
CANDIDATE_CONFIG = STAGING / "global/codex/config.luna-candidate.toml"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def persist_json(path: Path, data: dict[str, object], exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if exclusive and path.exists():
        raise ValueError(f"refusing to overwrite: {path}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_dir(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def candidate(content: str) -> str:
    model_pattern = re.compile(r'^model = "gpt-5\.6-sol"$', re.MULTILINE)
    effort_pattern = re.compile(r'^model_reasoning_effort = "medium"$', re.MULTILINE)
    if len(model_pattern.findall(content)) != 1 or len(effort_pattern.findall(content)) != 1:
        raise ValueError("config is not the expected Sol/medium control")
    return model_pattern.sub('model = "gpt-5.6-luna"', content)


def atomic_write(path: Path, content: str, mode: int) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".config-v2-model-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        fsync_dir(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate_gate(path: Path, approved_hash: str) -> dict[str, object]:
    if digest(path) != approved_hash:
        raise ValueError("approved gate hash does not match receipt")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    required = {"version", "decision", "control", "parent_candidate", "fixtures_sha256", "fixtures_path", "results_sha256", "results_path", "evidence_manifest_sha256", "evidence_manifest_path", "evaluator_sha256", "evaluator_path", "validator_sha256", "validator_path", "control_config_sha256", "control_config_path", "candidate_output_sha256", "candidate_config_sha256"}
    if set(receipt) != required or receipt["version"] != 1:
        raise ValueError("invalid quality-gate receipt")
    if receipt["decision"] != "ELIGIBLE_FOR_HUMAN_APPROVAL" or receipt["control"] != "gpt-5.6-sol/medium" or receipt["parent_candidate"] != "gpt-5.6-luna/medium":
        raise ValueError("quality-gate receipt does not authorize this transition")
    for field in ("fixtures_sha256", "results_sha256", "evidence_manifest_sha256", "evaluator_sha256", "validator_sha256", "control_config_sha256", "candidate_output_sha256", "candidate_config_sha256"):
        if not isinstance(receipt[field], str) or not re.fullmatch(r"[0-9a-f]{64}", receipt[field]):
            raise ValueError(f"invalid receipt digest: {field}")
    if receipt["candidate_config_sha256"] != digest(CANDIDATE_CONFIG):
        raise ValueError("quality gate was evaluated against another candidate config")
    evaluator = Path(receipt["evaluator_path"])
    validator = Path(receipt["validator_path"])
    fixtures = Path(receipt["fixtures_path"])
    results = Path(receipt["results_path"])
    evidence_manifest = Path(receipt["evidence_manifest_path"])
    control_config = Path(receipt["control_config_path"])
    if evaluator.resolve() != (STAGING / "audit/quality/evaluate_gate.py").resolve():
        raise ValueError("receipt names an untrusted evaluator")
    if validator.resolve() != (STAGING / "audit/quality/validate_quality.py").resolve():
        raise ValueError("receipt names an untrusted result validator")
    for field, artifact in (("evaluator_sha256", evaluator), ("validator_sha256", validator), ("fixtures_sha256", fixtures), ("results_sha256", results), ("evidence_manifest_sha256", evidence_manifest), ("control_config_sha256", control_config)):
        if not artifact.is_file() or digest(artifact) != receipt[field]:
            raise ValueError(f"quality evidence drift: {field}")
    rerun = subprocess.run([sys.executable, "-B", str(evaluator), str(results), "--fixtures", str(fixtures)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if rerun.returncode != 0 or json.loads(rerun.stdout).get("decision") != "ELIGIBLE_FOR_HUMAN_APPROVAL":
        raise ValueError("quality evidence no longer evaluates as eligible")
    return receipt


def load_journal(path: Path, config: Path) -> dict[str, object]:
    journal = json.loads(path.read_text(encoding="utf-8"))
    if journal.get("version") != 1 or Path(journal.get("config", "")).resolve(strict=False) != config.resolve(strict=False):
        raise ValueError("migration journal target mismatch")
    return journal


def rollback(config: Path, journal_path: Path) -> None:
    journal = load_journal(journal_path, config)
    backup = Path(journal["backup"])
    if digest(backup) != journal["before_hash"]:
        raise ValueError("backup hash mismatch")
    current_hash = digest(config)
    if current_hash == journal["before_hash"]:
        print("parent model already at Sol/medium control")
        return
    if current_hash != journal["installed_hash"]:
        raise ValueError("refusing rollback after config drift")
    atomic_write(config, backup.read_text(encoding="utf-8"), journal["mode"])
    journal["state"] = "ROLLED_BACK"
    persist_json(journal_path, journal)
    print("parent model rollback complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("plan", "apply", "rollback"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--expected-hash")
    parser.add_argument("--gate-receipt", type=Path)
    parser.add_argument("--approved-gate-hash")
    parser.add_argument("--migration-journal", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.config.is_symlink() or not args.config.is_file():
            raise ValueError("config must be a regular non-symlink file")
        if args.action == "rollback":
            rollback(args.config, args.migration_journal)
            return 0
        if not args.expected_hash or digest(args.config) != args.expected_hash:
            raise ValueError("config hash drift or missing expected hash")
        if not args.gate_receipt or not args.approved_gate_hash:
            raise ValueError("plan/apply require an exact human-approved quality-gate receipt hash")
        updated = candidate(args.config.read_text(encoding="utf-8"))
        installed_hash = hashlib.sha256(updated.encode()).hexdigest()
        gate = validate_gate(args.gate_receipt, args.approved_gate_hash)
        if args.expected_hash != gate["control_config_sha256"] or installed_hash != gate["candidate_output_sha256"]:
            raise ValueError("quality gate does not bind this exact control/candidate transition")
        if args.action == "plan":
            print(json.dumps({"status": "READY", "from": "gpt-5.6-sol/medium", "to": "gpt-5.6-luna/medium", "gate_sha256": args.approved_gate_hash}))
            return 0
        if args.migration_journal.exists():
            raise ValueError("migration journal path already exists")
        backup = args.migration_journal.with_suffix(".config.backup")
        if backup.exists():
            raise ValueError("backup path already exists")
        shutil.copy2(args.config, backup)
        with backup.open("rb") as stream:
            os.fsync(stream.fileno())
        fsync_dir(backup.parent)
        journal = {"version": 1, "state": "PREPARED", "config": str(args.config.resolve()), "before_hash": args.expected_hash, "installed_hash": installed_hash, "mode": stat.S_IMODE(args.config.stat().st_mode), "backup": str(backup.resolve()), "approved_gate_sha256": args.approved_gate_hash}
        persist_json(args.migration_journal, journal, exclusive=True)
        atomic_write(args.config, updated, journal["mode"])
        journal["state"] = "COMMITTED"
        persist_json(args.migration_journal, journal)
        print("parent model migrated to Luna/medium")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
