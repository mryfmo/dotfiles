# T97 learning triage

Validated finding: gh backed by the host keyring can return HTTP 401 in Claude Linux sandbox even though GitHub networking is allowed. The cause is AF_UNIX creation denied before D-Bus access; parent gh uses /run/user/1000/bus successfully. Capture socket/connect only with strace, never read/write payloads, to establish this without exposing credentials. Path-specific allowUnixSockets does not fix Linux seccomp filtering. Do not expand domains or allow all Unix sockets.

Validated recovery: branch creation with automatic upstream tracking attempts shared Git config. An interrupted switch can update index/worktree and create the branch before updating HEAD. Under explicit re-task, switching to the already-created branch recovered without reset. Future branches use --no-track; pushes omit -u.

No rule promotion performed. The T97 report includes a concrete residual-limit sentence for orchestrator re-tasking and a CompactionDB handoff; neither is represented as accepted policy.

Final Bot-review lesson: do not infer Claude's effective Git metadata permissions solely from launcher arguments or static sandbox settings. A later read-only scratch probe directly showed writable shared objects/refs/logs/worktree metadata, corroborated by test -w, despite no explicit launcher grant for Claude. This supports the proposed not-applicable disposition for P2 comment 4178090986 in this tested runtime only. Initial fetch success alone was not used to prove new-object writes.

Acceptance revision: successful SSH push dry-run is not evidence that HTTPS push using gh as a credential helper succeeds. The orchestrator's T72/T76/T95 evidence requires retaining that gh-backed push exception until credential provisioning. Preserve the transport/credential-helper scope in future reproduction conclusions; public fetch and authenticated push need not use the same credential path.

## Round 2 learning — global policy scope and authenticated fetch

The successful public fetch / SSH push dry-run does not validate gh-backed authenticated HTTPS operations. gh credential helper also serves private HTTPS fetches. Because the SKILL and Claude rule are installed globally, current repository visibility cannot justify omitting that case. The independent reviewer and task audit identified this; the orchestrator's round-2 revision supersedes its earlier public-only scope disposition. Both policy sentences now include authenticated git fetch while keeping the sandbox-first requirement. Do not generalize successful unauthenticated or SSH probes to the HTTPS credential-helper path. Learning remains task-local; no rule promotion or CompactionDB write by this worker.
