# T39 learning triage

## Candidates

1. **Unix-socket allow-listing is macOS-only.** Claude Code's
   `sandbox.network.allowUnixSockets` has effect on macOS only; Linux and
   WSL2 ignore it, and only `allowAllUnixSockets` opens Unix sockets under
   the seccomp filter. Any Linux socket need (herdr CLI, agmsg-dispatch from
   a sandboxed Bash) must be decided as `allowAllUnixSockets` or
   `excludedCommands`, backed by live E2E. The live E2E before flipping
   `failIfUnavailable` should include a sandboxed `herdr` call on Ubuntu.
2. **Validators encode the old value.** When a task changes a manifest
   default, grep the validator for the old value first. Here
   `validate_claude_sandbox` required `failIfUnavailable is True`, so the
   approved `false` would have failed validation.
3. **Settle forbidden files before the carry commit.** When a carry would
   bring in forbidden files, drop them from the index before the carry
   commit, so no commit in the PR ever contains them. This matches a "must
   not create or keep" rule.
4. **Fetch raw docs markdown.** code.claude.com serves raw markdown at
   `<page>.md`. `curl` plus `grep` gives verbatim reference text where the
   WebFetch summariser truncates long pages.

## Promotion

None. These are candidates only.
