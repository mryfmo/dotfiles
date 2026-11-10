## Findings

- P1 (high) [f2 s10] scripts/orchestrator/acp-relay.py:284: The Router can rename its writable broker directory and replace it with a symlink before shutdown; remove_socket then deletes a protected host file named sock through that link.
- P1 (high) [f2 s10] scripts/orchestrator/acp-broker:963: After the same directory replacement, broker_cleanup follows the link and deletes host files named sock or acp-*, contradicting the Threat table's claim that renaming deceives only the Router.
- P2 (medium) [f1 s6] scripts/orchestrator/acp-relay.py:232: A Router that replaces the socket entry or its parent with a symlink between bind and chmod can make the unsandboxed relay change a host file's permissions.

## Reproduced

- acp-record-place unit tests: 13 ran, 1 skipped, all others passed.
- Scratch directory replacement followed by Relay.remove_socket(): a protected file named sock was deleted.
- Scratch directory replacement followed by the broker's rm -f sock operation: a protected file named sock was deleted; chmod through the replaced path changed its mode.
- Three focused broker integration tests could not reach their assertions: this audit sandbox denied Unix-socket bind with EPERM.
- bash -n, git diff --check, and byte comparisons of the four source/deployed lever pairs passed; git status remained clean.

## Notes

The record helper's focused tests passed. The independent socket cleanup paths still cross the Router-writable directory by name, so the PR's residual-risk account does not cover host-file deletion.

Blocking: 2
Filed: 1
Verdict: incorrect
