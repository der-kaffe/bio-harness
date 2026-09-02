#!/usr/bin/env python3
"""Execute the approved global Codex migration with hash-guarded rollback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE = Path("/home/juanc/codex-bootstrap")
STAGING = WORKSPACE / "staging"
CODEX_HOME = Path("/home/juanc/.codex")
PERSONAL_SKILLS = Path("/home/juanc/.agents/skills")
REAL_CONFIG = CODEX_HOME / "config.toml"
REAL_RULES = CODEX_HOME / "rules/default.rules"
CANDIDATE_CODEX = STAGING / "global/codex"
CANDIDATE_SKILL = STAGING / "global/agents/skills/project-bootstrap"

EXPECTED_VERSION = "codex-cli 0.152.0"
EXPECTED_LINK_TEXT = "../.npm/_npx/35da2574b383c6cf/node_modules/job-forge/.codex/config.toml"
EXPECTED_TARGET = Path("/home/juanc/.npm/_npx/35da2574b383c6cf/node_modules/job-forge/.codex/config.toml")
EXPECTED_TARGET_HASH = "8ed32900ce879ed579f7502400e03382c2399d8c6743de7f3d05ae646068ba0d"
EXPECTED_RULES_HASH = "658e80093f41468648069ab2447400d2d91c7b94d33c318ec4f55fbbcf260375"
EXPECTED_RULE_COUNT = 39
EXPECTED_PERSONAL_SKILLS = 25
# Canonical digest uses globally sorted manifest paths (global/agents before
# global/codex), matching manifest_digest().
EXPECTED_CANDIDATE_TREE_HASH = "0a3bc0ba2ffe6b97750e65b672a6252060865e0cdc46338718255c7772988f71"


class MigrationError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_manifest(roots: list[Path], base: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for root in roots:
        for path in sorted(item for item in root.rglob("*") if item.is_file() and not item.is_symlink()):
            rel = str(path.relative_to(base))
            st = path.stat()
            result[rel] = {"sha256": sha256(path), "mode": stat.S_IMODE(st.st_mode), "size": st.st_size}
        symlinks = sorted(item for item in root.rglob("*") if item.is_symlink())
        if symlinks:
            raise MigrationError(f"unexpected symlink in candidate: {symlinks[0]}")
    return result


def manifest_digest(manifest: dict[str, dict[str, object]]) -> str:
    h = hashlib.sha256()
    for rel, metadata in sorted(manifest.items()):
        h.update(f"{rel}\0{metadata['sha256']}\n".encode())
    return h.hexdigest()


def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            h.update(f"L\0{rel}\0{os.readlink(path)}\n".encode())
        elif path.is_file():
            h.update(f"F\0{rel}\0{sha256(path)}\n".encode())
        elif path.is_dir():
            h.update(f"D\0{rel}\n".encode())
    return h.hexdigest()


def stat_record(path: Path, *, follow: bool) -> dict[str, object]:
    st = path.stat() if follow else path.lstat()
    return {
        "mode": stat.S_IMODE(st.st_mode),
        "uid": st.st_uid,
        "gid": st.st_gid,
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "device": st.st_dev,
        "inode": st.st_ino,
    }


def atomic_json(path: Path, data: object) -> None:
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def atomic_install(source: Path, destination: Path, mode: int | None = None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_name(f".{destination.name}.codex-migration-{os.getpid()}")
    if tmp.exists() or tmp.is_symlink():
        raise MigrationError(f"temporary collision: {tmp}")
    shutil.copyfile(source, tmp)
    os.chmod(tmp, mode if mode is not None else stat.S_IMODE(source.stat().st_mode))
    os.replace(tmp, destination)


def skill_inventory() -> dict[str, str]:
    return {
        path.name: tree_digest(path)
        for path in sorted(PERSONAL_SKILLS.iterdir())
        if path.is_dir() and not path.is_symlink()
    }


def candidate_manifest() -> dict[str, dict[str, object]]:
    return file_manifest([CANDIDATE_CODEX, CANDIDATE_SKILL], STAGING)


def preflight() -> dict[str, object]:
    version = subprocess.run(["codex", "--version"], check=True, capture_output=True, text=True).stdout.strip()
    if version != EXPECTED_VERSION:
        raise MigrationError(f"version drift: {version!r}")
    manifest = candidate_manifest()
    digest = manifest_digest(manifest)
    if digest != EXPECTED_CANDIDATE_TREE_HASH:
        raise MigrationError(f"candidate drift: {digest}")
    if not REAL_CONFIG.is_symlink():
        raise MigrationError("real config is no longer the expected symlink")
    link_text = os.readlink(REAL_CONFIG)
    if link_text != EXPECTED_LINK_TEXT:
        raise MigrationError(f"config symlink drift: {link_text}")
    target = REAL_CONFIG.resolve(strict=True)
    if target != EXPECTED_TARGET:
        raise MigrationError(f"config target drift: {target}")
    if sha256(target) != EXPECTED_TARGET_HASH:
        raise MigrationError("config target content drift")
    if sha256(REAL_RULES) != EXPECTED_RULES_HASH:
        raise MigrationError("rules content drift")
    rule_count = sum(1 for line in REAL_RULES.read_text().splitlines() if line.startswith("prefix_rule("))
    if rule_count != EXPECTED_RULE_COUNT:
        raise MigrationError(f"rules count drift: {rule_count}")
    last_rule = REAL_RULES.read_text().splitlines()[-1]
    if "codex-bootstrap/staging/global/codex" not in last_rule or not last_rule.startswith("prefix_rule("):
        raise MigrationError("rule 39 side effect is not identifiable")
    inventory = skill_inventory()
    if len(inventory) != EXPECTED_PERSONAL_SKILLS or "project-bootstrap" in inventory:
        raise MigrationError("personal skill inventory drift or project-bootstrap collision")
    collisions = [
        CODEX_HOME / "AGENTS.md",
        CODEX_HOME / "agents/researcher.toml",
        CODEX_HOME / "agents/planner.toml",
        CODEX_HOME / "agents/reviewer.toml",
        PERSONAL_SKILLS / "project-bootstrap",
    ]
    found = [str(path) for path in collisions if path.exists() or path.is_symlink()]
    if found:
        raise MigrationError(f"unexpected collisions: {found}")
    agents_dir_entries = []
    agents_dir = CODEX_HOME / "agents"
    if agents_dir.exists():
        agents_dir_entries = sorted(path.name for path in agents_dir.iterdir())
        if agents_dir_entries:
            raise MigrationError(f"unexpected global agent entries: {agents_dir_entries}")
    return {
        "version": version,
        "candidate_manifest": manifest,
        "candidate_tree_hash": digest,
        "config": {
            "link_text": link_text,
            "link_stat": stat_record(REAL_CONFIG, follow=False),
            "target": str(target),
            "target_hash": sha256(target),
            "target_stat": stat_record(target, follow=True),
        },
        "rules": {
            "hash": sha256(REAL_RULES),
            "count": rule_count,
            "stat": stat_record(REAL_RULES, follow=True),
            "rule_39_identified": True,
        },
        "personal_skills": inventory,
        "global_agents_before": agents_dir_entries,
        "collisions": [],
    }


def create_backup(backup: Path) -> None:
    if backup.exists() or backup.is_symlink():
        raise MigrationError(f"backup destination already exists: {backup}")
    if backup.parent != WORKSPACE / "backups":
        raise MigrationError("backup must be a direct child of workspace/backups")
    state = preflight()
    backup.mkdir(parents=True, mode=0o700)
    (backup / "config").mkdir(mode=0o700)
    (backup / "rules").mkdir(mode=0o700)
    (backup / "inventory").mkdir(mode=0o700)
    shutil.copy2(EXPECTED_TARGET, backup / "config/target-content.toml")
    os.symlink(EXPECTED_LINK_TEXT, backup / "config/config.toml.symlink")
    shutil.copy2(REAL_RULES, backup / "rules/default.rules")
    atomic_json(backup / "inventory/preflight.json", state)
    atomic_json(backup / "inventory/candidate-manifest.json", state["candidate_manifest"])
    atomic_json(
        backup / "migration-journal.json",
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "BACKUP_COMPLETE",
            "completed_steps": [],
        },
    )
    if sha256(backup / "config/target-content.toml") != EXPECTED_TARGET_HASH:
        raise MigrationError("backed-up config hash mismatch")
    if sha256(backup / "rules/default.rules") != EXPECTED_RULES_HASH:
        raise MigrationError("backed-up rules hash mismatch")
    if os.readlink(backup / "config/config.toml.symlink") != EXPECTED_LINK_TEXT:
        raise MigrationError("backed-up symlink representation mismatch")
    print(json.dumps({"status": "BACKUP_COMPLETE", "backup": str(backup)}, sort_keys=True))


def load_backup(backup: Path) -> dict[str, object]:
    data = json.loads((backup / "inventory/preflight.json").read_text())
    if sha256(backup / "config/target-content.toml") != data["config"]["target_hash"]:
        raise MigrationError("backup config verification failed")
    if sha256(backup / "rules/default.rules") != data["rules"]["hash"]:
        raise MigrationError("backup rules verification failed")
    return data


def checkpoint(backup: Path) -> None:
    saved = load_backup(backup)
    current = preflight()
    keys = [
        (saved["candidate_tree_hash"], current["candidate_tree_hash"], "candidate"),
        (saved["config"]["link_text"], current["config"]["link_text"], "symlink"),
        (saved["config"]["target"], current["config"]["target"], "target"),
        (saved["config"]["target_hash"], current["config"]["target_hash"], "target hash"),
        (saved["rules"]["hash"], current["rules"]["hash"], "rules hash"),
        (saved["personal_skills"], current["personal_skills"], "skill inventory"),
    ]
    for before, after, label in keys:
        if before != after:
            raise MigrationError(f"checkpoint drift: {label}")
    print(json.dumps({"status": "CHECKPOINT_PASS", "backup": str(backup)}, sort_keys=True))


def strict_config_probe(installed_config: Path, backup: Path) -> None:
    with installed_config.open("rb") as stream:
        parsed = tomllib.load(stream)
    expected = {
        "model": "gpt-5.6-sol",
        "model_provider": "openai",
        "model_reasoning_effort": "high",
        "sandbox_mode": "workspace-write",
        "approval_policy": "on-request",
        "features": {"memories": False},
    }
    if parsed != expected:
        raise MigrationError(f"installed config semantic mismatch: {parsed}")
    validation_home = backup / "validation-home"
    validation_state = backup / "validation-state"
    validation_home.mkdir(mode=0o700, exist_ok=False)
    validation_state.mkdir(mode=0o700, exist_ok=False)
    shutil.copy2(installed_config, validation_home / "config.toml")
    env = os.environ.copy()
    env["CODEX_HOME"] = str(validation_home)
    env["CODEX_SQLITE_HOME"] = str(validation_state)
    proc = subprocess.run(
        ["codex", "app-server", "--strict-config", "--listen", "stdio://"],
        cwd=WORKSPACE,
        env=env,
        input=b"",
        capture_output=True,
        timeout=30,
    )
    (backup / "strict-config.stdout").write_bytes(proc.stdout)
    (backup / "strict-config.stderr").write_bytes(proc.stderr)
    if proc.returncode != 0:
        raise MigrationError(f"strict config probe failed: {proc.returncode}")


def journal(backup: Path, status: str, steps: list[str], error: str | None = None) -> None:
    data: dict[str, object] = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "completed_steps": steps,
    }
    if error:
        data["error"] = error
    atomic_json(backup / "migration-journal.json", data)


def installed_skill_matches() -> bool:
    destination = PERSONAL_SKILLS / "project-bootstrap"
    return destination.is_dir() and tree_digest(destination) == tree_digest(CANDIDATE_SKILL)


def rollback(backup: Path, completed: list[str]) -> list[str]:
    notes: list[str] = []
    skill = PERSONAL_SKILLS / "project-bootstrap"
    if "skill" in completed and skill.exists():
        if installed_skill_matches():
            shutil.rmtree(skill)
        else:
            notes.append("preserved modified project-bootstrap")
    for name in ("researcher.toml", "planner.toml", "reviewer.toml"):
        destination = CODEX_HOME / "agents" / name
        source = CANDIDATE_CODEX / "agents" / name
        if "agents" in completed and destination.exists():
            if sha256(destination) == sha256(source):
                destination.unlink()
            else:
                notes.append(f"preserved modified {destination}")
    agents_dir = CODEX_HOME / "agents"
    if agents_dir.exists() and not any(agents_dir.iterdir()):
        agents_dir.rmdir()
    global_agents = CODEX_HOME / "AGENTS.md"
    if "AGENTS" in completed and global_agents.exists():
        if sha256(global_agents) == sha256(CANDIDATE_CODEX / "AGENTS.md"):
            global_agents.unlink()
        else:
            notes.append("preserved modified global AGENTS.md")
    if "rules" in completed and REAL_RULES.exists():
        if sha256(REAL_RULES) == sha256(CANDIDATE_CODEX / "rules/default.rules"):
            atomic_install(backup / "rules/default.rules", REAL_RULES)
        else:
            notes.append("preserved modified rules")
    if "config" in completed:
        restore = False
        if REAL_CONFIG.is_symlink():
            restore = False
        elif REAL_CONFIG.exists():
            if sha256(REAL_CONFIG) == sha256(CANDIDATE_CODEX / "config.toml"):
                REAL_CONFIG.unlink()
                restore = True
            else:
                notes.append("preserved modified config")
        else:
            restore = True
        if restore:
            if EXPECTED_TARGET.exists() and sha256(EXPECTED_TARGET) == EXPECTED_TARGET_HASH:
                os.symlink(EXPECTED_LINK_TEXT, REAL_CONFIG)
            else:
                atomic_install(backup / "config/target-content.toml", REAL_CONFIG, 0o600)
                notes.append("restored prior config as regular file because legacy target changed/missing")
    return notes


def migrate(backup: Path) -> None:
    checkpoint(backup)
    saved = load_backup(backup)
    completed: list[str] = []
    skill_tmp = PERSONAL_SKILLS / f".project-bootstrap.codex-migration-{os.getpid()}"
    try:
        # Final race check occurs immediately before the first mutation.
        current = preflight()
        if current["config"]["target_hash"] != saved["config"]["target_hash"]:
            raise MigrationError("pre-write config target race detected")

        completed.append("config")
        REAL_CONFIG.unlink()
        atomic_install(CANDIDATE_CODEX / "config.toml", REAL_CONFIG, 0o600)
        if REAL_CONFIG.is_symlink() or sha256(REAL_CONFIG) != sha256(CANDIDATE_CODEX / "config.toml"):
            raise MigrationError("config install verification failed")
        if REAL_CONFIG.stat().st_uid != os.getuid() or stat.S_IMODE(REAL_CONFIG.stat().st_mode) != 0o600:
            raise MigrationError("config ownership or mode verification failed")
        journal(backup, "CONFIG_INSTALLED", completed)
        strict_config_probe(REAL_CONFIG, backup)
        journal(backup, "CONFIG_VALIDATED", completed)

        atomic_install(CANDIDATE_CODEX / "AGENTS.md", CODEX_HOME / "AGENTS.md")
        completed.append("AGENTS")
        journal(backup, "AGENTS_INSTALLED", completed)

        agents_dir = CODEX_HOME / "agents"
        agents_dir.mkdir(mode=0o755)
        completed.append("agents")
        for name in ("researcher.toml", "planner.toml", "reviewer.toml"):
            atomic_install(CANDIDATE_CODEX / "agents" / name, agents_dir / name)
        journal(backup, "AGENTS_CONFIG_INSTALLED", completed)

        atomic_install(CANDIDATE_CODEX / "rules/default.rules", REAL_RULES)
        completed.append("rules")
        journal(backup, "RULES_INSTALLED", completed)

        if skill_tmp.exists() or skill_tmp.is_symlink():
            raise MigrationError(f"skill temp collision: {skill_tmp}")
        shutil.copytree(CANDIDATE_SKILL, skill_tmp, symlinks=False)
        if tree_digest(skill_tmp) != tree_digest(CANDIDATE_SKILL):
            raise MigrationError("staged skill copy hash mismatch")
        os.replace(skill_tmp, PERSONAL_SKILLS / "project-bootstrap")
        completed.append("skill")
        journal(backup, "MIGRATION_COMPLETE", completed)
        atomic_json(
            backup / "migration-result.json",
            {
                "status": "MIGRATION_COMPLETE",
                "completed_steps": completed,
                "config_hash": sha256(REAL_CONFIG),
                "AGENTS_hash": sha256(CODEX_HOME / "AGENTS.md"),
                "rules_hash": sha256(REAL_RULES),
                "skill_tree_hash": tree_digest(PERSONAL_SKILLS / "project-bootstrap"),
            },
        )
        print(json.dumps({"status": "MIGRATION_COMPLETE", "backup": str(backup)}, sort_keys=True))
    except Exception as exc:
        if skill_tmp.exists() and skill_tmp.is_dir() and not skill_tmp.is_symlink():
            shutil.rmtree(skill_tmp)
        notes = rollback(backup, completed)
        journal(backup, "ROLLED_BACK", completed, f"{type(exc).__name__}: {exc}; notes={notes}")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("backup", "checkpoint", "migrate"))
    parser.add_argument("backup", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "backup":
            create_backup(args.backup)
        elif args.action == "checkpoint":
            checkpoint(args.backup)
        else:
            migrate(args.backup)
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
