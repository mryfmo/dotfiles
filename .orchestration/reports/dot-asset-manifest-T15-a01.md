# Report: dot-asset-manifest-T15-a01 — revision round 3 ready_for_review

- Worker: claude-standard-dot-a003
- Worktree: `.claude/worktrees/env-converge-T10`, branch `feat/asset-manifest` from origin/main `7879aea`
- **PR: https://github.com/mryfmo/dotfiles/pull/181**, head `cf7019c`, CI all green (nix skipped), not merged
- **Commits:**
  - `e26d9e0` feat(agents): declare every third-party asset in one manifest
  - `794d473` refactor(install): render version pins from the asset manifest
  - `1a2dc78` test(agents): cover asset manifest rendering and validation
- Evidence: `.orchestration/validation/dot-asset-manifest-T15-a01.md`
- **Worktree recreated:** the nested worktree was missing again at task start (not in `git worktree list`). It was recreated with `git worktree add -b feat/asset-manifest <path> origin/main` from the main checkout. Every command used `git -C <worktree>`, and the main checkout stayed on `main`.

## Design and decisions

**Manifest.** `assets:` at the end of `home/dot_agents/agent-config.yaml`. It has 16 entries, all values verbatim, no bumps:

| Asset | Source | Pin | Verify | Rendered into |
|---|---|---|---|---|
| mise-tools | mise | `home/dot_mise/mise.lock` | mise-lock | pointer only (`files:` config + lock) |
| mise | github-release | v2026.9.12 | release-shasums | install/common/mise.sh `MISE_VERSION` |
| sheldon | crates | 0.8.5 | cargo-locked | install/common/sheldon.sh `SHELDON_VERSION` |
| starship | github-release | v1.25.1 | release-sha256 | install/ubuntu/server/starship.sh `STARSHIP_VERSION` |
| aws-cli | github-release | 2.35.21 | gpg (FB5DB77F…) | install/ubuntu/common/aws_cli.sh `AWS_CLI_VERSION`, `AWS_CLI_FINGERPRINT` |
| homebrew-installer | git-commit | c7952e40… | sha256 | install/macos/common/brew.sh `HOMEBREW_INSTALL_COMMIT`, `_SHA256` |
| tode / terminal-browser | installer-script | v0.3.4 / v0.11.1 | installer-sha256 (payload not pinned) | scripts/lib/installer-pins.sh |
| crit / zed | github-release | v0.20.3 / v1.21.0 | sha256 per arch | scripts/lib/installer-pins.sh |
| understand-anything-installer | git-commit | 797ce796… | sha256 | scripts/update-agent-assets.sh `CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT`, `_SHA256` |
| compactiondb | vendored | 2.0.0+dotfiles.6 | manifest-sha256 (`vendor/compactiondb/MANIFEST.sha256`, not yet verified) | — (upstream `unknown`; local fork of `archive/CompactionDB-2.0.0.zip`) |
| agmsg | vendored | snapshot-2026-06-22 | none | — (upstream fujibee/agmsg; L.7) |
| claude-plugins | claude-plugin | per-plugin: superpowers 6.4.1, crit 1.8.10, ponytail 4.10.0, understand-anything 2.9.7 | none | `enforced: false` (values from `~/.agents/.installed-manifest.json`) |
| codex-plugins | codex-plugin | superpowers `unknown`, ponytail 4.10.0 + `last_updated`/`last_revision` | none | Codex config template (ponytail marketplace) |
| gh-extensions | gh-extension | seachicken/gh-poi v0.18.4 | none | `enforced: false` (installed version; `install/common/gh_extensions.sh` pins none) |

**Rendering choice** (the task asked me to document why): I kept in-place assignments rather than a new `install/lib/asset-pins.sh`.
- chezmoi inlines `install/*.sh` through `{{ include }}`, so at run time a script cannot source a sibling file relative to itself.
- A shared fragment would need either the wrappers (not in allowed_files) or `CHEZMOI_SOURCE_DIR`-relative sourcing, which breaks direct and bats execution.
- So `render_asset_constants` rewrites each `NAME="..."` assignment in its target. It preserves `readonly` or plain style, requires exactly one match and a plain value (`[A-Za-z0-9._+-]+`, so no shell injection through a pin), and feeds `expected_outputs`, which makes `--check` report drift.
- There is no new file.

**Ponytail:** `last_updated`/`last_revision` moved from `codex.marketplaces.ponytail` to `assets.codex-plugins.plugins.ponytail`. `render_codex` merges them in front, keeping the original key order. The validator's marketplace equality check merges them the same way. `codex-config-managed.toml` is byte-identical.

**Validator (`validate_assets`):**
- `source`, `upstream`, `pin` and `verify` are required.
- `verify` must be in the allowed set for the source; `sha256` is required for sha256/installer-sha256, and `gpg_fingerprint` for gpg.
- Any `*_VERSION="literal"` under `install/**/*.sh` whose name is not a rendered constant fails. A derived value such as `"${VAR}"` is allowed.
- Rendered drift is enforced by the existing `validate_generated_agent_configs` (generator `--check`).

**Pointer comments:** each installer gained one comment, `# Rendered from assets.<name> in home/dot_agents/agent-config.yaml; change it there.`. The `installer-pins.sh` header gained two lines. The comment in `update-agent-assets.sh` now points at the manifest (a comment-only change, which is the task's "only to source the rendered constants" scope).

## Byte identity (validation)

- Generator `--check`: "up to date".
- `codex-config-managed.toml` and `claude-settings-managed.json`: unchanged (`git diff --quiet` exit 0).
- `diff <(git show 7879aea:scripts/lib/installer-pins.sh) scripts/lib/installer-pins.sh`: only the two header comment lines.
- Installers: only the one pointer comment each.
- `bash -n`, shellcheck and shfmt: clean on all 7 touched scripts.
- **Mutation check:** changing `assets.sheldon.pin` made `--check` fail with `stale: install/common/sheldon.sh`, and the tree was restored.

## Tests

- **Generator** (`test_generate_agent_configs`, 4 new):
  - rendering into readonly and plain targets (untouched assets skipped);
  - a missing assignment fails;
  - a non-plain pin (`$(...)`) fails;
  - `--check` reports both stale targets, then "up to date" after regeneration.
- **Validator** (`test_validate_agent_assets`, 3 new):
  - complete declarations pass;
  - 5 incomplete-declaration cases fail;
  - an unrendered literal `TOOL_VERSION` fails and a derived one passes.
- Required suites (generator, validator, supply-chain, runtime-health): 120 tests OK.
- Full suite: 425 tests, with only the known, unrelated `test_permgate.test_bench_runs_five_layer_two_fixtures` load flake (as in T14; passes in isolation and on CI).
- CI `test` jobs (all three OSes) and `public-bootstrap` jobs (which run the installers): green.
- Bats not run locally.

## Known interim limitation (for L.3) — please decide

`scripts/upgrade-tools.sh` (`bump_terminal_tool_pins`) still rewrites `scripts/lib/installer-pins.sh` wholesale from upstream latest, and it is outside allowed_files. After this PR, a `make upgrade` that bumps tode, terminal-browser, Crit or Zed leaves that file out of step with `assets:`. The generator's `--check` and the validator then fail, which blocks CI until the new values are copied into `assets:`. That is a manual step until L.3 redirects the bump into the manifest. This PR does not touch `upgrade-tools.sh`.

## Not done / out of scope

- No version bumps.
- The URLs (`TERMINAL_*_INSTALLER_URL`, the release base URLs in installers) stay in the scripts; `upstream:` records them.
- `install/common/gh_extensions.sh` still installs gh-poi unpinned (L.2).
- The CompactionDB MANIFEST.sha256 is still unverified (L.5/L.7).
- The PR is not merged.

## Revision round 1 (orchestrator review + CodeRabbit full review of PR #181)

Commits:
- `836a740` fix(validate): tighten the asset manifest checks and record real provenance
- `367023e` fix(upgrade): write bumped terminal tool pins into the asset manifest

**Head:** `367023e`. **CI all green** (nix skipped). `allowed_files` was widened to `scripts/upgrade-tools.sh` and its tests, and only those extra files were touched.

| Item | Disposition |
|---|---|
| **S1** `bump_terminal_tool_pins` wrote installer-pins.sh, so a regenerate reverted the bump | **Fixed (367023e).** The bump passes the fetched pins and SHA256s to `generate-agent-configs.py --set-asset NAME.FIELD=VALUE`. `set_asset_field` rewrites only the named line under `assets.<name>` (nested `sha256.<arch>` supported, comments kept, plain values only, unknown asset or field rejected). `main` parses the edited text and verifies every value **before** writing the manifest or any output, then renders the asset constants. The heredoc header copy is gone, so installer-pins.sh is only rendered. Live trial on the real repo (validation): two manifest lines and two rendered constants changed, `--check` clean, `$(id)` rejected, restored. |
| **S2** aws-cli provenance | **Fixed (836a740).** `source: https-download` (new, verify ∈ {sha256, gpg}), `upstream: https://awscli.amazonaws.com`. |
| **N1** install_path/installer for installing sources | **Fixed.** Required for github-release, https-download, crates, git-commit, installer-script and vendored. Added to homebrew-installer (Homebrew default prefix), compactiondb (`~/.agents/compactiondb`, from `update_compactiondb`'s rsync target) and agmsg (chezmoi `home/dot_agents/skills/agmsg`). |
| **N2** agmsg pin invented | **Fixed.** `pin: unknown`, note "imported in commit 83eb1e4 (2026-06-22) without an upstream version; replaced by an npm pin in L.7". |
| **N3** non-string pins | **Fixed.** `pin`, every `sha256`/`sha256.<arch>`, and `plugins.*.pin` must be strings. Tests cover a float top-level pin and a float plugin pin. |
| **N4** sweep scope | **Fixed.** `install/**/*.sh` and `scripts/**/*.sh`, `[A-Z0-9_]*_VERSION` and `[a-z0-9_]*version` literal assignments. |
| **N5** gh-poi pin / `enforced: false` | **Fixed.** gh-extensions `pin: unknown` with note "install/common/gh_extensions.sh installs seachicken/gh-poi unpinned". `enforced` removed everywhere; plugin entries note that pins are installed versions not enforced until L.2. |
| README 481-482 stays true | **Fixed.** The Asset manifest paragraph describes `make upgrade --set-asset`, `pin: unknown`, the widened sweep and the dropped `enforced`. The Crit and terminal-tool paragraphs say the pins are declared under `assets:` and rendered into installer-pins.sh. |
| **CodeRabbit** 4103807540 (`validate-agent-assets.py`): key the allowed set by `(render.file, constant)` | **Adopted (836a740)**, test case `install/ubuntu/common/copy.sh` duplicates `MISE_VERSION`. Replied on the thread (discussion_r4103925053). That was the only item in CodeRabbit's full review, and no further CodeRabbit review appeared on the new commits. |

**Tests added this round:**
- Generator: `set_asset_field` rewrite and rejection cases (5 subtests); `--set-asset` end to end with a PyYAML-free fixture parser; an invalid assignment leaves the manifest untouched.
- Validator: 9 incomplete-declaration subtests (adds install_path, installer and two float pins); 4 unrendered-literal cases across `install/` and `scripts/`, uppercase and lowercase, plus the duplicate rendered name.
- Runtime health: the bump calls the generator with all 10 `--set-asset` assignments (pins v9.9.9, 64-hex checksums) and leaves `installer-pins.sh` byte-identical to the committed file.

**Results:**
- Required suites (generator, validator, supply-chain, runtime-health): OK.
- Full suite: 429 tests with only the known `test_permgate.test_bench_runs_five_layer_two_fixtures` flake.
- Byte identity against the base still holds: templates unchanged, installer-pins differs only by the two header comment lines.

The "Known interim limitation (for L.3)" section above is **resolved** by S1.

## Revision round 2 (delta review of 836a740 + 367023e)

Commit: `f4db46b` fix(agents): harden the --set-asset manifest write path. **Head:** `f4db46b`. **CI all green** (nix skipped).

| Item | Disposition |
|---|---|
| (1) Read-back must require `isinstance(value, str)` | **Fixed (f4db46b).** The read-back walks the parsed manifest to the raw value and fails unless it is a `str` equal to the requested value: `ERROR: assets.crit.sha256.linux-amd64 did not update to the string '1234': 1234`, with nothing written (live, validation). Test: `test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string`. |
| (2) YAML error on re-parse → message, not traceback | **Fixed (f4db46b).** `except yaml.YAMLError` → `fail("--set-asset produced an unparsable manifest: …")`, with nothing written. The `except` target is guarded (`()` when PyYAML is absent), so the handler itself cannot raise `AttributeError`. Test: `test_set_asset_reports_an_unparsable_manifest_without_a_traceback`. |
| (3) Restrict `--set-asset` to pin, sha256, sha256.<arch> | **Fixed (f4db46b).** `SETTABLE_ASSET_FIELD = pin|sha256|sha256\.[A-Za-z0-9-]+`, enforced in `set_asset_field`: `ERROR: --set-asset may change only pin, sha256, or sha256.<arch>: crit.upstream` (live). Test: `test_set_asset_refuses_fields_other_than_pins_and_checksums` (render.file, upstream, sha256.linux-amd64.extra). |

**Complete disposition of every review item on PR #181:**
- Orchestrator crit comments:
  - r_c63bdd (summary): addressed.
  - c_f5aa59 **S1**: fixed in 367023e.
  - c_b45e03 **S2**: fixed in 836a740.
  - c_94aea3 **N2/N5**: fixed in 836a740.
  - c_0b001b **N1/N3/N4**: fixed in 836a740.
- Delta items (1)–(3): fixed in f4db46b.
- CodeRabbit inline **4103807540** (key by `(render.file, constant)`): fixed in 836a740. My reply is 4103925053, and CodeRabbit acknowledged the fix in 4103928427. CodeRabbit posted no other actionable items. I did not re-trigger it (1 review/hour plan limit).

**Validation:**
- Generator: 33 tests OK (7 `set_asset` tests).
- Required suites: 127 OK.
- Full suite: 432 tests, with only the known `test_permgate.test_bench_runs_five_layer_two_fixtures` flake.
- Generator `--check` and validator: ok.

## Revision round 3 (CodeRabbit review 5317380626 on f4db46b)

Commit: `cf7019c` fix(validate): reject unquoted and single-quoted literal installer versions. **Head:** `cf7019c`. **CI all green** (nix skipped).

| Item | Disposition |
|---|---|
| CodeRabbit **4104294574** (`validate-agent-assets.py:551`): `LITERAL_VERSION_ASSIGNMENT` matched only double-quoted values | **Fixed (cf7019c).** The pattern now matches `"…"` (no `$` or backtick), `'…'`, and unquoted tokens (no quotes, `$`, backtick, `;` or parentheses) up to an assignment boundary (`\s`, `;`, end of line). Derived values stay allowed: `"${VAR}"`, `${VAR}`, `"$(cmd)"`, backticks, and a bare `local version`. |

- **Tests:** two negative cases, `readonly TOOL_VERSION=1.2.3` and `TOOL_VERSION='1.2.3'; export TOOL_VERSION`, and four derived forms that must pass.
- **Mutation check (validation):** the old regex misses exactly the two new cases; neither regex flags the derived forms.
- **Repo check:** the validator still passes on the real repo, so no existing script had such a literal.
- **Thread:** my reply is `discussion_r4104363635`. CodeRabbit ran an analysis chain on it, and the post-round sweep with `scripts/pr-feedback.py` shows both CodeRabbit threads resolved. Its review on `cf7019c` (5317470018) has an empty body, so there are no new actionable items.
- **Unit suites:** validator and generator, 75 OK.

## Durable facts

[memory:decision] third-party asset versions live only in agent-config.yaml assets:, rendered by generate-agent-configs.py; installers carry no literal versions

```bash
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "third-party asset versions live only in agent-config.yaml assets:, rendered by generate-agent-configs.py; installers carry no literal versions"
# → a0724e54-d330-47b1-8b44-dc981e538fac
```

cost: n/a
