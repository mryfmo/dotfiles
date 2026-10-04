# Learning triage: dotfiles-T63-codex-execpolicy-forbidden-a01

Candidates only; nothing is promoted.

1. **`codex execpolicy check --rules <file> <cmd…>` is a deterministic, model-free test** of a rules file. It also validates the rules' `match`/`not_match` examples at load. Use it in place of model-driven E2E runs for policy acceptance.
2. **A trusted scratch project layer did not load rules for `codex exec`.** A scratch `<repo>/.codex/rules` trusted only through `-c projects.<path>.trust_level` did not take effect in two attempts. An end-to-end check of user-layer rules needs the real `~/.codex/rules` after `make update`, which is an operator step.
3. **Forbidden is a refusal under every approval policy.** `Decision::Forbidden` maps to `ExecApprovalRequirement::Forbidden` without consulting `approval_policy`, so the forbidden set stays effective under `--ask-for-approval never`.
4. **Profile args under zsh:** `$MODEL_PROFILE_EXPRESS_CODEX_ARGS` needs `${=VAR}` in zsh to split into `--profile express`.
