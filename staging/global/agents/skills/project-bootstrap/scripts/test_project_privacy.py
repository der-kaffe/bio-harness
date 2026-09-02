#!/usr/bin/env python3
"""Focused tests for repository-local privacy handling."""

from pathlib import Path
import subprocess
import tempfile
import unittest

import project_privacy


def git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(path), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


class PrivacyTests(unittest.TestCase):
    def test_non_git_is_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(project_privacy.inspect_project(root)["status"], "NON_GIT")
            self.assertFalse((root / ".git").exists())

    def test_preserves_existing_content_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(git(root, "init", "-q").returncode, 0)
            exclude = Path(git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip())
            if not exclude.is_absolute():
                exclude = root / exclude
            exclude.write_text("# existing\n*.local\n", encoding="utf-8")
            first = project_privacy.apply_privacy(root)
            second = project_privacy.apply_privacy(root)
            content = exclude.read_text(encoding="utf-8")
            self.assertEqual(first["status"], "UPDATED")
            self.assertEqual(second["status"], "UNCHANGED")
            self.assertTrue(content.startswith("# existing\n*.local\n"))
            for pattern in project_privacy.PATTERNS:
                self.assertEqual(content.splitlines().count(pattern), 1)

    def test_tracked_private_path_is_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git(root, "init", "-q")
            (root / ".ai").mkdir()
            (root / ".ai/PROJECT.md").write_text("tracked", encoding="utf-8")
            git(root, "add", ".ai/PROJECT.md")
            report = project_privacy.inspect_project(root)
            self.assertEqual(report["status"], "CONFLICT")
            with self.assertRaises(project_privacy.PrivacyError):
                project_privacy.apply_privacy(root)

    def test_invocation_from_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git(root, "init", "-q")
            child = root / "path with spaces/sub"
            child.mkdir(parents=True)
            self.assertEqual(Path(project_privacy.inspect_project(child)["root"]), root.resolve())


if __name__ == "__main__":
    unittest.main()
