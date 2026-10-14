# Learning triage: dotfiles-T128-gate-wrapper-path-a01

These are candidates only; nothing is promoted. The candidates of a05 and a06 stand (`.orchestration/dotfiles-T128-orchestrator-tools-a05/learning.md`, `.orchestration/dotfiles-T128-orchestrator-tools-a06/learning.md`).

1. [memory:failure] On macOS, `mktemp -d` without a template ignores `TMPDIR` and writes under the per-user `/var/folders/…/T`. The Claude sandbox denies that path ("mkdtemp failed … Operation not permitted"). A task text that says `mktemp -d` must become `mktemp -d "${TMPDIR:-/tmp}/<name>.XXXXXX"`, which honours `TMPDIR` on BSD and GNU alike.
2. [memory:decision] Under a private PATH, a stub has two constraints:
   - It needs an absolute shebang (`#!/bin/bash`), and it must record with builtins or absolute paths: `printf`, `pwd -P`, `/usr/bin/env`, `/bin/cat`, `/usr/bin/readlink`.
   - The trap removes the directory before the test can read it, so the stub lists the directory while it runs.
3. [memory:failure] BSD `ln -s` accepts an empty target, while GNU `ln -s` refuses it. A guard against an empty resolution must come before the `ln`. The mutant without that guard exited 0 on macOS and 1 on Linux, and only the test's exact exit-code check caught it on both.
4. [memory:decision] To resolve a binary outside mise shims in one call, use `mise which <name> 2> /dev/null || command -v <name>` in the trusted cwd, then refuse a path that is not absolute or that lies under `*/shims/*`. This matches "`mise which` when `command -v` is a shim or mise knows the name, else `command -v`": each case either refuses or picks the same binary.
