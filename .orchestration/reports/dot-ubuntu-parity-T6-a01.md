# dot-ubuntu-parity-T6-a01 — worker report

status: ready_for_review

## Objective

The linux+client-gated `.local/bin/server` block added to
`home/.chezmoiremove` in T3/B7 is a permanent no-op: chezmoi excludes
`.chezmoiignore`d target paths from target-state computation entirely, so
`.chezmoiignore` wins over `.chezmoiremove` for the same path. Verified
before editing that `home/.chezmoitemplates/chezmoiignore.d/ubuntu/client`
does list `.local/bin/server` (see validation) — confirming the conflict is
real in this repo, not hypothetical. The residual directory this entry was
meant to clean up was already removed manually by the orchestrator on the
real machine.

## Work done

One commit, `7813ebc`:

`fix(chezmoi): drop ineffective .chezmoiremove entry for ignored path`

- Removed the
  `{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}.local/bin/server{{ end }}`
  block from `home/.chezmoiremove`. No other lines touched.
- Checked `tests/unit/` for any reference to `.chezmoiremove` content or
  this specific path — none found (the one `.local/bin/server` hit in
  `tests/unit/test_runtime_health.py` is an unrelated bashrc-guard fixture
  from B7, not a `.chezmoiremove` assertion; confirmed by reading its
  context).

## Branch

Per the task's instruction, fetched `origin` and verified it already
contains T5 (`chore(orchestration): accept T5` / T5's artifact commit /
the timer-ordering fix), then created `fix/drop-ineffective-chezmoiremove`
from `origin/main` in this worktree.

## Validation

`uv run python -m unittest discover -s tests/unit -v` — 376 tests, OK, 1
pre-existing skip. Verbatim tail in
`.orchestration/validation/dot-ubuntu-parity-T6-a01.md`.

## CompactionDB

Registered a `[memory:decision]` about ignore-beats-remove semantics:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "chezmoi の .chezmoiignore は .chezmoiremove に優先する: ignore されたターゲットパスは target state の計算から除外されるため、.chezmoiremove に同じパスを列挙しても宣言的には削除されない(chezmoi の仕様)。ignore 済みパスの残骸を掃除するには、手動削除するか ignore 自体を解除する必要がある。"
```

Returned ID: `e9d5e7c0-93f7-47c2-8899-25df46df03b9`

## Scope / forbidden actions

Only `home/.chezmoiremove` and this task's own artifact paths touched. No
push, no PR, no `chezmoi apply`, no writes under `$HOME`, no commits to
`main`.

## cost

n/a (runtime does not expose token/cost figures to this session).
