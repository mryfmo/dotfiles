"""regime.yml keeps the properties that make pull_request_target safe for it (regime-cutover U103, plan P-01 part 1).

GitHub's default Actions event policy blocks pull_request_target in public repositories from 2026-12-02, and the
operator allows it for this repository by an explicit policy (gate G-23). That allowance rests on the workflow running
only the base's code with a read-only token and reading the pull request as data. Each property is one check here,
and each check is shown to go red on a copy of the workflow with that property taken away.
"""

from __future__ import annotations

import copy
import json
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/regime.yml"
BASE_BRANCH = "refs/heads/${{ github.base_ref }}"
BODY_EXPRESSION = "github.event.pull_request.body"
HEAD_REF = "refs/regime/pr-head"
UNSAFE_OPTION = "allow-unsafe-pr-checkout"
READ_ONLY = {"contents": "read"}
# A git subcommand that puts a commit into the work tree or moves HEAD; after the fetch, any of them could run the
# head's files as the base's. A verb inside a path (`refs/pull/`, `pr-head`) is not a subcommand.
TREE_VERBS = "checkout|switch|worktree|reset|restore|merge|rebase|cherry-pick|pull|read-tree|apply|am|stash"
MOVES_TREE = re.compile(rf"\bgit\b.*(?<![/\w-])(?:{TREE_VERBS})(?![/\w-])")
FETCH = re.compile(r"\bgit\b.*\bfetch\b")


def load(path: Path) -> dict:
    """The workflow parsed by PyYAML under uv (as test_regime_ci.py reads it): the test interpreter has no YAML parser."""
    read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
    uv = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
    result = subprocess.run([*uv, "-c", read, str(path)], capture_output=True, text=True, check=True)
    doc = json.loads(result.stdout)
    if not isinstance(doc, dict):
        raise AssertionError(f"{path} is not a mapping: {doc!r}")
    return doc


def line(text: str) -> str:
    """`regime.yml:<n>` of the line that holds `text`, or a note that it is gone: the message names what to restore."""
    for number, content in enumerate(WORKFLOW.read_text().splitlines(), 1):
        if text in content:
            return f"regime.yml:{number} ({text})"
    return f"regime.yml (no line holds {text!r} any more)"


def require(condition: object, protects: str, detail: str) -> None:
    if not condition:
        raise AssertionError(f"{line(protects)}: {detail}")


def mapping(value: object, protects: str) -> dict:
    require(isinstance(value, dict), protects, f"expected a mapping, found {value!r}")
    return value  # type: ignore[return-value]


def jobs(doc: dict) -> dict[str, dict]:
    return {name: mapping(job, f"{name}:") for name, job in mapping(doc.get("jobs"), "jobs:").items()}


def steps(doc: dict) -> list[dict]:
    found = [step for job in jobs(doc).values() for step in job.get("steps") or []]
    require(found, "steps:", "the workflow has no steps")
    return [mapping(step, "steps:") for step in found]


def run_lines(doc: dict) -> list[str]:
    return [text for step in steps(doc) for text in str(step.get("run", "")).splitlines()]


def check_trigger(doc: dict) -> None:
    # PyYAML reads the key `on` as the boolean true, which JSON spells "true".
    on = mapping(doc.get("true", doc.get("on")), "pull_request_target:")
    require(list(on) == ["pull_request_target"], "pull_request_target:", f"the triggers are {list(on)!r}")
    event = mapping(on["pull_request_target"], "pull_request_target:")
    require(event.get("branches") == ["main"], "branches: [main]", f"the event filter is {event!r}")


def check_permissions(doc: dict) -> None:
    require(doc.get("permissions") == READ_ONLY, "contents: read", f"the token is {doc.get('permissions')!r}")
    for name, job in jobs(doc).items():
        granted = job.get("permissions", {})
        widened = not isinstance(granted, dict) or not set(granted.items()) <= set(READ_ONLY.items())
        require(not widened, "contents: read", f"job {name} grants {granted!r}")


def check_checkout(doc: dict) -> None:
    checkouts = [step for step in steps(doc) if str(step.get("uses", "")).startswith("actions/checkout@")]
    require(checkouts, "uses: actions/checkout@", "no step checks anything out, so nothing pins the base")
    for step in checkouts:
        given = mapping(step.get("with"), "ref: refs/heads/${{ github.base_ref }}")
        require(given.get("ref") == BASE_BRANCH, "ref: refs/heads/${{ github.base_ref }}", f"checkout gets {given!r}")
        require(given.get("persist-credentials") is False, "persist-credentials: false", f"checkout gets {given!r}")


def check_no_unsafe_checkout(doc: dict) -> None:
    for step in steps(doc):
        require(UNSAFE_OPTION not in json.dumps(step), "uses: actions/checkout@", f"a step names it: {step!r}")


def check_head_is_data(doc: dict) -> None:
    protects = "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"
    fetches = 0
    for text in run_lines(doc):
        require(not text.rstrip().endswith("\\"), protects, f"a continued line hides its words: {text!r}")
        require(not MOVES_TREE.search(text), protects, f"a step moves the work tree or HEAD: {text!r}")
        if not FETCH.search(text):
            continue
        fetches += 1
        try:
            words = shlex.split(text)
        except ValueError as error:
            raise AssertionError(f"{line(protects)}: a fetch line this check cannot read: {text!r}") from error
        refspecs = [word for word in words[words.index("fetch") + 1 :] if not word.startswith("-")][1:]
        require(refspecs, protects, f"a fetch with no refspec: {text!r}")
        for refspec in refspecs:
            source, _, target = refspec.partition(":")
            head_as_data = source.startswith("refs/pull/") and target == HEAD_REF
            require(head_as_data, protects, f"a fetch writes elsewhere: {text!r}")
    require(fetches == 1, protects, f"{fetches} fetch lines; the head is fetched once, into {HEAD_REF}")


def check_body_is_data(doc: dict) -> None:
    protects = "PR_BODY: ${{ github.event.pull_request.body }}"
    scopes = [*jobs(doc).values(), *steps(doc)]
    carriers = [
        value for scope in scopes for value in (scope.get("env") or {}).values() if BODY_EXPRESSION in str(value)
    ]
    require(carriers, protects, "no env: mapping carries the body to the script")
    for text in run_lines(doc):
        require(BODY_EXPRESSION not in text, protects, f"the body is inlined into run: {text!r}")
        require("${{" not in text, protects, f"an expression is inlined into run: {text!r}")


def check_cancel_in_progress(doc: dict) -> None:
    group = mapping(doc.get("concurrency"), "cancel-in-progress: true")
    require(group.get("cancel-in-progress") is True, "cancel-in-progress: true", f"concurrency is {group!r}")


def regime_steps(doc: dict) -> list[dict]:
    return doc["jobs"]["regime"]["steps"]


def checkout_options(doc: dict) -> dict:
    return next(step["with"] for step in regime_steps(doc) if step.get("uses", "").startswith("actions/checkout@"))


def fetch_step(doc: dict) -> dict:
    return next(step for step in regime_steps(doc) if FETCH.search(step.get("run", "")))


def verify_step(doc: dict) -> dict:
    return next(step for step in regime_steps(doc) if "PR_BODY" in step.get("env", {}))


def inline_body(doc: dict) -> None:
    verify_step(doc)["run"] += ' --body "${{ github.event.pull_request.body }}"'


def set_in(getter: Callable[[dict], dict], key: str, value: object) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)[key] = value

    return mutate


def delete_in(getter: Callable[[dict], dict], key: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        del getter(doc)[key]

    return mutate


def append_run(getter: Callable[[dict], dict], text: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)["run"] += text

    return mutate


def triggers(doc: dict) -> dict:
    return doc.get("true", doc.get("on"))


def regime_job(doc: dict) -> dict:
    return doc["jobs"]["regime"]


class Invariant(NamedTuple):
    """One safety property: the check that holds on the head, and the edits that must each turn it red."""

    check: Callable[[dict], None]
    breaks: dict[str, Callable[[dict], None]]


TRIGGER = Invariant(
    check_trigger,
    {
        "a second trigger": set_in(triggers, "push", {"branches": ["main"]}),
        "a wider branch filter": set_in(lambda d: triggers(d)["pull_request_target"], "branches", ["main", "release"]),
        "no branch filter": delete_in(lambda d: triggers(d)["pull_request_target"], "branches"),
    },
)
PERMISSIONS = Invariant(
    check_permissions,
    {
        "contents: write": set_in(lambda d: d["permissions"], "contents", "write"),
        "a second scope": set_in(lambda d: d["permissions"], "pull-requests", "write"),
        "a job that writes": set_in(regime_job, "permissions", {"contents": "write"}),
        "a job with write-all": set_in(regime_job, "permissions", "write-all"),
    },
)
CHECKOUT = Invariant(
    check_checkout,
    {
        "no ref": delete_in(checkout_options, "ref"),
        "the head as ref": set_in(checkout_options, "ref", "${{ github.event.pull_request.head.sha }}"),
        "no persist-credentials": delete_in(checkout_options, "persist-credentials"),
        "persist-credentials: true": set_in(checkout_options, "persist-credentials", True),
    },
)
UNSAFE_CHECKOUT = Invariant(
    check_no_unsafe_checkout,
    {
        "the option on the checkout": set_in(checkout_options, UNSAFE_OPTION, True),
        "the option in a run": append_run(verify_step, f" --{UNSAFE_OPTION}"),
    },
)
HEAD_IS_DATA = Invariant(
    check_head_is_data,
    {
        "a fetch into a branch": lambda d: fetch_step(d).__setitem__(
            "run", fetch_step(d)["run"].replace(HEAD_REF, "refs/heads/pr")
        ),
        "a checkout of the fetched head": append_run(fetch_step, f"git checkout {HEAD_REF}\n"),
        "a second fetch of the head": append_run(fetch_step, 'git fetch origin "${HEAD_SHA}"\n'),
        "no fetch at all": lambda d: fetch_step(d).__setitem__("run", "true\n"),
    },
)
BODY_IS_DATA = Invariant(
    check_body_is_data,
    {
        "the body inlined into run": inline_body,
        "no env carries the body": delete_in(lambda d: verify_step(d)["env"], "PR_BODY"),
        "another expression inlined into run": append_run(verify_step, ' "${{ github.head_ref }}"'),
    },
)
CANCEL_IN_PROGRESS = Invariant(
    check_cancel_in_progress,
    {
        "cancel-in-progress: false": set_in(lambda d: d["concurrency"], "cancel-in-progress", False),
        "no concurrency group": delete_in(lambda d: d, "concurrency"),
    },
)


class RegimeWorkflowTest(unittest.TestCase):
    """The head's regime.yml holds every property; a failure message names the line to restore."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)

    def test_the_only_trigger_is_pull_request_target_into_main(self) -> None:
        check_trigger(self.doc)

    def test_the_token_is_contents_read_and_no_job_widens_it(self) -> None:
        check_permissions(self.doc)

    def test_every_checkout_takes_the_base_branch_without_credentials(self) -> None:
        check_checkout(self.doc)

    def test_no_step_names_the_unsafe_pr_checkout_option(self) -> None:
        check_no_unsafe_checkout(self.doc)

    def test_the_head_is_fetched_once_into_its_own_ref_and_never_checked_out(self) -> None:
        check_head_is_data(self.doc)

    def test_the_body_reaches_the_script_through_env_and_never_through_run(self) -> None:
        check_body_is_data(self.doc)

    def test_a_newer_head_cancels_the_older_run(self) -> None:
        check_cancel_in_progress(self.doc)


class RedCopyTest(unittest.TestCase):
    """Each check goes red on a copy of the workflow with its property taken away, so a regression cannot pass."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)

    def goes_red(self, invariant: Invariant) -> None:
        self.assertTrue(invariant.breaks)
        for label, mutate in invariant.breaks.items():
            with self.subTest(label):
                broken = copy.deepcopy(self.doc)
                mutate(broken)
                self.assertFalse(self.doc == broken, f"regime.yml already carries this edit: {label}")
                with self.assertRaises(AssertionError) as caught:
                    invariant.check(broken)
                self.assertIn("regime.yml", str(caught.exception))

    def test_the_trigger_check_goes_red(self) -> None:
        self.goes_red(TRIGGER)

    def test_the_permissions_check_goes_red(self) -> None:
        self.goes_red(PERMISSIONS)

    def test_the_checkout_check_goes_red(self) -> None:
        self.goes_red(CHECKOUT)

    def test_the_unsafe_option_check_goes_red(self) -> None:
        self.goes_red(UNSAFE_CHECKOUT)

    def test_the_head_fetch_check_goes_red(self) -> None:
        self.goes_red(HEAD_IS_DATA)

    def test_the_body_check_goes_red(self) -> None:
        self.goes_red(BODY_IS_DATA)

    def test_the_cancel_in_progress_check_goes_red(self) -> None:
        self.goes_red(CANCEL_IN_PROGRESS)

    def test_a_workflow_the_parser_cannot_read_fails_instead_of_passing(self) -> None:
        # Standing order 21: a failed read is never an absence. A parse error stops the suite, and a document that is
        # not a mapping is refused before any check could read its missing keys as "nothing to widen".
        with tempfile.TemporaryDirectory() as temp:
            broken = Path(temp) / "regime.yml"
            broken.write_text("on: [\n")
            with self.assertRaises(subprocess.CalledProcessError):
                load(broken)
            broken.write_text("- a list\n")
            with self.assertRaises(AssertionError):
                load(broken)


if __name__ == "__main__":
    unittest.main()
