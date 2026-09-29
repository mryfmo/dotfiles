# T38 learning triage

## Candidates

1. **Validate every ref argument before use.** A guard that takes a ref
   argument (`--base`) must resolve it with `git rev-parse --verify --quiet
   --end-of-options <ref>^{commit}` before any other step. git failures in
   diff, show or merge-base were each treated as "nothing to check", so one
   unresolvable ref turned every check into a pass. This is the fail-open
   pattern to look for in any guard that ignores git return codes.
2. **Sweep only when checks are terminal.** Run the PR feedback sweep only
   after every check is terminal (`gh pr checks --watch`). Otherwise
   `in_progress`/`queued` items need 20-character reasons and a new sweep at
   acceptance anyway.
3. **A missing bot review leaves notices behind.** With auto review off, a
   PR still gets a CodeRabbit "Review skipped" status and comment, plus a
   chatgpt-codex-connector onboarding comment when no Codex account is
   connected. The collector picks all of these up as items. The optional-bot
   gate needs them dispositioned, not reviewed.
4. **Tap-trust warning is a follow-up.** The macos-14 runner pre-taps
   aws/tap, azure/bicep and hashicorp/tap. test.yaml already trusts two of
   them, but the macos.yaml public-bootstrap job does not, so every PR sweep
   carries a Homebrew tap-trust warning. Trusting them in macos.yaml would
   remove a recurring disposition.

## Promotion

None. These are candidates only.
