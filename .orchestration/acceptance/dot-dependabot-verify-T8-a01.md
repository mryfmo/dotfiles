# Acceptance: dot-dependabot-verify-T8-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator)
cost: n/a

- The task premise (three PermissionError failures) was wrong and the worker refuted it with job-API evidence: the PermissionError is the expected network-denial oracle of the sandboxed statusline smoke step; the real failure was the unpinned `shfmt` on macOS, fixed on main by bf2110f (#158). setup-uv v8–v10 breaking changes mapped against our usage (SHA-pinned, cache disabled, no version files): none apply. #155 verdict: safe as-is.
- #125 changes the installed Nix from 2.34.8 to 2.35.2; no local nix, and the nix CI job is path-gated so it did not run. Verdict: static compatibility only; residual runtime risk confined to the nix job, which executes on the next genuine flake change.
- No repository changes; worker stayed within read-only scope.
