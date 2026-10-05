# AGMSG-TASK dotfiles-T82b-codex-hook-trust-pins-a01

Drafted 2026-10-05 11:30Z by the orchestrator seat (dispatched to `claude-standard-dot-a005`, worker-c; Codex-boundary source `codex.hooks`, so a Claude seat). Follow-up of T82 PONG 1 and the standing `make update` warning "hook trust divergence" (ponytail). Goal: no interactive `/hooks` trust step on any host.

## Objective

Codex runs a config-defined or plugin hook only when `[hooks.state."<key>"]` carries `trusted_hash` for the hook's current content; otherwise it skips it silently. Pin the trust in the manifest so `make update` deploys it everywhere:

1. **Derive Codex's hash algorithm from a known pair.** The deployed `~/.codex/standard.config.toml` and `security.config.toml` already hold `[hooks.state."~/.codex/config.toml:permission_request:0:0"] trusted_hash = "sha256:64d9851fb629f7cd5608706436fb5b8588dc60abf355893ebe3eaca401a9ff65"` (plus `enabled = true`) for the permgate hook defined in `~/.codex/config.toml` (`[[hooks.PermissionRequest]]` matcher `*`, command `~/.local/bin/common/permgate codex`, timeout 10, statusMessage "Evaluating permission request"). Find the canonical form whose sha256 reproduces that value (candidates: the hook object as canonical JSON with sorted keys, the TOML table text, the command string alone, with or without matcher/timeout/statusMessage); the Codex source (`codex-rs/hooks`, schema under `codex-rs/hooks/schema/generated`) is the reference, fetched with WebFetch. VERIFY: the derived function must reproduce `64d9851f…` from the deployed permgate definition and, for the three ponytail plugin hooks, the hashes Codex itself wrote into `security.config.toml` (`5f81d38f…` session_start, `6a6f42bc…` user_prompt_submit, `1423b56c…` subagent_start) from the installed `ponytail` plugin `hooks/claude-codex-hooks.json`. Both reproductions pasted verbatim are the acceptance evidence for the algorithm.
2. **Pin the four config hooks** (`permission_request`, `pre_compact`, `post_compact`, `session_end`, indices `0:0`) in the manifest `codex.hooks.state`. The key embeds the absolute path of the user's `config.toml`, which differs per host (`~` vs `~`), so the manifest key must use `{{ .chezmoi.homeDir }}` and the renderer must emit it so the chezmoi template expands it inside the quoted TOML key (check `quote_toml_key` / the `[hooks.state.*]` emission in `scripts/generate-agent-configs.py`; add template-aware quoting if `json.dumps` would escape the braces or quotes wrongly). Carry `enabled = true` as the live profile entry does, if the renderer supports it (add the field if not). Keep the hashes host-independent: if Codex hashes the absolute command path, the hash differs per host too; then the manifest needs per-OS values or the renderer must compute the hash at render time from the rendered hook (preferred: compute in the renderer from the same definition it renders, so the pin can never drift; say which you did).
3. **Refresh the ponytail pins** to the current hook content (the values Codex wrote in `security.config.toml`), which removes the three "hook trust divergence" warnings on both hosts; keep the crit pin.
4. **Tests:** `tests/unit/test_generate_agent_configs.py` covers the templated key, `enabled`, and the hash computation (fixture hook → known hash from step 1); `make render-check` clean; `uv run --no-project --with pyyaml scripts/validate-agent-assets.py` rc=0.
5. **Live verification is the orchestrator's** (after `make update` on this host): a headless `codex --profile express exec` run must leave a `session_end|…|codex` row in the main checkout's CompactionDB. Do not run `make update` yourself.

Forbidden: `make update`/`apply`; editing `home/dot_agents/permgate-policy.yaml` or the permgate script; any Claude-boundary source (`claude.*` blocks, Claude templates); thread resolution; local bats.

[memory:decision] dotfiles-T82b (orchestrator 2026-10-05): Codex hook trust is pinned in the manifest (`codex.hooks.state`, templated per-host keys, hashes reproduced from Codex's own algorithm) and deployed by `make update`; no interactive `/hooks` trust step; the ponytail pins follow the installed plugin content.

## Repo / branch

- Work ONLY in your own worktree (worker-c). `git fetch origin`; `git switch -c feat/codex-hook-trust-pins --no-track origin/main` (main at b277a45c or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `home/dot_agents/agent-config.yaml` (`codex.hooks.state` only), `scripts/generate-agent-configs.py` (Codex-rendering parts), `home/.chezmoitemplates/codex-config-managed.toml` (rendered), `scripts/validate-agent-assets.py` only if the hook-table comparison needs the new fields, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py` (if touched), README one paragraph (the `/hooks` operator step becomes "deployed by make update").
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T82b-codex-hook-trust-pins-a01.md` (main checkout, through the gate; mask before RESULT; `cost: n/a`).

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -8
uv run --no-project python -m unittest tests.unit.test_generate_agent_configs 2>&1 | tail -3
make render-check 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
grep -c 'hooks.state' home/.chezmoitemplates/codex-config-managed.toml
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only; end on a quota notice and record it); fix P0/P1 findings, inline or review-body; do not resolve threads.
3. Artifacts at the exact expected paths, masked; validation with verbatim outputs, PR number, head SHA; the two hash reproductions.
4. CompactionDB `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` with the `[memory:decision]` text; paste the command and the returned id.
5. `AGMSG-RESULT v1 task_id=dotfiles-T82b` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. `cost: n/a`. max_turns=30.

### PONG decision 1 (orchestrator, 2026-10-05 11:40Z) — apply-time hashing and managed override

Item 1 accepted as proven (algorithm reproduces all nine current hashes, permgate included). Decisions on the blockers:

- **(a) Compute at apply time, not render time.** Extend the chezmoi modify scripts that merge the managed Codex config (`home/dot_codex/modify_private_config.toml` and the per-profile `home/dot_codex/modify_private_*.config.toml`, now in `allowed_files`, plus their tests) so that, for every `hooks.state` key the manifest declares, the script computes `trusted_hash` at apply time with the proven algorithm from the hook definition it has just merged (config-defined hooks: the rendered `[[hooks.<Event>]]` table of the merged document, so the absolute command path is the host's own) and, for a plugin hook, from the installed plugin's hook file on that host (resolve the plugin path from the key `<plugin>@<marketplace>:hooks/<file>:<event>:<i>:<j>` under `~/.codex/plugins/cache/<marketplace>/<plugin>/…`; if the file is absent, keep the manifest's literal and warn). The manifest therefore declares *which* hooks are trusted (key, `enabled`, optional literal fallback), not a host-specific digest. Keep the key templated with `{{ .chezmoi.homeDir }}` where it holds a path.
- **(b) Managed keys override.** For keys the manifest declares, the merge replaces an existing `[hooks.state."<key>"]` entry (that is what removes the stale ponytail `35ad…` values and the three warnings); keys the manifest does not declare are kept untouched, so trust the operator granted elsewhere survives. The "hook trust divergence" warning then compares the computed value against the existing one and reports the replacement once.
- **Semantics and security (README, one paragraph):** the manifest trusts exactly the hooks this repository ships or installs (the four config hooks, crit, ponytail); a hook anybody else writes into `config.toml` or a plugin stays untrusted. For a plugin, trusting the installed content means a plugin upgrade by `make update` is trusted by the same `make update`; say so explicitly.
- **Ponytail values:** use what Codex reports as current on this host at the time of your change only as the literal fallback; the apply-time computation is the source of truth.
- Scope stays Codex-boundary (Claude seat). Add tests: the modify script's hash for a fixture config hook equals the proven algorithm's value; a declared key replaces a stale entry; an undeclared key is preserved; a missing plugin file keeps the literal and warns.

Reply `AGMSG-PONG v1 … status=working` when you resume; RESULT as before.

## Revise round 1 (orchestrator, 2026-10-05 12:30Z) — audit of c54fdc0c: `incorrect` (5 findings; 3 to fix here, 2 dispositioned by the orchestrator)

1. **`make update` ordering (P1).** `chezmoi apply` computes the trust hashes, and the plugin update step runs afterwards, so a plugin whose hooks change in the same `make update` stays untrusted until the next apply. Fix: after the agent-asset update step in the `update` target, refresh the Codex hook trust (re-apply only the Codex config files: `chezmoi apply --force ~/.codex/config.toml ~/.codex/*.config.toml`, or an equivalent `make codex-hook-trust` target that runs the modify scripts again) so the hashes follow the installed plugin content within one `make update`. `Makefile` (and `scripts/update-agent-assets.sh` if the refresh belongs there) join `allowed_files`; add a unit test that pins the target order (the refresh comes after the plugin update) and keep `make update` unattended (no prompt, no network dependency for the refresh).
2. **Two cached plugin versions (P2).** Resolve the active version instead of falling back: prefer what Codex records as installed (the marketplace/plugin manifest under `~/.codex/plugins` or the version the Codex config names); if that is not recorded, take the newest version directory by semantic version, then by mtime; fall back to the literal with a warning only when no copy exists. Test with two cached versions.
3. **Evidence corrections (P3):** the report's "CI and Bot" line still says `mergeable_state=behind`; make it `clean` with the final-head wording; validation line 5 labels `af569d15` the final head, which is `c54fdc0c` (the diff head is `af569d15`).
4. **Orchestrator dispositions (no change from you):** (P2 spec) config hooks are hashed from the manifest definitions rather than the merged document — accepted as the intended design (a hook altered on disk by anyone else no longer matches and Codex marks it `modified`); PONG decision 1's wording is corrected here; add one README sentence stating that config-hook trust follows the manifest definition, so a hand-edited hook in `~/.codex/config.toml` is deliberately untrusted. (P2 process) running `codex app-server` outside the sandbox for the read-only `hooks/list` probe is recorded as a disclosed boundary deviation; do not repeat it; if a future verification needs it, ask first with a PONG.

Then push, `gh pr checks --watch`, Bot wait (end on a quota notice and record it), `AGMSG-RESULT v1 … round=1`. Do not run `make update`; the orchestrator deploys and verifies live.

## Revise round 2 (orchestrator, 2026-10-05 13:22Z) — audit of 315e7394: `incorrect` (2 findings, both in `active_plugin_version`)

1. **Symlinked version directories (P2, `generate-agent-configs.py:701`).** `Path.is_dir()` follows symlinks; Codex (`core-plugin-common/src/installed.rs`, rust-v0.160.0) excludes symlinked version entries. With a real `4.12.0` directory and a `local` symlink the block hashes `local` while Codex loads `4.12.0`. Exclude symlinks (`entry.is_symlink()` → skip) in the version listing; regression test with a real version directory plus a symlinked `local`.
2. **Semver validity (P2, `:659`).** The regex accepts numeric pre-release identifiers with leading zeros (`1.10.0-01`), which the `semver` parser Codex uses rejects, falling back to lexical order (`1.9.0` wins). Match the parser's rules (numeric identifiers in pre-release must not have leading zeros; build identifiers may) before comparing; a candidate that fails to parse takes the lexical path exactly as Codex does. Regression test: `1.10.0-01` vs `1.9.0` selects `1.9.0`.
3. Re-run the generated-output check and the live dry run; keep the report/validation accurate for the new head. Then push, `gh pr checks --watch`, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=2`. No `make update`.

## Revise round 3 (orchestrator, 2026-10-05 13:55Z) — audit of d8702155: `incorrect` (3 findings)

1. **Build-metadata ordering (P2, `generate-agent-configs.py:705`).** Mirror the `semver` crate's `Ord` for `BuildMetadata` exactly (dtolnay/semver `src/impls.rs`, the version Codex 0.160.0 vendors; fetch it with WebFetch): an empty build is less than a non-empty one (`1.0.0+123` > `1.0.0`), identifiers are compared per the crate's rules (numeric identifiers with leading zeros are not equal to their stripped form; follow the crate's length-then-lexical handling), and `1.0.0+01` ≠ `1.0.0+1`. Regression tests for both cases from the finding.
2. **Decoded TOML keys (P2, `:792`).** Compare `[hooks.state.<key>]` table names by their decoded TOML key, not the header text: parse basic (double-quoted, with escapes) and literal (single-quoted) quoting so an existing `[hooks.state.'…']` entry for a declared key is replaced rather than duplicated. Regression test: an existing single-quoted entry → one generated double-quoted entry, output parses as TOML (use `tomllib`).
3. **Report (P3):** "all nine hashes" → the eight managed hooks verified (the discovery output lists ten hooks; say which two are not managed).

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=3`. No `make update`.

## Revise round 4 (orchestrator, 2026-10-05 14:34Z) — audit of 25522053: `incorrect` (2 findings; 1 to fix, 1 dispositioned)

1. **Commented table headers (P2, `generate-agent-configs.py:869`).** `split_chunks()` does not recognise `[hooks.state."custom-hook"] # comment` as a table header, so when the preceding declared chunk is dropped the commented table goes with it (data loss in both base and profile merges); a commented declared header is not matched either and is duplicated (invalid TOML). Fix the header recognition in the shared chunk splitter (header = optional whitespace, `[…]`, optional trailing `# comment`), apply the same to the key decoding, and add regression coverage for both cases (unrelated commented table preserved; commented declared header replaced once, output parses with `tomllib`). Check whether the pre-existing merge paths (runtime prefixes, retired servers) share the splitter and gain the same fix.
2. **Sandbox (P2, dispositioned by the orchestrator):** the modify-script dry runs you ran outside the sandbox are read-only against `~/.codex/config.toml` with output to a temp file; recorded as a disclosed deviation together with the app-server probe. From now on run such dry runs inside the sandbox (reading `~/.codex` is permitted there; write only under `$TMPDIR`); if a dry run needs more, ask with a PONG first.

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=4`. No `make update`.

## Revise round 5 (orchestrator, 2026-10-05 15:10Z) — audit of 00a5b09a: `incorrect` (1 finding)

1. **Headers inside multiline strings (P2, `generate-agent-configs.py:975`, base script `:80`).** With trailing comments accepted, a line such as `[hooks.state."custom-hook"] # example` inside a multiline string (a profile's `developer_instructions = """…"""`, or `'''…'''`) is now taken for a table header; the chunk is split and reordered and the output no longer parses (`aeb025e8` preserved it). Fix in the shared splitter: track multiline basic (`"""`) and literal (`'''`) string context line by line (a header is recognised only outside a multiline string; handle a delimiter opening and closing on the same line, and `"""` escaped inside a basic multiline string), so content inside such strings is never a chunk boundary. Regression coverage: a profile config whose multiline `developer_instructions` contains a header-like line with and without a trailing comment survives the base and a profile merge unchanged and parses with `tomllib`; keep the round-4 tests green.

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=5`. No `make update`.

## Revise round 6 (orchestrator, 2026-10-05 15:45Z) — audit of f6e99bad: `incorrect` (1 finding) plus a safety net

1. **Inline-table and dotted forms (P2, `generate-agent-configs.py:868`).** A declared key already present under `[hooks.state]` as `"<key>" = { trusted_hash = "…", enabled = false }` or as dotted assignments (`"<key>".trusted_hash = "…"`) is not recognised, survives, and collides with the appended `[hooks.state."<key>"]` table. Inside the `[hooks.state]` parent chunk, remove the assignment lines whose decoded leading key (quoted or bare, before `=` or before `.trusted_hash`/`.enabled`) is a declared key, with the same one-line divergence warning; keep every other line. Regression tests for both forms in the base and a profile merge, output parsed with `tomllib`.
2. **Parse guard (orchestrator requirement, both base and profile scripts).** After merging, parse the result with `tomllib` when available (Python ≥ 3.11; the deployed interpreter qualifies) and check that every declared key appears exactly once; on failure, write the *unmodified current content* back, print one `WARN: codex config merge produced invalid TOML; keeping the existing file` line to stderr, and exit 0, so `chezmoi apply` can never deploy an unreadable Codex configuration whatever representation a future config uses. Test: an input that would still trip the merge (construct one by patching the splitter in the test) leaves the current content byte-identical and prints the warning.

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=6`. No `make update`.

## Revise round 7 (orchestrator, 2026-10-05 16:20Z) — audit of a6c997b7: `incorrect` (1 finding): canonical table identity

1. **Equivalent header spellings (P2, `generate-agent-configs.py:916`).** `[hooks . state]` or `["hooks"."state"]` are recognised as headers but kept under their raw names, so the runtime grouping misses the existing parent, appends another `[hooks.state]`, the guard trips and the stale trust survives. Close the whole class: derive every table identity from the decoded key path (decode each dotted segment, bare or quoted, with `tomllib` when available and the existing grammar otherwise) and use that canonical identity wherever the merge compares, groups or prefixes table names (`runtime_prefix`, parent detection, declared keys, retired servers), while emitting each kept chunk with its original text. Regression cases: `[hooks . state]` and `["hooks"."state"]` parents with stale entries → replaced once, parses, no guard fallback; a declared child spelled `[ hooks . state . "<key>" ]`; the round-4 to round-6 cases stay green.

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=7`. No `make update`.

## Revise round 8 (orchestrator, 2026-10-05 17:00Z) — audit of ad05e8be: `incorrect` (3 findings): dotted scopes, README source sentence, report evidence

1. **Dotted assignments at every scope (P2, `generate-agent-configs.py:954`).** Round 6 bounded the textual removal to the `[hooks.state]` chunk, so a declared key written as a dotted assignment under `[hooks]` (`state."<key>".trusted_hash = "sha256:stale"`) or at the root (`hooks.state."<key>".enabled = false`) survives, collides with the appended table, and the guard keeps the whole current file (stale trust, managed updates discarded). Apply `drop_declared_assignments` to the root chunk and the `[hooks]` chunk as well, resolving the leading dotted key through `key_path` with the scope prefix (`hooks.state.` at the root, `state.` under `[hooks]`, none under `[hooks.state]`) so quoted and bare spellings decode uniformly, with the same one-line divergence warning. **Boundary (orchestrator decision, final):** inline-table *containers* holding declared keys (`state = { "<key>" = {…}, … }` under `[hooks]`, `hooks = {…}` or `hooks.state = {…}` at the root) are out of scope for textual replacement by design: rewriting an inline table's interior is a different operation, Codex never writes that form, and the round-6 parse guard keeps the file and warns. Do not extend the merge further. Tests: `[hooks]` + `state."<key>".trusted_hash = …` and root `hooks.state."<key>".trusted_hash = …`, each in a base and a profile merge, output parsed with `tomllib`, replaced once, no guard fallback; one container case proving the guard leaves the current content byte-identical and prints its WARN; rounds 4–7 stay green.
2. **Hash source sentence (P3, `README.md:370` and the manifest comment at `agent-config.yaml:159`).** "a config hook from the merged config" contradicts the implementation and PONG decision 1: a config hook is hashed from the manifest definition embedded in the modify script, a plugin hook from the installed plugin file. Correct that one sentence and that one comment; nothing else in the paragraph.
3. **Report evidence (P3, `reports/…:55`).** "`make unit-test`: 880 tests OK" has no pasted output and the original validation blocks are empty: paste the raw output if you still have it, otherwise delete the historical claim; the 902-test result of the final head keeps its pasted support. Main-checkout artifact, same gated write as before.

Then push, CI, Bot wait (quota notice ends it), `AGMSG-RESULT v1 … round=8`. No `make update`.
