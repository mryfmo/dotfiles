# T66: permgate × Pi — decision protocol + tool_call gate extension (π2)

task_id: T66
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 2, incl. the PR #132 review-hardened decision protocol)
depends: T65 (accepted)

[memory: decision — permgate's pi provider path emits a machine-readable one-line JSON decision (allow|deny|ask, exit 0) and signals internal failure via nonzero exit; the Pi tool_call extension maps ask to interactive confirm or non-interactive deny, and treats nonzero/timeout/malformed output as fail-closed deny.]

## Goal

Bring fail-closed permission gating to Pi (which ships none) via the
official tool_call blocking surface, with an unambiguous gate protocol.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_permgate (pi provider argument +
  decision-protocol output for the pi path ONLY; claude/codex hook output
  paths byte-identical — pin with a test)
- home/dot_agents/permgate-policy.yaml (pi section referencing the same
  deterministic deny/allow layers; LLM stays shadow/disabled)
- home/dot_pi/agent/extensions/permgate.ts (NEW)
- scripts/validate-agent-assets.py (extend the pi assets category with a
  content-hash check for permgate.ts — hash constant + regeneration note)
- tests/unit/ (matching modules)
- Your artifact paths (T66 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes (no vitest,
no npm installs — extension tests run via node from tests/unit); running
the real pi binary; changing claude/codex permgate behavior; enabling any
LLM classifier.

## Decision protocol (fixed by the plan; do not reinterpret)

`permgate pi <normalized-action-json-on-stdin-or-argv (choose and document
one, matching how the extension will call it)>`:

- stdout: exactly one line `{"decision":"allow"}` / `{"decision":"deny"}`
  / `{"decision":"ask"}`; exit 0.
- Internal failure (config load, parse, decision, logging): NONZERO exit;
  stdout contents unspecified (extension must not parse it on nonzero).
- Decision mapping reuses the existing deterministic layers (deny patterns
  -> deny; allow patterns -> allow; else ask). Shadow-LLM recording may
  still occur but never changes the decision.

## Extension spec (fixed)

- File: home/dot_pi/agent/extensions/permgate.ts, exporting the factory
  form the pinned v0.84.2 loader expects (verify against the pinned
  extensions types source; cite lines).
- On `tool_call` for tools bash/write/edit: normalize {tool, command or
  path}, invoke permgate pi with 7s timeout.
- allow -> proceed; deny -> block with a one-line "blocked by policy"
  error result; ask -> if an interactive UI context exists use
  ctx.ui.confirm, else deny; nonzero exit / timeout / malformed JSON ->
  deny. read/grep/find/ls pass through untouched.
- No network, no state files, no imports beyond pi-provided virtual
  modules and node builtins.

## Tests (pin each; node-run from tests/unit, stub child_process)

(a) four decisions incl. ask-interactive and ask-noninteractive;
(b) nonzero exit -> deny; timeout -> deny; malformed JSON -> deny;
(c) pass-through tools never invoke permgate;
(d) permgate pi CLI: each decision's stdout/exit; internal-failure path
exits nonzero; claude/codex paths byte-identical outputs on a fixture
(golden test);
(e) validate hash check: matching hash passes, tampered extension fails.

Type/syntax gate: `tsc --noEmit` if available without new deps, else
document and use node --check on the transpiled-esque check the repo can
support; state the choice.

## Validation (record in validation artifact)

1. make format / unit-test / validate-agent-assets green (totals + new).
2. Full git diff of executable_permgate (protocol addition) pasted.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T66 set); memory add with the decision fact; effects=none.
Live gate verification is T72 E2E-π2.
Reply `AGMSG-RESULT v1 task_id=T66 status=ready_for_review`. max_turns=25.
