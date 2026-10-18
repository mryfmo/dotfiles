# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a02

These are candidates only; nothing is promoted.

1. [memory:failure] A probe that reads a CLI's output to decide a destructive branch has to pin the output format with an option. The environment does not do it. The round-1 fix read `uv tool dir` to skip an uninstall uv could not do. In a herdr pane `FORCE_COLOR` and `CLICOLOR_FORCE` made uv wrap the path in colour codes, so the check never matched and the uninstall was skipped while hcom was installed. #405 had already fixed the same cause with `uv tool list --color never`. Grep the tree for an earlier fix of a CLI's output before parsing that CLI again, and make the test stub colour unless told not to.
2. [memory:failure] "Move aside" into the run's `mktemp -d` directory is deletion: the EXIT trap removes it on success and on SIGTERM. A file the user owns that a step displaces goes to a kept path the output names.
3. [memory:decision] A test fixture that is kinder than the real tool hides the finding. The fake npm overwrote any entry, so EEXIST never showed. Make the fixture apply the real tool's rule (npm's bin-link ownership: its own relative or absolute link into this prefix's package). The existing happy-path test then goes red too, and that is the evidence the fixture changed.
4. [memory:decision] Extglob `@(…)` inside `[[ ]]` needs bash 4.1 or later. macOS `/bin/bash` is 3.2.57, so two plain patterns are the portable form; `bash -n` with `/bin/bash` checks it.
5. [memory:failure] `tests/unit/test_update_agent_assets.py` cannot run in this sandbox (macOS `mktemp -d` without a template ignores `TMPDIR`). Plan its red and green runs outside the sandbox from the start, and record the sandboxed failure as evidence.
