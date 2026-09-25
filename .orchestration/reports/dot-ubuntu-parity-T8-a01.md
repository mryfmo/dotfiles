# dot-ubuntu-parity-T8-a01 — worker report

status: ready_for_review

## Objective

Follow-up to T7's discovery: `install/ubuntu/client/zed.sh::install_pinned_zed`
moved the extracted app into `${staging}` (under `${HOME}/.local/share`)
before its own `mkdir -p "$(dirname "${ZED_APP_DIR}")"` ran two lines
later, so the move failed whenever `~/.local/share` didn't already exist —
invisible on any real machine, but a genuine fresh-bootstrap failure (same
class as T5's usage-snapshot timer bug).

## Work done

One commit, `96e59cf`:

`fix(ubuntu): create zed parent dir before staging move`

- `install/ubuntu/client/zed.sh`: moved the single
  `mkdir -p "$(dirname "${ZED_APP_DIR}")" || return` line from after the
  first `mv` to right after `tar -xzf ... || return` (before
  `rm -rf "${staging}"` / `mv "${tmpdir}/zed.app" "${staging}"`). Pure
  relocation of one line — no duplication, no other logic touched.
- `tests/install/ubuntu/client/zed.bats`: removed the
  `mkdir -p "${BATS_TEST_TMPDIR}/.local/share"` workaround T7 added to the
  "main downloads, verifies, and links zed…" test, since the script itself
  now guarantees this directory exists before it's needed. Re-ran
  `bats -f 'main downloads, verifies, and links zed when not already
installed'` — still `ok` without the workaround, confirming the real
  fix (not the test) now covers the fresh-`$HOME` case.

Did not run any other bats test in this file (the two `zed_artifact` tests
and the "already installed" no-op test), per `non-target-bats`
forbidden_actions — verified by reading that none of them exercise
`install_pinned_zed`'s mv/mkdir ordering, so the reorder can't affect them.

## Validation

`bats -f` on the one named test (before removing the workaround it was
already passing due to T7's fixture; after removing the workaround it
still passes, now because of the real script fix — both states captured
in validation). `bash -n install/ubuntu/client/zed.sh` clean. `make format`
clean (shfmt reports no diff). `uv run python -m unittest discover -s
tests/unit -v`: 376 tests, OK, 1 pre-existing skip. `uv run --with pyyaml
scripts/validate-agent-assets.py`: ok.

## Branch

Fetched `origin`, confirmed it already has T7 (`chore(orchestration):
accept T7 and file T8 ...`), created `fix/zed-fresh-home` from
`origin/main`.

## CompactionDB

Registered a decision resolving T7's `[memory:failure]` record
(`aac17d27-411a-49f0-a892-b2c47bd3771d`):

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T7 で発見した install/ubuntu/client/zed.sh::install_pinned_zed の fresh-HOME バグ(failure id aac17d27-411a-49f0-a892-b2c47bd3771d)を T8 で修正: mkdir -p \"\$(dirname \"\${ZED_APP_DIR}\")\" を tar 展開直後・最初の mv より前に移動。これにより ~/.local/share が未作成の fresh bootstrap でも動作する。T7 がテスト側に入れた mkdir -p \"\${BATS_TEST_TMPDIR}/.local/share\" ワークアラウンドは不要になったため削除し、bats -f で ok を確認。"
```

Returned ID: `c614ffea-f9be-4564-8a48-ec2b9f7c76cb`

## Scope / forbidden actions

Only `install/ubuntu/client/zed.sh` and `tests/install/ubuntu/client/zed.bats`
touched, both within `allowed_files`. No push, no PR, no `chezmoi apply`,
no writes under `$HOME`, no commits to `main`, no non-target bats executed.

## cost

n/a (runtime does not expose token/cost figures to this session).
