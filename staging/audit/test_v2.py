#!/usr/bin/env python3
"""Deterministic infrastructure and policy tests for the unified V2 candidate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
STAGING = ROOT / "staging"
CODEX = STAGING / "global/codex"
SKILL = STAGING / "global/agents/skills/project-bootstrap"
BLUEPRINT = STAGING / "blueprint/project"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


privacy = load_module("v2_privacy", SKILL / "scripts/project_privacy.py")
toolbox = load_module("v2_toolbox", CODEX / "toolbox/_system/toolbox.py")
migration = load_module("v2_migration", STAGING / "migration/v2_migrate.py")
quality_validate = load_module("validate_quality", STAGING / "audit/quality/validate_quality.py")
quality_gate = load_module("v2_quality_gate", STAGING / "audit/quality/evaluate_gate.py")


def git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(path), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def init_repo(path: Path) -> None:
    result = git(path, "init", "-q")
    if result.returncode:
        raise RuntimeError(result.stderr)


def make_tool(root: Path, name: str, description: str = "deterministic sample") -> Path:
    package = root / name
    package.mkdir(parents=True)
    (package / "tool.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
    (package / "test_tool.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
    (package / "tool.toml").write_text(
        f'name="{name}"\ndescription="{description}"\ntags=["sample"]\nentrypoint="tool.py"\ntest="test_tool.py"\ndeterministic=true\nmutates=false\n',
        encoding="utf-8",
    )
    return package


def make_quality_receipt(root: Path, control_config: Path) -> tuple[Path, str]:
    fixture_path = STAGING / "audit/quality/fixtures.json"
    fixtures = quality_validate.validate_fixtures(quality_validate.load(fixture_path))
    runs: list[dict[str, object]] = []
    sequence = 0
    for model in ("gpt-5.6-sol", "gpt-5.6-luna"):
        for fixture_id, fixture in fixtures.items():
            if fixture["role"] != "orchestrator":
                continue
            sequence += 1
            runs.append({"sequence": sequence, "model": model, "effort": "medium", "role": "orchestrator", "fixture": fixture_id, "result": "PASS", "acceptance_evidence": [{"criterion": criterion, "status": "PASS", "evidence": f"Observed passing outcome for {criterion}."} for criterion in fixture["acceptance"]], "rework_count": 0, "escalation_count": 0, "model_calls": 1, "tokens": "UNKNOWN", "cost": "UNKNOWN", "latency": "UNKNOWN"})
    results = root / "quality-results.json"
    results.write_text(json.dumps({"version": 1, "runs": runs}), encoding="utf-8")
    receipt = root / "gate-receipt.json"
    command = [sys.executable, "-B", str(STAGING / "audit/quality/evaluate_gate.py"), str(results), "--fixtures", str(fixture_path), "--control-config", str(control_config), "--candidate-config", str(CODEX / "config.luna-candidate.toml"), "--receipt", str(receipt)]
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    return receipt, hashlib.sha256(receipt.read_bytes()).hexdigest()


class GitPrivacyTests(unittest.TestCase):
    def test_a_empty_git_repo_and_d_existing_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            exclude = root / git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
            exclude.write_text("# preserve me\n*.private\n", encoding="utf-8")
            self.assertEqual(privacy.apply_privacy(root)["status"], "UPDATED")
            content = exclude.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# preserve me\n*.private\n"))
            self.assertEqual(privacy.apply_privacy(root)["status"], "UNCHANGED")

    def test_b_tracked_agents_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            agents = root / "AGENTS.md"
            agents.write_text("shared instructions\n", encoding="utf-8")
            git(root, "add", "AGENTS.md")
            before = agents.read_bytes()
            privacy.apply_privacy(root)
            self.assertEqual(agents.read_bytes(), before)

    def test_c_tracked_private_paths_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            for name in (".ai", ".codex", ".agents"):
                (root / name).mkdir()
                (root / name / "tracked").write_text(name, encoding="utf-8")
                git(root, "add", f"{name}/tracked")
            report = privacy.inspect_project(root)
            self.assertEqual(report["status"], "CONFLICT")
            self.assertEqual(len(report["tracked_private_paths"]), 3)

    def test_e_linked_worktree_uses_resolved_git_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "main repo"
            worktree = Path(directory) / "linked worktree"
            base.mkdir()
            init_repo(base)
            (base / "seed").write_text("seed", encoding="utf-8")
            git(base, "add", "seed")
            commit = git(base, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "seed")
            self.assertEqual(commit.returncode, 0, commit.stderr)
            added = git(base, "worktree", "add", "-qb", "fixture-branch", str(worktree))
            self.assertEqual(added.returncode, 0, added.stderr)
            report = privacy.apply_privacy(worktree)
            expected = git(worktree, "rev-parse", "--git-path", "info/exclude").stdout.strip()
            expected_path = Path(expected) if Path(expected).is_absolute() else worktree / expected
            self.assertEqual(Path(report["exclude"]), expected_path.resolve())

    def test_f_dirty_repo_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            (root / "dirty.txt").write_text("human work", encoding="utf-8")
            before = git(root, "status", "--short").stdout
            privacy.apply_privacy(root)
            self.assertEqual(git(root, "status", "--short").stdout, before)

    def test_g_non_git_and_malformed_git_are_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(privacy.inspect_project(root)["status"], "NON_GIT")
            (root / ".git").write_text("malformed", encoding="utf-8")
            self.assertEqual(privacy.inspect_project(root)["status"], "NON_GIT")

    def test_h_existing_untracked_ai_is_not_modified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            router = root / ".ai/PROJECT.md"
            router.parent.mkdir()
            router.write_text("private human work", encoding="utf-8")
            before = router.read_bytes()
            privacy.apply_privacy(root)
            self.assertEqual(router.read_bytes(), before)

    def test_repository_path_with_spaces_and_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo with spaces"
            child = root / "nested path"
            child.mkdir(parents=True)
            init_repo(root)
            self.assertEqual(Path(privacy.inspect_project(child)["root"]), root.resolve())

    def test_nested_repository_resolves_inner_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outer = Path(directory)
            inner = outer / "nested"
            inner.mkdir()
            init_repo(outer)
            init_repo(inner)
            self.assertEqual(Path(privacy.inspect_project(inner)["root"]), inner.resolve())

    def test_symlinked_exclude_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            exclude = root / git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
            outside = root / "outside-exclude"
            outside.write_text("outside", encoding="utf-8")
            exclude.unlink()
            exclude.symlink_to(outside)
            with self.assertRaises(privacy.PrivacyError):
                privacy.inspect_project(root)

    def test_read_only_exclude_directory_fails_without_content_loss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            exclude = root / git(root, "rev-parse", "--git-path", "info/exclude").stdout.strip()
            before = exclude.read_bytes()
            original_mode = exclude.parent.stat().st_mode & 0o777
            exclude.parent.chmod(0o500)
            try:
                with self.assertRaises(OSError):
                    privacy.apply_privacy(root)
            finally:
                exclude.parent.chmod(original_mode)
            self.assertEqual(exclude.read_bytes(), before)


class ToolboxTests(unittest.TestCase):
    def test_j_k_l_project_global_discovery_and_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as project_dir, tempfile.TemporaryDirectory() as global_dir:
            project = Path(project_dir)
            global_root = Path(global_dir)
            make_tool(project / ".ai/tools", "same-name", "project semantics")
            make_tool(global_root, "same-name", "global semantics")
            make_tool(global_root, "global-only")
            with mock.patch.object(toolbox, "_global_root", return_value=global_root):
                found = toolbox.discover(project)
            self.assertEqual([(item["scope"], item["name"]) for item in found], [("project", "same-name"), ("global", "global-only"), ("global", "same-name")])

    def test_m_invalid_toml_and_n_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "invalid"
            invalid.mkdir()
            (invalid / "tool.toml").write_text("not = [toml", encoding="utf-8")
            with self.assertRaises(tomllib.TOMLDecodeError):
                toolbox.validate_package(invalid)
            package = make_tool(root, "traversal")
            text = (package / "tool.toml").read_text(encoding="utf-8").replace('entrypoint="tool.py"', 'entrypoint="../tool.py"')
            (package / "tool.toml").write_text(text, encoding="utf-8")
            with self.assertRaises(toolbox.ToolError):
                toolbox.validate_package(package)

    def test_o_symlinked_package_and_implementation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = make_tool(root, "real-tool")
            link = root / "linked-tool"
            link.symlink_to(real, target_is_directory=True)
            with self.assertRaises(toolbox.ToolError):
                toolbox.validate_package(link)
            external = root / "external.py"
            external.write_text("", encoding="utf-8")
            (real / "tool.py").unlink()
            (real / "tool.py").symlink_to(external)
            with self.assertRaises(toolbox.ToolError):
                toolbox.validate_package(real)

    def test_p_scaffold_overwrite_and_malicious_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            toolbox.scaffold(root, "safe-tool")
            with self.assertRaises(toolbox.ToolError):
                toolbox.scaffold(root, "safe-tool")
            for name in ("bad;touch-x", "bad\nname", "../escape", "UPPER"):
                with self.assertRaises(toolbox.ToolError):
                    toolbox.scaffold(root, name)
            self.assertFalse((root.parent / "escape").exists())

    def test_project_scaffold_cannot_write_global(self) -> None:
        with tempfile.TemporaryDirectory() as project_dir, tempfile.TemporaryDirectory() as global_dir:
            project = Path(project_dir)
            global_root = Path(global_dir)
            with mock.patch.object(toolbox, "_global_root", return_value=global_root):
                toolbox.scaffold(project, "local-only")
            self.assertTrue((project / ".ai/tools/local-only/tool.toml").is_file())
            self.assertEqual(list(global_root.iterdir()), [])

    def test_discovery_does_not_execute_tool(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            marker = project / "executed"
            package = make_tool(project / ".ai/tools", "no-execute")
            (package / "tool.py").write_text(f'from pathlib import Path\nPath({str(marker)!r}).write_text("bad")\n', encoding="utf-8")
            toolbox.discover(project)
            self.assertFalse(marker.exists())


class StaticPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = {item["id"]: item for item in json.loads((STAGING / "audit/quality/fixtures.json").read_text(encoding="utf-8"))["fixtures"]}

    def test_i_q_r_s_adoption_and_extraction_outcomes(self) -> None:
        workflow = (SKILL / "references/bootstrap-workflow.md").read_text(encoding="utf-8")
        self.assertIn("MIGRATION_PROPOSED", workflow)
        self.assertEqual(self.fixtures["tool-one-off"]["expected_path"], "direct")
        self.assertIn("extract-or-reuse", self.fixtures["tool-repeat"]["expected_path"])
        self.assertEqual(self.fixtures["tool-reasoning-repeat"]["expected_path"], "reasoning-not-tool")

    def test_t_context_budgets(self) -> None:
        self.assertLessEqual(len((CODEX / "AGENTS.md").read_text(encoding="utf-8").split()), 300)
        routing_words = len((CODEX / "routing/MODEL_ROUTING.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(routing_words, 500)
        self.assertLessEqual(routing_words, 750)
        self.assertLessEqual(len((BLUEPRINT / ".ai/PROJECT.md.template").read_text(encoding="utf-8").split()), 200)
        self.assertLessEqual(len((BLUEPRINT / ".ai/tools/example/tool.toml.template").read_text(encoding="utf-8").split()), 120)

    def test_u_v_w_x_agent_catalog_and_pins(self) -> None:
        expected = {"researcher", "quick-implementer", "implementer", "validator", "planner", "reviewer"}
        files = {path.stem for path in (CODEX / "agents").glob("*.toml")}
        self.assertEqual(files, expected)
        configs = {}
        for path in (CODEX / "agents").glob("*.toml"):
            with path.open("rb") as stream:
                data = tomllib.load(stream)
            self.assertEqual(data["name"], path.stem)
            for field in ("model", "model_reasoning_effort", "sandbox_mode", "description"):
                self.assertIn(field, data)
            configs[path.stem] = data
        self.assertEqual((configs["planner"]["model"], configs["planner"]["model_reasoning_effort"]), ("gpt-5.6-sol", "medium"))
        self.assertEqual((configs["reviewer"]["model"], configs["reviewer"]["model_reasoning_effort"]), ("gpt-5.6-sol", "low"))
        self.assertNotIn("commit-pusher", files)

    def test_y_no_external_review_dependency(self) -> None:
        reviewer = (CODEX / "agents/reviewer.toml").read_text(encoding="utf-8")
        self.assertNotIn("$code-review", reviewer)

    def test_z_no_automatic_multi_agent_v2(self) -> None:
        self.assertNotIn("multi_agent_v2", (CODEX / "config.toml").read_text(encoding="utf-8"))
        self.assertNotIn("multi_agent_v2", (SKILL / "SKILL.md").read_text(encoding="utf-8"))
        config = tomllib.loads((CODEX / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual((config["model"], config["model_reasoning_effort"]), ("gpt-5.6-sol", "medium"))

    def test_aa_blueprint_parity_and_self_containment(self) -> None:
        packaged = SKILL / "assets/project"
        left = {path.relative_to(BLUEPRINT): path.read_bytes() for path in BLUEPRINT.rglob("*") if path.is_file()}
        right = {path.relative_to(packaged): path.read_bytes() for path in packaged.rglob("*") if path.is_file()}
        self.assertEqual(left, right)
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for relative in ("assets/project", "references/bootstrap-workflow.md", "references/private-workspace.md", "references/operating-workflows.md", "references/tooling.md", "references/model-routing.md", "scripts/project_privacy.py"):
            self.assertIn(relative, skill if relative != "scripts/project_privacy.py" else (SKILL / "references/private-workspace.md").read_text(encoding="utf-8"))
            self.assertTrue((SKILL / relative).exists())

    def test_ab_routing_not_always_imported(self) -> None:
        global_agents = (CODEX / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("routing/MODEL_ROUTING.md", global_agents)
        self.assertNotIn("@", global_agents)

    def test_ac_private_cannot_override_shared_truth(self) -> None:
        combined = (CODEX / "AGENTS.md").read_text(encoding="utf-8") + (BLUEPRINT / ".ai/PROJECT.md.template").read_text(encoding="utf-8")
        self.assertIn("cannot silently override shared truth", combined)
        self.assertIn("Tracked project instructions", combined)

    def test_ad_quality_precedes_cost(self) -> None:
        routing = (CODEX / "routing/MODEL_ROUTING.md").read_text(encoding="utf-8").lower()
        self.assertLess(routing.index("correctness"), routing.index("cost"))
        self.assertIn("price alone never establishes sufficiency", routing)

    def test_quality_token_failure_cases_exist_and_fail_loudly(self) -> None:
        expected = {
            "quality-required-context": "include-requirement",
            "quality-security-context": "include-security-constraint",
            "quality-approval-context": "include-human-gate",
            "quality-shared-authority": "tracked-truth-and-conflict",
            "quality-wrong-tool": "reject-tool",
            "quality-cheap-architecture": "planner-sol-medium",
            "quality-required-validation": "detached-validation",
            "quality-required-review": "reviewer-sol-low",
        }
        self.assertEqual({key: self.fixtures[key]["expected_path"] for key in expected}, expected)

    def test_validator_detects_source_mutation_contract(self) -> None:
        validator = (CODEX / "agents/validator.toml").read_text(encoding="utf-8")
        self.assertIn("capture repository status", validator.lower())
        self.assertIn("unexpected tracked or untracked changes", validator)
        self.assertIn("Do not edit source", validator)


class MigrationTests(unittest.TestCase):
    def test_v2_install_preserves_config_and_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex_home = root / ".codex"
            agents_home = root / ".agents"
            codex_home.mkdir()
            (agents_home / "skills/project-bootstrap").mkdir(parents=True)
            config = codex_home / "config.toml"
            config.write_text('model = "gpt-5.6-sol"\nmodel_reasoning_effort = "medium"\n', encoding="utf-8")
            unrelated = agents_home / "skills/unrelated/SKILL.md"
            unrelated.parent.mkdir()
            unrelated.write_text("human skill", encoding="utf-8")
            old = agents_home / "skills/project-bootstrap/old.txt"
            old.write_text("old", encoding="utf-8")
            config_before = config.read_bytes()
            unrelated_before = unrelated.read_bytes()
            baseline = migration.snapshot(codex_home, agents_home)
            backup = root / "backup"
            manifest = migration.install(baseline, codex_home, agents_home, backup)
            self.assertEqual(config.read_bytes(), config_before)
            self.assertEqual(unrelated.read_bytes(), unrelated_before)
            self.assertFalse(old.exists())
            self.assertEqual(tomllib.loads((codex_home / "agents/planner.toml").read_text())["model"], "gpt-5.6-sol")
            migration.rollback(manifest, codex_home, agents_home, backup)
            self.assertEqual(config.read_bytes(), config_before)
            self.assertEqual(unrelated.read_bytes(), unrelated_before)
            self.assertTrue(old.exists())
            self.assertFalse((codex_home / "routing/MODEL_ROUTING.md").exists())
            self.assertFalse((codex_home / "routing").exists())

    def test_prepared_file_action_is_recoverable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex_home, agents_home = root / ".codex", root / ".agents"
            codex_home.mkdir()
            agents_home.mkdir()
            baseline = migration.snapshot(codex_home, agents_home)
            backup = root / "backup"
            backup.mkdir()
            manifest = {"version": 2, "baseline": baseline, "journal": [], "directories": []}
            manifest_path = backup / "manifest.json"
            migration.persist_manifest(manifest_path, manifest)
            key = sorted(baseline["files"])[0]
            source = migration.candidate_map()[key]
            target = migration.target_for(key, codex_home, agents_home)
            selected_root = codex_home if key.startswith("codex/") else agents_home
            migration.ensure_parent(target, selected_root, manifest, manifest_path)
            manifest["journal"].append({"key": key, "action": "write", "installed_hash": migration.digest(source), "state": "PREPARED"})
            migration.persist_manifest(manifest_path, manifest)
            migration.atomic_copy(source, target)
            command = [sys.executable, "-B", str(STAGING / "migration/v2_migrate.py"), "rollback", "--codex-home", str(codex_home), "--agents-home", str(agents_home), "--backup", str(backup)]
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE, check=False)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertFalse(target.exists())

    def test_rollback_rejects_different_roots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex_home, agents_home = root / "a/.codex", root / "a/.agents"
            codex_home.mkdir(parents=True)
            agents_home.mkdir(parents=True)
            baseline = migration.snapshot(codex_home, agents_home)
            backup = root / "backup"
            manifest = migration.install(baseline, codex_home, agents_home, backup)
            other_codex, other_agents = root / "b/.codex", root / "b/.agents"
            other_codex.mkdir(parents=True)
            other_agents.mkdir(parents=True)
            with self.assertRaises(migration.MigrationError):
                migration.rollback(manifest, other_codex, other_agents, backup)

    def test_separate_parent_migration_requires_gate(self) -> None:
        script = STAGING / "migration/migrate_parent_model.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.toml"
            config.write_text('model = "gpt-5.6-sol"\nmodel_reasoning_effort = "medium"\n', encoding="utf-8")
            expected = hashlib.sha256(config.read_bytes()).hexdigest()
            journal = root / "migration.json"
            result = subprocess.run([sys.executable, "-B", str(script), "apply", "--config", str(config), "--expected-hash", expected, "--migration-journal", str(journal)], text=True, stdout=subprocess.PIPE, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("gpt-5.6-sol", config.read_text(encoding="utf-8"))

    def test_separate_parent_migration_applies_and_rolls_back(self) -> None:
        script = STAGING / "migration/migrate_parent_model.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.toml"
            original = 'model = "gpt-5.6-sol"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "workspace-write"\n'
            config.write_text(original, encoding="utf-8")
            expected = hashlib.sha256(config.read_bytes()).hexdigest()
            gate, gate_hash = make_quality_receipt(root, config)
            journal = root / "migration.json"
            apply_result = subprocess.run([sys.executable, "-B", str(script), "apply", "--config", str(config), "--expected-hash", expected, "--gate-receipt", str(gate), "--approved-gate-hash", gate_hash, "--migration-journal", str(journal)], text=True, stdout=subprocess.PIPE, check=False)
            self.assertEqual(apply_result.returncode, 0, apply_result.stdout)
            self.assertIn("gpt-5.6-luna", config.read_text(encoding="utf-8"))
            migration_record = json.loads(journal.read_text(encoding="utf-8"))
            migration_record["state"] = "PREPARED"
            journal.write_text(json.dumps(migration_record), encoding="utf-8")
            rollback_result = subprocess.run([sys.executable, "-B", str(script), "rollback", "--config", str(config), "--migration-journal", str(journal)], text=True, stdout=subprocess.PIPE, check=False)
            self.assertEqual(rollback_result.returncode, 0, rollback_result.stdout)
            self.assertEqual(config.read_text(encoding="utf-8"), original)

    def test_parent_migration_rejects_drifted_gate_evidence(self) -> None:
        script = STAGING / "migration/migrate_parent_model.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.toml"
            config.write_text('model = "gpt-5.6-sol"\nmodel_reasoning_effort = "medium"\n', encoding="utf-8")
            expected = hashlib.sha256(config.read_bytes()).hexdigest()
            gate, gate_hash = make_quality_receipt(root, config)
            receipt_data = json.loads(gate.read_text(encoding="utf-8"))
            Path(receipt_data["results_path"]).write_text('{"version":1,"runs":[]}', encoding="utf-8")
            command = [sys.executable, "-B", str(script), "apply", "--config", str(config), "--expected-hash", expected, "--gate-receipt", str(gate), "--approved-gate-hash", gate_hash, "--migration-journal", str(root / "migration.json")]
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(hashlib.sha256(config.read_bytes()).hexdigest(), expected)

    def test_migration_rejects_symlinked_target_component(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            codex_home = root / ".codex"
            agents_home = root / ".agents"
            outside = root / "outside"
            codex_home.mkdir()
            agents_home.mkdir()
            outside.mkdir()
            (codex_home / "agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(migration.MigrationError):
                migration.snapshot(codex_home, agents_home)


class QualityGateTests(unittest.TestCase):
    def test_safety_regression_blocks_luna_parent(self) -> None:
        fixture_data = quality_validate.load(STAGING / "audit/quality/fixtures.json")
        fixtures = quality_validate.validate_fixtures(fixture_data)
        orch = sorted(identifier for identifier in fixtures if identifier.startswith("orch-"))
        runs = []
        sequence = 0
        for fixture in orch:
            sequence += 1
            runs.append(self._run(sequence, fixtures[fixture], "gpt-5.6-sol", "PASS"))
        for fixture in orch:
            sequence += 1
            result = "SAFETY_REGRESSION" if fixture == "orch-destructive" else "PASS"
            runs.append(self._run(sequence, fixtures[fixture], "gpt-5.6-luna", result))
        decision = quality_gate.evaluate({"version": 1, "runs": runs}, fixtures)
        self.assertEqual(decision["decision"], "BLOCKED")
        self.assertIn("safety regression", decision["blockers"])

    def test_placeholder_evidence_cannot_authorize(self) -> None:
        fixtures = quality_validate.validate_fixtures(quality_validate.load(STAGING / "audit/quality/fixtures.json"))
        run = self._run(1, fixtures["orch-factual"], "gpt-5.6-sol", "PASS")
        run["acceptance_evidence"][0]["evidence"] = "NOT_RUN"
        with self.assertRaises(ValueError):
            quality_validate.validate_results({"version": 1, "runs": [run]}, fixtures)

    def test_failed_control_blocks_candidate(self) -> None:
        fixtures = quality_validate.validate_fixtures(quality_validate.load(STAGING / "audit/quality/fixtures.json"))
        orch = [fixture for fixture in fixtures.values() if fixture["role"] == "orchestrator"]
        runs = []
        sequence = 0
        for model in ("gpt-5.6-sol", "gpt-5.6-luna"):
            for fixture in orch:
                sequence += 1
                result = "QUALITY_REGRESSION" if model.endswith("sol") and fixture["id"] == "orch-factual" else "PASS"
                runs.append(self._run(sequence, fixture, model, result))
        decision = quality_gate.evaluate({"version": 1, "runs": runs}, fixtures)
        self.assertEqual(decision["decision"], "BLOCKED")
        self.assertIn("control outcome is not passing", decision["blockers"])

    @staticmethod
    def _run(sequence: int, fixture: dict[str, object], model: str, result: str) -> dict[str, object]:
        evidence_status = "PASS" if result in {"PASS", "PASS_WITH_MINOR_DIFFERENCE"} else ("UNKNOWN" if result == "INCONCLUSIVE" else "FAIL")
        return {
            "sequence": sequence,
            "model": model,
            "effort": "medium",
            "role": "orchestrator",
            "fixture": fixture["id"],
            "result": result,
            "acceptance_evidence": [{"criterion": criterion, "status": evidence_status if index == 0 else "PASS", "evidence": f"Observed {evidence_status.lower()} outcome for {criterion}."} for index, criterion in enumerate(fixture["acceptance"])],
            "rework_count": "UNKNOWN",
            "escalation_count": "UNKNOWN",
            "model_calls": "UNKNOWN",
            "tokens": "UNKNOWN",
            "cost": "UNKNOWN",
            "latency": "UNKNOWN",
        }


if __name__ == "__main__":
    unittest.main(verbosity=2)
