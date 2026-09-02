#!/usr/bin/env python3
"""Manifest-only discovery, validation, and safe project-tool scaffolding."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

NAME_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
FIELDS = {"name", "description", "tags", "entrypoint", "test", "deterministic", "mutates"}
REQUIRED = FIELDS


class ToolError(RuntimeError):
    pass


def _within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _project_root(start: Path) -> Path:
    start = start.resolve(strict=True)
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return Path(result.stdout.rstrip("\n")).resolve(strict=True) if result.returncode == 0 else start


def _global_root() -> Path:
    return Path(__file__).resolve(strict=True).parents[1]


def _roots(project: Path) -> list[tuple[str, Path]]:
    return [("project", _project_root(project) / ".ai/tools"), ("global", _global_root())]


def _safe_child(package: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ToolError(f"{field} must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ToolError(f"{field} escapes the package")
    candidate = package / relative
    if candidate.is_symlink() or not candidate.is_file():
        raise ToolError(f"{field} must name a regular non-symlink file")
    resolved = candidate.resolve(strict=True)
    if not _within(resolved, package.resolve(strict=True)):
        raise ToolError(f"{field} escapes the package")
    return resolved


def validate_package(package: Path) -> dict[str, object]:
    if package.is_symlink() or not package.is_dir():
        raise ToolError("tool package must be a real directory, not a symlink")
    package = package.resolve(strict=True)
    manifest = package / "tool.toml"
    if manifest.is_symlink() or not manifest.is_file():
        raise ToolError("tool.toml must be a regular non-symlink file")
    with manifest.open("rb") as stream:
        data = tomllib.load(stream)
    unknown = set(data) - FIELDS
    missing = REQUIRED - set(data)
    if unknown:
        raise ToolError(f"unknown manifest fields: {','.join(sorted(unknown))}")
    if missing:
        raise ToolError(f"missing manifest fields: {','.join(sorted(missing))}")
    name = data["name"]
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or name != package.name:
        raise ToolError("name must be a safe lowercase package-matching slug")
    if not isinstance(data["description"], str) or not data["description"].strip():
        raise ToolError("description must be non-empty")
    tags = data["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ToolError("tags must be an array of non-empty strings")
    if type(data["deterministic"]) is not bool or type(data["mutates"]) is not bool:
        raise ToolError("deterministic and mutates must be booleans")
    _safe_child(package, data["entrypoint"], "entrypoint")
    _safe_child(package, data["test"], "test")
    return data


def discover(project: Path) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for scope, root in _roots(project):
        if not root.is_dir():
            continue
        for manifest in sorted(root.glob("*/tool.toml")):
            if manifest.parent.name == "_system":
                continue
            try:
                data = validate_package(manifest.parent)
                found.append({"scope": scope, **data, "status": "VALID"})
            except (OSError, ToolError, tomllib.TOMLDecodeError) as error:
                found.append({"scope": scope, "name": manifest.parent.name, "status": "INVALID", "error": str(error)})
    return found


def _select(project: Path, target: str) -> tuple[str, Path]:
    if ":" not in target:
        raise ToolError("target must be project:<name> or global:<name>")
    scope, name = target.split(":", 1)
    if scope not in {"project", "global"} or not NAME_RE.fullmatch(name):
        raise ToolError("invalid scope or tool name")
    roots = dict(_roots(project))
    package = roots[scope] / name
    root = roots[scope].resolve(strict=False)
    if package.is_symlink() or not _within(package.resolve(strict=False), root):
        raise ToolError("tool package escapes its scope")
    return scope, package


def _run_test(package: Path, test_path: str) -> dict[str, object]:
    test = _safe_child(package, test_path, "test")
    command = [sys.executable, str(test)] if test.suffix == ".py" else [str(test)]
    result = subprocess.run(command, cwd=package, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False)
    tail = "\n".join(result.stdout.splitlines()[-12:])
    return {"test_exit": result.returncode, "test_output_tail": tail}


def _ensure_scaffold_path(root: Path, package: Path) -> None:
    root = root.resolve(strict=True)
    if not _within(package.resolve(strict=False), root):
        raise ToolError("scaffold path escapes project root")
    cursor = root
    for part in package.relative_to(root).parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise ToolError(f"refusing symlinked scaffold component: {cursor}")


def scaffold(project: Path, name: str) -> dict[str, object]:
    if not NAME_RE.fullmatch(name):
        raise ToolError("invalid tool name")
    root = _project_root(project)
    package = root / ".ai/tools" / name
    _ensure_scaffold_path(root, package)
    if package.exists():
        raise ToolError("tool package already exists; refusing overwrite")
    package.mkdir(parents=True)
    files = {
        "tool.toml": f'name = "{name}"\ndescription = "Describe one narrow deterministic responsibility."\ntags = []\nentrypoint = "tool.py"\ntest = "test_tool.py"\ndeterministic = true\nmutates = false\n',
        "tool.py": '#!/usr/bin/env python3\n"""One narrow deterministic tool."""\n\nimport sys\n\n\ndef main() -> int:\n    return 0\n\n\nif __name__ == "__main__":\n    sys.exit(main())\n',
        "test_tool.py": '#!/usr/bin/env python3\nimport unittest\n\n\nclass ToolTest(unittest.TestCase):\n    def test_placeholder(self) -> None:\n        self.assertTrue(True)\n\n\nif __name__ == "__main__":\n    unittest.main()\n',
    }
    for filename, content in files.items():
        descriptor = os.open(package / filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
    return {"status": "CREATED", "scope": "project", "name": name, "path": str(package)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("keywords", nargs="+")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("target")
    validate_parser.add_argument("--run-test", action="store_true")
    scaffold_parser = subparsers.add_parser("scaffold")
    scaffold_parser.add_argument("name")
    args = parser.parse_args()
    project = Path(args.project)
    try:
        if args.command == "list":
            result: object = discover(project)
        elif args.command == "search":
            terms = [term.casefold() for term in args.keywords]
            result = [item for item in discover(project) if item.get("status") == "VALID" and all(term in " ".join([str(item.get("name", "")), str(item.get("description", "")), " ".join(item.get("tags", []))]).casefold() for term in terms)]
        elif args.command == "validate":
            scope, package = _select(project, args.target)
            data = validate_package(package)
            result = {"status": "VALID", "scope": scope, "name": data["name"]}
            if args.run_test:
                result.update(_run_test(package, str(data["test"])))
        else:
            result = scaffold(project, args.name)
    except (OSError, subprocess.SubprocessError, ToolError, tomllib.TOMLDecodeError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
