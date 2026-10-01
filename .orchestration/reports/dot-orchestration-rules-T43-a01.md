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

## Revision 6 (orchestrator status=revise after T48; amendment r6)

### Real-data finding at c8cc4e4 (resolved by r6-b below): 10 regressions, not 8

`--old-ref 72b8901 --repo-ref c3afc7a` now gives **`regressions: 10`**, exit 1. The amendment expected the same 8. I implemented item 2 literally (afb2c9d). The PONG at 01:26Z reported the finding, and the orchestrator answered with amendment r6-b. What I found:

- **The two extra rows** come only from item 2, the new-file flag:
  - `scripts/pr-feedback.py | 0 | 5 | 11 | REGRESSION | new file, 5 of 11 defs`
  - `tests/unit/test_pr_feedback.py | 0 | 5 | 21 | REGRESSION | new file, 5 of 21 defs`

  The other 8 are the known T41 losses, all noted `source unchanged`.
- **Cause, from git facts (validation §9).** The 72b8901 graph's own `.ua/meta.json` `gitCommitHash` is `7b69b1e`. Neither file exists at `7b69b1e`, and neither appears in the 72b8901 graph, so both are genuinely new to the graph. Running with `--old-ref 7b69b1e` (the old graph's real revision) gives the same 10.
  - Side note on parameters: the real-data runs use graph **commit** ids. The rule's definition is each graph's `gitCommitHash`, which here would be `--old-ref 7b69b1e --repo-ref 72b8901`. The source is identical between 72b8901 and c3afc7a, so the result does not change.
- **These are not under-extractions.** The *accepted* graph at HEAD (gitCommitHash 72b8901) also gives both files exactly 5 nodes.
- **Measured consequence.** In the accepted graph, **138 of 185** files that have a def grammar already have fewer symbols than def-like lines. The extractor does not emit a node per `def`: methods, nested functions and `modify_private_*.config.toml` bodies are not separate nodes. So item 2 as written flags about three quarters of new files in every refresh, and each one would need a citation. The measurement script and its full per-file list are in §9.
- **Possible directions, for the orchestrator (none implemented):**
  - keep only the r5 zero-symbol check, which does not catch the `:184` reproduction;
  - a ratio threshold, which is a heuristic;
  - treat `new < defs` on new files as a non-failing note.

### Changes (afb2c9d, plus c8cc4e4 merging origin/main 85919df / T48 0a34a68)

1. **Def-line counts never explain a loss.** A decrease on any path that exists at REF is now `REGRESSION`. The only `explained` outcome is a deletion under `--old-ref` (absent at REF and not renamed, shown `gone`).
   - A renamed path whose successor keeps at least the old count shows `ok`. The amendment lists this among the "explained outcomes", but the r4 test the orchestrator accepted pins `ok`, so I kept `ok`.
   - A rename whose successor has fewer symbols is `REGRESSION`.
   - Without `--old-ref`, every decrease is `REGRESSION`.
   - The `source unchanged` note stays, for information.
   - The successor's def count is no longer computed, because it cannot affect the outcome.
2. **Def-line counts only flag.** A path new to the graph that exists at REF with fewer symbols than def-like lines is `REGRESSION`, noted `new file, <new> of <defs> defs`. The r5 zero-symbol check is its special case. The `def-like lines` column stays as information on every row.
3. **Shell names.** `SHELL_DEF = ^\s*(?:function\s+\S+|[^\s()=]+\s*\(\))(?:\s*[{(].*)?\s*$`.
   - **Deviation:** the name class also excludes `=`. The amendment's literal `[^\s()]+` would count the array assignment `arr=()` as a function. `=` cannot appear in a bash function name defined with the `name()` form, so excluding it loses nothing.
   - The new test pins `foo?() {`, `function bar@baz {` and `arr=()` together: 2 defs, not 3.
4. **Docstring** rewritten around the two principles ("structural facts explain; counts only flag"). The obsolete ceilings (`min` rule, rename-similarity ceiling for kept nodes) are dropped. One remains: the new-file check is only as complete as the def grammar.
   - Rule, SKILL, mirror and README are unchanged. "Or cites the source change behind each decrease" stays.
   - **Wording gap to flag:** that phrase does not cover a new-file flag, which has no decrease to cite. If item 2 stays as written, the rule would need a clause for it. I did not add one, because the threshold is still open.
5. **Tests** (14 in the module):
   - Flipped expectations, same inputs:
     - `test_partial_deletion_is_explained_only_up_to_the_source_loss` is renamed `…_in_changed_source_is_regression`. Its "fully accounted" case (2 → 1, 1 def) now expects `REGRESSION`, exit 1.
     - `test_unchanged_source_cannot_explain_a_loss` is renamed `test_unchanged_source_loss_is_noted`. Its no-`--old-ref` case now expects `REGRESSION`.
     - `test_ref_is_the_new_graph_revision_not_the_base` is renamed `test_def_column_reads_the_new_graph_revision`. Both refs now give `REGRESSION`; the def column shows 1 at HEAD and 2 at HEAD~1.
     - `test_uv_run_script_shebang_is_python` now expects `| tool | 2 | 1 | 1 | REGRESSION |`; the def column `1`, not `-`, still proves the grammar.
     - The low-similarity move's note becomes `new file, 0 of 2 defs`.
   - New:
     - `test_new_file_with_fewer_symbols_than_defs_is_regression`, the `:184` reproduction: new `b.py` with 2 defs and 1 node gives `REGRESSION`, `new file, 1 of 2 defs`, exit 1.
     - `test_shell_names_with_punctuation_are_counted`.
   - **Negative check against c878b0d** (§9): the 2 new tests and the 2 flipped ones fail. r5 gives `b.py … ok`, `s.sh … 0 … ok`, `a.py … explained`, and `a.py … explained`.

### Checks (verbatim in §9, exits captured directly)

- base-ok (after merging origin/main), exit 0.
- `make render-check`: up to date, exit 0. The merged `agent-config.yaml` combines the T48 audit block with the T43 PATH line, and they are consistent.
- `make unit-test`: 627 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with `--old-ref HEAD --repo-ref HEAD`: `regressions: 0`, exit 0.
- Real data: 10 regressions, exit 1, as described above.
- Bad `--old-ref`: exit 2.
- `gh pr checks 214`: in §9.

### Notes

- **task_rev:** no dispatch carried an r6 task_rev. I worked against the task file as it stood when the T48 acceptance told me to switch (`95d26e4f096aed469004e6804096fc63fab8afab8126d8c1d89d6cb95937c35b`) and re-checked it, unchanged, before committing.
- **Understand-Anything hook:** it fired after the commits. I did not act on it.
- **Stray bytecode:** importing the helper for the measurement left `home/dot_local/bin/common/__pycache__`. It is git-ignored; I removed it.
- **CompactionDB (main checkout):** **4629b961-4b39-4d7c-aeef-73801df1e2f0** records items 1 and 3 and says item 2's threshold was pending. r6-b's decision supersedes that clause.

[memory:decision] T43 r6: in ua-symbol-coverage only structural git facts explain a loss (with --old-ref: a deletion, or a rename whose successor keeps the old count); every other decrease on a path present at REF is a REGRESSION to be cited, and def-like counts never explain; SHELL_DEF accepts any name without whitespace, parentheses or =. The r6 new-file flag (new < def-like lines) over-flags (138 of 185 grammar files in the accepted graph already have fewer symbols than def lines); its threshold is pending the orchestrator decision (2026-10-01).

cost (revision 6): 0 subagent dispatches, 1 advisor consult; about 35k context tokens consumed this round (session budget counter; no per-task figure exposed).

r6 commits: afb2c9d (fix) and c8cc4e4 (merge of origin/main). r6-b follows.

## Revision 6-b (amendment r6-b, task_rev cb8b03b2…68b7 verified; PING 01:28:58Z)

The orchestrator accepted the measurement: `new < defs` is not a usable gate. Commit **56f308c** sits on top of c8cc4e4, with no force push. PR #214 head: `56f308c1217888b9c3c67b0bd6c1821e36ed7119` (all CI checks pass, nix skipped; mergeStateStatus CLEAN).

1. **Item 2 is back to the r5 rule.** A path new to the graph is a `REGRESSION` only when it exists at REF with at least one def-like line and **zero** symbols, noted `new file, no symbols`. Items 1 (def counts never explain) and 3 (shell name characters) are unchanged from afb2c9d.
2. **Docstring.** It now states the measured ceiling: the def-like count overcounts graph nodes, because nested functions and methods often get no node. So partial under-extraction of a brand-new file cannot be detected from the count. In the accepted graph of 2026-10-01, 138 of 185 files with a def grammar have fewer symbols than def-like lines. Only the zero-symbol case is flagged, and the `def-like lines` column is informational.
3. **Tests.**
   - The `:184` reproduction is inverted to pin the documented behaviour. `test_new_file_with_fewer_symbols_than_defs_is_regression` became `test_partially_covered_new_file_is_not_flagged`: a new `b.py` with 2 defs and 1 node gives `| b.py | 0 | 1 | 2 | ok |  |`, exit 0.
   - The zero-symbol test `test_low_similarity_move_with_no_symbols_is_regression` is kept, and its note is back to `new file, no symbols`. All 14 module tests pass.
4. **The 138/185 measurement.** Command and verbatim output are in validation §9:

   ```
   python3 <scratchpad>/measure.py
   ```

   The script, verbatim in §9, loads the helper with `SourceFileLoader`. For every `filePath` in `.ua/knowledge-graph.json`, it compares `symbol_counts` against `def_lines(<.ua/meta.json gitCommitHash>, path)`. Output: `files with a def grammar 185, symbols < def-like lines 138`, then the per-file list. `scripts/pr-feedback.py` has 5 symbols for 11 def-like lines, and `tests/unit/test_pr_feedback.py` has 5 for 21.

**Checks** (verbatim in §10, exits captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 627 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with `--old-ref HEAD --repo-ref HEAD`: `regressions: 0`, exit 0.
- **Real data** (`--old-ref 72b8901 --repo-ref c3afc7a`): **`regressions: 8`**, exit 1. These are the 8 known rows, all `source unchanged`. Both `pr-feedback` files are back to `ok`.
- Bad `--old-ref`: exit 2.
- `gh pr checks 214`: in §10.

**For the acceptance record:** this round flags the Codex `:184` P1 as not-applicable, with the measurement as the reason; it is not fixed. That disposition is the orchestrator's call.

[memory:decision] T43 r6-b: ua-symbol-coverage flags a path new to the graph only when it has def-like lines at REF and zero symbols; partial under-extraction of a new file is a documented ceiling because 138 of 185 grammar files in the accepted graph already have fewer symbols than def-like lines. Supersedes the pending-threshold clause of 4629b961; items 1 (only deletions and symbol-keeping renames explain) and 3 (shell names) stand (2026-10-01).

CompactionDB (main checkout): **635d9dd5-1058-4db9-aec8-6a10373ee1d3**.

cost (revision 6 + 6-b): 0 subagent dispatches, 1 advisor consult; about 45k context tokens consumed (session budget counter; no per-task figure exposed).

## Revision 7 (orchestrator status=revise 02:08:35Z; task_rev fe4ce571…15e9 verified)

All three findings are fixed in one commit, **72746d4**, directly on 56f308c (base-ok holds, so there was no merge and no force push). PR #214 head: `72746d47ed6dca80ac61b6e1b53caf7fc606e68d` (all CI checks pass, nix skipped; mergeStateStatus CLEAN).

1. **Comment lines are not definitions** (audit P2 on afb2c9d). `count_defs` skips lines whose first non-blank character is `#` in every grammar.
   - Test `test_comment_lines_are_not_definitions`: a new `s.sh` with `real()`, `#disabled() { :; }` and `  # gone() {` gives `| s.sh | 0 | 1 | 1 | ok |`.
   - The r6-b script gives `… | 2 | ok |`: `#disabled()` matched the r6 name class.
2. **Python definitions come from `ast`.** For the Python grammar (`.py`, a `python` shebang or a `uv run` shebang), `count_defs` counts `FunctionDef`, `AsyncFunctionDef` and `ClassDef` nodes from `ast.walk(ast.parse(text))`. It falls back to the comment-skipping `PYTHON_DEF` regex only on `SyntaxError` or `ValueError` (for example, NUL bytes).
   - Test `test_python_defs_inside_strings_do_not_count`: a new `doc.py` containing only `DOC = """\ndef not_a_real_function():\n"""` gives `| doc.py | 0 | 0 | 0 | ok |`, exit 0.
   - The r6-b script counts 1 there and reports `new file, no symbols`, exit 1.
   - The uv-shebang test still passes, with def column 1.
3. **A new grammar file missing from the graph fails closed.**
   - `blobs()` now keeps `(mode, blob)` for blob entries. It runs once for REF whenever `--repo-ref` is given, and for OLD with `--old-ref`.
   - `missing_from_graph()` takes candidates from that single `git ls-tree -r -z REF`: any path with a grammar extension, or mode 100755 whose line 1 is a `#!` shebang that selects a grammar. A candidate becomes a row when it has at least one def-like line, appears in neither graph, and its parent directory is the parent of some path in the new graph.
   - The row is `| path | 0 | 0 | N | REGRESSION | missing from graph |`, and it counts toward `files:` and `regressions:`.
   - Test `test_grammar_file_missing_from_graph_fails_in_covered_directories`: with both graphs unchanged (`a.py` only), `b.py` with two functions in the covered root gives `| b.py | 0 | 0 | 2 | REGRESSION | missing from graph |` and exit 1. `sub/c.py`, in an uncovered directory, gives no row. The test also asserts `regressions: 1`.
   - The r6-b script exits 0 on the same input.
4. **Docstring:** one passage per item (the missing-from-graph sentence sits in the "counts only flag" bullet). It states that the def-like column for Python is now the `ast` count.
   - The 138/185 ceiling was re-measured with the new counting and is unchanged (validation §11).

**Measurement first (item 3), on the accepted graph** (`.ua/knowledge-graph.json`, `.ua/meta.json` gitCommitHash `72b890157078…`), run with the r7 working copy before committing:
- With `--repo-ref 72b8901` (the graph's own revision): **no candidates**, `regressions: 0`, exit 0. The rule is consistent with the accepted graph, so I applied it as instructed.
- With `--repo-ref HEAD`: two rows, `home/dot_local/bin/common/executable_ua-symbol-coverage` and `tests/unit/test_ua_symbol_coverage.py`. Both are **genuine omissions**: this PR added them (557502b, renamed in 12d3f80) after the graph's revision 72b8901, so the accepted graph cannot list them. No other path is listed.

**Self-compare: which ref?** The r4–r6 form `--old-ref HEAD --repo-ref HEAD` now reports exactly those 2 rows (`regressions: 2`, exit 1), which is correct behaviour for a graph that is stale against HEAD. The rule-correct self-compare passes both refs as the graph's own `gitCommitHash`: `--old-ref 72b8901 --repo-ref 72b8901` gives **`regressions: 0`**, exit 0. Both outputs are in §11. After this PR merges, the next `.ua/` refresh will pick both files up.

**Checks** (verbatim in §11, every exit captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 630 tests OK (1 skipped), exit 0, including the 3 new tests and the uv-shebang test.
- `make validate-agent-assets`: ok, exit 0.
- **Real data** (`--old-ref 72b8901 --repo-ref c3afc7a`): **`regressions: 8`**, exit 1. These are the same 8 rows, all `source unchanged`; item 3 adds no row on this data.
- Bad `--old-ref`: exit 2.
- `gh pr checks 214`: in §11.

**Negative check** (§11): all 3 new tests fail against 56f308c, with the outputs quoted above.

**Notes**
- The Understand-Anything hook fired after the commit; I did not act on it.
- Measurements ran with `PYTHONDONTWRITEBYTECODE=1`; no `__pycache__` was left in `bin/common`.
- CompactionDB (main checkout): **67792095-e3fc-4f88-a6c1-3ede3a6f76ae**.

[memory:decision] T43 r7: ua-symbol-coverage def-like counts skip # comment lines in every grammar and count Python definitions with ast (regex only on SyntaxError); a grammar file at REF with def-like lines that appears in neither graph is a REGRESSION (missing from graph) when the new graph already covers its directory. The self-compare uses both refs = the graph own gitCommitHash (2026-10-01).

cost (revision 7): 0 subagent dispatches; about 25k context tokens consumed this round (session budget counter; no per-task figure exposed).

## Revision 8 (orchestrator status=revise 02:37:57Z; task_rev c5991cd2…66e3 verified)

Both items from the audit of 72746d4 are fixed in one commit, **1b6741b**, directly on 72746d4 (base-ok holds, no merge, no force push). PR #214 head: `1b6741b8fe4f58b4eaa24b360fffceec2c8cee56` (all CI checks pass, nix skipped; mergeStateStatus CLEAN).

1. **P2: fail closed on an unreadable candidate.** In `missing_from_graph`, a mode-100755 extensionless candidate is now read with a checked `git show REF:path`. A non-zero return raises `CoverageError("cannot read <path> at <REF>: …")`, so the run exits 2 before printing a table, as `def_lines` already does. Non-executable extensionless paths are still skipped without being read.
   - Test `test_unreadable_candidate_fails_closed`: a fake `git` earlier on `PATH` fails only `show HEAD:tool` for a committed 0755 `tool` with a `#!/bin/sh` shebang and delegates everything else to the real git. The run gives exit 2, `ua-symbol-coverage: cannot read tool at HEAD` on stderr, and no `regressions:` line.
   - The r7 script exits 0 there (fail-open).
   - `run_coverage` gained an optional `env` parameter for this test.
2. **P3: compare blob ids only.** The `source unchanged` check compares `old_blobs[path][1]` with `new_blobs[source][1]`, the blob ids. A chmod-only change keeps the note.
   - Test `test_chmod_only_change_keeps_the_source_unchanged_note`: `a.py` is committed at 0644 and then chmod-ed to 0755 with identical bytes, and the graph goes 2 → 1. With `--old-ref HEAD~1`, the row is `| a.py | 2 | 1 | 2 | REGRESSION | source unchanged |`.
   - The r7 script prints the row without the note, which also proves that git recorded the mode change.

**Checks** (verbatim in §12, every exit captured directly):
- base-ok, exit 0.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 632 tests OK (1 skipped), exit 0, including both new tests.
- `make validate-agent-assets`: ok, exit 0.
- Self-compare with both refs at the graph's gitCommitHash (`--old-ref 72b8901 --repo-ref 72b8901`): `regressions: 0`, exit 0.
- **Real data** (`--old-ref 72b8901 --repo-ref c3afc7a`): **`regressions: 8`**, exit 1, all `source unchanged`.
- Bad `--old-ref`: exit 2.
- `gh pr checks 214`: in §12.

**Negative check** (§12): both tests fail against 72746d4. The first exits 0 instead of 2; the second is missing the note.

**Notes:** the Understand-Anything hook fired after the commit and was not acted on. No `__pycache__` was left. CompactionDB (main checkout): **4bac6923-9905-4348-aa1c-592b2a59fc18**.

[memory:decision] T43 r8: ua-symbol-coverage fails closed (exit 2) when a missing-from-graph candidate cannot be read at REF, and its source unchanged note compares blob ids only, so a chmod-only change keeps the note (2026-10-01).

cost (revision 8): 0 subagent dispatches; about 15k context tokens consumed this round (session budget counter; no per-task figure exposed).
