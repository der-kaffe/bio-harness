#!/usr/bin/env python3
"""Isolated migration and rollback simulation; writes only audit/simulation/run-001."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path


STAGING = Path(__file__).resolve().parents[1]
RUN = STAGING / "audit/simulation/run-001"
CANDIDATE_CODEX = STAGING / "global/codex"
CANDIDATE_SKILL = STAGING / "global/agents/skills/project-bootstrap"
STAMP = "20260901T000000Z"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded(path: Path) -> Path:
    resolved_parent = path.parent.resolve()
    if RUN.resolve() not in (resolved_parent, *resolved_parent.parents):
        raise RuntimeError(f"path escaped simulation root: {path}")
    return path


def write(path: Path, content: str) -> None:
    bounded(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def make_home(name: str, collision: bool = False) -> tuple[Path, Path]:
    root = RUN / name
    home = root / "home"
    codex = home / ".codex"
    legacy = root / "job-forge-cache/.codex/config.toml"
    write(legacy, 'model = "legacy-job-forge"\n[mcp_servers.geometra]\ncommand = "legacy"\n')
    codex.mkdir(parents=True)
    bounded(codex / "config.toml").symlink_to(os.path.relpath(legacy, codex))
    rules = [f'prefix_rule(pattern=["legacy", "rule", "{n:02d}"], decision="allow")' for n in range(1, 38)]
    rules += [
        'prefix_rule(pattern=["node", "fetch-codex-manual.mjs"], decision="allow")',
        'prefix_rule(pattern=["rm", "-rf", "staging-generated-state"], decision="allow")',
    ]
    write(codex / "rules/default.rules", "\n".join(rules) + "\n")
    write(home / ".agents/skills/existing-skill/SKILL.md", "---\nname: existing-skill\ndescription: fixture\n---\n")
    if collision:
        write(home / ".agents/skills/project-bootstrap/SKILL.md", "human-owned collision\n")
    return root, home


def snapshot(root: Path, home: Path) -> dict[str, object]:
    codex = home / ".codex"
    link = codex / "config.toml"
    backup = root / f"backups/{STAMP}"
    backup.mkdir(parents=True)
    link_text = os.readlink(link)
    target = link.resolve(strict=True)
    shutil.copy2(target, backup / "config.resolved.toml")
    shutil.copy2(codex / "rules/default.rules", backup / "default.rules")
    manifest = {
        "config_link_text": link_text,
        "config_target": str(target),
        "config_hash": digest(target),
        "rules_hash": digest(codex / "rules/default.rules"),
        "candidate_hashes": {
            str(path.relative_to(STAGING)): digest(path)
            for path in sorted((STAGING / "global").rglob("*"))
            if path.is_file()
        },
    }
    write(backup / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def preflight(home: Path, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    config = home / ".codex/config.toml"
    if not config.is_symlink() or os.readlink(config) != manifest["config_link_text"]:
        errors.append("config symlink changed since snapshot")
    elif digest(config.resolve(strict=True)) != manifest["config_hash"]:
        errors.append("config target content changed since snapshot")
    for path in [home / ".codex/AGENTS.md", *[home / f".codex/agents/{name}.toml" for name in ("researcher", "planner", "reviewer")], home / ".agents/skills/project-bootstrap"]:
        if path.exists() or path.is_symlink():
            errors.append(f"collision: {path.relative_to(home)}")
    return errors


def install(home: Path, stop_after: str | None = None) -> None:
    config = home / ".codex/config.toml"
    bounded(config).unlink()
    shutil.copy2(CANDIDATE_CODEX / "config.toml", config)
    if stop_after == "config":
        return
    shutil.copy2(CANDIDATE_CODEX / "AGENTS.md", home / ".codex/AGENTS.md")
    for source in sorted((CANDIDATE_CODEX / "agents").glob("*.toml")):
        target = home / ".codex/agents" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(CANDIDATE_CODEX / "rules/default.rules", home / ".codex/rules/default.rules")
    if stop_after == "rules":
        return
    shutil.copytree(CANDIDATE_SKILL, home / ".agents/skills/project-bootstrap")


def rollback(root: Path, home: Path, manifest: dict[str, object]) -> list[str]:
    refused: list[str] = []
    backup = root / f"backups/{STAMP}"
    candidate_paths = [
        (home / ".codex/AGENTS.md", CANDIDATE_CODEX / "AGENTS.md"),
        *[(home / f".codex/agents/{name}.toml", CANDIDATE_CODEX / f"agents/{name}.toml") for name in ("researcher", "planner", "reviewer")],
    ]
    for installed, candidate in candidate_paths:
        if installed.exists():
            if digest(installed) == digest(candidate):
                bounded(installed).unlink()
            else:
                refused.append(f"human-modified: {installed.relative_to(home)}")
    skill = home / ".agents/skills/project-bootstrap"
    if skill.exists():
        installed_files = {str(p.relative_to(skill)): digest(p) for p in skill.rglob("*") if p.is_file()}
        source_files = {str(p.relative_to(CANDIDATE_SKILL)): digest(p) for p in CANDIDATE_SKILL.rglob("*") if p.is_file()}
        if installed_files == source_files:
            shutil.rmtree(bounded(skill))
        else:
            refused.append("human-modified: .agents/skills/project-bootstrap")
    shutil.copy2(backup / "default.rules", home / ".codex/rules/default.rules")
    config = home / ".codex/config.toml"
    if config.exists() or config.is_symlink():
        bounded(config).unlink()
    target = Path(str(manifest["config_target"]))
    if target.exists() and digest(target) == manifest["config_hash"]:
        config.symlink_to(str(manifest["config_link_text"]))
    else:
        shutil.copy2(backup / "config.resolved.toml", config)
        os.chmod(config, 0o600)
        refused.append("legacy symlink target unavailable/changed; restored content as regular file")
    return refused


def main() -> None:
    if RUN.exists():
        raise SystemExit(f"refusing to overwrite existing simulation: {RUN}")
    RUN.mkdir(parents=True)
    results: dict[str, object] = {}

    collision_root, collision_home = make_home("collision", collision=True)
    collision_manifest = snapshot(collision_root, collision_home)
    collision_errors = preflight(collision_home, collision_manifest)
    results["collision_preflight"] = {"errors": collision_errors, "config_still_symlink": (collision_home / ".codex/config.toml").is_symlink()}

    drift_root, drift_home = make_home("target-drift")
    drift_manifest = snapshot(drift_root, drift_home)
    write((drift_home / ".codex/config.toml").resolve(strict=True), "changed after snapshot\n")
    results["target_drift_preflight"] = preflight(drift_home, drift_manifest)

    for checkpoint in ("config", "rules"):
        root, home = make_home(f"partial-{checkpoint}")
        manifest = snapshot(root, home)
        assert not preflight(home, manifest)
        install(home, stop_after=checkpoint)
        rollback_result = rollback(root, home, manifest)
        results[f"partial_{checkpoint}_rollback"] = {
            "config_symlink_restored": (home / ".codex/config.toml").is_symlink(),
            "rules_hash_restored": digest(home / ".codex/rules/default.rules") == manifest["rules_hash"],
            "notes": rollback_result,
        }

    root, home = make_home("complete")
    manifest = snapshot(root, home)
    assert not preflight(home, manifest)
    install(home)
    installed_rules = (home / ".codex/rules/default.rules").read_text()
    results["complete_install"] = {
        "config_regular": (home / ".codex/config.toml").is_file() and not (home / ".codex/config.toml").is_symlink(),
        "agents": sorted(path.name for path in (home / ".codex/agents").glob("*.toml")),
        "zero_custom_rules": "prefix_rule(" not in installed_rules,
        "skill_assets_present": (home / ".agents/skills/project-bootstrap/assets/project/ACTIVATION.md").is_file(),
    }
    write(home / ".codex/AGENTS.md", (home / ".codex/AGENTS.md").read_text() + "\nHuman edit after migration.\n")
    legacy_target = Path(str(manifest["config_target"]))
    bounded(legacy_target).unlink()
    rollback_notes = rollback(root, home, manifest)
    results["delayed_rollback"] = {
        "human_agents_preserved": "Human edit after migration" in (home / ".codex/AGENTS.md").read_text(),
        "config_regular_fallback": (home / ".codex/config.toml").is_file() and not (home / ".codex/config.toml").is_symlink(),
        "config_hash_restored": digest(home / ".codex/config.toml") == manifest["config_hash"],
        "rules_hash_restored": digest(home / ".codex/rules/default.rules") == manifest["rules_hash"],
        "notes": rollback_notes,
    }

    write(RUN / "report.json", json.dumps(results, indent=2, sort_keys=True) + "\n")
    assert collision_errors and results["collision_preflight"]["config_still_symlink"]
    assert results["target_drift_preflight"]
    assert all(results[f"partial_{checkpoint}_rollback"]["config_symlink_restored"] for checkpoint in ("config", "rules"))
    assert all(results["complete_install"].values())
    assert results["delayed_rollback"]["human_agents_preserved"]
    assert results["delayed_rollback"]["config_regular_fallback"]
    assert results["delayed_rollback"]["config_hash_restored"]
    assert results["delayed_rollback"]["rules_hash_restored"]
    print(f"PASS: isolated migration and rollback simulation -> {RUN / 'report.json'}")


if __name__ == "__main__":
    main()
