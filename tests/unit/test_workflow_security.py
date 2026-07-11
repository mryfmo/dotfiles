import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
EXPECTED_PERMISSIONS = {
    "agent-assets.yml": {"contents": "read"},
    "docs.yml": {"contents": "write"},
    "macos.yaml": {"contents": "read"},
    "remote.yaml": {"contents": "read"},
    "test.yaml": {"contents": "read"},
    "ubuntu.yaml": {"contents": "read"},
}
CHECKOUT_CREDENTIAL_EXEMPTIONS = {
    (
        "docs.yml",
        "deploy",
        "Checkout repository",
    ): "make deploy pushes the generated documentation",
}


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
            if (
                candidate.strip()
                and len(candidate) - len(candidate.lstrip()) <= step_indent
            ):
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


class WorkflowSecurityTest(unittest.TestCase):
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

    def test_workflows_have_exact_top_level_permissions(self):
        actual = {
            path.name: top_level_permissions(path.read_text())
            for path in sorted(WORKFLOWS.glob("*.y*ml"))
        }
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
        self.assertEqual(
            dict.fromkeys(CHECKOUT_CREDENTIAL_EXEMPTIONS, 1), exemption_hits
        )
        self.assertTrue(
            all(reason.strip() for reason in CHECKOUT_CREDENTIAL_EXEMPTIONS.values())
        )

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


if __name__ == "__main__":
    unittest.main()
