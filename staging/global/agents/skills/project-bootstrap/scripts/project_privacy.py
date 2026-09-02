#!/usr/bin/env python3
"""Inspect or establish repository-local exclusions for private AI paths."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile

PATTERNS = ("/.ai/", "/.codex/", "/.agents/")
TRACKED_PATHS = (".ai", ".codex", ".agents")


class PrivacyError(RuntimeError):
    pass


def _git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _resolved_git_path(root: Path, *args: str) -> Path:
    result = _git(root, *args)
    if result.returncode:
        raise PrivacyError(result.stderr.strip() or "git path resolution failed")
    value = result.stdout.rstrip("\n")
    if not value or any(ord(char) < 32 for char in value):
        raise PrivacyError("git returned an unsafe path")
    candidate = Path(value)
    return candidate if candidate.is_absolute() else root / candidate


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def inspect_project(start: Path) -> dict[str, object]:
    start = start.resolve(strict=True)
    top = _git(start, "rev-parse", "--show-toplevel")
    if top.returncode:
        return {"status": "NON_GIT", "path": str(start)}
    root = Path(top.stdout.rstrip("\n")).resolve(strict=True)
    tracked_result = _git(root, "ls-files", "-z", "--", *TRACKED_PATHS)
    if tracked_result.returncode:
        raise PrivacyError(tracked_result.stderr.strip() or "cannot inspect tracked paths")
    tracked = sorted(item for item in tracked_result.stdout.split("\0") if item)

    exclude_raw = _resolved_git_path(root, "rev-parse", "--git-path", "info/exclude")
    common_raw = _resolved_git_path(root, "rev-parse", "--git-common-dir")
    common = common_raw.resolve(strict=True)
    exclude = exclude_raw.resolve(strict=False)
    if not _is_within(exclude, common):
        raise PrivacyError("resolved exclude path escapes the Git common directory")
    if exclude_raw.is_symlink() or exclude_raw.parent.is_symlink():
        raise PrivacyError("refusing symlinked Git exclude path")

    relative = exclude.relative_to(common)
    cursor = common
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise PrivacyError(f"refusing symlinked Git exclude component: {cursor}")

    content = exclude.read_bytes() if exclude.exists() else b""
    existing = {line.decode("utf-8", "strict") for line in content.splitlines()}
    missing = [pattern for pattern in PATTERNS if pattern not in existing]
    return {
        "status": "CONFLICT" if tracked else "READY",
        "root": str(root),
        "exclude": str(exclude),
        "tracked_private_paths": tracked,
        "missing_patterns": missing,
    }


def apply_privacy(start: Path) -> dict[str, object]:
    report = inspect_project(start)
    if report["status"] == "NON_GIT":
        return report
    if report["status"] == "CONFLICT":
        raise PrivacyError("tracked private-looking paths must be resolved by a human")
    missing = list(report["missing_patterns"])
    if not missing:
        report["status"] = "UNCHANGED"
        return report

    exclude = Path(str(report["exclude"]))
    exclude.parent.mkdir(parents=True, exist_ok=True)
    if exclude.is_symlink():
        raise PrivacyError("refusing symlinked exclude file")
    before = exclude.read_bytes() if exclude.exists() else b""
    mode = stat.S_IMODE(exclude.stat().st_mode) if exclude.exists() else 0o644
    addition = b""
    if before and not before.endswith(b"\n"):
        addition += b"\n"
    addition += b"# Codex private workspace (local only)\n"
    addition += "".join(f"{pattern}\n" for pattern in missing).encode("utf-8")

    handle, temp_name = tempfile.mkstemp(prefix=".exclude-v2-", dir=exclude.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(before + addition)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp_name, mode)
        if exclude.is_symlink():
            raise PrivacyError("exclude target changed to a symlink")
        os.replace(temp_name, exclude)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    report["status"] = "UPDATED"
    report["added_patterns"] = missing
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("inspect", "apply"))
    parser.add_argument("--path", default=".")
    args = parser.parse_args()
    try:
        report = inspect_project(Path(args.path)) if args.action == "inspect" else apply_privacy(Path(args.path))
    except (OSError, UnicodeError, PrivacyError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] not in {"CONFLICT", "ERROR"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
