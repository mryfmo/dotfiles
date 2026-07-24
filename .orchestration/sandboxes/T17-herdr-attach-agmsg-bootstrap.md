# T17 sandbox record

- Codex workspace-write sandbox at `/Users/mryfmo/Workspace/dotfiles`.
- Mutating delivery behavior was exercised only through fake scripts under
  unittest temporary HOME directories.
- The hook-present fixture mirrors the real matcher object containing nested
  command hooks; it proves the already-configured path never invokes the fake
  delivery script.
- No live `delivery.sh set`, join, claim, send (except the required result
  signal), Herdr mutation, or chezmoi apply was executed.
- OpenSandbox was not available or needed; fake CLI/script tests isolated all
  side effects.
