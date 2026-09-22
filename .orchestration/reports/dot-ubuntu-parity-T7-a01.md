# dot-ubuntu-parity-T7-a01 — worker report

status: ready_for_review

## Objective

CI run 35798238740 (Unit test / ubuntu-latest client) failed 4 T4 mock-based
bats tests:

- `tests/install/ubuntu/client/gnome_settings.bats:11` "main is a no-op
  without gsettings on PATH"
- same file `:21` "main is a no-op headless even when gsettings exists"
- `tests/install/ubuntu/client/misc.bats:52` "install_chromium is a no-op
  when snap is unavailable"
- `tests/install/ubuntu/client/zed.bats:51` "main downloads, verifies, and
  links zed…"

The task's stated root cause (confirmed by the CI BW01 warning) is that
`run env PATH=<mock-dir-only> ... bash ./install/...` fails because `env`
itself must resolve `bash` through that same stripped PATH; with no
coreutils in the mock dir, that resolution fails with exit 127 before the
script under test ever runs.

## What I found by actually running each test (per the task's explicit "do

run bats -f this time" instruction)

Reproduced the failure for all 4 named tests individually via
`bats -f '<test name>' <file>` before touching anything (verbatim in
validation). Three of them exactly matched the stated root cause (BW01,
exit 127). **The 4th did not** — it never restricts PATH at all
(`env HOME=... bash -c '...'`), so it can't hit the exit-127 issue. Digging
into its actual failure (also in validation) turned up two more, real,
separate things:

1. The test's mocked `curl` builds a fake tarball, but unlike its two
   sibling `zed_artifact` tests in the same file, it never mocks `uname`,
   so `zed_artifact` returns the pinned checksum for whatever architecture
   the CI/dev host really is. The mocked `curl`'s fake content's real
   sha256 can never match that pinned constant, so
   `install_pinned_zed`'s checksum check always fails.
2. After fixing (1) so the checksum check passes, extraction still failed:
   `install_pinned_zed` in `install/ubuntu/client/zed.sh` does
   `mv "${tmpdir}/zed.app" "${staging}"` (moving into
   `${HOME}/.local/share/zed.app.tmp`) two lines _before_ its own
   `mkdir -p "$(dirname "${ZED_APP_DIR}")"` runs. On any real machine
   `~/.local/share` already exists, so this is invisible there — but on a
   genuinely fresh `$HOME` (exactly what a bats test's isolated
   `BATS_TEST_TMPDIR` is, and exactly the "fresh bootstrap" class of bug
   T5 fixed for the usage-snapshot timer), the intermediate `mv` fails
   because its destination's parent directory doesn't exist yet.

Item (2) is a genuine bug in the install script itself, not in the test.
This task's `forbidden_actions` explicitly bars editing install scripts
(test-only), so I did **not** fix `zed.sh`. I worked around it in the test
only, by pre-creating `${BATS_TEST_TMPDIR}/.local/share` before calling
`main` — the same fixture-precondition pattern this same file's other test
already uses (it pre-creates its own `.local/share/zed.app` and
`.local/bin`). **Recommending a follow-up task** to reorder `zed.sh`'s
`mkdir -p "$(dirname "${ZED_APP_DIR}")"` to run before the first `mv`.

## Work done

One commit, `18ccbb9`:

`fix(tests): resolve interpreters and core tools under stripped PATH in T4 bats`

- `gnome_settings.bats` (2 tests) and `misc.bats` (1 test): changed the
  `bash` interpreter invocation to `/bin/bash` (absolute path) in the
  `env PATH=<mock> ... bash ...` calls, so `env` execs it directly without
  a PATH search. Matches the existing `/bin/bash -c '...'` convention
  already used in `tests/install/common/setup.bats` for the identical
  reason.
- `zed.bats` (1 test): added a `uname` mock (matching the file's sibling
  tests) and a `sha256sum` mock (returning the pinned constant directly),
  plus `mkdir -p "${BATS_TEST_TMPDIR}/.local/share"` before `main` runs.

No changes to any install script — only the 3 named `.bats` files, all
within `allowed_files`.

## Validation

Ran only the 4 named tests individually via `bats -f`, both before (to
reproduce) and after the fix (to confirm green) — never the full suite or
any other test in these files, per the task's explicit
`non-target-bats` prohibition (those do real apt/snap installs). All 4:
`ok`. Full verbatim transcripts, including the debugging steps that found
bugs (1) and (2) above, are in
`.orchestration/validation/dot-ubuntu-parity-T7-a01.md`.

`make format` clean (shfmt reports no diff on the 3 changed files).
`uv run python -m unittest discover -s tests/unit -v`: 376 tests, OK, 1
pre-existing skip. `uv run --with pyyaml scripts/validate-agent-assets.py`:
ok.

## Branch

Fetched `origin`, confirmed it already has T6 merged, created
`fix/t4-bats-stripped-path` from `origin/main`.

## CompactionDB

Two entries registered:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "この repo の install-script bats テストはローカル実行禁止(実システムを変異させるため)だが、新設するモックベース(no-op/stub)テストは出荷前に bats -f '<テスト名>' <file> で個別実行して確認する。env PATH=<mockのみ> bash script の形は env が bash 自体を PATH 解決できず exit 127 で死ぬ — 対処は env PATH=... /bin/bash script のようにインタープリタを絶対パスで起動し、env には script が見るPATHだけを渡すこと(既存 tests/install/common/setup.bats の /bin/bash 直起動パターンと同じ規約)。"
```

→ `b3a6c98a-763a-4f64-b803-33c48b3c20dd`

```
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content "install/ubuntu/client/zed.sh::install_pinned_zed は mv \"\${tmpdir}/zed.app\" \"\${staging}\" を、staging の親ディレクトリ (\${HOME}/.local/share) を mkdir -p する前に実行している(mkdir は2行後)。実機では ~/.local/share が既に存在するため気付かれないが、T5 が systemd timer で踏んだ fresh-bootstrap(~/.local/share 未作成)と同じ条件で real mv が失敗する。T7 のスコープでは install スクリプト本体の変更が禁止のためテスト側の fixture(mkdir -p \"\${BATS_TEST_TMPDIR}/.local/share\")で回避し、zed.sh 側の mkdir 順序修正は別タスクへ切り出すことを推奨。"
```

→ `aac17d27-411a-49f0-a892-b2c47bd3771d`

## Scope / forbidden actions

Only the 3 named `.bats` files touched, no install-script edits, no other
bats tests executed, no push/PR/`chezmoi apply`/`$HOME` writes/commits to
`main`.

## Recommendation for the orchestrator

Please open a small follow-up task to fix `install/ubuntu/client/zed.sh`
itself: move the `mkdir -p "$(dirname "${ZED_APP_DIR}")"` line (currently
after the first `mv`) to before it, so `install_pinned_zed` works
correctly on a genuinely fresh `$HOME` and not just on machines that
already have `~/.local/share`.

## cost

n/a (runtime does not expose token/cost figures to this session).
