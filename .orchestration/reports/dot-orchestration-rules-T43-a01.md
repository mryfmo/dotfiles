# T43 report: graph symbol-coverage gate, UA hook scope rule, make render-check (dot-orchestration-rules-T43-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 2cf825882d080212e2f6fb0b29164861074308864d162289cdbd84c77949fe89 (sha256 verified against the main-checkout file and the `origin/main:` blob at 258339f)
- branch: `feat/orchestration-rules-T43` from origin/main 258339f. worker-c was clean and detached before the switch.
- commit: 557502b
- PR: https://github.com/mryfmo/dotfiles/pull/214 (revision 2 head 1843dd1 = fix 99c1174 + .orchestration-only merge of origin/main f45cf73; CI 12/12 pass incl. the CodeRabbit status check, nix skipped; MERGEABLE)

## Changes

1. **`scripts/ua-symbol-coverage.py`** (new, stdlib only, executable).
   - Usage: `<old-graph.json> <new-graph.json> [--repo-ref REF]` (argparse, hyphenated option).
   - Counts `function`+`class` nodes per `filePath` in each graph and prints a markdown table: file, old, new, def-like lines at REF, and a status of `ok`, `explained` or `REGRESSION`. It ends with `files: N, regressions: M`.
   - Exits 1 when any file has `new < old`, unless the source is gone at REF or its def-like line count is below `old`. Without `--repo-ref`, every decrease counts as a regression.
   - Def-like grammar:
     - Python: `def`, `async def`, `class`.
     - Ruby: `def`, `class`, `module`.
     - Shell: `function name` or `name()`, including subshell bodies.
     - Selected by file extension or shebang. `-` means the file type has no grammar.
   - Proof on real data: run against T41 revision 1 (c3afc7a, `--repo-ref 72b8901`), it reports exactly the 8 regressions the audit and orchestrator found, and exits 1. A self-compare of the current graph gives `regressions: 0`, exit 0.
2. **`tests/unit/test_ua_symbol_coverage.py`** (new): one test with two tiny synthetic graphs in a temporary git repo (a.py with 2 defs). Dropping a symbol gives exit 1 and a `REGRESSION` row. Keeping or adding symbols gives exit 0 and an `ok` row.
3. **Rules.**
   - `home/dot_config/claude/rules/understand-anything.md` gets two bullets: the coverage-table acceptance gate, and the rule that task workers treat the auto-update hook as out of scope unless `.ua/**` is in `allowed_files` and record "hook fired; not acted on" (the orchestrator never runs the graph update itself).
   - `home/dot_config/codex/AGENTS.md` `## Understand-Anything` mirrors both bullets in Japanese; that section already mirrors the UA rule.
   - The agmsg-orchestration SKILL gets the coverage sentence in "Review and integration invariants", the hook sentence as Worker Playbook step 13, and "Name the render check as `make render-check` …" in Orchestrator Playbook step 3, the task-file checklist.
4. **`make render-check`:** a new target running `uv run --with pyyaml scripts/generate-agent-configs.py --check`. The generator already prints `ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py`, and its behaviour is unchanged.
5. **README:** the model-selection/generator paragraph gains a sentence about `make render-check`, and the Understand-Anything paragraph gains one sentence for the coverage rule.

## Checks

- `make render-check`: up to date.
- `make unit-test`: 611 OK (1 skipped).
- `make validate-agent-assets`: ok.
- Self-compare: `regressions: 0`, exit 0.
- CI: see validation.

## Notes

- **Live finding from the T39 sandbox** (it became active in this worker session partway through T43, after the T39 settings were applied). Sandboxed Bash hit two failures:
  - Every `uv`-based make target (`make render-check`, `make unit-test`, `make validate-agent-assets`) fails with `Read-only file system (os error 30) at path "~/.cache/uv/.tmp…"`, because `~/.cache/uv` is not in `sandbox.filesystem.allowWrite`.
  - `gh` fails with `HTTP 401: Requires authentication`. Its token most likely comes from the keyring over a D-Bus Unix socket, and that socket is blocked on Linux, where `allowUnixSockets` is ignored. This is gap (a) from the T39 report.
  - Both commands succeed after the normal unsandboxed retry (`allowUnsandboxedCommands: true`). Section 1 of the validation file was run that way, and section 2 keeps the sandboxed failures verbatim.
  - Suggested follow-up (not done here, outside T43's scope): decide the `uv` cache path (add `~/.cache/uv` to allowWrite, or set `UV_CACHE_DIR`) and the `gh` or keyring socket access (`allowAllUnixSockets` or `excludedCommands: [gh]`) before flipping `failIfUnavailable`.
- The understand-anything auto-update hook fired after the commit. I did not act on it, per the task note and the new rule: hook fired; not acted on.
- No `.ua/**`, plugin, hook, or `generate-agent-configs.py` change.

[memory:decision] T43: `.ua/` graph acceptance requires
`scripts/ua-symbol-coverage.py` (per-file function+class node comparison
against the previous graph, zero unexplained regressions); the
Understand-Anything auto-update hook is out of scope for task workers unless
`.ua/**` is allowed; `make render-check` is the one render-check command
(operator 2026-09-29).

## CompactionDB (main checkout)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T43: .ua/ graph acceptance requires scripts/ua-symbol-coverage.py (per-file function+class node comparison against the previous graph, zero unexplained regressions); the Understand-Anything auto-update hook is out of scope for task workers unless .ua/** is allowed; make render-check is the one render-check command (operator 2026-09-29)."
992478eb-e330-408e-802c-d8506b7ec378
```

## Effects

None outside the repository working tree.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.

## Revision 2 (orchestrator status=revise 20:58:06Z: coverage gate fails open)

The Codex audit of 557502b (Verdict: incorrect) found two P2s; both were reproduced with the new tests.

1. **An unresolvable `--repo-ref` failed open.** At `ua-symbol-coverage.py:65`, any failed `git show` counted as a deleted file, so every loss was "explained" and the script exited 0. This is the same fail-open class as the T38 `--base` bug.
   - Fix: `verify_ref()` runs `git rev-parse --verify --quiet --end-of-options REF^{commit}` and rejects empty or `-`-prefixed values. It raises `CoverageError`, and `main()` exits **2** before printing any table.
   - For a valid ref, a failed `git show` means the path is absent only when `git ls-tree --name-only REF -- path` is empty. Any other failure also exits 2.
2. **`defs < before` excused the whole decrease** (old=2, source defs=1, new=0 passed).
   - Fix: with an integer def count, a decrease is `explained` only when `after >= min(before, defs)`; any lower `after` is `REGRESSION`.
   - A file type with no def grammar (`-`) never explains a decrease. Absent at REF gives `gone`, which is explained.
3. **Tests.** `tests/unit/test_ua_symbol_coverage.py` now has 4 tests: the original regression-vs-clean case, and the four requested cases.
   - An unresolvable ref (`no-such-ref`, `--output=leak`, empty) exits 2, prints a stderr message and no `regressions:` line, and creates no `leak` file.
   - A file gone at REF is explained.
   - A partial deletion with extra loss (2 → 0 with 1 def) is a REGRESSION.
   - A partial deletion fully accounted for (2 → 1 with 1 def) is explained.
   - Against 557502b's script, the unresolvable-ref subtests (it returned 0, or 1 for the empty ref) and the extra-loss case (it returned 0) fail. The other two pass on both versions.
4. **Real data.** T41 rev1 against 72b8901 still gives `regressions: 8`, exit 1. The self-compare gives `regressions: 0`, exit 0. `--repo-ref no-such-ref` gives exit 2 with `does not resolve to a commit`.
5. **Checks** (outside the sandbox, because of the `uv` cache issue): `make unit-test` 614 OK; `make validate-agent-assets` ok; `make render-check` up to date.
6. **Commits.** 99c1174 is the fix. 1843dd1 merges origin/main f45cf73, which is `.orchestration` only, so base-ok holds without a force push. The PR is still #214.

cost (revision 2): 0 subagent dispatches; orchestrating session n/a.

## Revision 3 (orchestrator status=revise 22:28:22Z; task_rev 8003c164…6edd verified)

This round fixes the three items from the Codex GitHub review of 1843dd1 and the audits of 99c1174 and 1843dd1. The fix is commit **12d3f80**, and **681957f** merges origin/main c8fc05c; neither needed a force push. PR #214 head is `681957f982df43abeea6a98602ca450514b76ed1`: all CI checks pass (nix skipped), and mergeStateStatus is CLEAN.

1. **`--repo-ref` now means the revision the new graph was built from.** That is the new graph's `.ua/meta.json` `gitCommitHash`, normally `HEAD`, never the pre-change base. The change is in:
   - the rule bullet in `home/dot_config/claude/rules/understand-anything.md`;
   - the Codex mirror `home/dot_config/codex/AGENTS.md`;
   - the SKILL "Review and integration invariants" sentence;
   - the README;
   - the script's docstring and usage text, plus the argparse `--repo-ref` help.

   The new test `test_ref_is_the_new_graph_revision_not_the_base` uses two commits: `a.py` has `one` and `two` at the base, and `one` alone at HEAD. The old graph has 2 symbols and the new graph 1. With `--repo-ref HEAD` (function deleted at REF) the row is `| a.py | 2 | 1 | 1 | explained |` and the exit is 0. With `--repo-ref HEAD~1` (source unchanged at REF) the row is `| a.py | 2 | 1 | 2 | REGRESSION |` and the exit is 1.
2. **The helper is on PATH.**
   - `git mv scripts/ua-symbol-coverage.py home/dot_local/bin/common/executable_ua-symbol-coverage` (mode 0755, module docstring kept). chezmoi applies it as `~/.local/bin/common/ua-symbol-coverage`, and `home/dot_zshenv` puts that directory on PATH.
   - The rule, mirror, SKILL and README now invoke `ua-symbol-coverage`, and the test loads the new path. There is no duplicate: `git grep 'scripts/ua-symbol-coverage'` outside `.orchestration` exits 1.
   - The pattern follows `executable_agent-session-staleness`, an existing Python executable in the same directory with its test in `tests/unit/`.
   - `make render-check` is unchanged.
3. **`uv run` shebangs now use the Python grammar.** `def_pattern` treats a first line containing `uv run` as Python. The new test `test_uv_run_script_shebang_is_python` uses an extensionless `tool` with `#!/usr/bin/env -S uv run --script` and 1 def, with a graph going from 2 symbols to 1. It gives `| tool | 2 | 1 | 1 | explained |` and exit 0.
   - The pre-fix negative check is pasted in the validation file: with the fix reverted, the row is `| tool | 2 | 1 | - | REGRESSION |` and the exit is 1.
   - On real data, `executable_permgate` now reads `| 16 | 16 | 25 | ok |` (25 def-like lines, not `-`).

**Checks** (verbatim in validation §6, every exit captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 618 tests OK (1 skipped), including all 6 coverage tests; exit 0.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with `--repo-ref HEAD`: `files: 365, regressions: 0`, exit 0.
- Real data, the T41 rev1 graph (c3afc7a) against the 72b8901 graph with `--repo-ref c3afc7a` (the new semantics): `regressions: 8`, exit 1. These are the same 8 files the audit found.
- `gh pr checks 214`: exit 0.

The self-compare no longer uses `| tail -3; echo $?`: the table goes to a file first, and `tail` reads that file afterwards.

**Notes**
- The Understand-Anything auto-update hook fired after both commits. It was not acted on, per the rule (no `.ua/**` in `allowed_files`).
- A `python3 -m py_compile` check left `home/dot_local/bin/common/__pycache__/…pyc`. It is git-ignored, but chezmoi could apply it. I removed it at once and nothing was committed. I found no repo-level guard against this; a learning candidate records it.
- CompactionDB (main checkout): a correcting r3 decision, id **c8d78aa6-faef-45fc-9ad9-027e5b195969**. It is needed because the r1 decision `992478eb-…` names `scripts/ua-symbol-coverage.py`, which no longer exists. Command and output are in validation §6.

[memory:decision] T43 r3: the .ua/ symbol-coverage gate is the PATH helper ua-symbol-coverage (home/dot_local/bin/common/executable_ua-symbol-coverage; scripts/ua-symbol-coverage.py removed), run with --repo-ref set to the revision the new graph was built from (its .ua/meta.json gitCommitHash, normally HEAD), never the pre-change base; a first line containing "uv run" selects the Python def grammar (orchestrator r3 2026-09-30).

- Sandbox: make targets, `git push`, `gh` and the main-checkout CompactionDB/artifact writes ran unsandboxed for the stated T39 limits (uv cache, AF_UNIX socket test, keyring D-Bus, main checkout outside the write allowlist). Everything else ran sandboxed.

cost (revision 3): 0 subagent dispatches; about 30k context tokens consumed this round (session budget counter; no per-task figure exposed).

## Revision 4 (orchestrator status=revise 23:22:16Z; task_rev 9ca1adc2…dd06 verified)

Both new P1 findings from the Codex GitHub review of 681957f are fixed in one commit, **6b53337**. It sits directly on 681957f; base-ok still holds, so there was no merge and no force push. PR #214 head: `6b533379cd9029bf30b2f1c424a62b8ae317781c` (all CI checks pass, nix skipped; mergeStateStatus CLEAN).

1. **Renames no longer fail open** (`executable_ua-symbol-coverage`).
   - New `--old-ref <previous-graph-rev>`, the previous graph's `.ua/meta.json` `gitCommitHash`. It requires `--repo-ref`; `--old-ref` alone is an argparse error with exit 2, and an unresolvable `--old-ref` exits 2 through `verify_ref(…, "--old-ref")`.
   - `renames()` runs one `git diff -z --name-status -M --diff-filter=R OLD REF --`.
   - A path absent at REF that was renamed is judged by its successor: status `ok` when the successor's new count is at least the old count, otherwise the `min(old, defs at REF)` rule decides between `explained` and `REGRESSION`, using the successor's def count. The row shows `renamed → <new path>`, and its new column holds the successor's count.
   - A genuine deletion (absent, not renamed, `--old-ref` given) stays `gone` / `explained`.
   - With `--repo-ref` but no `--old-ref`, an absent path that had symbols is a `REGRESSION` (fail closed).
   - Docstring, usage and argparse help name both refs. The docstring also records one known ceiling: `-M` pairs renames only at ≥50% similarity, so a rename that also rewrites most of the file still reads as a deletion plus a new file. The amendment specified `-M`, so I left the threshold unchanged.
   - Rule bullet, Codex mirror, SKILL sentence and README now invoke `ua-symbol-coverage <previous-graph> <new-graph> --old-ref <previous-graph-rev> --repo-ref <new-graph-rev>`. The README wording is equivalent.
   - Tests: the 4 test names below.
     - `test_rename_preserving_symbols_is_ok` expects `| pkg/a.py | 2 | 2 | renamed → pkg/b.py | ok |` and exit 0.
     - `test_rename_dropping_symbols_is_regression` is the review's reproduction: the new graph has only a file node for `pkg/b.py`. It expects `| pkg/a.py | 2 | 0 | renamed → pkg/b.py | REGRESSION |`, `regressions: 1` and exit 1.
     - `test_deleted_path_with_old_ref_is_explained` expects `gone | explained` and exit 0. It **replaces** r2's `test_file_gone_at_ref_is_explained`, whose assertion (absent path explained without `--old-ref`) was exactly the fail-open.
     - `test_absent_path_without_old_ref_is_regression` expects `gone | REGRESSION` and exit 1.
   - Negative check (validation §7): all four fail against the r3 script (12d3f80). Two of them fail only because r3 does not know `--old-ref`. `test_absent_path_without_old_ref_is_regression` is the one that proves the fail-open is gone: r3 exits 0 on it.
2. **Codex managed PATH now includes `~/.local/bin/common`.**
   - `home/dot_agents/agent-config.yaml:122` adds `{{ .chezmoi.homeDir }}/.local/bin/common` right after `.local/bin` in `shell_environment_policy.set.PATH`.
   - I regenerated with `uv run --with pyyaml scripts/generate-agent-configs.py` ("generated agent configs updated"). The only rendered change is `home/.chezmoitemplates/codex-config-managed.toml:31`, and `make render-check` is green.
   - No existing test pinned the string. New test `test_managed_codex_path_includes_installed_common_bin` parses the rendered template as TOML and asserts the entry is present and comes after `.local/bin`.
   - **User-visible impact (Dotfiles safety):** after the next `chezmoi apply`, Codex's managed PATH has `~/.local/bin/common` after `~/.local/bin` and before `/opt/homebrew/bin` and the system directories. None of the 21 `executable_*` names there exists in `/usr/local/bin`, `/usr/bin`, `/bin`, `/usr/sbin`, `/sbin` or `/opt/homebrew/bin` on this host (`collisions=0`, validation §7), so no system binary is shadowed.
   - On this machine `zsh -lc` already prepended the directory through `home/dot_zshenv`, so behaviour there is unchanged. Commands run with `sh -c` now resolve the helpers too.

**Checks** (verbatim in validation §7, every exit captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 622 tests OK (1 skipped), exit 0, including the 4 new coverage tests and the PATH test.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with `--old-ref HEAD --repo-ref HEAD`, so `renames()` runs against the real repo: `files: 365, regressions: 0`, exit 0.
- Real data, the 72b8901 graph against the c3afc7a graph with `--old-ref 72b8901 --repo-ref c3afc7a`: `regressions: 8`, exit 1. That range has no renames or deletions of graph files, so the same 8 files are reported.
- Bad `--old-ref`: exit 2. `--old-ref` without `--repo-ref`: exit 2.
- `gh pr checks 214`: see §7.

**Notes**
- The Understand-Anything auto-update hook fired after the commit (and spuriously after non-commit commands). It was not acted on.
- CompactionDB (main checkout): r4 decision **984c14d8-674c-4a32-92fc-561a0f487b97**. Command and output are in §7.

[memory:decision] T43 r4: ua-symbol-coverage takes --old-ref <previous-graph gitCommitHash> with --repo-ref <new-graph gitCommitHash>; renames between them (git diff -M --diff-filter=R) are judged by the successor path under min(old, defs at REF), genuine deletions stay explained, and without --old-ref a path absent at REF is a REGRESSION (fail closed). Codex shell_environment_policy PATH includes ~/.local/bin/common after ~/.local/bin (orchestrator r4 2026-10-01).

- Formatter churn: the PostToolUse formatter rewrote the whole of `tests/unit/test_generate_agent_configs.py` after one Edit (55+/14−). I restored the branch version and inserted only the 12-line test.
- Sandbox: the same unsandboxed classes as r3 (make targets, the generator write through the uv cache, `git push`, `gh`, and the main-checkout CompactionDB and artifact writes).

cost (revision 4): 0 subagent dispatches, 1 advisor consult; about 32k context tokens consumed this round (session budget counter; no per-task figure exposed).

## Revision 5 (orchestrator status=revise 23:56:13Z; task_rev f0445f17…9355 verified)

This round fixes the shared root cause behind both findings from the Codex GitHub review of 6b53337: the gate let an undercounted or missing def-line count explain a symbol loss. The fix is one commit, **c878b0d**, directly on 6b53337. base-ok holds, so there was no merge and no force push. PR #214 head: `c878b0d495ee161d010239b20bd191f8007d7aff` (all CI checks pass, nix skipped; mergeStateStatus CLEAN). The CLI is unchanged. The rule, SKILL, mirror and README wording is also unchanged, because none of them describe the per-row exit semantics; the docstring carries the two new REGRESSION reasons and both ceilings.

1. **Unchanged source cannot explain a loss.**
   - With `--old-ref`, `blobs()` runs one `git ls-tree -r -z` per ref instead of a `rev-parse` per path.
   - A path whose blob is identical at OLD and REF is `REGRESSION` on any decrease, noted `source unchanged`, whatever its def-like count. The same applies to a rename whose successor keeps the blob.
   - The `min(old, defs)` rule still applies to changed files.
   - Test `test_unchanged_source_cannot_explain_a_loss`: the source has 2 defs and the graph goes 3 → 2. Without `--old-ref` the min rule gives `explained`, exit 0. With `--old-ref HEAD~1` (blob unchanged) the row is `| a.py | 3 | 2 | 2 | REGRESSION | source unchanged |`, exit 1.
2. **Ruby visibility prefixes.**
   - `RUBY_DEF` becomes `^\s*(?:(?:private|protected|public)\s+)?(?:def|class|module)\s+\S+`.
   - Test `test_ruby_visibility_prefixed_defs_are_counted`: `lib.rb` holds `class A`, `def one`, `private def two`, and the graph drops the private method. The row is `| lib.rb | 3 | 2 | 3 | REGRESSION |`, exit 1.
   - The r4 script gives `| lib.rb | 3 | 2 | 2 | explained |`.
3. **New paths backed by source, with zero symbols, fail closed.**
   - A path absent from the old graph that exists at REF with at least one def-like line and has 0 new symbols is `REGRESSION`, noted `new file, no symbols`.
   - A rename successor whose predecessor had symbols is skipped here, because the predecessor's row already judges it.
   - Test `test_low_similarity_move_with_no_symbols_is_regression` is the reviewer's reproduction. `a.py` becomes `b.py` with 80 added lines, which is below git's rename threshold, and the new graph has only a file node for `b.py`. It gives `| a.py | 2 | 0 | gone | explained |` plus `| b.py | 0 | 0 | 2 | REGRESSION | new file, no symbols |`, exit 1.
   - The r4 script shows `b.py` as `ok` and exits 0.
   - Docstring ceiling: a moved and rewritten file that keeps *some* nodes is judged only by this zero check.
4. The table gains a `note` column. Existing row assertions match by substring and stay green.

**Negative check** (validation §8): all three new tests fail against the r4 script (6b53337) because of the logic, not the CLI: `explained`, `explained`, `ok`, as quoted above.

**Checks** (verbatim in §8, every exit captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 625 tests OK (1 skipped), exit 0, including the 3 new tests.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with `--old-ref HEAD --repo-ref HEAD`: `files: 365, regressions: 0`, exit 0.
- Bad `--old-ref`: exit 2.
- Real data (`--old-ref 72b8901 --repo-ref c3afc7a`): `regressions: 8`, exit 1. The full table is in §8.

**Real-data rows.** None turned from `explained` into `REGRESSION`, because the r4 table had no `explained` rows on this data. The same 8 regressions now carry the `source unchanged` note. `git diff --stat 72b8901 c3afc7a -- ':!.ua' ':!.orchestration'` is empty, so every decrease is a real T41 under-extraction. The 8 files:
- `.claude/contextdb/contextdb/storage.py`
- `…/gh-comment-attach-files/scripts/attach_comment_files.py`
- `executable_agent-fanout`
- `bin/server/history.sh`
- `install/ubuntu/client/{docker,tailscale,zed}.sh`
- `scripts/run_bashcov_unit_test.rb`

No row reports `new file, no symbols`.

**Notes**
- The Understand-Anything hook fired again after the commit; I did not act on it.
- No formatter churn this round: the test edits went through Bash, not Edit.
- CompactionDB (main checkout): r5 decision **18479d26-8d15-4882-9254-723be0fd18bb**. The command and output are in §8.

[memory:decision] T43 r5: ua-symbol-coverage never lets an undercounted or absent def count explain a loss: with --old-ref, a path whose blob is identical at OLD and REF is a REGRESSION on any symbol decrease (source unchanged); a path new to the graph with def-like lines at REF but zero symbols is a REGRESSION (new file, no symbols); Ruby private/protected/public def prefixes are counted (orchestrator r5 2026-10-01).

cost (revision 5): 0 subagent dispatches; about 20k context tokens consumed this round (session budget counter; no per-task figure exposed).
