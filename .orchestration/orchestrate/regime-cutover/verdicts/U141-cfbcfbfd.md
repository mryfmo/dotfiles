# U141 audit verdict: PR 633 (mryfmo/dotfiles), head cfbcfbfd6592442b556caac396255dbfb8e76fa1, base 8227cc52d9bfd98eb530309578444c5342a6e9af

## Findings

- P3 (high) [f1 s1] scripts/orchestrator/hcom-seat:217: the comment and the PR body say the srt line is refused "before anything is made", which overstates: the private tool directory, its links and the git state directories are made earlier by pre-existing idempotent code, so the refusal runs at the earliest point after srt is pinned, before any seats root, store or process exists (note N1 below); wording only.
- P3 (high) [f1 s1] scripts/generated-agent-outputs.json:378: the generated outputs index moved with the pin refresh although SCOPE names only the manifest pin line; it is the generator write run's own output and render-check needs it (note N2 below); scope wording only.


## Reviewer preamble

Verdict: APPROVE (mergeable). No blocking finding. Two notes (N1 wording, N2 scope) for the record; neither needs a change before merge.

Audited 2026-11-03 from the coordinator's checkout (read-only) against `git archive` trees of head and base under
`$TMPDIR/dotfiles-wt/U141-audit-1793692283/` and the worker tree `$TMPDIR/dotfiles-wt/U141` (clean, at head).
Brief: `.orchestration/orchestrate/regime-cutover/briefs/U141-pin-srt-doctor-row-launcher-refusal.md`.

## Diff shape

11 files, +164/-8. Every changed path is in SCOPE except `scripts/generated-agent-outputs.json` (see N2). No `/tmp`
literal, no private design directory name in the diff, the commit message or the PR body. Commit unsigned (%G? = N),
message ends with the required Co-Authored-By line. The `hcom-seat` change is +17 lines: a comment, `readonly SRT_LINE=0.0`,
and the four-statement refusal after `pin_exec srt`; no seat setting, canary or other behaviour touched (FORBIDDEN met).

## (1) Version read in hcom-seat: status-first, fails closed, checked argv

`scripts/orchestrator/hcom-seat:1598-1608` (head):
- `srt_version=$("${srt_cmd[@]}" --version 2> /dev/null)` followed by `or refuse ...` on the same statement: status checked
  first. `srt_cmd` is the argv `pin_exec srt` produced (`pinned`: physical interpreter + physical file), not a PATH lookup.
  The fake-driven test confirms the call reaches the fake by its pinned argv with the private tool PATH only
  (`test_the_launch_path_never_inherits_a_caller_path_entry`).
- Empty output: after first-line/first-token trimming the empty string fails the regex and refuses (`cannot read the srt version from ''`).
- Order: `refuse` is `echo >&2; exit 2`. No seats root (mkdir at 1661), no hcom store (1863), no seat directory, no
  hcom/herdr/omp process exists before line 1598. Test asserts `not Path(seats).exists()`, no omp/hcom call, and `[["--version"]]` as the only srt calls.
- N1 (wording, not a defect): "before anything is made" (comment at 217, PR body) is broader than the truth. Before the
  check hcom-seat already creates/refreshes the private tool directory `~/.local/state/hcom-seat/tools` and its links
  (831-884), runs the pinned mise, and `git_state_check` (called at 1082, non-dry-run) creates absent `info/`, `hooks/`
  and `config.worktree` in the repository's git common dir. All pre-existing behaviour, idempotent, and required to find
  and pin srt before it can be run, so the check is at its earliest possible point. The brief's own bar ("before any seats
  root or process exists"; the second comment's "no seats root, store or process exists yet") is met exactly.

## (2) Regex and major.minor comparison: no bypass found

Regex `^([0-9]+\.[0-9]+)(\.[0-9A-Za-z.+-]+)?$` over the first token of the first line, then `[[ ${BASH_REMATCH[1]} == "${SRT_LINE}" ]]` (quoted, string equality).
Probe results (bash, same expressions):
```
PASS:   0.0.81 ; 0.0 ; 0.0.81-beta.1 ; 0.0.81.2 ; "0.0.81 (build 7)" (token 0.0.81) ; 0.0..
REFUSE (unparsable): 0.0foo ; 0.0-rc1 ; v0.0.81 ; "srt 0.0.81" ; "" ; " 0.0.81" ; 0.0.81<TAB>x ; 0.0.81<CR> ; 0.0.* ; 0.0.81;rm
REFUSE (other line):  0.01.5 (line 0.01) ; 00.0.81 (line 00.0) ; 0.1.0 (line 0.1) ; 1.0.81 (line 1.0)
```
A `0.0` prefix cannot smuggle another line: anything after `0.0` must be `.`+token or end of string, and `0.01`/`00.0`
compare unequal. `v` prefix and trailing text in the same token refuse. Trailing text after a space is dropped as a
second token, which is the intended tolerance for `<version> (<build>)` forms. Bare `0.0` and `0.0..` pass; both name
the 0.0 line and the mise pin holds the exact release, so this is not a bypass of the comparison.
Real srt on this host: `srt --version` prints exactly `0.0.81` + newline (od-verified), exit 0.

## (3) check_srt in scripts/check-tools.sh:238-282

- Resolution: `if ! target="$(mise which srt 2>/dev/null)"` or empty: status checked. Fallback `command -v srt` with
  `or true` is the one absorbed status; the following `-z`/`-x` test governs it and both read failure and absence
  produce the optional warning the brief prescribes for an absent srt. Acceptable; not a producer decision that could read as a pass.
- Pin reader: `pin="$(awk -F'"' '/^"npm:@anthropic-ai\/sandbox-runtime" = "/ { print $4; exit }' "$config")"` with
  `or pin=''`: status checked; result must match `^[0-9]+(\.[0-9]+)+$` or the next config is tried; applied
  `~/.config/mise/config.toml` first, then `${BASH_SOURCE[0]%/*}/..~/config.toml` (same idiom as check_hcom).
  `latest`, an inline-table form, a missing line, or an unreadable file all fall through; no pin anywhere is a required failure (fails closed).
- Version: `output="$("$target" --version 2>/dev/null)"` failing or empty is a required failure; first line, first token,
  exact string compare with the pin; difference is a required failure naming both.
- Probes (fake srt, `mise(){ return 1; }`): applied pin 9.9.9 vs installed 0.0.81 gives `required failed: srt 0.0.81 differs from the pin 9.9.9`, req=1;
  applied `latest` falls back to checkout, req=0; applied inline-table falls back, req=0; `latest` in both gives `no exact sandbox-runtime pin`, req=1;
  applied absent + checkout path unreadable gives the same, req=1; `v0.0.81` req=1; `srt 0.0.81` req=1 (token `srt`); empty output exit 0 gives `printed no version`, req=1;
  `mise which` returning a path takes precedence over PATH.
- Applied config: `home/dot_config/mise/config.toml.tmpl` is `{{ include "dot_mise/config.toml" -}}`, so the rendered file
  carries the same `"npm:@anthropic-ai/sandbox-runtime" = "0.0.81"` line the awk anchors on once `make update` runs.
- Note: an applied config holding a stale exact pin is compared (not the checkout's); that is the brief's design ("the pin of the applied config").

## (4) Installed copy and sha256 pins

`cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat`: identical.
sha256 of both: 4f2e395852acd6ba898793e1b3d92b1153982f24033fed8d35aa487224c397a4, equal to
`home/dot_agents/agent-config.yaml:852` (claude.levers.sha256 hcom-seat) and `scripts/generated-agent-outputs.json:378`.
`make render-check`: "generated agent configs are up to date", exit 0. `make validate-agent-assets`: "agent asset validation ok", exit 0.
`test_lever_self_check` passes (installed copies are the checkout bytes).

## (5) Unit test and red proof (reproduced)

New test `test_an_srt_of_another_line_is_refused_before_anything_starts`: subtests 0.1.0, 1.0.81, fail, empty each refused
(exit 2, empty stdout, stderr names `0.0 line` and either `srt <v> is not of the 0.0 line hcom-seat encodes` or
`cannot read the srt version`), no seats root, no omp/hcom call, only `--version` reached srt; then 0.0.99 launches with one omp call.
Existing assertions adjusted to account for the extra `--version` call (two places), nothing weakened.
- Green (head archive): Ran 1 test in 13.935s, OK.
- Red (8227cc52 archive + new test and fixture copied in; grep -c SRT_LINE on its hcom-seat = 0):
  FAILED (failures=5): each of the four injected versions launched ((0, ...) != (2, '')) and the final `5 != 1` omp count; Ran 1 test in 18.688s.
  Matches the worker's pasted red proof.
- Full modules: test_hcom_seat + the three others on the head archive: Ran 135 tests in 616.641s, 1 error, 1 skip;
  the single error is test_supply_chain_policy running `git ls-files` in a non-repository (archive artefact). Rerun of
  test_lever_self_check, test_pin_records, test_supply_chain_policy in the worker tree (a real repo at head): Ran 62 tests in 26.128s, OK.
  So all 135 pass (73 seat tests in the archive, 62 in the worker tree).

## (6) Bats cases do not read the runner's real srt or mise

All three cases define `mise() { return 1; }` inside the `bash -c` after sourcing, so `mise which` never reaches a real mise.
Cases 1-2 put the fake directory first on PATH (`PATH="${bin}:${PATH}"`) and use a scratch HOME with no applied config,
so the pin is read from the checkout config through the script's own fallback. Case 3 uses PATH=/usr/bin:/bin and an
empty HOME. Fake `--version` scripts are generated per case (pin value, 9.9.9, exit 1). CI runs tests/install/common/
via scripts/run_unit_test.sh:56 on every matrix target; not run on the host (policy met).

## (7) Acceptance commands (run by the auditor on the head archive; A2 against the host's srt and applied config)

```
A1  python3 -I scripts/pin_records.py mise-holds home/dot_mise/config.toml
    npm:@anthropic-ai/sandbox-runtime ; npm:ccstatusline ; npm:ccusage ; npm:prettier ; npm:pnpm
    grep -c 'sandbox-runtime" = "latest"' home/dot_mise/config.toml -> 0
A2  found:   srt -> ~/.local/share/mise/installs/npm-anthropic-ai-sandbox-runtime/latest/bin/srt (pin 0.0.81)
    0.0.81
    req=0            (host applied config still says latest; the fallback branch produced the pin)
A3  grep -c '@test "\[common\] check_srt' tests/install/common/check_tools.bats -> 3
A4  grep -c SRT_LINE scripts/orchestrator/hcom-seat -> 6 ; bash -n -> exit 0
A5  see (5)
A6  make render-check exit 0 ; cmp exit 0
A7  PR body Contract "Left out" names: no Linux measurement, no seat settings/canary change, host make update is the operator's step. Trusted: sentence present.
VERIFY  shellcheck 0.11.0 -x on hcom-seat and check-tools: exit 0
        scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check: 128 files already formatted, exit 0 (worker tree)
        uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed: exit 0 (worker tree)
```

## Notes

- N1 (wording): "refused before anything is made" overstates; see (1). Suggest "before any seats root, store or process
  exists" if the comment is ever touched again. No change required for this unit.
- N2 (scope): scripts/generated-agent-outputs.json is not named in SCOPE but is the generator's output index
  (generate-agent-configs.py OUTPUT_INDEX_PATH), written by the generator write run SCOPE allows; make render-check
  would fail without it. Accept as part of "through the generator write run only".
- No other enumeration of the mise holds needs the new entry: the skew check and the statusline smoke take tool names
  explicitly (npm:ccstatusline npm:ccusage); pinned-tool-version covers lint tools only; README names prettier as the lint hold.
- PR body: all required sections present, Verification lines agree with the auditor's results, red proof matches.

## Coordinator note

The fallback reviewer (Claude Fable 5.1, read-only, rules from origin/main AGENTS.md) wrote this file in its own shape with the line `Verdict: APPROVE (mergeable)` and two notes N1 and N2; the coordinator added the `## Findings` section above (the two notes as filed P3 findings, frequency 1 and severity 1 each) and the three closing lines so the readers of the store can parse it. The reviewer's text is unchanged. This head (cfbcfbfd) was red on CI (two test fixtures fake srt without a `--version` answer, decisions row `U141 round 2:`), so a round-2 head follows and gets its own audit with these findings as data.

Blocking: 0
Filed: 2
Verdict: correct
