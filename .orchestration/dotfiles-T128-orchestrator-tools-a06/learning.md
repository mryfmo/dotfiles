# Learning triage: dotfiles-T128-orchestrator-tools-a06

These are candidates only; nothing is promoted. a05's candidates stand (`.orchestration/dotfiles-T128-orchestrator-tools-a05/learning.md`).

1. [memory:failure] One boundary drew three P1s because each hole was fixed only once it was found. The boundary is a trusted script running a trusted module with an untrusted checkout as cwd. The three holes were the head's `make` target, uv's `.python-version` discovery, and the inherited environment. Specify the whole execution context of such a run in the first round:
   - a trusted interpreter resolved outside the checkout;
   - `env -i` with an allowlist taken from the module's own environment reads;
   - `-I -P`, plus `PYTHONSAFEPATH=1` for the children it starts;
   - no tool that discovers configuration from its cwd.
2. [memory:decision] A test that asserts an exact environment needs a stub whose own additions are known. Under `env -i`, macOS Python adds `LC_CTYPE` (PEP 538) and `__CF_USER_TEXT_ENCODING` to its `os.environ`, while bash exports `PWD`, `SHLVL` and `_`. Use a bash stub and allow its three names. Write paths into the stub's text, since `env -i` drops the variables stubs usually read (`CALLS`). Compare names only, so a failure prints no value.
3. [memory:failure] GitGuardian's generic-password rule fires on a string literal that follows a password-like name, and `PWD` counts. A set literal of environment-variable names with `PWD` first was reported as a hardcoded password. In code, keep no string literal directly after `PWD` (or `PASS`, `PASSWD`); name the set or put such a name last. Keep the literal out of commit messages too. A finding on an already-pushed commit stays in the PR scan until it is resolved in the dashboard.
