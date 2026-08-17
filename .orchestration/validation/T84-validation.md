# T84 Validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/T84-crit-comments.json
review_outcome: approved
review_notes: Resolved scope approval `r_0f7b46` covers the complete staged/unstaged diff, hunk preservation, profile attributes, WARN-only doctor behavior, and all gates.

## Pre-edit status

`chezmoi status` reported:

```text
 M .agents/agent-config.yaml
MM .codex/deep.config.toml
 M .local/bin/common/agent-fanout
 M .local/bin/common/setup-gh
 M .local/bin/common/setup-gpg
MM .zprofile
MM .zshenv
MM .zshrc
 R .chezmoiscripts/common/06-install-agent-assets.sh
```

Deep's pre-edit `chezmoi diff` was mode-only, `old mode 100600` / `new mode 100644`.

## Complete zsh hunk table

| File / pre-edit hunk | Classification | Resolution |
|---|---|---|
| `.zshenv` file description: deployed documents all-shell/non-interactive Mosh/Herdr use; source documents the managed Claude updater | conflict (documentation from both sides) | Combined both facts in the shdoc description. |
| `.zshenv` shims-first `path`/`PATH` block exists only in deployed | local-only improvement | Preserved first, including mise shims, local/common, Homebrew, and `/usr/local` entries before inherited PATH. |
| `.zshenv` deployed `[[ -r private ]]` vs source `[ -f private ]` | conflict | Kept the deployed readability guard; it is the stronger condition for `source`. |
| `.zprofile` deployed shdoc emphasizes Homebrew then mise shims; source explains ARM Homebrew vs stale `/usr/local` | conflict (documentation from both sides) | Combined both behaviors and added a zsh shebang for static tooling. |
| `.zprofile` deployed uses `[[ -x brew ]]`; source uses `[ -x brew ]` | local-only hardening/style | Kept the native zsh conditional. |
| `.zprofile` source unconditionally activates mise before PATH; deployed guards mise and activates `zsh --shims` after PATH | conflict | Kept guarded deployed placement/`--shims`; missing mise no longer breaks login startup. |
| `.zprofile` deployed declares unique `path PATH` and spells out `/usr/local` plus local bins; source filters nonexistent directories with `(N-/)` | conflict | Kept all semantics: explicit ordered entries, unique `path PATH`, and equivalent `[[ -d ]]` filtering (shfmt-compatible and symlink-following like `-/`). |
| `.zshrc` guarded interactive mise activation exists only in deployed | local-only improvement | Preserved before interactive PATH setup. |
| `.zshrc` deployed adds common fpath unconditionally; source uses `(N-/)` | conflict | Preserved source filtering with equivalent `[[ -d ]]` and retained existing fpath order. |
| `.zshrc` deployed Herdr comments explain both Ghostty and Rootshell; source has one shdoc description | conflict (documentation) | Preserved both behavior statements in shdoc-compatible English and added file-level shdoc. Function behavior is unchanged. |
| `.zshrc` deployed guards `sheldon`; source initializes unconditionally | local-only improvement | Preserved the deployed command-existence guard. |

The Claude updater is identical on both sides and was retained unchanged; it was not an unclassified diff hunk.

## Post-edit zsh diff

The remaining read-only `chezmoi diff` hunks are deliberate source-side wins only:

- `.zshenv`: combined updater documentation and explicit `"${path[@]}"` array expansion; functional PATH order matches deployed.
- `.zprofile`: shdoc/shebang plus explicit `[[ -d ]]` filtering, preserving the source `(N-/)` behavior while retaining deployed ordering and guarded `--shims` activation.
- `.zshrc`: file/function shdoc, explicit fpath existence filtering, and shfmt redirect spacing; mise, sheldon, Herdr, and updater behavior otherwise match deployed.

Rendered syntax passed for all three targets:

```text
chezmoi cat ~/.zshenv  | zsh -n  # pass
chezmoi cat ~/.zprofile | zsh -n  # pass
chezmoi cat ~/.zshrc    | zsh -n  # pass
```

## Profile attribute evidence

- Source modes remain executable (`755`) for deep, express, review, security, and standard modifier scripts.
- `modify_private_` makes all five computed targets private (`600`).
- Post-edit deep diff is empty because live deep is already 600.
- Post-edit express/review/security/standard diffs contain only `old mode 100644` / `new mode 100600`; no content diff exists.
- All five live files contain Codex-owned runtime tables, so the sibling private treatment is justified uniformly.

## Doctor live smoke

`./scripts/check-agent-runtime.py` exited 0. It reported the four pending sibling profile changes as `permission divergence (mode-only)`, the three zsh targets as `two-sided drift`, ordinary ` M` targets as `unapplied source update`, and ended with `active agent runtime files match this chezmoi source tree`. No apply or repair command ran.

## Gates

```text
make format                                                    PASS
make validate-agent-assets                                     PASS
make unit-test                                                 PASS (338 tests)
shellcheck --shell=bash --exclude=SC1090 zsh trio              PASS
shfmt --indent 4 --space-redirects --diff zsh trio             PASS
zsh -n source and chezmoi-rendered zsh trio                    PASS
uv run --with pyyaml scripts/generate-agent-configs.py --check PASS
git diff --check                                               PASS
AGENT_REVIEWED=1 REVIEW_EVIDENCE=... make require-crit-review  PASS
```

ShellCheck has no zsh parser, so its bash parser was used after keeping the files shfmt/bash-parseable; SC1090 was excluded only for the intentionally dynamic, readability-guarded private zsh source.

The first generator freshness invocation omitted `--with pyyaml` and failed dependency discovery; the corrected repository-standard invocation above passed. The first post-change full unit run exposed one stale exact-syntax assertion for `(N-/)`; the test now asserts the equivalent directory guard and the rerun passed 338/338.

## Forbidden-action confirmation

- No Bats, `chezmoi apply`, live zsh/profile edit, dependency mutation, Git commit, or Git push occurred.
- `effects=none`

