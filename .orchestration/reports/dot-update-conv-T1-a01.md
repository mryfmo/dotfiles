# dot-update-conv-T1-a01 report

cost: n/a

## Result

- F1: make update now runs public and private chezmoi apply without excluding scripts. Chezmoi's content-hash state executes newly committed run_once scripts once while leaving unchanged scripts skipped; make upgrade remains the only pin-advancement path.
- F2: update_codex_superpowers captures Codex combined output. Normal failures print only the existing unavailable/login guidance, successful installs print one success line, and raw CLI output is emitted only when DOTFILES_DEBUG is set.
- F3: lifecycle Bats expectations now require script-inclusive public/private apply, and the runtime-health unit test rejects any leaked Error: line.

## Validation

- Test-first RED reproduced the raw Codex Error: leak; focused GREEN passed.
- bash syntax, shellcheck -x, shfmt, git diff check, agent-asset validation, and the full 363-test Python suite pass.
- In adh-test, old commit b884aec initialized a pre-bootstrap state with 23 real rendered run_once hashes. Literal make update ran twice: both exited 0, run_once_51 changed the scratch user's shell only on the first run, the second run did not repeat it, and final chezmoi status/drift warnings were empty.
- The actual Superpowers function under an unauthenticated Codex stub emitted the two guidance lines, returned 0, and emitted zero raw Error: lines.
- Crit-data approvals r_57d210 and r_a8a6ea are resolved and make require-crit-review passes with repo-local evidence.

Full verbatim evidence is in .orchestration/validation/dot-update-conv-T1-a01.md.

## Durable decision

[memory:decision] make update converges every committed public/private chezmoi entry, including new run_once content hashes, while make upgrade alone advances tool pins; Codex plugin command output remains hidden unless DOTFILES_DEBUG is enabled.

CompactionDB command:

    python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-update-conv-T1-a01: make update applies public and private chezmoi scripts so newly committed run_once content hashes execute exactly once while unchanged hashes remain skipped; make upgrade remains the only tool-pin advancement path. Codex Superpowers add output is captured and raw CLI errors are shown only when DOTFILES_DEBUG is set.'

Memory ID: e24e8cbb-92a4-4643-b4c8-440ebe111a46

## Constraints honored

- No git commit, push, local Bats execution, Codex login, credential transfer, mise config/lock change, or home/ source edit.
- VM access used only limactl shell adh-test for task work; the credential-free scratch user, home, and sudoers entry were removed.
- No persistent external installation side effects remain.
