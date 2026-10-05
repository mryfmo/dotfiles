# Report: dotfiles-T82b-codex-hook-trust-pins-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/codex-hook-trust-pins` from `origin/main` 413e3f37.
- **task_rev:**
  - dispatched: `sha256:d9cb4b5b…`;
  - after PONG decision 1: `sha256:2316332f…`;
  - both matched.
- **PR:** #284, https://github.com/mryfmo/dotfiles/pull/284.
- **Commit and diff head:** `af569d15`; the final head is `c54fdc0c`, the `gh pr update-branch` merge of main `aeb025e8` (#283, docs only). CI is green on both, and `mergeable_state` is `clean`.
- **CI and Bot (round 0):** CI is green on the diff head `af569d15` and on the final head `c54fdc0c`, and `mergeable_state` is `clean` on `c54fdc0c`. (After the first CI, GitHub briefly reported `unknown` and then `behind`, because main had moved to `aeb025e8`; the update-branch merge `c54fdc0c` fixed that.) Bot: no review; the Codex quota notice (2026-10-05T11:52:58Z) ended the wait at its first poll (12:07:37Z).
- **Status:** ready_for_review.

Example paths are spelt with `∕` (U+2215) where a literal path would be masked or flagged by the evidence scan.

## History

My first pass ended in `AGMSG-PONG status=blocked` with four findings. The orchestrator's PONG decision 1 decided both open points: (a) hash at apply time in the Codex modify scripts, now in `allowed_files`; (b) declared keys override existing entries, and undeclared keys are kept. This report covers the full task after that decision.

## Item 1: the hash algorithm (proven)

From Codex `rust-v0.160.0` (the installed `codex-cli 0.160.0`): `hooks/src/engine/discovery.rs` (`hook_hash`, the handler normalisation), `config/src/fingerprint.rs` (`version_for_toml`) and `hooks/src/events/common.rs` (`matcher_pattern_for_event`).

`trusted_hash = "sha256:" + sha256(json(identity, sort_keys, compact))`, where:

- `identity = {event_name, matcher, hooks: [{type, command, timeout, async, statusMessage}]}`;
- the matcher is dropped for `user_prompt_submit`, `stop` and `interrupt`;
- the timeout defaults to 600 (minimum 1); for `session_end` and `interrupt` it defaults to 1 and is clamped to 1..3;
- the command is the raw command, before `${VAR}` substitution.

**Verification:** my implementation reproduces the `currentHash` that Codex's app-server (read-only `hooks/list`) reports for the eight managed hooks on this host (the four config hooks, crit and the three Ponytail hooks). The listing has ten hooks; the other two are not declared by the manifest and were not verified: `~∕.codex∕hooks.json` `session_start` (Herdr's integration, `herdr-agent-state.sh`) and `<main checkout>∕.codex∕hooks.json` `stop` (agmsg turn delivery, `check-inbox.sh`). [Corrected in revise round 3; the earlier text said nine.] That includes the task's permgate pair (`64d9851f…`) and crit (`bf6ad428…`). Both reproductions are in the validation file.

## Items 2–3: apply-time trust (PONG decision 1)

- **Manifest** (`codex.hooks.state`): declares the four config hooks, keyed `{{ .chezmoi.homeDir }}∕.codex∕config.toml:<event>:0:0` and `enabled: true` with no literal hash, plus crit and the three Ponytail hooks with `enabled: true` and a literal fallback `trusted_hash`.
- **Ponytail values (deviation from the original item 3):** the fallbacks are the hashes Codex reports as current for the installed ponytail 4.12.0 (`7ee5d5ae…`, `8c9efc5a…`, `7954d675…`). The task's `security.config.toml` values (`5f81d38f…`/`6a6f42bc…`/`1423b56c…`) were stale; Codex reported them `modified`. The decision makes the apply-time computation the source of truth and these values the fallback only.
- **Renderer** (`scripts/generate-agent-configs.py`):
  - `codex_hook_trust()` builds the declared list and the config-hook definitions, mirroring `codex_command_hook_lines()`: one matcher group per definition, in render order.
  - `HOOK_TRUST_CODE` is the shared apply-time block: `codex_hook_hash`, `declared_hook` (resolves a config key against the definitions, and a plugin key against `~∕.codex∕plugins∕cache∕<marketplace>∕<plugin>∕*∕<file>`; exactly one installed copy is required, otherwise it falls back), `declared_hook_state` and `drop_declared_hook_state`.
  - It is rendered into every profile modify script. In the hand-maintained `home∕dot_codex∕modify_private_config.toml`, it fills the region between two marker lines (`render_codex_base_modify`, part of `expected_outputs`), so `make render-check` fails on any drift.
  - `codex_hook_trust` rejects state fields other than `trusted_hash` and `enabled`.
- **Base merge:** declared keys the managed template carries are hashed on this host and replace the managed literal and any existing entry, with one `hook trust divergence … replacing <old> with <new>` warning. Declared keys missing from the template are not injected. Undeclared keys are kept.
- **Profile merge:** the declared chunks join the profile's managed `[hooks.state]`. Existing entries for declared keys are replaced with the same warning. The base harvest skips declared keys, and undeclared profile and base entries keep the earlier behaviour.
- **Missing plugin file:** the manifest literal is used, and the apply prints `warning: cannot compute hook trust for <key> (<reason>); using the manifest's pinned hash`.
- **Dry run on this host** (live `~∕.codex∕config.toml` as stdin, output to a temp file; `~∕.codex` untouched): all eight declared hashes equal Codex's `currentHash`, the three stale Ponytail pins (`35ad4fd9…`) are replaced with one warning each, and a second pass is byte-identical and quiet. The `standard` profile dry run is idempotent too.
- **Apply-time scope:** 8 declared keys, all hashed from their definitions on the host (4 config, crit, 3 Ponytail); none uses its fallback here.

## Item 4: tests

- **`test_generate_agent_configs.py`:**
  - `test_hook_trust_hash_reproduces_codex_current_hashes`: permgate, pre_compact, session_end and crit (with the matcher dropped for `stop`) equal Codex's reported values.
  - `test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared`: a stale declared entry is replaced with the warning, the undeclared operator entry is kept, and a second apply is byte-identical and quiet.
  - `test_profile_modify_scripts_hash_plugin_hooks_or_fall_back_to_the_pin`: with the plugin missing, the literal is used and a warning printed; once installed, the hash is computed from the file.
- **`test_codex_config_merge.py`:** `test_declared_hook_trust_replaces_stale_entries_and_keeps_undeclared`, with the real base script and a fixture template that declares keys like the rendered one. It checks the replacement and warning, that undeclared keys are kept, the Ponytail literal fallback with its warning, and that a declared key absent from the template (crit) is not injected.
- **Checks:**
  - `make unit-test`: 880 tests, OK (skipped=1), on the round-0 working tree committed as `af569d15`. The raw output is in the validation file's round-0 "Task validation commands" section, restored in round 8.
  - `make render-check`: clean.
  - The validator: rc=0.
  - `grep -c 'hooks.state'` on the template: 9 (the header plus 8 keys).

## Item 5 and README

- **Item 5:** live verification is the orchestrator's (after `make update`). I did not run `make update`.
- **README:** the `∕hooks` paragraph now says `make update` deploys trust for the declared hooks, hashed at apply time. A hook anyone else adds stays untrusted until you review and trust it in `∕hooks`, and a plugin upgrade by `make update` is trusted by the same `make update`. The setup-block comment says no `∕hooks` step is needed for Ponytail.

## Notes

- **Notes for the orchestrator:**
  - `standard.config.toml` changed during the task: it held `35ad4fd9…` at first and the current Ponytail hashes later. Another session trusted them in the meantime.
  - The `codex app-server` probe and other sessions also wrote Codex's own state and logs under `~∕.codex`; I edited nothing there.
- **Version risk:** the algorithm is pinned to Codex 0.160.0. If a Codex upgrade changes it, the computed hashes stop matching, and Codex marks those hooks `modified` (skipped, not run untrusted). The comment in `codex_hook_hash` names the source version.

cost: n/a

[memory:decision] dotfiles-T82b (orchestrator 2026-10-05): Codex hook trust is pinned in the manifest (`codex.hooks.state`, templated per-host keys, hashes reproduced from Codex's own algorithm) and deployed by `make update`; no interactive `∕hooks` trust step; the ponytail pins follow the installed plugin content.

## Revise round 1 (task_rev `sha256:7ed97e8a…b9265867`): fix commits `944ed523` and `315e7394`

The audit of c54fdc0c returned `incorrect` with 5 findings: 3 fixed here, 2 dispositioned by the orchestrator.

1. **`make update` ordering (P1): fixed.**
   - `scripts/update-agent-assets.sh` gains `refresh_codex_hook_trust` (shdoc-commented), the last call of `main`, after every Codex plugin update.
   - It lists the managed Codex config files (`chezmoi managed --path-style=absolute --include=files`, filtered to `.codex/config.toml` and `.codex/<profile>.config.toml`) and re-applies them with `chezmoi apply --force`. There is no prompt and no network. It warns instead of failing, so the rest of `make update` (the Herdr reload) still runs. It skips quietly without `chezmoi` or without any managed Codex config.
   - `make codex-hook-trust` runs the same function on its own.
   - **Placement:** `944ed523` first ran a `$(MAKE) codex-hook-trust` step in the `update` recipe. CI then failed, because `tests/install/common/lifecycle.bats` ("update installs statusline tools after applies and before agent assets") pins `make update`'s exact call sequence and is outside `allowed_files`. `315e7394` moves the refresh into the script, which the task allows ("or `scripts/update-agent-assets.sh` if the refresh belongs there"). The pinned sequence is unchanged, and the refresh still follows the plugin update.
   - **Tests:**
     - `test_make_update_refreshes_codex_hook_trust_after_the_plugin_update` pins the refresh as the last `main` step after the Codex plugin updates, the `--force` form and the filter.
     - `test_hook_trust_refresh_reapplies_only_the_codex_config_files` sources the script with a fake `chezmoi` and checks three things: only the two Codex config files are re-applied, out of a listing that also has `AGENTS.md` and `.zshrc`; no apply runs without them; a failed apply warns and exits 0.
2. **Two cached plugin versions (P2): fixed, by mirroring Codex itself.**
   - The plugin hook is read from the version Codex loads: `core-plugin-common/src/installed.rs` `active_plugin_version`, rust-v0.160.0. That means `local` when present, else the highest valid version directory, ordered by semver (`compare_plugin_versions`) and lexically when either side is not semver.
   - **Deviation:** this replaces the suggested "semver, then mtime" with Codex's exact rule, so trust follows the copy Codex actually runs. Codex records no separate installed-version file here; `~/.codex/plugins/cache/<marketplace>/<plugin>/<version>` is its record.
   - The fallback to the literal now happens only when no copy exists ("no installed copy under …") or the active copy's hook file is unreadable.
   - `test_profile_modify_scripts_hash_the_plugin_version_codex_loads`: with `1.9.0`, `1.12.0` and `1.12.0-rc.1` cached, the hash comes from `1.12.0`; once a `local` copy is added, it comes from `local`.
3. **Evidence (P3): corrected.** The "CI and Bot (round 0)" line above now states `clean` on the final head `c54fdc0c`, and the validation header now separates the diff head (`af569d15`) from the final head (`c54fdc0c`).
4. **Orchestrator dispositions:**
   - **README:** gained the sentence "Config-hook trust follows the manifest definition, so a hook hand-edited in `~/.codex/config.toml` deliberately stops matching and stays untrusted", plus a description of the `make codex-hook-trust` refresh step.
   - **The `codex app-server` probe:** recorded as a disclosed boundary deviation. I will not repeat it without asking first.

- **Re-run on 315e7394:**
  - `make unit-test`: 884 tests OK.
  - `make render-check`: clean.
  - The validator: rc=0.
  - The live base dry run: the same eight Codex-current hashes, the three Ponytail replacements, and a byte-identical, quiet second pass.
  - CI and the Bot wait are in the validation file.
- **CI and Bot on 315e7394:** CI is green and `mergeable_state` is `clean`. The full 15-minute Bot wait (12:59:02Z–13:14:12Z) found `bot: none`, with no quota notice.
- **Not run:** `make update` (the live check is the orchestrator's).

cost: n/a

## Revise round 2 (task_rev `sha256:ff5bb44b…f1cb7932`): fix commit `d8702155`

The audit of 315e7394 returned `incorrect` with 2 findings, both in `active_plugin_version`. Both are fixed.

1. **Symlinked version directories (P2).** The version listing now skips symlinked entries (`not entry.is_symlink()` before `is_dir()`), as Codex reads each entry's own type (`installed.rs`, rust-v0.160.0). A real `4.12.0` next to a symlinked `local` now selects `4.12.0`.
2. **Semver validity (P2).**
   - `parse_semver` accepts a version only as the `semver` crate does: a numeric pre-release identifier with a leading zero fails (`1.10.0-01`), and build identifiers may keep leading zeros (`1.10.0+01` stays semver).
   - A version that fails to parse takes Codex's lexical path, so `1.9.0` wins over `1.10.0-01`.
3. **Regression test:** `test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver` covers both. Run against the previous head's generator, the same scenarios give `local` and `1.10.0-01`; with the fix they give `4.12.0` and `1.9.0` (validation file, verbatim).

- **Re-run on d8702155:**
  - `make unit-test`: 885 tests OK.
  - `make render-check`: clean.
  - The validator: rc=0.
  - The live base dry run: the same eight Codex-current hashes, the three Ponytail replacements, and a byte-identical, quiet second pass.
- **Not run:** `make update`.
- **CI and Bot on d8702155:** CI is green and `mergeable_state` is `clean`. The full 15-minute Bot wait (13:32:43Z–13:47:50Z) found `bot: none`, with no quota notice.

cost: n/a

## Revise round 3 (task_rev `sha256:e0916f49…51d19f0c`)

The audit of d8702155 returned `incorrect` with 3 findings, all fixed.

1. **Build-metadata ordering (P2): fixed.** The comparison mirrors semver 1.0.27, the version in Codex 0.160.0's `Cargo.lock` (`src/impls.rs`):
   - `Version` derives `Ord` over (major, minor, patch, pre, build).
   - `Prerelease`: a release sorts above any pre-release; numeric identifiers compare by length, then lexically; numeric sorts below alphanumeric; a longer set wins on equal prefixes.
   - `BuildMetadata`: an empty build sorts below a non-empty one; numeric identifiers compare by stripped length, stripped value, then original length (`0 < 00 < 1 < 01`).
   - `all_ascii_digits` mirrors Rust's `bytes().all(is_ascii_digit)`, true for the empty string.
   - `parse_semver` also rejects a major, minor or patch above `u64::MAX`, as the crate does.
   - Results: `1.0.0+123` > `1.0.0`; `1.0.0+01` > `1.0.0+1`, so they are not equal; `1.0.0+0` < `1.0.0+00`.
   - Test `test_plugin_versions_order_build_metadata_like_the_semver_crate`, with `active_plugin_version` selecting `1.0.0+123` over `1.0.0`.
2. **Decoded TOML keys (P2): fixed.** `hook_state_key` decodes a `hooks.state.<key>` table name to its TOML key, with `tomllib`, or with a key grammar for basic, literal and bare keys on Python < 3.11. The matching uses it in three places:
   - `drop_declared_hook_state`;
   - the profile scripts' base harvest;
   - the base merge's matching of declared against managed keys.

   An existing `[hooks.state.'<key>']` entry is therefore replaced by the one generated double-quoted entry, not duplicated. Tests in the profile and base merges: the output parses with `tomllib`, the key appears once, and the replacement warning is printed. On the previous head, the base script's output for that input fails to parse (`TOMLDecodeError: Cannot declare … twice`); the validation file has it verbatim.
3. **Report (P3): fixed.** It now says eight managed hooks; see the corrected Item 1 paragraph, which names the two unmanaged ones.

- **Re-run on the round-3 head `25522053`:** `make unit-test` (888 tests, OK, skipped=1), `make render-check`, the validator (rc=0), ruff, and the live base dry run (eight managed entries, idempotent). CI is green on all 13 checks, `mergeable_state` is `clean`, and the Bot wait found no review, inline comment or quota notice after the cutoff (`bot: none`). All of it is in the validation file.
- **Not run:** `make update`.

cost: n/a

## Revise round 4 (task_rev `sha256:3cb54131…aefa4116`)

The audit of 25522053 returned `incorrect` with 2 findings: one fixed, one dispositioned by the orchestrator.

1. **Commented table headers (P2): fixed in `00a5b09a`.** The root cause was in `table_name`, the header reader under `split_chunks`. It required a line to end in `]`, so `[name] # comment` stayed in the previous chunk.
   - **New reading:** it now scans the name quote-aware, so `]` or `#` inside a quoted key is part of the name. A header may be followed by whitespace and a `# comment`. Anything else after the closing bracket (`[a] = 1`, `[a] x`) is still not a header.
   - **Both copies fixed:** the base merge's hand-maintained copy and the generator's copy in every profile modify script. They are byte-identical.
   - **Shared paths:** the base merge and every profile script split through this one function, so the runtime-prefix carry-over (`hooks.state`, `marketplaces`, `tui.model_availability_nux`, `projects`), the retired-MCP purge and the hook-trust matching all get the fix. `hook_state_key` decodes the name `table_name` returns, so the comment never reaches it.
   - **Tests in both merges,** each in two variants:
     - a commented declared header is replaced once;
     - an uncommented declared header followed by commented unrelated tables (`[hooks.state."custom-hook"] # mine`, `[projects."/work"]  # trusted`) keeps both tables;
     - in each variant the output parses with `tomllib`.
   - **Direct `table_name` cases:** quoted `]` and `#`, escaped quotes, `[[array]] # c`, and non-headers.
   - **On the previous head:** the same tests fail with `TOMLDecodeError … twice` for the commented declared header, and `KeyError: 'custom-hook'` (the unrelated table lost) for the uncommented one. The validation file has the output verbatim.
2. **Out-of-sandbox dry runs (P2): dispositioned by the orchestrator** as a disclosed deviation, together with the earlier `codex app-server` probe. This round's live dry run ran inside the sandbox: it read `~/.codex/config.toml` and wrote only under `$TMPDIR`. It produced eight managed entries and the same output as round 3 from `[hooks.state]` on. It is idempotent and parses.

- **Re-run on `00a5b09a`:**
  - `make unit-test`: 891 tests, OK (skipped=1).
  - `make render-check`, the validator (rc=0) and ruff all pass.
  - CI and the Bot wait are in the validation file.
- **Evidence correction:** the round-3 validation section's printed `--jq` filter for Bot issue comments had its `\n` expanded to a line break by the shell's `echo`. The round-3 and round-4 copies now show the filter as executed.
- **Not run:** `make update`.

cost: n/a

## Revise round 5 (task_rev `sha256:64b069c5…16c96cb`)

The audit of 00a5b09a returned `incorrect` with 1 finding, fixed in `f6e99bad`.

1. **Headers inside multiline strings (P2): fixed.** `split_chunks`, shared by the base merge and every profile modify script, now tracks multiline string context line by line through `multiline_string_after(line, delimiter)`. It reads a table header only when no multiline string is open at the start of the line. The tracker:
   - skips single-line basic and literal strings, and stops at a `#` comment outside strings;
   - opens and closes a `"""` or `'''` delimiter on the same line;
   - honours backslash escapes inside a multiline basic string, so `\"""` stays inside it while `\\"""` closes it;
   - lets up to two quotes before the closing delimiter belong to the string (`"""x""""`).

   The base copy and the generated copy are byte-identical.
   - **Tests in both merges:** a profile table holds a multiline `developer_instructions = """…"""` and a `notes = '''…'''`, with header-like lines with and without a trailing comment, an escaped `\"""`, and a one-line `"""[a] # b"""`. The fixture survives verbatim, parses with `tomllib`, and the hook-state table next to it is unchanged.
   - **Direct tracker cases:** 13 of them.
   - **Previous head:** the same tests fail there. The commented line `[hooks.state."custom-hook"] # example` is moved out of the string, and `multiline_string_after` does not exist yet. The validation file has the output verbatim.
   - **Round 4:** its tests stay green.

- **Re-run on `f6e99bad`:**
  - `make unit-test`: 894 tests, OK (skipped=1).
  - `make render-check`, the validator (rc=0) and ruff all pass.
  - The live base dry run ran inside the sandbox. It read `~/.codex/config.toml`, wrote only under `$TMPDIR`, and its output is byte-identical to round 4. It is idempotent and parses.
  - CI and the Bot wait are in the validation file.
- **Not run:** `make update`.

cost: n/a

## Revise round 6 (task_rev `sha256:86e60274…c540aee4a4`)

The audit of f6e99bad returned `incorrect` with 1 finding. The orchestrator also required a parse guard. Both are in `a6c997b7`.

1. **Inline-table and dotted forms (P2): fixed.** Inside the `[hooks.state]` chunk, `drop_declared_hook_state` now also removes the assignment lines of a declared key, through `drop_declared_assignments`. It covers:
   - inline tables: `"<key>" = { trusted_hash = "…", enabled = false }`;
   - dotted assignments: `"<key>".trusted_hash = …` and `"<key>" . enabled = …`.

   How it decides:
   - **Leading key:** it reads the quoted or bare key before `=` or `.`. The key is decoded with `hook_state_key`, the same decoder the table names use.
   - **Multiline strings:** lines inside one are never read as assignments. A removed assignment whose value opens a multiline string takes that string's lines with it.
   - **Warning:** each removed key gets the same one-line divergence warning, with the old hash read from the removed lines.
   - **Other lines:** every one is kept.

   The `[hooks.state]` table is recognised however its name is spelled (`is_hook_state_parent`).
   - **Tests in the base merge and a profile merge:** both forms, next to an undeclared inline entry and a `[projects]` table. The output parses with `tomllib` and the declared key has the managed value. The undeclared entry and the table are unchanged, and the warning is printed once.
2. **Parse guard (orchestrator requirement): added to the base merge and every profile modify script.**
   - **Check:** `guarded_merge` parses the merged output with `tomllib` and checks that every declared key is under `hooks.state`. A duplicate already fails the parse, so each key appears exactly once.
   - **On failure:** it writes the current content back unchanged, prints `WARN: codex config merge produced invalid TOML; keeping the existing file` to stderr, and exits 0.
   - **Both base return paths are guarded:** a fresh file and an existing one.
   - **Test, in both scripts:** the splitter is patched to emit every chunk twice. The output is byte-identical to the current content, the WARN line is printed, and the exit code is 0.

- **Previous head:** the round-6 tests fail there. Both forms give `TOMLDecodeError … twice`, and the broken merge output is written instead of the current content. The validation file has the output verbatim.
- **Re-run on `a6c997b7`:**
  - `make unit-test`: 898 tests, OK (skipped=1).
  - `make render-check`, the validator (rc=0) and ruff all pass.
  - None of the existing merge tests hits the guard.
  - The live base dry run ran inside the sandbox. It read `~/.codex/config.toml`, wrote only under `$TMPDIR`, and its output is byte-identical to round 5. It is idempotent and parses.
  - **CI:** the first run failed only in `public-bootstrap (ubuntu-24.04, client)`: snapd got HTTP 408 from api.snapcraft.io for the `cups` snap. Fail-fast then cancelled the other two bootstrap jobs. The failed jobs were re-run once (`gh run rerun 37335551064 --failed`), and all 13 checks passed.
  - **Merge state and Bot:** `mergeable_state` is `clean`. The Bot wait found no review, inline comment or quota notice after the cutoff (`bot: none`). The evidence is in the validation file.
- **Not run:** `make update`.

cost: n/a

## Revise round 7 (task_rev `sha256:008356f1…7374859ed`)

The audit of a6c997b7 returned `incorrect` with 1 finding, fixed in `ad05e8be`.

1. **Equivalent header spellings (P2): fixed for the whole class.** `table_name`, which `split_chunks` uses in the base merge and every profile modify script, now returns `canonical_table_name(raw)`:
   - each dotted segment is decoded by `key_path`, with `tomllib` or, without it, the bare/quoted key grammar;
   - each segment is written bare where TOML allows, else as a basic string.

   Every comparison, grouping and prefix test the merges make runs on the names `split_chunks` returns, so all of them now use the decoded identity:
   - `runtime_prefix` and `is_runtime_table`;
   - `[hooks.state]` parent detection, now just `name == "hooks.state"`;
   - declared hook-state keys;
   - retired MCP servers and their children;
   - managed versus current table matching, and the profile scripts' base harvest.

   Kept chunks are still emitted with their original text, and the canonical function lives once, in the generated hook-trust block.
   - **Tests in the base merge and a profile merge:**
     - `[hooks . state]` and `["hooks"."state"]` parents, each with a stale inline entry for a declared key and an undeclared inline entry;
     - a declared child spelled `[ hooks . state . "<key>" ]`.

     Each case is replaced once, parses with `tomllib`, keeps the undeclared entry and `[projects]`, prints one warning, and does not fall back to the guard.
   - **Retired servers:** `[ mcp_servers . "github" ]` with its child `["mcp_servers".github.env]` is purged.
   - **Canonical names:** the `tomllib` path and the fallback grammar agree on 9 spellings.
   - **Previous head:** the stale trust survives for both parent spellings, because the guard kept the file, and the retired server is kept. The child-spelling case already passed there, because the key decoder handled it, and it stays as a regression check.
   - **Rounds 4–6:** their tests stay green.
2. **Visible wording change:** warnings name tables canonically. A bare-safe quoted key such as `hooks.state."hook"` now prints as `hooks.state.hook`; the existing test expectation is updated, along with three `table_name` expectations. Real hook keys contain `/`, `:` or `@` and stay quoted, so the live warnings in the dry run read exactly as before.

- **Re-run on `ad05e8be`:**
  - `make unit-test`: 902 tests, OK (skipped=1).
  - `make render-check`, the validator (rc=0) and ruff all pass.
  - The live base dry run ran inside the sandbox. It read `~/.codex/config.toml`, wrote only under `$TMPDIR`, and its output is byte-identical to round 6. It is idempotent and parses.
  - CI and the Bot wait are in the validation file.
- **Not run:** `make update`.

cost: n/a

## Revise round 8 (task_rev `sha256:6cea00f3…71367246d`)

The audit of ad05e8be returned `incorrect` with 3 findings. All are fixed: the code and docs in `0f6e7008`, the report evidence in the main checkout.

1. **Dotted assignments at every scope (P2): fixed.** `drop_declared_assignments` now runs on the root chunk and the `[hooks]` chunk as well as `[hooks.state]`.
   - **How it reads a line:** it takes the assignment's whole dotted key (`DOTTED_KEY_ASSIGNMENT`), decodes it with `key_path`, and puts the chunk's own key path in front. That path is empty at the root, `hooks` under `[hooks]`, and `hooks.state` under `[hooks.state]` (`HOOK_STATE_SCOPES`). A line whose full path is `hooks.state.<declared key>[.…]` is removed, quoted or bare, with the same one-line divergence warning.
   - **Cleanup:** `is_hook_state_parent` and the single-segment `LEADING_HOOK_STATE_KEY` are gone.
   - **Boundary (orchestrator decision):** inline-table containers holding declared keys stay with the parse guard and are not rewritten. Those are `state = { … }` under `[hooks]`, and `hooks = { … }` or `hooks.state = { … }` at the root.
   - **Tests in the base merge and a profile merge:**
     - `[hooks]` with `state."<key>".trusted_hash` and `state . "<key>" . enabled`;
     - the root with `hooks.state."<key>".trusted_hash` and `"hooks".state."<key>".enabled`.

     In each case the output parses with `tomllib`, the declared entry is the managed one and appears once, one warning is printed, and the guard does not trip.
   - **Container case (base):** the current content is kept byte-identical, with the WARN line and exit 0.
   - **Previous head:** the `[hooks]` case keeps the stale hash. In the root case the stale lines are dropped without the warning. The container case already passed, because of the round-6 guard.
2. **Hash source sentence (P3): fixed.** The `README.md` sentence and the manifest comment above `codex.hooks.state` now say: a config hook from its manifest definition embedded in the modify script, a plugin hook from the installed plugin file. Nothing else in the paragraph changed; prettier passes.
3. **Report evidence (P3): fixed.** The round-0 claim `make unit-test: 880 tests OK` now has its raw output. The six round-0 validation blocks were empty because the original paste failed. The saved outputs (20:47–20:52 +09:00, the working tree committed as `af569d15`) are restored there verbatim with a provenance note, including `Ran 880 tests in 215.464s` and `OK (skipped=1)`.

- **Re-run on `0f6e7008`:**
  - `make unit-test`: 905 tests, OK (skipped=1).
  - `make render-check`, the validator (rc=0), ruff and prettier all pass.
  - The live base dry run ran inside the sandbox. It read `~/.codex/config.toml`, wrote only under `$TMPDIR`, and its output is byte-identical to round 7. It is idempotent and parses.
  - **CI, Bot and merge state on `0f6e7008`:** CI was green on the first run, and the Bot wait found nothing after the cutoff (`bot: none`).
  - **`main` moved:** it reached `0f18bce9` (#285, herdr-agents), which shares only `README.md` with this PR, in another section; the merge was clean. `gh pr update-branch` made the final head `569bc44d`. CI on it is green (12 check runs plus the CodeRabbit status), and `mergeable_state` is `clean`.
- **Not run:** `make update`.

cost: n/a
