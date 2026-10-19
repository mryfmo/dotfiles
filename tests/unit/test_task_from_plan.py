"""Exercise generation, non-execution and output confinement on committed fixture plans."""

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

from tests.unit.test_task_consistency_c11_c15 import TRACE, RepositoryTest, uv_command

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts/orchestrator/task-from-plan.py"
PROGRAMS = ".orchestration/plans/024-design-programs.md"
WAVES = ".orchestration/plans/024-omp-cutover-and-corrective-order.md"
LEGACY = {
    ".orchestration/tasks/dotfiles-T133-result-precheck-a01.md": "---\nformat: 2\nallowed_files: []\n---\n# poisoned sibling\n",
    ".orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md": "---\nformat: 2\nallowed_files: []\n---\n# poisoned completion\n",
}
FILES = {
    ".orchestration/plans/024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    "| P1-1 demo generator | B1 a demo purpose | (1) で作る | the generated task passes the consistency check |\n",
    PROGRAMS: "# programs\n\n**(1) `scripts/demo.sh`**: prints `printf known-output` and checks `sh -c 'exit 3'`.\n\n"
    "**(2) other**: unused\n",
    ".orchestration/plans/024-design-quality.md": "| id | row |\n| --- | --- |\n| Q-A 境界 | P1-1 のタスクは security: true |\n",
    WAVES: "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-1 demo | P1-2 sibling |\n\n## 7. STOP\n",
    "scripts/demo.sh": "#!/usr/bin/env bash\necho demo\n",
    "tests/unit/test_demo.py": "# exercises scripts/demo.sh\n",
    "Makefile": "unit-test:\n\t@true\n",
    **LEGACY,
}
LOAD = "import json, sys, yaml; print(json.dumps(yaml.safe_load(sys.stdin.read().split('\\n---\\n', 1)[0].lstrip('-\\n'))))"


class TaskFromPlanTest(RepositoryTest):
    def test_the_generator_never_executes_a_plan_command(self):
        marker = self.temp / "ran"
        template = self.production / "task-template.md"
        template.write_text(template.read_text().replace("check:\n", f"check:\n  - touch {marker}\n"))
        self.commit(
            {
                PROGRAMS: FILES[PROGRAMS].replace("`printf known-output`", f"`touch {marker}`"),
                "Makefile": f"unit-test:\n\ttouch {marker}\n",
            },
            "marker commands",
        )
        code, out, front, text = self.generate(trace=True)
        self.assertFalse(marker.exists(), out)
        self.assertEqual(code, 0, out)
        self.assertTrue(all(p["claim"].startswith("verify:") and "output" not in p for p in front["premises"]))
        self.assertIn("not run", text)
        self.assertIn("C14: not run (no trusted sha)", out)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)
        for call in map(json.loads, (self.temp / "trace.jsonl").read_text().splitlines()):
            self.assertNotIn("worktree", call["argv"])
            self.assertNotIn("--premises-sha", call["argv"])

    def test_the_generator_refuses_a_symlinked_or_existing_output(self):
        folder = self.repo / ".orchestration/tasks"
        target = self.temp / "target.md"
        target.write_text("unchanged")
        for kind in ("ordinary", "inside", "outside", "dangling", "parent", "direct"):
            out = folder / "dotfiles-T9-new-a01.md"
            if kind == "ordinary":
                out.write_text("unchanged")
            elif kind == "parent":
                (folder / "linked").symlink_to(self.temp, target_is_directory=True)
                out = folder / "linked/dotfiles-T9-new-a01.md"
            elif kind == "direct":
                out = self.temp / "outside.md"
            else:
                out.symlink_to(
                    folder / "missing"
                    if kind == "dangling"
                    else target
                    if kind == "outside"
                    else folder / "dotfiles-T133-result-precheck-a01.md"
                )
            code, text, _, _ = self.generate(out=str(out))
            self.assertNotEqual(code, 0, (kind, text))
            self.assertEqual(target.read_text(), "unchanged")
            if kind not in ("parent", "direct"):
                out.unlink()
        self.assertEqual(self.generate(out=str(folder / "dotfiles-T9-fresh-a01.md"))[0], 0)

    def run_three(self, trace=False, worker_binding=None):
        from tests.unit.test_task_consistency_c11_c15 import BASE

        task = self.repo / ".orchestration/tasks/dotfiles-T9-base-a01.md"
        task.write_text(BASE)
        run = uv_command()
        for name, args in (
            ("task-from-plan.py", ["P1-1", "--out", ".orchestration/tasks/new.md"]),
            ("plan-check.py", ["--root", str(self.repo), "--invariants"]),
            ("task-consistency-check.py", ["--root", str(self.repo), str(task)]),
        ):
            command = (
                [*run, "-c", TRACE, str(self.temp / "trace.jsonl"), str(self.production / name), *args]
                if trace
                else [*run, str(self.production / name), *args]
            )
            if worker_binding is not None:
                binding = "import importlib.util,sys,pathlib;s,p=sys.argv[1:3];spec=importlib.util.spec_from_file_location('m',s);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);getattr(m,'checker',m).executable=lambda name:pathlib.Path(p);sys.argv=[s,*sys.argv[3:]];sys.exit(m.main())"
                command = [*run, "-c", binding, str(self.production / name), str(worker_binding), *args]
            result = subprocess.run(command, cwd=self.repo, env=self.env, capture_output=True, text=True, check=False)
            yield name, result.returncode, result.stdout + result.stderr

    def test_all_three_scripts_refuse_repository_local_filters_before_status_or_diff(self):
        marker = self.temp / "filter-ran"
        self.commit({".gitattributes": f"{PROGRAMS} filter=probe\n"}, "filter selection")
        for location in ("local", "worktree", "included"):
            if location == "worktree":
                self.git("config", "extensions.worktreeConfig", "true")
            if location == "included":
                config = self.temp / "included.config"
                config.write_text(f'[filter "probe"]\n clean = touch {marker}\n')
                self.git("config", "include.path", str(config))
            else:
                self.git("config", "--" + location, "filter.probe.clean", f"touch {marker}")
            os.utime(self.repo / PROGRAMS, None)
            for name, code, out in self.run_three():
                self.assertNotEqual(code, 0, (name, out))
                self.assertIn("filter.probe.clean", out)
                self.assertIn("file:", out)
                self.assertFalse(marker.exists(), (name, out))
            self.git(
                "config", "--" + location, "--unset", "filter.probe.clean"
            ) if location != "included" else self.git("config", "--unset", "include.path")
        worker = self.repo / ".claude/worktrees/seat/git"
        worker.parent.mkdir(parents=True)
        worker.write_text(f"#!/bin/sh\ntouch {marker}\n")
        worker.chmod(0o755)
        for name, code, out in self.run_three(worker_binding=worker):
            self.assertNotEqual(code, 0, (name, out))
            self.assertIn("worker-root", out)
            self.assertFalse(marker.exists())

    def test_all_three_scripts_refuse_a_checkout_with_gitmodules(self):
        (self.repo / ".gitmodules").write_text('[submodule "probe"]\n path = probe\n url = ./probe\n')
        sub = self.repo / "probe"
        sub.mkdir()
        (sub / ".gitattributes").write_text("tracked filter=probe\n")
        (sub / "tracked").write_text("fixture\n")
        for args in (
            ("init", "-q"),
            ("add", "."),
            ("commit", "-q", "-m", "submodule"),
            ("config", "filter.probe.clean", f"touch {self.temp / 'filter-ran'}"),
        ):
            subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=sub, env=self.env, check=True)
        self.git("add", "probe")
        for name, code, out in self.run_three():
            self.assertNotEqual(code, 0, (name, out))
            self.assertIn(".gitmodules", out)
        self.assertFalse((self.temp / "filter-ran").exists())
        (self.repo / ".gitmodules").unlink()
        self.git("rm", "--cached", "-f", "probe")
        for name, code, out in self.run_three():
            self.assertEqual(code, 0, (name, out))

    def test_all_three_scripts_refuse_a_redirected_worktree(self):
        self.git("config", "core.worktree", str(self.temp))
        for name, code, out in self.run_three():
            self.assertNotEqual(code, 0, (name, out))
            self.assertIn("core.worktree", out)
            self.assertIn("file:", out)
        self.git("config", "--unset", "core.worktree")
        for name, code, out in self.run_three():
            self.assertEqual(code, 0, (name, out))

    def test_all_three_scripts_disable_lazy_fetch_for_missing_objects(self):
        marker = self.temp / "helper-ran"
        self.git("config", "credential.helper", f"!touch {marker}")
        self.git("config", "remote.origin.promisor", "true")
        config = "home/dot_agents/agent-config.yaml"
        self.commit({config: "claude: {permissions: {ask: []}}\n"}, "missing-object input")
        for rel in (PROGRAMS, config, ".orchestration/tasks/dotfiles-T9-design-a01.md"):
            oid = self.git("rev-parse", f"HEAD:{rel}").strip()
            (self.repo / ".git/objects" / oid[:2] / oid[2:]).unlink()
        for name, code, out in self.run_three(trace=True):
            self.assertNotEqual(code, 0, (name, out))
        calls = [json.loads(line) for line in (self.temp / "trace.jsonl").read_text().splitlines()]
        self.assertTrue(calls)
        for call in calls:
            self.assertTrue(call["env"].get("GIT_NO_LAZY_FETCH") == "1" or "GIT_NO_LAZY_FETCH=1" in call["argv"], call)
        self.assertFalse(marker.exists())

    def setUp(self):
        super().setUp()
        self.production = self.temp / "trusted/scripts/orchestrator"
        self.production.mkdir(parents=True)
        for name in ("task-from-plan.py", "task-consistency-check.py", "plan-check.py", "task-template.md"):
            shutil.copyfile(GENERATOR.with_name(name), self.production / name)
        from tests.unit.test_plan_check import CLEAN
        from tests.unit.test_task_consistency_c11_c15 import DESIGN

        self.commit(
            {
                **CLEAN,
                **FILES,
                ".orchestration/tasks/dotfiles-T9-design-a01.md": DESIGN,
                "scripts/tool.py": "print('tool')\n",
            },
            "init",
            init=True,
        )

    def generate(self, *args, todo="P1-1", out=".orchestration/tasks/dotfiles-T9-demo-a01.md", trace=False):
        """Run the generator; return (exit, stdout + stderr, front matter or None, text or "")."""
        run = uv_command()
        result = subprocess.run(
            [
                *run,
                *(["-c", TRACE, str(self.temp / "trace.jsonl")] if trace else []),
                str(self.production / GENERATOR.name),
                todo,
                "--out",
                out,
                *args,
            ],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        if not (self.repo / out).is_file():
            return result.returncode, result.stdout + result.stderr, None, ""
        text = (self.repo / out).read_text()
        front = json.loads(
            subprocess.run([*run, "-c", LOAD], input=text, capture_output=True, text=True, check=True).stdout
        )
        return result.returncode, result.stdout + result.stderr, front, text

    def test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs(self):
        code, out, front, text = self.generate("--seat", "a009")
        self.assertEqual(code, 0, out)
        self.assertEqual(out.splitlines()[0], "dotfiles-T9-demo-a01.md: OK")
        self.assertIs(front["security"], True)
        allowed = ["scripts/demo.sh", "tests/unit/test_demo.py", ".orchestration/dotfiles-T9-demo-a01/**"]
        self.assertEqual(front["allowed_files"], allowed)
        first, second = front["premises"]
        self.assertEqual((first["command"], first.get("output")), ("printf known-output", None))
        self.assertEqual(second["command"], "sh -c 'exit 3'")
        self.assertTrue(second["claim"].startswith("verify:") and "pending" in second["claim"], second)
        self.assertIn("# from: tests/unit/test_demo.py (git grep -l demo.sh)", text)
        head = self.git("rev-parse", "origin/main").strip()
        self.assertIn("- `make unit-test`: verify: not run", text)
        self.assertIn(head, text)
        self.assertIn("`dotfiles-T9-demo-a01-followup-a01`", text)
        controls = [r["control"] for r in front["threat_table"]]
        self.assertIn("the task-file copy on the branch (.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
        self.assertNotIn("dotfiles-T133-result-precheck-a01", text)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)  # the scratch worktree is gone

    def test_generator_uses_the_bundled_template_without_task_records(self):
        self.git("rm", "-q", "-r", ".orchestration/tasks")
        self.commit({}, "no task records")
        code, out, front, text = self.generate()
        self.assertEqual(code, 0, out)
        controls = " || ".join(r["control"] for r in front["threat_table"])
        for name in ("task metadata", "metadata separators", "in-process effects", "orchestrator effect merge"):
            self.assertIn(name, controls)
        self.assertIn("(.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
        self.assertIn("- `make format`: verify: not run", text)
        self.assertIn("owned by `dotfiles-T9-demo-a01-followup-a01`", text)
        self.assertIn("`task_copy=<sha256 of .orchestration/dotfiles-T9-demo-a01/task.md>`", text)

    def test_generator_refuses_dirty_plan_commands_before_execution(self):
        marker = self.temp / "ran"
        program = FILES[PROGRAMS].replace("`printf known-output`", f"`touch {marker}`")
        self.commit({PROGRAMS: program}, "a marker command")
        for dirty in ("unstaged", "staged", "untracked"):
            with self.subTest(dirty=dirty):
                rel = ".orchestration/plans/024-extra.md" if dirty == "untracked" else PROGRAMS
                (self.repo / rel).write_text(program + "\nan uncommitted line\n")
                if dirty == "staged":
                    self.git("add", rel)
                code, out, front, _ = self.generate()
                self.assertEqual((code != 0, marker.exists(), front), (True, False, None), out)
                self.assertIn("uncommitted", out)
                self.git("reset", "-q", "--hard")
                (self.repo / ".orchestration/plans/024-extra.md").unlink(missing_ok=True)
        code, out, front, text = self.generate()
        self.assertEqual((code, marker.exists()), (0, False), out)
        self.assertIn(f"plan group at {self.git('rev-parse', 'HEAD').strip()}", text)

    def test_wave_selection_matches_whole_todo_ids(self):
        waves = "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-10, P1-11 | P1-12 |\n"
        self.commit({WAVES: waves + "| P-W1 | P1-1 | |\n\n## 7. STOP\n"}, "two waves")
        code, out, _, text = self.generate("--seat", "a009")
        self.assertEqual(code, 0, out)
        self.assertIn("wave P-W1", text)
        self.assertIn("seat a009", text)
        self.assertNotIn("P-W0", text)

    def test_generator_preserves_wildcard_scopes_and_their_threat_rows(self):
        program = FILES[PROGRAMS].replace(
            "`scripts/demo.sh`**", "`scripts/demo.sh`**, `scripts/*.py`, `scripts/*.sh`, `home/dot_config/**`"
        )
        self.commit({PROGRAMS: program, "scripts/tool.py": "print(1)\n", "home/dot_config/x.toml": "a = 1\n"}, "scopes")
        code, out, front, _ = self.generate()
        self.assertEqual(code, 0, out)
        self.assertTrue({"scripts/*.py", "home/dot_config/**"} <= set(front["allowed_files"]), front["allowed_files"])
        controls = " || ".join(r["control"] for r in front["threat_table"])
        for name in ("scripts/*.py", "home/dot_config/**", "scripts/tool.py", "home/dot_config/x.toml"):
            self.assertIn(name, controls)

    def test_program_item_continues_until_the_next_numbered_heading(self):
        item = "\n\n```\n{schema: x}\n```\n\nThen `scripts/late.sh` runs `printf late-output`.\n\n"
        program = FILES[PROGRAMS].replace("\n\n**(2) other**: unused", item + "**(2) other**: `printf other-item`")
        self.commit({PROGRAMS: program, "scripts/late.sh": "echo late\n"}, "a longer item")
        code, out, front, _ = self.generate()
        self.assertEqual(code, 0, out)
        self.assertIn("scripts/late.sh", front["allowed_files"])
        commands = [p["command"] for p in front["premises"]]
        self.assertIn("printf late-output", commands)
        self.assertNotIn("printf other-item", commands)

    def test_generator_retains_unavailable_single_word_and_redirecting_commands(self):
        written, check = self.temp / "written", self.temp / "check.out"
        spans = f"`no-such-tool-a02 --list`, `pwd`, `printf hi > {written}` and `make unit-test > {check}`"
        self.commit({PROGRAMS: FILES[PROGRAMS].replace("`sh -c 'exit 3'`", spans)}, "command forms")
        code, out, front, text = self.generate()
        self.assertEqual(code, 0, out)
        premises = {p["command"]: p for p in front["premises"]}
        self.assertTrue({"no-such-tool-a02 --list", "pwd", f"printf hi > {written}"} <= set(premises), premises)
        self.assertTrue(premises["no-such-tool-a02 --list"]["claim"].startswith("verify:"), premises)
        self.assertIn("pending", premises["no-such-tool-a02 --list"]["claim"])
        self.assertNotIn("output", premises["pwd"])
        self.assertNotIn("output", premises[f"printf hi > {written}"])
        self.assertFalse(written.exists())
        self.assertIn(f"- `make unit-test > {check}`: verify: not run", text)
        self.assertNotIn(f"make unit-test > {check}", premises)


if __name__ == "__main__":
    unittest.main()
