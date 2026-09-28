# T33d learning triage

## Candidates

1. A fake CLI must follow the real I/O contract of the caller. If the
   caller passes input via argv and leaves stdin inherited, a fake that
   reads stdin blocks on the test runner's stdin, which can be an open
   pipe or socket. The test then fails or passes depending on how the
   suite was launched, and it looks like a load flake.
2. To tell load flakes from stdin flakes, rerun with `sleep N | <test>`
   (an open pipe) and with `< /dev/null` (EOF). Deterministic flipping
   between the two proves stdin dependence. Separately, run with every core
   busy and stdin at EOF to rule load in or out.
3. Raising a timeout does not fix a blocking read: it only moves the hang.
   Always check whether the timed-out call was waiting on I/O before adding
   headroom.
4. Product hardening candidate (not done: product code is out of scope):
   subprocess calls to external CLIs from hooks/tools should set
   `stdin=subprocess.DEVNULL` unless they intentionally feed input
   (`executable_permgate` `classify()` codex branch).

## Promotion

None. These are candidates only.
