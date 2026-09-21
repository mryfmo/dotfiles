# dot-residuals-T1-a01 report

Status: ready_for_review

cost: n/a

## Result

- F1: the client bashrc now sources private `prompt.sh` and `aliases.sh` only when readable; public `history.sh` and `cache.sh` remain unconditional.
- F2: every `make update` now reuses `install/common/gh_extensions.sh`. Unauthenticated runs warn and remain retryable; authenticated runs install missing extensions, while already-installed extensions are left unchanged so `make update` does not become an upgrade path.
- F3: Linux Crit checks `${HOME}/.local/bin/crit` directly, prepends that directory to `PATH`, and refreshes Bash's command cache so an older mise shim cannot win or trigger repeated downloads.
- F4: `ensure_crit_cli` is now an allowed manifest repair step, so `REPAIR=1 make doctor` can invoke the scoped updater function.
- README now states that the next `make update` after `setup-gh` installs configured GitHub CLI extensions.

## Validation

- Test-first RED reproduced all four defects; focused tests then passed 4/4.
- Related unit suites passed 75/75; full unit discovery also exited 0.
- `bash -n`, shfmt diff, ShellCheck, `git diff --check`, and agent-asset validation passed.
- Auth retry trace produced the expected warning followed by `gh extension install seachicken/gh-poi`; an installed-extension fixture was preserved without an install call.
- `adh-test` public-only scratch user produced zero private-source errors, private stand-ins were sourced, and the user/home were removed.
- Local Bats was not run, per repository policy; updated Bats coverage remains for CI.
- Codex completed a Crit-data self-review with resolved approval record `r_1c1148`; the review gate passed with the repo-local receipt.

Full command evidence: `.orchestration/validation/dot-residuals-T1-a01.md`.

## Durable decision

[memory:decision] Recurring updates reuse the existing GitHub-extension installer and install only missing extensions; Linux Crit resolution treats `~/.local/bin/crit` as authoritative, and its manifest step is repairable by the runtime doctor.

CompactionDB command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-residuals-T1-a01: make update reuses install/common/gh_extensions.sh to install only missing authenticated gh extensions; Linux Crit resolution treats ~/.local/bin/crit as authoritative and make doctor may repair the ensure_crit_cli manifest step.'
```

Memory ID: `efc9f127-c02a-40a4-b4b6-bc335c7d90ba`

## Constraints honored

- No git commit or push.
- No local Bats execution.
- No mise config or lock changes.
- VM work used only `limactl shell adh-test`; no login or credentials were used, and both scratch users/homes were removed.
