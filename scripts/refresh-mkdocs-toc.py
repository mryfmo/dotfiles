#!/usr/bin/env python3
"""Refresh mkdocs-toc-md output without triggering its build-command warning."""

from __future__ import annotations

import sys

# MkDocs does not expose a stable public Python API; this intentionally uses the
# internal Click entry point so we can keep sys.argv free of the literal "build"
# token that mkdocs-toc-md treats as a warning condition.
from mkdocs.__main__ import cli


def main() -> None:
    """Run the intentional first pass that refreshes the generated TOC page."""
    sys.argv = [sys.argv[0], "toc-refresh"]
    cli(args=["build", "--clean"], standalone_mode=True)


if __name__ == "__main__":
    main()
