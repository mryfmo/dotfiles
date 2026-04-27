#!/usr/bin/env python3
"""Refresh mkdocs-toc-md output without triggering its build-command warning."""

from __future__ import annotations

import sys

from mkdocs.__main__ import cli


# mkdocs-toc-md decides whether to warn by checking for the literal word
# "build" in sys.argv. This command is the intentional first pass of a two-pass
# docs build, so keep the real Click arguments explicit while avoiding that
# false-positive warning in CI logs.
sys.argv = [sys.argv[0], "toc-refresh"]
cli(args=["build", "--clean"], standalone_mode=True)
