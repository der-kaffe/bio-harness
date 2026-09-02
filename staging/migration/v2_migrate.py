#!/usr/bin/env python3
"""Preview, install, or roll back Harness V2 with hash-aware targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

STAGING = Path(__file__).resolve().parents[1]
CANDIDATE_CODEX = STAGING / "global/codex"
CANDIDATE_SKILL = STAGING / "global/agents/skills/project-bootstrap"
AGENT_NAMES = ("researcher", "quick-implementer", "implementer", "validator", "planner", "reviewer")


class MigrationError(RuntimeError):
    pass


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def candidate_map() -> dict[str, Path]:
    result = {
        "codex/AGENTS.md": CANDIDATE_CODEX / "AGENTS.md",
        "codex/routing/MODEL_ROUTING.md": CANDIDATE_CODEX / "routing/MODEL_ROUTING.md",
        "codex/toolbox/_system/toolbox.py": CANDIDATE_CODEX / "toolbox/_system/toolbox.py",
        "codex/toolbox/_system/test_toolbox.py": CANDIDATE_CODEX / "toolbox/_system/test_toolbox.py",
    }
    for name in AGENT_NAMES:
        result[f"codex/agents/{name}.toml"] = CANDIDATE_CODEX / f"agents/{name}.toml"
    for source in sorted(CANDIDATE_SKILL.rglob("*")):
        if source.is_file():
            result[f"agents/skills/project-bootstrap/{source.relative_to(CANDIDATE_SKILL)}"] = source
    return result


def target_for(key: str, codex_home: Path, agents_home: Path) -> Path:
    prefix, relative = key.split("/", 1)
    if prefix == "codex":
        root = codex_home
        target = root / relative
        _check_target(root, target)
        return target
    if prefix == "agents":
        root = agents_home
        target = root / relative
        _check_target(root, target)
        return target
    raise MigrationError(f"unknown target root: {key}")


def _check_target(root: Path, target: Path) -> None:
    if root.is_symlink():
        raise MigrationError(f"refusing symlinked migration root: {root}")
    resolved_root = root.resolve(strict=False)
    resolved_target = target.resolve(strict=False)
    try:
        relative = target.relative_to(root)
        resolved_target.relative_to(resolved_root)
    except ValueError as error:
        raise MigrationError(f"target escapes migration root: {target}") from error
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise MigrationError(f"refusing symlinked migration component: {cursor}")


def state(path: Path) -> dict[str, object]:
    if path.is_symlink():
        raise MigrationError(f"refusing symlink target: {path}")
    if not path.exists():
        return {"exists": False, "sha256": None, "mode": None}
    if not path.is_file():
        raise MigrationError(f"target is not a regular file: {path}")
    return {"exists": True, "sha256": digest(path), "mode": stat.S_IMODE(path.stat().st_mode)}


def universe(codex_home: Path, agents_home: Path) -> set[str]:
    keys = set(candidate_map())
    installed_skill = agents_home / "skills/project-bootstrap"
    if installed_skill.exists():
        if installed_skill.is_symlink():
            raise MigrationError("refusing symlinked project-bootstrap target")
        for path in installed_skill.rglob("*"):
            if path.is_symlink():
                raise MigrationError(f"refusing symlink inside project-bootstrap: {path}")
            if path.is_file():
                keys.add(f"agents/skills/project-bootstrap/{path.relative_to(installed_skill)}")
    return keys


def snapshot(codex_home: Path, agents_home: Path) -> dict[str, object]:
    files = {key: state(target_for(key, codex_home, agents_home)) for key in sorted(universe(codex_home, agents_home))}
    return {
        "version": 1,
        "codex_home": str(codex_home.resolve(strict=False)),
        "agents_home": str(agents_home.resolve(strict=False)),
        "files": files,
        "candidate": {key: digest(source) for key, source in sorted(candidate_map().items())},
        "config_intentionally_unchanged": True,
    }


def load_baseline(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as stream:
        baseline = json.load(stream)
    if baseline.get("version") != 1 or baseline.get("config_intentionally_unchanged") is not True:
        raise MigrationError("invalid V2 baseline")
    return baseline


def verify(baseline: dict[str, object], codex_home: Path, agents_home: Path) -> None:
    if str(codex_home.resolve(strict=False)) != baseline["codex_home"] or str(agents_home.resolve(strict=False)) != baseline["agents_home"]:
        raise MigrationError("baseline roots do not match requested roots")
    if baseline["candidate"] != {key: digest(source) for key, source in sorted(candidate_map().items())}:
        raise MigrationError("candidate drifted after baseline")
    current_keys = universe(codex_home, agents_home)
    if current_keys != set(baseline["files"]):
        raise MigrationError("target universe drifted after baseline")
    for key, expected in baseline["files"].items():
        if state(target_for(key, codex_home, agents_home)) != expected:
            raise MigrationError(f"target drift: {key}")


def atomic_copy(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise MigrationError(f"source is not a regular non-symlink file: {source}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.v2-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as output, source.open("rb") as input_stream:
            shutil.copyfileobj(input_stream, output)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary, stat.S_IMODE(source.stat().st_mode))
        if target.is_symlink():
            raise MigrationError(f"target became a symlink: {target}")
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def persist_manifest(path: Path, manifest: dict[str, object]) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".manifest-v2-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_dir(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def ensure_parent(target: Path, root: Path, manifest: dict[str, object], manifest_path: Path) -> None:
    missing: list[Path] = []
    cursor = target.parent
    while cursor != root and not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent
    for directory in reversed(missing):
        entry = {"root": str(root.resolve(strict=False)), "path": str(directory.relative_to(root)), "state": "PREPARED"}
        manifest["directories"].append(entry)
        persist_manifest(manifest_path, manifest)
        directory.mkdir()
        fsync_dir(directory.parent)
        entry["state"] = "COMMITTED"
        persist_manifest(manifest_path, manifest)


def install(baseline: dict[str, object], codex_home: Path, agents_home: Path, backup: Path) -> dict[str, object]:
    verify(baseline, codex_home, agents_home)
    if backup.exists():
        raise MigrationError("backup directory already exists")
    backup.mkdir(parents=True, mode=0o700)
    journal: list[dict[str, object]] = []
    manifest = {"version": 2, "baseline": baseline, "journal": journal, "directories": []}
    manifest_path = backup / "manifest.json"
    try:
        for key, before in baseline["files"].items():
            target = target_for(key, codex_home, agents_home)
            if before["exists"]:
                backup_target = backup / "files" / key
                backup_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup_target)
                with backup_target.open("rb") as stream:
                    os.fsync(stream.fileno())
                fsync_dir(backup_target.parent)
        fsync_dir(backup)
        persist_manifest(manifest_path, manifest)

        candidates = candidate_map()
        for key in sorted(baseline["files"]):
            target = target_for(key, codex_home, agents_home)
            if key in candidates:
                ensure_parent(target, codex_home if key.startswith("codex/") else agents_home, manifest, manifest_path)
                action = {"key": key, "action": "write", "installed_hash": digest(candidates[key]), "state": "PREPARED"}
                journal.append(action)
                persist_manifest(manifest_path, manifest)
                atomic_copy(candidates[key], target)
            else:
                action = {"key": key, "action": "remove", "installed_hash": None, "state": "PREPARED"}
                journal.append(action)
                persist_manifest(manifest_path, manifest)
                target.unlink()
            action["state"] = "COMMITTED"
            persist_manifest(manifest_path, manifest)
    except Exception:
        rollback(manifest, codex_home, agents_home, backup, partial=True)
        raise
    return manifest


def rollback(manifest: dict[str, object], codex_home: Path, agents_home: Path, backup: Path, partial: bool = False) -> None:
    if manifest.get("version") != 2 or not isinstance(manifest.get("journal"), list) or not isinstance(manifest.get("directories"), list):
        raise MigrationError("invalid V2 rollback manifest")
    baseline = manifest.get("baseline", {})
    if str(codex_home.resolve(strict=False)) != baseline.get("codex_home") or str(agents_home.resolve(strict=False)) != baseline.get("agents_home"):
        raise MigrationError("rollback roots do not match the recorded installation")
    journal_keys = {action.get("key") for action in manifest["journal"]}
    baseline_keys = set(baseline.get("files", {}))
    expected_prefix = sorted(baseline_keys)[:len(manifest["journal"])]
    actual_order = [action.get("key") for action in manifest["journal"]]
    if not journal_keys <= baseline_keys or actual_order != expected_prefix:
        raise MigrationError("rollback journal does not match recorded target universe")
    manifest_path = backup / "manifest.json"
    for action in reversed(manifest["journal"]):
        key = action["key"]
        target = target_for(key, codex_home, agents_home)
        before = manifest["baseline"]["files"][key]
        current = state(target)
        if current == before:
            action["state"] = "ROLLED_BACK"
            persist_manifest(manifest_path, manifest)
            continue
        expected_exists = action["installed_hash"] is not None
        if current["exists"] != expected_exists or current["sha256"] != action["installed_hash"]:
            raise MigrationError(f"refusing rollback after later target change: {key}")
        if before["exists"]:
            backup_target = backup / "files" / key
            _check_target(backup, backup_target)
            if digest(backup_target) != before["sha256"]:
                raise MigrationError(f"backup hash mismatch: {key}")
            atomic_copy(backup_target, target)
            os.chmod(target, before["mode"])
        elif target.exists():
            target.unlink()
        action["state"] = "ROLLED_BACK"
        persist_manifest(manifest_path, manifest)
    for entry in reversed(manifest["directories"]):
        root = Path(entry["root"])
        if root.resolve(strict=False) not in {codex_home.resolve(strict=False), agents_home.resolve(strict=False)}:
            raise MigrationError("recorded directory root mismatch")
        directory = root / entry["path"]
        _check_target(root, directory)
        if directory.exists():
            try:
                directory.rmdir()
            except OSError as error:
                raise MigrationError(f"created directory is not empty: {directory}") from error
        entry["state"] = "ROLLED_BACK"
        persist_manifest(manifest_path, manifest)
    if not partial:
        print("rollback complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("snapshot", "plan", "install", "rollback"))
    parser.add_argument("--codex-home", type=Path, required=True)
    parser.add_argument("--agents-home", type=Path, required=True)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "snapshot":
            if not args.output:
                raise MigrationError("snapshot requires --output")
            data = snapshot(args.codex_home, args.agents_home)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            persist_manifest(args.output, data)
            print(f"snapshot targets={len(data['files'])}")
        elif args.action == "plan":
            if not args.baseline:
                raise MigrationError("plan requires --baseline")
            data = load_baseline(args.baseline)
            verify(data, args.codex_home, args.agents_home)
            print(f"plan valid targets={len(data['files'])} config=unchanged")
        elif args.action == "install":
            if not args.baseline or not args.backup:
                raise MigrationError("install requires --baseline and --backup")
            data = load_baseline(args.baseline)
            installed = install(data, args.codex_home, args.agents_home, args.backup)
            print(f"installed actions={len(installed['journal'])} config=unchanged")
        else:
            if not args.backup:
                raise MigrationError("rollback requires --backup")
            with (args.backup / "manifest.json").open(encoding="utf-8") as stream:
                manifest = json.load(stream)
            rollback(manifest, args.codex_home, args.agents_home, args.backup)
    except (OSError, ValueError, MigrationError) as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
