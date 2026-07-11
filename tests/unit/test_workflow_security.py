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


if __name__ == "__main__":
    unittest.main()
