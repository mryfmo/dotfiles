---
reviewed_at: 2026-10-10T08:58:00Z
reviewer: claude-review-dot-a002
profile: review
session: 76641dce-e0d5-4654-b475-8f2ebdbf8cc9
design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md@34c5a1bfae28bf092439b72e4f1e37035c6a2cf48787e4cdf54b0b608ee4ea68
task: dotfiles-T124-design-review-a01
round: 2
previous: .orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review.md
---

# Design review round 2: T124 design v2

Scope as requested: each v1 correction checked as applied, INV-9's source checked against `executable_permgate`, the INV-3 bootstrap exemption checked for narrowness, and v2 read for anything that reopens a v1 finding. Same worktree and sources as round 1, plus `executable_permgate:63-68,78-89,149-168,202-204`, the storage facade's history rows (`storage_history` emits `id`, `from`, `to`, `body`, `at` in ISO UTC) and SKILL step 10's gate location.

## Invariants

INV-1: accepted. Applied as written: gate as the mandatory point at the task id the gate already derives (`require-crit-review.py:786`), worker-side run as the early signal, dispatch pre-check dropped, `kind` covers tasks without a PR.

INV-2: accepted. Applied as written (one module, ratchet up, prose out). One consequence to decide, not a reopen: the shared list contains the whole `scripts/` prefix and the tokens `hook`, `crit`, `plugin` (`require-crit-review.py:53-88`), so nearly every regime task becomes `security: true` and needs a threat model and a design review. If that is intended, say so; otherwise define two tiers in the same module (review tier = the existing lists; design tier = installers, supply chain, the four gate scripts, permission and sandbox policy, hooks). Implementation note: `scripts/lib/` holds only shell today; the module imports as a namespace package from a script's `sys.path[0]`, but the unit tests that load the gate by path need the same path on `sys.path`.

INV-3: rejected: the hash scheme does not work for the waves it must gate, and one sentence is impossible. (1) Three hashes are named: the receipt's `design:` (sections), `design_sha256=` in the TASK body (whole file), and "recomputed by the gate from the file at dispatch", which the gate cannot do; it only sees the current file. Right: one hash, over a canonical serialization of the front-matter keys `invariants`, `threat_model`, `trust_anchors` (JSON, sorted keys), recomputed by the gate from the current main-checkout task file and compared with the receipt; a legitimate change to those keys needs a new review RESULT, which is T1's point. Drop `design_sha256=` from the TASK body or define it as that same value. (2) The receipt for every T124 wave hashes this design document, but the gate recomputes from `.orchestration/tasks/<wave task>.md`; they never match, so waves 2b, 3a and 3b cannot pass INV-3 as written. Right: the task front matter carries `design_review: {receipt: <path>, design: <design task file>}`; the gate hashes the named design file's keys and requires the wave task's `invariants` ids to be a subset of the design's. (3) This design document has no front matter, so round 1's and this receipt can only hash the whole file, as the task's output format says; the first canonical hash exists once wave 1's task file is `format: 2`. (4) Narrowness: waves 1 and 2a are exactly the PRs that merge before INV-3 exists in the merged gate, so the set is the narrowest, and no prose exemption is needed if the gate runs from `main` (see Trust anchors below); the acceptance records citing both receipts is provenance, fine to keep.

INV-4: accepted. Applied as written; the disposition lock on `violated` is there.

INV-5: rejected: one check points the wrong way and one coverage limit is unstated. (1) `revise count ≥ audits − 1` is satisfied by omitting audit files (fewer audits, inequality still holds); it detects the direction nobody games. Right: every `AGMSG-ACCEPTANCE status=revise` that follows an audit carries `audit=<sha7>`, the gate and the stop gate require `<task>-audit-<sha7>.md.last.md` in the main checkout for each named sha and count (a) over those; a named sha without its file is a refusal. (2) `scripts/agent-stop-gate.sh` is a Claude Code Stop hook (`:3`), so the loop-time rule exists only when `orchestrator_kind` is claude; under `codex-orchestrate` only the merge backstop runs. State it. Everything else is applied as written: history counts (a'), main-checkout files, (c) dropped, (d) pending the `pr-feedback.py` field, the superseding-task overlap check, the boundary-check catches.

INV-6: accepted. Applied as written (diff count, distinct constant, PR within exactly one wave, validator warns).

INV-7: rejected: narrow. The grammar, the lock, the acceptance-record input and the circularity fix are applied as written. Missing: scope. "A missing `Orchestration findings:` line makes the audit `blocked`" applies to every audit the moment wave 2a merges, while the prompt that asks for the line arrives in wave 3b and the SKILL's headless bullet still says `[P0-P3] confidence dimension file:line rationale` (`SKILL.md:77`). Right: the parse is mandatory only for `format: 2` tasks (the same grandfather as INV-8), wave 3b lands before 2a, and 3b also rewrites `SKILL.md:77`.

INV-8: accepted. Add two gaming tests to the list: a revise ACCEPTANCE naming an audit sha whose file is absent (INV-5), and a permgate count above the sandbox record's (INV-9).

INV-9: rejected: the source is real but does not carry what the rule reads. Checked: `append_log` writes `$XDG_STATE_HOME/permgate/decisions.jsonl` (`executable_permgate:63-68,138-147`), one record per PermissionRequest with `ts` (ISO UTC), `agent`, `tool`, `input_hash`, `input_summary`, `layer`, `decision`, `latency_ms` (`:157-168`); history rows carry `at` in the same form, so the TASK-to-RESULT window is computable. Not there: any seat attribution. `agent` is `sys.argv[1]` (`:204`), the runtime kind the hook command passes, and no `session_id` or `cwd` is kept, so in a window where the orchestrator and two Claude workers all raise prompts, "for the worker identity" cannot be evaluated. Right: permgate records `session_id` and `cwd` from the hook input (both are in Claude Code's hook payload); the gate maps the worker identity to its session through the seat lock `run/actas.<team>__<name>.session`, which `check-regime-boundary` already reads, or through `cwd` equal to the worker's worktree. Two more corrections: (1) count semantics: a record exists for every permission prompt, including refused ones and non-sandbox prompts, so compare `tool == Bash` records with the sandbox record's count of permission-gated commands (T119's round-4 record counted exactly that set), not "out-of-sandbox"; (2) coverage: the hook never fires for a Codex worker seat (SKILL line 55), which also cannot escalate, so INV-9 covers Claude workers and the design should say so. Consequences for waves: a permgate change is operator-routed and gets a Codex `security`-profile review per the model-selection rule, so it is a new wave (0 or 2c) before 2b, and the auditor needs the window's records as a gate-produced extract (`<task>-permgate.jsonl`) in its input list, since its read-only sandbox does not read `~/.local/state`.

## Trust anchors: one claim reopens a v1 finding

"never changed in the same PR as a task they govern" is false as the procedure stands. SKILL step 10 has the orchestrator move the review worktree to the audited head and run the audit and the gate there, so `make require-crit-review` in waves 2a and 2b executes the PR's own `require-crit-review.py`. `pr_base_errors` pins only the collector to the base SHA (`require-crit-review.py:475-476`). Right: the acceptance procedure runs `main`'s script against the review tree, `<main>/scripts/require-crit-review.py --base origin/main` with the review worktree as cwd, and the gate refuses when `git -C <main> rev-parse HEAD` equals the audited head, the same rule `herdr-agents` already applies to the masker (`executable_herdr-agents:1988`). This also makes the INV-3 bootstrap automatic: waves 1 and 2a are checked by the pre-change gate by construction.

## Nothing else reopens a v1 finding

The standing fact is stated; every count moved to history, GitHub or the main checkout; the waiver is described as visible, not prevented; the grandfather exists; waves are split as asked; wave 4 is dropped; INV-5(b)'s threshold is confirmed with T119 in view.

## Residual, unchanged from round 1

The worker-conduct gap closes only for Claude workers and only after the permgate change; the design now says so for the first half and should say so for the second.

Design verdict: revise
