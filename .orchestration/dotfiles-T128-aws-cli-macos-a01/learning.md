# Learning triage: dotfiles-T128-aws-cli-macos-a01

These are candidates only; nothing is promoted.

1. [memory:failure] Two Linux tests of `test_aws_cli_acquisition.py` call macOS `mktemp -d` without the module's own `mktemp` shim. Under the Claude sandbox they fail with `mkdtemp failed on /var/folders/…: Operation not permitted`, on `origin/main` as on this branch (validation §5). Other tests in the module already carry the shim, with the comment "macOS mktemp -d ignores TMPDIR".
   - A seat that runs the module in its sandbox sees two failures that are not its own.
   - Mechanism candidate: the two tests take the shim, as their neighbours do. That is a one-line environment change each, which this task's "the Linux tests stay as they are" kept out of scope. Until then, a validation file shows the `origin/main` baseline beside the run, as this one does.
2. [memory:decision] An upstream installer the task relies on is worth reading before the branch is written, as reference data through WebFetch. Here it confirmed the three facts the branch needs: the install root under `XDG_DATA_HOME`, the symlink under `XDG_BIN_HOME`, and the exit 0 for an installed version. It also surfaced two behaviours the task did not name: the second version.txt fetch and the exit 2 on a downgrade. They went into the alive PONG before the Bot saw the PR.
3. [memory:decision] A shell function named `bash` in the sourced prelude intercepts the script's `bash <install.sh>` call, while the harness's own `bash -c` resolves the real binary on PATH. Assignments in the prefix of a call (`XDG_DATA_HOME=… bash …`) are visible inside the function, so the test reads them there. No PATH stub named `bash` is needed, and none could be used, since the harness would run it.
