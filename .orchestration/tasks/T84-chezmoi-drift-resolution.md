# T84: chezmoi ドリフトの本質解消(ローカル改良の取り込み+権限属性+ドリフト検査)

task_id: T84
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: operator directive 2026-08-17 「本質対処」(drift triage by orchestrator)

[memory: decision — chezmoi drift is resolved by class, not by blanket apply: uncommitted local improvements are merged into source hunk-by-hunk (never overwritten), permission divergence is fixed with source attributes (modify_private_), and the deployment-skip class gets automated detection via a doctor chezmoi-drift check.]

## Class B: zsh トリオのソース統合(最重要・退行厳禁)

Deployed ~/.zshenv, ~/.zprofile, ~/.zshrc contain functional hardening
that exists in NO git commit (verified: `git log --all -S shims|Mosh`
empty): shims-first PATH for non-interactive SSH (Mosh/Herdr
bootstrap), guarded mise/sheldon init, `mise activate --shims` at
login, explicit /usr/local + ~/.local/bin ordering. The current repo
sources (home/dot_zshenv, home/dot_zprofile, home/dot_zshrc) have
their own later edits (e.g. ce79eac Claude postinstall updater).

1. For each pair (deployed file vs repo source), produce a HUNK TABLE:
   every differing hunk -> {local-only improvement / source-only
   feature / conflict}. Zero hunks unclassified.
2. Merge INTO the repo source: keep every local-only improvement AND
   every source-only feature; resolve conflicts preferring the
   behavior-preserving side and justify each in the table. The merged
   file must render (via chezmoi template semantics if any) to content
   that keeps the live SSH bootstrap working: shims-first PATH in
   .zshenv MUST survive (it runs for non-interactive remote commands
   where .zprofile/.zshrc do not).
3. shdoc-compatible English comments per repo policy.
4. Verify: `zsh -n` on rendered results; `chezmoi diff` for the three
   targets after your edit must show ONLY hunks you explicitly justify
   as intended source-side wins (ideally empty except comment changes).

## Class C: deep.config.toml 権限属性

Rename home/dot_codex/modify_deep.config.toml ->
home/dot_codex/modify_private_deep.config.toml (git mv) so the computed
target is mode 600, matching the live file that carries Codex-owned
runtime state. Check the sibling profile configs
(express/review/security/standard) and apply the same attribute if they
are generated to targets that Codex also rewrites; justify each
decision. Update scripts/generate-agent-configs.py or lifecycle
references if any hardcode the old source filename (grep first).

## Class A prevention: doctor drift check

Add to the existing doctor flow (scripts/check-agent-runtime.py or the
make doctor entrypoint — follow the existing structure): a chezmoi
drift section that runs `chezmoi status`, reports each drifted target
with its class hint (' M' = un-applied source update, 'MM' = two-sided,
mode-only = permission divergence), and exits WARN (not fail) on
drift. No auto-apply — detection only.

## Gates

make format / validate-agent-assets / unit-test; shellcheck+shfmt on
touched shell; `chezmoi diff` evidence for the three zsh targets
before/after in the validation artifact.

## Allowed files

home/dot*zshenv, home/dot_zprofile, home/dot_zshrc,
home/dot_codex/modify*_deep.config.toml (+ siblings if justified),
scripts/check-agent-runtime.py or doctor entrypoint + Makefile hook,
tests/unit, artifact paths (T84 set). Reads of ~/.zshenv, ~/.zprofile,
~/.zshrc, ~/.codex/_.config.toml are allowed and required.

## Forbidden actions

git commit; git push; chezmoi apply; bats; deleting any live
functionality from either side; auto-apply in the doctor check;
touching ~/.z\* deployed files.

## Completion / RESULT contract

Five artifacts; memory add; effects=none; cost line.
Reply `AGMSG-RESULT v1 task_id=T84`. max_turns=25.
