# T97 isolation and recovery

Worker: codex-security-dot-a007, worker-e. Codex workspace-write / approval never. Shared Git config is read-only; objects/refs/logs/worker-e metadata are writable.
Initial branch creation failed while writing tracking config. Under revision 1 re-task, `git switch fix/claude-sandbox-github-calls` recovered clean tracked state; no reset, lock removal or config mutation by this worker.

All three scratch sessions used the generated express Claude profile, print mode, --no-session-persistence, --permission-prompts none, --tools Bash, --strict-mcp-config and JSON streaming. No settings override or unsandboxed Bash input was supplied. Parent process ran inside this Codex sandbox. Scratch has distinct mount/network namespaces, HTTP/HTTPS proxy variables and one additional seccomp filter. gh AF_UNIX creation denial reproduced directly. No credential contents or socket payloads traced.

Three scratch CLI invocations exited 0 after reporting child command failures; this is not a claim those child gh commands succeeded. Temporary prompt/transcript/metadata-only trace files live under /tmp/t97-*. Only tool inputs/results, not scratch reasoning/signatures, are in repo evidence. Main checkout was read only. No actual push, no permission relaxation, no product edits. Only five task artifacts remain untracked.

Final continuation: branch docs/claude-sandbox-gh-keyring-limit starts at 04bce61b; product head 8ffa554738c6f8b524f33787332a31337e935122 is pushed and PR258 created. Two docs are the only product edits. Seven orchestration artifacts remain local for transfer. A fourth scratch express session performed only read-only mountinfo/test -w checks for Bot P2; shared objects/refs/logs/worker-e metadata are actually rw while common config stays ro. No permission override, write probe, token provisioning or actual data push from scratch occurred.
