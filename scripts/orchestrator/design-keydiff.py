"""Print the hashed front-matter keys of a design file that differ from HEAD's copy (plan 007 T718, C-15).

Run with `uv run --no-project --with pyyaml scripts/orchestrator/design-keydiff.py <design.md>`. A key whose
value is a mapping on both sides prints the sorted sub-keys that differ (`invariants ['INV-6']`); any other
change prints `<key> changed`. Read-only: it writes nothing, and its output is pasted into a review request
as data.
"""

import argparse
import subprocess
from pathlib import Path

import yaml

KEYS = "threat_model trust_anchors invariants implementing_tasks premises supersedes reset_of design_review".split()  # noqa: SIM905 (one line)


def front(text):
    """The YAML mapping between the file's first two `---` lines."""
    return yaml.safe_load(text.split("---\n", 1)[1].split("\n---\n")[0]) or {}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("design", type=Path, help="design file, relative to the current directory")
    path = parser.parse_args().design
    head = subprocess.run(["git", "show", f"HEAD:./{path}"], capture_output=True, text=True, check=True).stdout
    old, new = front(head), front(path.read_text())
    for key in KEYS:
        a, b = old.get(key), new.get(key)
        if a == b:
            continue
        if isinstance(a, dict) and isinstance(b, dict):
            print(key, sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)))
        else:
            print(key, "changed")


if __name__ == "__main__":
    main()
