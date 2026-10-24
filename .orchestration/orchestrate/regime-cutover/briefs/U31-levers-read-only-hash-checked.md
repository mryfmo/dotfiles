# U31 Levers from a read-only, hash-checked path; the OS gate becomes code — brief

GOAL
The pre-authorized levers (U16: `hcom-seat`, `hcom-dispatch`, `bus-history.sh`, `worktree-gc.sh`; U28 later) can no longer be rewritten by a sandboxed session before they run, and `hcom-seat` loads only allow-listed extension directories, so the Codex residual 4365593028 (re-raised by the audit seat, D-024-144) is closed and the managed settings can be applied on Linux and WSL2 hosts too. Until that lands, part 1 turns today's operator gate ("do not apply these settings on a Linux or WSL2 host") into a rendered rule, so a `make update` on the Linux host deploys U17 and U18 without deploying the lever allow rules.

SCOPE
One branch `feat/levers-read-only-path` from `origin/main`, two commits in this order. May write: `scripts/generate-agent-configs.py`, `home/.chezmoitemplates/claude-settings-managed.json` (regenerated), `home/dot_agents/agent-config.yaml` (the `claude:` block), `scripts/validate-agent-assets.py`, `scripts/update-agent-assets.sh` (one install step), `scripts/orchestrator/hcom-seat` (the `--ext` allow-list), `scripts/orchestrator/README.md`, `README.md` ("Claude Code sandbox"), the tests of those files, `home/dot_local/bin/common/` only if the install target is placed there. Nothing else.

CONTEXT
1. The residual (Codex security review 4365593028 on PR #483, kept by D-024-144): "a sandboxed Claude session that can edit the checkout can replace `scripts/orchestrator/hcom-seat` or create an OMP extension and pass it via `--ext`, then invoke this newly auto-approved prefix … On Linux/WSL2 … the matching allow rule can approve that retry silently; on macOS it reaches Herdr through the allowed socket … Install a hash-verified launcher in a read-only path and allowlist immutable extension paths." `scripts/orchestrator/README.md:173` records the same with the macOS argument (the herdr socket in `allowUnixSockets` already gives sandboxed commands that escape class) and the Linux gate.
2. Today the gate is procedural: `render_claude_settings` renders `permissions.allow` flat (the only OS variant is the sandbox block, generate-agent-configs.py:386-494), so a `make update` on a Linux host would deploy the five rules. U17 and U18 are Linux-motivated and need `make update` there.
3. Sandbox write set (this session's config): the checkout, `$TMPDIR`, the hcom store, the seat worktrees, the uv and mise caches. `~/.local/bin/common` and `~/.local/lib` are not writable from the sandbox, and a path outside the write set cannot be edited by a sandboxed command; the permission rule matches the command text, so the rule must name the read-only path, not the checkout path.
4. Allow rules anchor by text: `Bash(scripts/orchestrator/hcom-seat *)` matches that spelling only; a rule for the installed copy reads `Bash(~/.local/bin/common/hcom-seat *)` or the absolute form the docs give for home paths (`~/path`); check the permissions doc "How path patterns match" is about Read/Edit, while Bash rules are prefix matches on the command string; measure with a scratch settings file and `claude -p` is not possible without login, so measure through the rendered rule text plus the existing U16 tests, and state in the README that the coordinator invokes the installed path.
5. chezmoi deploys `home/dot_local/bin/common/executable_*` to `~/.local/bin/common/` with mode 0755; `make doctor`/`validate-agent-assets` can check that the installed copy's sha256 equals the checkout's at render time, and the lever itself can refuse to run when its own bytes differ from the manifest-pinned sha256 (self-check at start, like the asset pins).

ACCEPTANCE
Part 1 (first commit, mergeable alone):
1. `render_claude_settings` renders the five lever allow rules only in the darwin variant of the template (the linux variant keeps `Bash(agmsg-dispatch:*)` until U26 and nothing else); the validator asserts the linux variant has no lever rule while the residual stands; tests for both variants; README row 173 says the gate is now rendered.
Part 2 (second commit):
2. The four levers are deployed by chezmoi as `~/.local/bin/common/<lever>` (same bytes as the checkout, `executable_` source files or an installer step; choose the one the repo already uses for `hcom-reply` and cite it), each with a start-up self-check against a sha256 pinned in the manifest and refreshed by the generator, refusing with exit 2 on mismatch.
3. `hcom-seat --ext <dir>` accepts only directories from a manifest allow-list (the bridge and the SIWC extension paths); any other path is refused before launch; tests.
4. The allow rules name the installed path on both OS variants; the checkout-path rules are removed; the validator refuses a lever rule that names a path inside the checkout; the README section and the manifest comments updated; the coordinator's SKILL or README sentence "run levers from the installed path" added where U16 wrote "from the checkout root".
5. `make unit-test`, `make validate-agent-assets`, `make render-check` green; CI green; PR body with `Program-Unit: regime-cutover/U31`, a threat table (the rewrite row now `closed:` by the self-check test, the `--ext` row `closed:` by the allow-list test, the Linux retry row `closed:` by the rendered-rule test), the footer; audit by the audit seat.

TIMEBOX
3 hours.

FORBIDDEN
No change to the omp policies; no new allow rule beyond the five; no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (line 20).
