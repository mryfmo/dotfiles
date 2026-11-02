import re
import shutil
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from workflow_lock import LOCKFILE, RefusedYaml, expected_uses, load_yaml, lockfile, read_yaml  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
# The lockfile rule (regime-cutover U134, plan P-35). `.github/workflows/actions.lock` is written by `gh actions-lock`
# and read by GitHub's runner. The Secure use reference, https://docs.github.com/en/actions/reference/security/secure-use
# ("Using third-party actions"): a lockfile "records the exact commit for every action your workflows depend on,
# including transitive dependencies, and verifies the identity of each source repository at run time", and it
# "supersedes SHA pinning for repositories that adopt it". The concept page,
# https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles: "For repositories that adopt a
# lockfile, SHA pinning within workflow files is no longer necessary." The repository's own invariant is coverage
# (coverage_problems below; round 2 after the audit U134-2d9e0a8c): every `uses:` of every step and job, read from the
# parsed workflow, names a full semver tag and has one lockfile entry whose ref is that tag and whose commit is a 40-hex
# sha with both repository ids; every `uses` an entry lists is an entry, recursively, under the same checks; an entry
# nothing reaches is unused; a lockfile with a repeated key is refused; the lockfile's workflows rows and the workflow
# files name each other.
FULL_SEMVER_TAG = re.compile(r"v\d+\.\d+\.\d+")
LOCKED_COMMIT = re.compile(r"sha1-([0-9a-f]{40})")
REFERENCE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^@\s]*)?@([^@\s]+)")  # <owner>/<repo>[/<path>]@<ref>
WORKFLOW_SUFFIXES = (".yml", ".yaml")
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
    document = load_yaml(WORKFLOWS / name)
    if not isinstance(document, dict):
        raise AssertionError(f"{name} is not a mapping: {document!r}")
    return document


def workflow_uses(name: str, document: object) -> tuple[list[tuple[str, str]], list[str]]:
    """Every `uses:` of a parsed workflow as (where, reference), with the problems of a document that is not a
    workflow. A step's `uses` and a job's (a reusable workflow) both count, however the key is spelled (the round-1
    audit's `"uses":` passed a text scan); the local (`./`) and image (`docker://`) forms, which the lockfile does not
    record, are left out as the SHA test left them out."""
    found: list[tuple[str, str]] = []
    problems: list[str] = []
    jobs = document.get("jobs") if isinstance(document, dict) else None
    if not isinstance(jobs, dict):
        return found, [f"{name}: no jobs mapping"]
    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            problems.append(f"{name}: jobs.{job_id} is not a mapping")
            continue
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            problems.append(f"{name}: jobs.{job_id}.steps is not a list")
            steps = []
        holders = [(f"jobs.{job_id}", job)] + [(f"jobs.{job_id}.steps[{i}]", step) for i, step in enumerate(steps)]
        for where, holder in holders:
            if not isinstance(holder, dict):
                problems.append(f"{name}: {where} is not a mapping")
            elif "uses" in holder:
                reference = holder["uses"]
                if not isinstance(reference, str):
                    problems.append(f"{name}: {where}.uses is not a reference: {reference!r}")
                elif not reference.startswith(("./", "docker://")):
                    found.append((f"{name}: {where}", reference))
    return found, problems


def entry_problems(key: str, entry: object) -> list[str]:
    """What one lockfile entry lacks. Its ref is a full semver tag; its commit is sha1-<40 hex>; it carries owner_id
    and repo_id, the identity the runner verifies; its key's suffix is that ref or, the form `gh actions-lock` writes
    for a transitive entry (the parent action's action.yml names it by sha), the 40 hex of that commit; a `uses` list,
    when present, holds references."""
    match = REFERENCE.fullmatch(key)
    if match is None:
        return [f"actions.lock: {key!r} is not an <owner>/<repo>@<ref> key"]
    if not isinstance(entry, dict):
        return [f"actions.lock: {key} is not a mapping"]
    problems = []
    suffix, ref, commit = match.group(1), entry.get("ref"), entry.get("commit")
    if not (isinstance(ref, str) and FULL_SEMVER_TAG.fullmatch(ref)):
        problems.append(f"actions.lock: {key} has ref {ref!r}, not a full semver tag v<major>.<minor>.<patch>")
    locked = LOCKED_COMMIT.fullmatch(commit) if isinstance(commit, str) else None
    if locked is None:
        problems.append(f"actions.lock: {key} has commit {commit!r}, not sha1-<40 hex>")
    if FULL_SEMVER_TAG.fullmatch(suffix):
        if ref != suffix:
            problems.append(f"actions.lock: {key} is keyed by {suffix} and its ref is {ref!r}")
    elif locked is None or locked.group(1) != suffix:
        problems.append(
            f"actions.lock: {key} is keyed by {suffix!r}, neither a full semver tag nor the sha of its commit"
        )
    for field in ("owner_id", "repo_id"):
        if not isinstance(entry.get(field), int) or isinstance(entry.get(field), bool):
            problems.append(f"actions.lock: {key} has no {field}")
    uses = entry.get("uses", [])
    if not (isinstance(uses, list) and all(isinstance(item, str) for item in uses)):
        problems.append(f"actions.lock: {key} lists uses that are not references: {uses!r}")
    return problems


def coverage_problems(workflows: dict[str, object], lock: object) -> list[str]:
    """Everything the parsed workflows (by file name) and the parsed lockfile disagree on, one line each; [] when the
    lockfile covers the workflows. Each reference a workflow names is a full semver tag with an entry; the entries are
    walked through their `uses` lists, so a transitive entry is used and a transitive reference without an entry is
    missing; every other entry is unused; every workflow has a row listing its references once, and every row names a
    workflow file."""
    if not isinstance(lock, dict) or not all(isinstance(lock.get(key), dict) for key in ("dependencies", "workflows")):
        return ["actions.lock: no dependencies and workflows mappings"]
    dependencies, rows = lock["dependencies"], lock["workflows"]
    problems: list[str] = []
    direct: dict[str, str] = {}  # each reference the workflows name, with the first place that names it
    for name, document in sorted(workflows.items()):
        found, found_problems = workflow_uses(name, document)
        problems += found_problems
        for where, reference in found:
            match = REFERENCE.fullmatch(reference)
            if match is None:
                problems.append(f"{where}: {reference!r} is not <owner>/<repo>@<tag>")
                continue
            if not FULL_SEMVER_TAG.fullmatch(match.group(1)):
                problems.append(f"{where}: {reference} is not pinned to a full semver tag v<major>.<minor>.<patch>")
            direct.setdefault(reference, where)
        named = sorted({reference for _, reference in found})
        row = rows.get(f".github/workflows/{name}")
        if row is None:
            problems.append(f"actions.lock: no workflows row for .github/workflows/{name}")
        elif not isinstance(row, list) or len(row) != len(set(map(str, row))) or sorted(map(str, row)) != named:
            problems.append(f"actions.lock: the row for {name} lists {row!r}, the workflow names {named}")
    for row_key in rows:
        listed = Path(str(row_key))
        if (
            listed.parent != Path(".github/workflows")
            or listed.suffix not in WORKFLOW_SUFFIXES
            or listed.name not in workflows
        ):
            problems.append(f"actions.lock: {row_key!r} is listed, and it is not a workflow file of .github/workflows/")
    reached: set[str] = set()
    pending = sorted(direct.items())
    while pending:
        key, via = pending.pop(0)
        if key in reached:
            continue
        reached.add(key)
        entry = dependencies.get(key)
        if entry is None:
            problems.append(f"{via}: {key} has no lockfile entry")
            continue
        problems += entry_problems(key, entry)
        if isinstance(entry, dict) and isinstance(entry.get("uses"), list):
            pending += [(str(item), f"actions.lock: {key} uses") for item in entry["uses"]]
    for key in dependencies:
        if key not in reached:
            problems.append(f"actions.lock: {key} is locked, and no workflow or entry uses it")
    return problems


def lockfile_problems(workflows_dir: Path, lock_path: Path) -> list[str]:
    """The coverage check over a directory's workflow files and a lockfile, all parsed in one run by the loader that
    refuses a repeated key; a refused file is a problem by name, and the check stops there."""
    if not lock_path.is_file():
        return [f"no {lock_path.name}: `gh actions-lock` writes it"]
    files = sorted(entry for entry in workflows_dir.iterdir() if entry.is_file() and entry.suffix in WORKFLOW_SUFFIXES)
    read = read_yaml([*files, lock_path])
    problems = [f"{entry.name}: {read[entry].error}" for entry in [*files, lock_path] if read[entry].error is not None]
    if problems:
        return problems
    return coverage_problems({entry.name: read[entry].document for entry in files}, read[lock_path].document)


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

    def test_every_external_action_has_one_lockfile_entry_and_no_entry_is_unused(self):
        # The runner enforces actions.lock at run time; this check makes a workflow edit that names an unlocked or
        # floating action, a hand edit that moves an entry's ref off its key, a dropped transitive entry, a repeated
        # entry, a stale entry or a stale row fail before the workflow runs (coverage_problems; LockfileCoverageTest
        # runs each on a scratch copy).
        self.assertEqual([], lockfile_problems(WORKFLOWS, LOCKFILE))

    def test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time(self):
        # ci:39185982423:1: the event's recorded base sha can lag the base branch (on PR #420 it was the head's fork
        # point, 740772ef, from before the verifier landed), so the job checks out the base branch's tip at run time and
        # verifies against exactly that commit.
        text = (WORKFLOWS / "regime.yml").read_text()
        self.assertNotIn("pull_request.base.sha", text)
        self.assertIn("ref: refs/heads/${{ github.base_ref }}", [line.strip() for line in text.splitlines()])
        # the tip's sha, read with its producer's status checked (standing order 21, U120 round 3)
        self.assertIn("base=$(git rev-parse HEAD) || exit 1", text)
        self.assertIn('--base "${base}"', text)

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


def entry_text(key: str, entry: dict) -> str:
    """One dependencies entry as `gh actions-lock` writes it (four-space indents, single quotes), so a scratch lockfile
    is edited by swapping whole entries."""
    lines = [f"    '{key}':"]
    lines += [f"        {field}: '{entry[field]}'" for field in ("ref", "commit") if field in entry]
    lines += [f"        {field}: {entry[field]}" for field in ("owner_id", "repo_id") if field in entry]
    if entry.get("uses"):
        lines.append("        uses:")
        lines += [f"            - '{item}'" for item in entry["uses"]]
    return "\n".join(lines) + "\n"


ZERO_SHA = "0" * 40


class LockfileCoverageTest(unittest.TestCase):
    """Each edit of a scratch copy of the workflows and the lockfile fails the coverage check, naming it. The first
    three are the mutations the round-1 audit found accepted (U134-2d9e0a8c: a floating tag, a mismatched ref, a
    transitive reference without an entry), then its duplicate entry, its row for a file that is no workflow and its
    quoted `"uses":` key; the rest are the forms the SHA test refused and the reach of the transitive walk. The
    fixtures are read from the lockfile (the checkout entry), never written as constants, so a bump moves them too."""

    def setUp(self) -> None:
        self.reference = expected_uses("actions/checkout")
        self.owner_repo, _, self.tag = self.reference.rpartition("@")
        self.entry = lockfile()["dependencies"][self.reference]
        self.sha = LOCKED_COMMIT.fullmatch(self.entry["commit"]).group(1)
        self.row = f"    '.github/workflows/apply-check.yml':\n        - '{self.reference}'\n"

    def scratch(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        copy = Path(temp.name) / "workflows"
        shutil.copytree(WORKFLOWS, copy)
        return copy

    def swap(self, old: str, new: str) -> Callable[[str], str]:
        def edit(text: str) -> str:
            self.assertEqual(1, text.count(old), f"{old!r} is not in the text once")
            return text.replace(old, new)

        return edit

    def problems_after(self, edits: dict[str, Callable[[str], str]]) -> list[str]:
        """The coverage check's problems on a scratch copy of the workflows directory with each named file edited (a
        file that is not there starts empty, so an edit can add a workflow)."""
        copy = self.scratch()
        for name, edit in edits.items():
            target = copy / name
            before = target.read_text() if target.is_file() else ""
            after = edit(before)
            self.assertNotEqual(before, after, f"the edit of {name} changed nothing")
            target.write_text(after)
        return lockfile_problems(copy, copy / "actions.lock")

    def assertProblems(self, expected: list[str], problems: list[str]) -> None:
        """Each expected fragment is in exactly one problem, and there is no other problem."""
        for fragment in expected:
            self.assertEqual(1, sum(fragment in problem for problem in problems), f"{fragment!r} in {problems}")
        self.assertEqual(len(expected), len(problems), problems)

    def test_the_scratch_copy_passes_before_any_edit(self) -> None:
        self.assertEqual([], self.problems_after({}))

    def test_a_floating_tag_with_an_entry_whose_ref_is_that_tag_is_refused(self) -> None:
        # U134-2d9e0a8c:182: checkout@v7 with ref v7 passed the `ref == the workflow's suffix` escape.
        major = self.tag.split(".")[0]
        floating = f"{self.owner_repo}@{major}"
        problems = self.problems_after(
            {
                "apply-check.yml": self.swap(f"uses: {self.reference}", f"uses: {floating}"),
                "actions.lock": lambda text: (
                    self.swap(self.row, self.row.replace(self.reference, floating))(text)
                    + entry_text(floating, {**self.entry, "ref": major})
                ),
            }
        )
        self.assertProblems(
            [
                f"apply-check.yml: jobs.apply-container.steps[0]: {floating} is not pinned to a full semver tag",
                f"actions.lock: {floating} has ref '{major}', not a full semver tag",
                f"actions.lock: {floating} is keyed by '{major}', neither a full semver tag nor the sha of its commit",
            ],
            problems,
        )

    def test_an_entry_whose_ref_is_another_full_tag_than_its_key_is_refused(self) -> None:
        # U134-2d9e0a8c:182: checkout@v7.0.1 with ref v999.0.0 passed, since any full semver ref did.
        moved = entry_text(self.reference, {**self.entry, "ref": "v0.0.0"})
        problems = self.problems_after({"actions.lock": self.swap(entry_text(self.reference, self.entry), moved)})
        self.assertProblems(
            [f"actions.lock: {self.reference} is keyed by {self.tag} and its ref is 'v0.0.0'"], problems
        )

    def test_a_transitive_reference_without_an_entry_is_refused(self) -> None:
        # U134-2d9e0a8c:185: the transitive set was read from the entries that exist, so a dropped entry passed.
        child = f"example/child@{ZERO_SHA}"
        listing = entry_text(self.reference, {**self.entry, "uses": [child]})
        problems = self.problems_after({"actions.lock": self.swap(entry_text(self.reference, self.entry), listing)})
        self.assertProblems([f"actions.lock: {self.reference} uses: {child} has no lockfile entry"], problems)

    def test_a_second_level_entry_is_reached_and_used(self) -> None:
        # U134-2d9e0a8c:185: an entry reachable only through a transitive entry was reported unused.
        child = f"example/child@{ZERO_SHA}"
        grandchild = "example/grandchild@v2.0.0"
        child_entry = {"ref": "v1.0.0", "commit": f"sha1-{ZERO_SHA}", "owner_id": 1, "repo_id": 2, "uses": [grandchild]}
        grandchild_entry = {"ref": "v2.0.0", "commit": f"sha1-{ZERO_SHA}", "owner_id": 1, "repo_id": 3}
        listing = entry_text(self.reference, {**self.entry, "uses": [child]})
        problems = self.problems_after(
            {
                "actions.lock": lambda text: (
                    self.swap(entry_text(self.reference, self.entry), listing)(text)
                    + entry_text(child, child_entry)
                    + entry_text(grandchild, grandchild_entry)
                ),
            }
        )
        self.assertEqual([], problems)

    def test_a_duplicated_entry_is_refused_by_the_loader(self) -> None:
        # U134-2d9e0a8c:165: yaml.safe_load kept the last of two entries for one key and said nothing.
        problems = self.problems_after({"actions.lock": lambda text: text + entry_text(self.reference, self.entry)})
        self.assertEqual(1, len(problems), problems)
        self.assertTrue(problems[0].startswith("actions.lock: "), problems[0])
        self.assertIn(f"found duplicate key '{self.reference}'", problems[0])

    def test_the_loader_refuses_a_duplicate_key_naming_both_lines_and_a_merge_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            doubled = Path(temp) / "doubled.yml"
            doubled.write_text("a: 1\nb:\n  c: 1\n  d: 2\n  c: 3\n")
            with self.assertRaises(RefusedYaml) as caught:
                load_yaml(doubled)
            self.assertIn("doubled.yml: ", str(caught.exception))
            self.assertIn("found duplicate key 'c', first at line 3", str(caught.exception))
            self.assertIn("line 5, column 3", str(caught.exception))
            merged = Path(temp) / "merged.yml"
            merged.write_text("base: &base\n  a: 1\nb:\n  <<: *base\n")
            with self.assertRaises(RefusedYaml) as caught:
                load_yaml(merged)
            self.assertIn("found a merge key", str(caught.exception))
            plain = Path(temp) / "plain.yml"
            plain.write_text("a: 1\nb:\n  c: 1\n  d: 2\n")
            self.assertEqual({"a": 1, "b": {"c": 1, "d": 2}}, load_yaml(plain))

    def test_a_row_for_a_file_that_is_no_workflow_is_refused(self) -> None:
        # U134-2d9e0a8c:195: a row for actions.lock itself passed on the file's existence.
        row = "    '.github/workflows/actions.lock':\n        - 'actions/setup-node@v4'\n"
        problems = self.problems_after({"actions.lock": self.swap("workflows:\n", "workflows:\n" + row)})
        self.assertProblems(
            ["actions.lock: '.github/workflows/actions.lock' is listed, and it is not a workflow file"], problems
        )

    def test_a_workflow_without_a_row_is_refused(self) -> None:
        extra = f"jobs:\n  extra:\n    steps:\n      - uses: {self.reference}\n"
        problems = self.problems_after({"extra.yml": lambda text: text + extra})
        self.assertProblems(["actions.lock: no workflows row for .github/workflows/extra.yml"], problems)

    def test_a_quoted_uses_key_without_an_entry_is_refused(self) -> None:
        # U134-2d9e0a8c:133: `- "uses": actions/setup-node@v4` passed the text scan for `uses:`.
        step = '\n      - "uses": actions/setup-node@v4\n'
        settled = "          persist-credentials: false\n"
        problems = self.problems_after({"apply-check.yml": self.swap(settled, settled + step)})
        self.assertProblems(
            [
                "apply-check.yml: jobs.apply-container.steps[1]: actions/setup-node@v4 is not pinned to a full semver",
                "apply-check.yml: jobs.apply-container.steps[1]: actions/setup-node@v4 has no lockfile entry",
                "actions.lock: the row for apply-check.yml lists",
            ],
            problems,
        )

    def test_a_workflow_pinned_by_sha_is_refused_although_the_entry_form_is_valid(self) -> None:
        # The form the SHA test required: the lockfile's narrowing makes the tag the reference, and the sha the entry's.
        by_sha = f"{self.owner_repo}@{self.sha}"
        problems = self.problems_after(
            {
                "apply-check.yml": self.swap(f"uses: {self.reference}", f"uses: {by_sha}"),
                "actions.lock": lambda text: (
                    self.swap(self.row, self.row.replace(self.reference, by_sha))(text) + entry_text(by_sha, self.entry)
                ),
            }
        )
        self.assertProblems(
            [f"apply-check.yml: jobs.apply-container.steps[0]: {by_sha} is not pinned to a full semver tag"], problems
        )

    def test_an_entry_nothing_reaches_is_unused(self) -> None:
        unused = "example/unused@v1.0.0"
        entry = {"ref": "v1.0.0", "commit": f"sha1-{ZERO_SHA}", "owner_id": 1, "repo_id": 2}
        problems = self.problems_after({"actions.lock": lambda text: text + entry_text(unused, entry)})
        self.assertProblems([f"actions.lock: {unused} is locked, and no workflow or entry uses it"], problems)

    def test_an_entry_without_an_id_or_with_a_short_commit_is_refused(self) -> None:
        without = {field: value for field, value in self.entry.items() if field != "owner_id"}
        problems = self.problems_after(
            {"actions.lock": self.swap(entry_text(self.reference, self.entry), entry_text(self.reference, without))}
        )
        self.assertProblems([f"actions.lock: {self.reference} has no owner_id"], problems)
        short = {**self.entry, "commit": f"sha1-{self.sha[:7]}"}
        problems = self.problems_after(
            {"actions.lock": self.swap(entry_text(self.reference, self.entry), entry_text(self.reference, short))}
        )
        self.assertProblems(
            [f"actions.lock: {self.reference} has commit 'sha1-{self.sha[:7]}', not sha1-<40 hex>"], problems
        )

    def test_a_missing_lockfile_is_refused(self) -> None:
        copy = self.scratch()
        (copy / "actions.lock").unlink()
        self.assertEqual(
            ["no actions.lock: `gh actions-lock` writes it"], lockfile_problems(copy, copy / "actions.lock")
        )


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
