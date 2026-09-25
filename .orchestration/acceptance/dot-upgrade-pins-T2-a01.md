# Acceptance: dot-upgrade-pins-T2-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Independent re-derivation

- Crit v0.20.3 and Zed v1.21.0 Linux SHA256 values equal the GitHub release asset digests (gh api releases/tags).
- `MISE_CONFIG_DIR=<worktree>/home/dot_mise mise install --locked`: all 33 tools resolve; main pair untouched afterwards.
- `make unit-test` 391 OK, `validate-agent-assets.py` OK, `git diff --check` OK, review guard satisfied with the worker receipt.
- Version-consumer hits grep'd by the worker; only historical .orchestration records remain.
- Spill into main via the ~/.config/mise symlink was reversed by the worker (main pair clean); root fix tracked as dot-mise-symlink-T3-a01.

## effects

tool-refresh; agent-assets; herdr-integration; repo-bootstrap; brew-metadata — reverse mappings stated in the report (manifest steps via remove-agent-asset; brew-metadata declared irreversible: cache timestamps only, no package change). Accepted.

## Integration

Committed as chore(mise) on `chore/upgrade-pins`, PR #171.

## Revision 1 (PR #171 CI)

status: revise — `tests/install/common/mise.bats:135` hardcodes herdr 0.9.0 (bats not ok 57 on ubuntu server). Missed exact-version consumer; orchestrator's consumer list omitted it too. Fix: make the assertion version-agnostic (assert the herdr key is pinned, not a literal version) so this consumer disappears.

## Revision 1 result

status: accepted — mise.bats asserts the herdr key with any non-empty version; no literal old versions remain under tests/. Pushed as 73a03ae on PR #171.
