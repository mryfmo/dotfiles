# dot-ubuntu-parity-T9-a01 — worker report

status: ready_for_review

## Objective

Same CI failure as T5 ("Failed to enable unit: Unit file
usage-snapshot.timer does not exist") recurred after T5's `after_` fix
landed. Second, distinct root cause: `setup.sh`'s CI guard
(`is_ci && ... RUNNER_TEMP`, confirmed at `setup.sh:344`) forces the
Snippet-install/public-bootstrap job's apply to target a temporary destDir
under `RUNNER_TEMP`, not the real `$HOME`. The systemd unit files land
under that temp destDir, but `systemctl --user` always reads the real
user's `${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user` — no chezmoi
script ordering fix can make the unit visible there.

## Work done

One commit, `7e8ef1d`:

`fix(usage): only enable the timer when its unit is visible to the user manager`

- `home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl`:
  added a guard checking
  `[ -f "${XDG_CONFIG_HOME:-${HOME}/.config}/systemd/user/usage-snapshot.timer" ]`
  after the existing systemctl/XDG_RUNTIME_DIR guard. If the unit isn't
  there, prints "unit not visible to the user manager (temp destDir
  apply?); skipping" and exits 0 instead of calling `systemctl --user
enable` against a target it can never see. Existing guards and the
  sha256 embedding comments are unchanged.
- Documented in a 4-line script comment why a single file-existence check
  safely covers both the temp-destDir case and any future run-order
  regression: from this script's point of view, both failure modes look
  identical (unit not where systemd expects it), so one check handles
  both.

## Validation

Rendered the modified template with `chezmoi execute-template -S
"$(pwd)/home" --file ...` against this worktree's own source (confirmed
`.chezmoi.sourceDir` resolved to this worktree first) — this machine's
real chezmoi data already has `system=client`, `os=linux`,
`osRelease.idLike=debian`, so no data needed to be faked. `bash -n` on the
rendered output: clean.

Ran the rendered script directly in both required scenarios:

- (a) real `$HOME`: the unit file already exists and is already enabled on
  this machine (confirmed via `systemctl --user is-enabled
usage-snapshot.timer` → `enabled`), so `systemctl --user enable --now`
  ran idempotently; script exited 0.
- (b) `$HOME` pointed at an empty temp directory (no unit present): the
  new guard printed the skip message and exited 0 without attempting
  `systemctl` at all.

Both exit codes and the scenario-(b) message are pasted verbatim in
validation.

`make format` (the actual project gate — whole-repo `shfmt --diff .`)
clean; note that a _direct single-file_ shfmt invocation on this
`.sh.tmpl` flags a pre-existing indentation quirk in lines I didn't
touch, but the whole-repo walk (what `make format` actually runs, and
what every prior T2–T8 task was verified against) never picks up
`.sh.tmpl` files at all, confirmed by diffing the file at `HEAD` (before
my edit) directly — the same "diff" appears there too, so this is not
something I introduced or a real gate failure. `uv run python -m
unittest discover -s tests/unit -v`: 376 tests, OK, 1 pre-existing skip.
`uv run --with pyyaml scripts/validate-agent-assets.py`: ok.

Ran no bats tests in this task (none were named as targets; this task's
change has no bats coverage of its own).

## Branch

Fetched `origin`, confirmed it already has T8
(`chore(orchestration): accept T8`), created `fix/usage-timer-visibility`
from `origin/main`.

## CompactionDB

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "Snippet install CI は setup.sh の CI ガード(RUNNER_TEMP 配下の destDir 強制)により実 \$HOME ではなく仮 destDir へ適用する。systemctl 等、実ユーザー環境(実 XDG_CONFIG_HOME/実HOME)に副作用を及ぼすスクリプトは、chezmoi の run_once/run_onchange 順序(after_ 等)だけでは不十分——効果対象(unit ファイル等)が実際にその実環境から見える場所に存在するかをファイル存在チェックで確認し、見えなければ skip する。これは temp-destDir 適用と将来の順序退行の両方を同じ1つのガードで安全に覆う。"
```

Returned ID: `90f10560-425a-4dd8-9cb9-19bee270ef73`

## Scope / forbidden actions

Only the one named `.tmpl` file touched, within `allowed_files`. No push,
no PR, no `chezmoi apply`, no writes under the real `$HOME` (scenario (b)
used an isolated `mktemp -d` as `$HOME`, not the real one), no commits to
`main`, no non-target bats executed (none were in scope).

## cost

n/a (runtime does not expose token/cost figures to this session).
