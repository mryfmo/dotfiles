# dot-ubuntu-parity-T13-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot
evidence:
  - 92a3ff6: both unguarded expansions fixed with ${arr[@]+"${arr[@]}"} idiom + rationale comment;
    full 3-array audit correct (claude_args already branch-guarded, endorsed untouched)
  - independent re-run: format clean / unit-test green(下記)
  - macOS bash 3.2 再現は CI に委ねる旨明記 — macos-14 の green で最終確認する
cost: n/a
