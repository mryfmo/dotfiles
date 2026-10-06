# Learning: dotfiles-T103-gh-auth-stores-a01

- **A token in the environment hides an empty store.** `GH_TOKEN` and its siblings take precedence over every `GH_CONFIG_DIR`, so `gh auth status` succeeds for a store that holds nothing. The login script and the doctor both clear those variables before asking gh.
- **Interactive steps in a bootstrap need two gates.** `setup.sh` also runs in the `public-bootstrap` CI jobs. The login step is skipped on CI and without a terminal, and the script itself refuses to prompt without one, so nothing can hang waiting for a device code.
- **Test a terminal-only path with a pty, not by faking `-t`.** `pty.openpty()` gives the script a real terminal on stdin, so the login branch runs exactly as it would for the operator.
- **A doctor report line is neither a failure nor a warning.** `check-agent-runtime.py` treated every non-`WARN:` message as an error and as a repair candidate. The new `found:` lines needed their own predicate in the printer, the error filter and `repair_actions`.
- **Bot sweep scope:** a Bot review on an earlier head blocks the merge as an unresolved thread. Sweep every Bot review and inline thread on the PR after the last push, not only the items on the final head.
