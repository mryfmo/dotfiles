Found **two P1 security defects** in [PR #412](https://github.com/mryfmo/dotfiles/pull/412) at `325f520`.

- **P1 · High confidence · `scripts/validate-agent-assets.py:1845` — Unquoted glob expansion incorrectly clears the unresolved command context, allowing a prohibited dynamic assignment.** With Bash `nullglob`, an unmatched glob disappears:
  ```bash
  shopt -s nullglob
  NAME=ANTHROPIC_API_KEY
  env /__codex_audit_no_such_dir__/* "$NAME"=audit_dummy /usr/bin/printenv ANTHROPIC_API_KEY
  ```
  The validator accepts this; Bash prints `audit_dummy`. Glob expansion needs unresolved provenance until its effect on the command boundary is established.

- **P1 · High confidence · `scripts/validate-agent-assets.py:1856` — `builtin --` loses declaration context, allowing a dynamic authentication name to bypass validation.**
  ```bash
  NAME=ANTHROPIC_API_KEY
  builtin -- export "$NAME"=audit_dummy
  ```
  `builtin` preserves command-prefix context, but `--` clears it because `builtin` is absent from `AUTH_WRAPPERS`; the following `export` is consequently ignored. The validator accepts this, while Bash exports the dummy credential.

Both reproductions passed `validate_anthropic_auth_route()` without diagnostics for mocked tracked shell files **and JSON command strings**. Harmless Bash probes independently confirmed their runtime effects.

These findings invalidate the threat table’s scanner **`closed`** disposition and the applied-input row’s promise to refuse unresolved names and prefixes. The existing corpus’s 185 non-YAML cases matched expectations but missed both bypasses.

Other controls checked: discovery uses argument-array subprocess invocation; templates undergo string replacement; structured parsing introduces no executable deserialization; direct symlinks are skipped; diagnostic payload redaction remains present. No additional execution, path-traversal, or credential-disclosure finding was established. Workflow/dependency configuration is unchanged, and no executable was added. Task-copy binding, metadata checks, final-head evidence and merge/update/removal safeguards remain procedural controls requiring orchestrator verification.

📝 まとめ: 指定 head の読み取り専用監査を完了し、認証チェックを迂回する P1 を 2 件確認しました。修正・受け入れ判断は orchestrator に委ねます。

Not checked: live CI because GitHub connectivity failed; YAML execution because PyYAML was unavailable; the full filesystem-writing test suite. No files were changed. The demonstrated authentication-policy bypasses remain open.

Verdict: incorrect