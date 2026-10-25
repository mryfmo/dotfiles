import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
EXPECTED_PERMISSIONS = {
    "apply-check.yml": {"contents": "read"},
    "agent-assets.yml": {"contents": "read"},
    "docs-check.yml": {"contents": "read"},
    "docs.yml": {"contents": "write"},
    # U81: the drift watch keeps its one tracking issue; it runs on schedule and dispatch only.
    "drift-watch.yml": {"contents": "read", "issues": "write"},
    "macos.yaml": {"contents": "read"},
    "private-bootstrap.yaml": {"contents": "read"},
    "regime.yml": {"contents": "read"},
    "remote.yaml": {"contents": "read"},
    "test.yaml": {"contents": "read"},
    "ubuntu.yaml": {"contents": "read"},
}
# The docs deploy pushes with a token handed to its deploy step only, so no checkout keeps credentials.
CHECKOUT_CREDENTIAL_EXEMPTIONS: dict[tuple[str, str, str], str] = {}


def top_level_permissions(text: str) -> dict[str, str]:
    lines = text.splitlines()
    try:
        start = lines.index("permissions:") + 1
    except ValueError:
        return {}
    permissions = {}
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if not line.strip():
            continue
        match = re.fullmatch(r"  ([a-z-]+): (read|write|none)", line)
        if match:
            permissions[match.group(1)] = match.group(2)
        else:
            permissions[f"invalid:{line}"] = "invalid"
    return permissions


def checkout_steps(text: str) -> list[tuple[str, str, str]]:
    lines = text.splitlines()
    steps = []
    for index, line in enumerate(lines):
        match = re.match(
            r"""(\s*)(-\s+)?uses:\s*(?P<quote>['"]?)actions/checkout@[^\s'"]+(?P=quote)(?:[ \t]+#.*)?[ \t]*$""",
            line,
        )
        if not match:
            continue
        step_indent = len(match.group(1)) - (0 if match.group(2) else 2)
        start = index if match.group(2) else index - 1
        while start >= 0 and not re.match(rf" {{{step_indent}}}-\s+", lines[start]):
            start -= 1
        if start < 0:
            continue
        end = index + 1
        while end < len(lines):
            candidate = lines[end]
            if candidate.strip() and len(candidate) - len(candidate.lstrip()) <= step_indent:
                break
            end += 1
        name_match = re.match(r"\s*-\s+name:\s*(.+)", lines[start])
        step_name = name_match.group(1) if name_match else ""
        job_name = ""
        for parent in reversed(lines[:start]):
            job_match = re.match(r"  ([A-Za-z0-9_-]+):\s*$", parent)
            if job_match:
                job_name = job_match.group(1)
                break
        steps.append((job_name, step_name, "\n".join(lines[start:end])))
    return steps


def checkout_step_disables_credentials(block: str) -> bool:
    lines = block.splitlines()
    step_indent = len(lines[0]) - len(lines[0].lstrip())
    values = []
    for index, line in enumerate(lines):
        match = re.match(rf"( {{{step_indent + 2}}})with:\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        for option in lines[index + 1 :]:
            if option.strip() and len(option) - len(option.lstrip()) <= indent:
                break
            option_match = re.fullmatch(
                rf" {{{indent + 2}}}persist-credentials:\s*([^#\s]+)(?:\s+#.*)?",
                option,
            )
            if option_match:
                values.append(option_match.group(1))
    return values == ["false"]


def load_workflow(name: str) -> dict:
    """The workflow parsed by PyYAML, which uv provides as for regime.yml's tests."""
    read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
    uv = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
    result = subprocess.run([*uv, "-c", read, str(WORKFLOWS / name)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


class WorkflowSecurityTest(unittest.TestCase):
    def test_tokens_reach_only_the_steps_that_use_them(self):
        # A job-wide token reaches every step and every tool a step installs; each one goes to its users only.
        for workflow, job_name, holders in (
            ("test.yaml", "test", {"Install tools": "GITHUB_TOKEN", "Upload coverage to Codecov": "CODECOV_TOKEN"}),
            ("docs.yml", "deploy", {"Deploy docs": "GH_TOKEN"}),
        ):
            with self.subTest(workflow=workflow):
                job = load_workflow(workflow)["jobs"][job_name]
                self.assertEqual([], [key for key in job.get("env", {}) if "TOKEN" in key])
                self.assertEqual(
                    holders,
                    {step["name"]: key for step in job["steps"] for key in step.get("env", {}) if "TOKEN" in key},
                )

    def test_codecov_upload_installs_a_pinned_cli(self):
        steps = load_workflow("test.yaml")["jobs"]["test"]["steps"]
        (upload,) = [step for step in steps if step.get("uses", "").startswith("codecov/codecov-action@")]
        self.assertRegex(upload["with"].get("version", "latest"), r"^\d+\.\d+\.\d+$")

    def test_external_actions_use_full_commit_shas(self):
        mutable = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = re.search(r"uses:\s+([^\s]+)", line)
                if not match:
                    continue
                reference = match.group(1)
                if reference.startswith(("./", "docker://")):
                    continue
                if not re.fullmatch(r"[^@]+@[0-9a-f]{40}", reference):
                    mutable.append(f"{path.name}:{number}: {reference}")
        self.assertEqual([], mutable)

    def test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time(self):
        # ci:39185982423:1: the event's recorded base sha can lag the base branch (on PR #420 it was the head's fork
        # point, 740772ef, from before the verifier landed), so the job checks out the base branch's tip at run time and
        # verifies against exactly that commit.
        text = (WORKFLOWS / "regime.yml").read_text()
        self.assertNotIn("pull_request.base.sha", text)
        self.assertIn("ref: refs/heads/${{ github.base_ref }}", [line.strip() for line in text.splitlines()])
        self.assertIn('--base "$(git rev-parse HEAD)"', text)

    def test_workflows_have_exact_top_level_permissions(self):
        actual = {path.name: top_level_permissions(path.read_text()) for path in sorted(WORKFLOWS.glob("*.y*ml"))}
        self.assertEqual(EXPECTED_PERMISSIONS, actual)

    def test_workflows_have_no_job_level_permission_overrides(self):
        overrides = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if re.match(r" {4,}permissions\s*:", line):
                    overrides.append(f"{path.name}:{number}")
        self.assertEqual([], overrides)

    def test_checkout_does_not_persist_credentials_without_explicit_exemption(self):
        insecure = []
        stale_exemptions = []
        exemption_hits = dict.fromkeys(CHECKOUT_CREDENTIAL_EXEMPTIONS, 0)
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for job_name, step_name, block in checkout_steps(path.read_text()):
                exemption = (path.name, job_name, step_name)
                if exemption in CHECKOUT_CREDENTIAL_EXEMPTIONS:
                    exemption_hits[exemption] += 1
                    if checkout_step_disables_credentials(block):
                        stale_exemptions.append(exemption)
                elif not checkout_step_disables_credentials(block):
                    insecure.append(f"{path.name}: {job_name}: {step_name}")
        self.assertEqual([], insecure)
        self.assertEqual([], stale_exemptions)
        self.assertEqual(dict.fromkeys(CHECKOUT_CREDENTIAL_EXEMPTIONS, 1), exemption_hits)
        self.assertTrue(all(reason.strip() for reason in CHECKOUT_CREDENTIAL_EXEMPTIONS.values()))

    def test_checkout_setting_does_not_leak_from_the_next_step(self):
        workflow = """jobs:
  test:
    steps:
      - name: Checkout repository
        uses: actions/checkout@0000000000000000000000000000000000000000
      - name: Unrelated step
        with:
          persist-credentials: false
"""
        [(_, _, block)] = checkout_steps(workflow)
        self.assertFalse(checkout_step_disables_credentials(block))

    def test_unnamed_checkout_setting_does_not_leak_from_the_next_step(self):
        workflow = """jobs:
  test:
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
      - name: Unrelated step
        with:
          persist-credentials: false
"""
        [(_, step_name, block)] = checkout_steps(workflow)
        self.assertEqual("", step_name)
        self.assertFalse(checkout_step_disables_credentials(block))

    def test_quoted_unnamed_checkout_is_detected(self):
        trailing_spaces = "   "
        for quote in ("'", '"'):
            with self.subTest(quote=quote):
                workflow = f"""jobs:
  test:
    steps:
      - uses: {quote}actions/checkout@0000000000000000000000000000000000000000{quote}{trailing_spaces}
"""
                [(_, step_name, block)] = checkout_steps(workflow)
                self.assertEqual("", step_name)
                self.assertFalse(checkout_step_disables_credentials(block))

    def test_checkout_rejects_duplicate_or_non_false_credential_settings(self):
        for settings in (
            "persist-credentials: true",
            "persist-credentials: false\n          persist-credentials: true",
            "persist-credentials: false\n          persist-credentials: false",
        ):
            with self.subTest(settings=settings):
                block = f"""      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          {settings}
"""
                self.assertFalse(checkout_step_disables_credentials(block))

    def test_no_run_script_interpolates_an_expression(self):
        # F190 (docs.github.com secure-use, "Use an intermediate environment variable"): a `${{ }}` inside run: is
        # pasted into the script before the shell parses it, so every value reaches a script through env:.
        found = [
            f"{path.name}:{number}" for path in sorted(WORKFLOWS.glob("*.y*ml")) for number in run_expressions(path)
        ]
        self.assertEqual([], found)

    def test_the_run_expression_reader_sees_inline_and_block_scripts(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "w.yml"
            path.write_text(
                "jobs:\n  a:\n    steps:\n"
                "      - run: echo ${{ github.ref }}\n"
                "      - name: b\n        env:\n          X: ${{ github.ref }}\n        run: |\n"
                "          echo ok\n          echo ${{ github.sha }}\n"
                "      - name: c\n        if: ${{ always() }}\n        run: echo fine\n"
            )
            self.assertEqual([4, 10], run_expressions(path))

    def test_every_job_has_a_timeout(self):
        # F191: a hung job otherwise runs for GitHub's default 360 minutes.
        missing = [
            f"{path.name}: {name}"
            for path in sorted(WORKFLOWS.glob("*.y*ml"))
            for name, block in job_blocks(path.read_text()).items()
            if not re.search(r"^    timeout-minutes: [1-9][0-9]*$", block, re.MULTILINE)
        ]
        self.assertEqual([], missing)
        self.assertIn("build", job_blocks((WORKFLOWS / "macos.yaml").read_text()))

    def test_the_pull_request_docs_build_watches_the_deploys_paths(self):
        # F151: a docs/-only change rebuilds the site on main, and a pull request gets the strict build first.
        deploy = workflow_paths((WORKFLOWS / "docs.yml").read_text(), "push")
        check = workflow_paths((WORKFLOWS / "docs-check.yml").read_text(), "pull_request")
        self.assertIn("docs/**", deploy)
        self.assertEqual(deploy | {".github/workflows/docs-check.yml"}, check)
        self.assertIn("run: make docs", (WORKFLOWS / "docs-check.yml").read_text())

    def test_the_installed_coderabbit_app_stays_off(self):
        # F189: the app is installed and its default reviews every pull request and push, so the file must exist
        # and hold only the switch that turns automatic reviews off.
        settings = [
            line for line in (WORKFLOWS.parents[1] / ".coderabbit.yaml").read_text().splitlines() if line.strip()
        ]
        settings = [line for line in settings if not line.lstrip().startswith("#")]
        self.assertEqual(["reviews:", "  auto_review:", "    enabled: false"], settings)


def run_expressions(path: Path) -> list[int]:
    """Line numbers of `${{` inside a step's `run:` value, inline or block."""
    found = []
    block_indent = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        indent = len(line) - len(line.lstrip())
        if block_indent is not None:
            if not line.strip() or indent > block_indent:
                if "${{" in line:
                    found.append(number)
                continue
            block_indent = None
        match = re.match(r"(\s*)(- )?run:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(3)
        if value in ("|", ">", "|-", ">-"):
            block_indent = len(match.group(1)) + (2 if match.group(2) else 0)
        elif "${{" in value:
            found.append(number)
    return found


def job_blocks(text: str) -> dict[str, str]:
    """Each job's text under `jobs:`, keyed by its two-space name."""
    body = text.split("\njobs:\n", 1)[1]
    blocks: dict[str, str] = {}
    name = None
    for line in body.splitlines():
        match = re.fullmatch(r"  ([A-Za-z0-9_-]+):\s*", line)
        if match:
            name = match.group(1)
            blocks[name] = ""
        elif line and not line.startswith(" "):
            break
        elif name is not None:
            blocks[name] += line + "\n"
    return blocks


def workflow_paths(text: str, event: str) -> set[str]:
    """The `paths:` filter of one `on:` event."""
    section = text.split(f"\n  {event}:\n", 1)[1].split("\n    paths:\n", 1)[1]
    return set(re.findall(r'^      - "([^"]+)"$', section.split("\n\n", 1)[0], re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
