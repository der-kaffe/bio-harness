#!/usr/bin/env python3
"""Focused tests for the toolbox utility."""

from pathlib import Path
import tempfile
import unittest
from unittest import mock

import toolbox


class ToolboxTests(unittest.TestCase):
    def test_scaffold_validate_and_refuse_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            created = toolbox.scaffold(root, "sample-tool")
            self.assertEqual(created["status"], "CREATED")
            package = root / ".ai/tools/sample-tool"
            self.assertEqual(toolbox.validate_package(package)["name"], "sample-tool")
            with self.assertRaises(toolbox.ToolError):
                toolbox.scaffold(root, "sample-tool")

    def test_rejects_traversal_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "bad-tool"
            package.mkdir()
            (package / "test_tool.py").write_text("", encoding="utf-8")
            (package / "tool.toml").write_text(
                'name="bad-tool"\ndescription="bad"\ntags=[]\nentrypoint="../escape.py"\ntest="test_tool.py"\ndeterministic=true\nmutates=false\n',
                encoding="utf-8",
            )
            with self.assertRaises(toolbox.ToolError):
                toolbox.validate_package(package)

            target = root / "outside.py"
            target.write_text("", encoding="utf-8")
            (package / "tool.py").symlink_to(target)
            (package / "tool.toml").write_text(
                'name="bad-tool"\ndescription="bad"\ntags=[]\nentrypoint="tool.py"\ntest="test_tool.py"\ndeterministic=true\nmutates=false\n',
                encoding="utf-8",
            )
            with self.assertRaises(toolbox.ToolError):
                toolbox.validate_package(package)

    def test_project_precedes_same_name_global(self) -> None:
        with tempfile.TemporaryDirectory() as project_directory, tempfile.TemporaryDirectory() as global_directory:
            project = Path(project_directory)
            global_root = Path(global_directory)
            toolbox.scaffold(project, "shared-name")
            global_package = global_root / "shared-name"
            global_package.mkdir()
            for source in (project / ".ai/tools/shared-name").iterdir():
                (global_package / source.name).write_bytes(source.read_bytes())
            with mock.patch.object(toolbox, "_global_root", return_value=global_root):
                found = toolbox.discover(project)
            self.assertEqual([item["scope"] for item in found], ["project", "global"])


if __name__ == "__main__":
    unittest.main()
