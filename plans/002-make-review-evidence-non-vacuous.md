# Plan 002: Reject empty agent-review evidence

> **Executor instructions**: Implement only the operational guard described
> here. Do not turn a local self-reported receipt into an authentication system.
> Add rejection tests first, make the smallest parser change, and preserve the
> explicit human Crit path.
>
> **Drift check**: `git diff --stat e7c2808..HEAD -- scripts/require-crit-review.py tests/unit/test_require_crit_review.py AGENTS.md README.md`
> Changed review marker semantics are a STOP condition requiring plan refresh.

## Status

- **Priority**: P0
- **Effort**: S
- **Risk**: LOW — agent evidence becomes stricter; human review remains supported
- **Depends on**: none
- **Category**: governance, correctness, tests
- **Planned at**: commit `e7c2808`, revised 2026-07-11 after Crit 0.18.0 probing

## Plan quality self-audit

- [x] Scope is limited to the demonstrated `null`/empty-evidence bug.
- [x] The plan does not claim cryptographic reviewer or target authenticity.
- [x] Required Steps, Commands, Scope, tests, STOP, maintenance, and safety sections exist.
- [x] Positive and adversarial evidence shapes are explicit.
- [x] Human and agent marker paths are explicitly separated.

## Why this matters

`AGENT_REVIEWED=1` currently accepts a repo-local JSON file containing only
`null`. This lets an agent accidentally satisfy the process guard without saving
any review result. Crit 0.18.0 returns `null` when unresolved comments are empty,
but `crit comments --all --json <review.json>` emits a non-empty resolved-list
shape when resolved records exist.

This local script is an operational mistake-prevention gate, not a security or
identity boundary: a process that can edit the worktree can also fabricate local
evidence. Repository protection against malicious/self-approved changes belongs
in GitHub branch protection, required checks, and required reviewers. The exact
goal here is smaller: agent evidence must be non-empty and structurally match the
resolved-list shape emitted by Crit. The guard does not prove its provenance.

## Current state

- `scripts/require-crit-review.py:252-260` accepts parsed evidence when the
  unresolved-comment result is empty.
- `scripts/require-crit-review.py:265-268` converts JSON `null` to an empty list.
- `tests/unit/test_require_crit_review.py:188-200` requires `null` to satisfy an
  agent review.
- `tests/unit/test_require_crit_review.py:135-157` covers trusted human-review
  receipt paths; these must remain available.
- `README.md:255-263` and guard output instruct agents to save
  `crit comments --json`, which yields `null` after all comments are resolved.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Focused tests | `uv run python -m unittest tests.unit.test_require_crit_review -v` | all pass |
| Full tests | `make unit-test` | all pass |
| Compile | `uv run python -m py_compile scripts/require-crit-review.py` | exit 0 |
| Review guard | `make require-crit-review` | correct result for current diff |

## Scope

**In scope**:

- `scripts/require-crit-review.py`
- `tests/unit/test_require_crit_review.py`
- `AGENTS.md`, `README.md`, `home/dot_config/codex/AGENTS.md`, and
  `home/dot_config/claude/rules/crit-review.md` only to change the agent evidence command from
  `crit comments --json` to `crit comments --all --json <review.json>` and state
  the local guard's non-authentication boundary

**Out of scope**:

- Cryptographic reviewer identity, commit/diff attestation, or branch protection.
- Raw Crit `review.json` copies, which can contain source anchors and comment bodies.
- A change-set digest or custom evidence generator.
- Changing which file paths trigger review.
- Removing the explicit human `CRIT_REVIEWED=1` path.

## Required acceptance contract

For `AGENT_REVIEWED=1` with reviewer `codex`, `claude`, or `claude-code`:

1. `review_surface` is `crit-data` and `review_source` is repo-local JSON.
2. JSON root is a non-empty list matching `crit comments --all --json` output.
3. Every list entry is an object with non-empty string `id`, `body`, and
   `scope`; `resolved` is exactly `true`. The Crit-provided `author` field is
   optional and is not used as an authenticity signal.
4. At least one entry has `scope: review` or `scope: line`/`file` plus a path.
5. Any unresolved, malformed, empty, `null`, dict-root, or unknown evidence fails.
6. `review_outcome` is `approved` or `addressed`.

For `CRIT_REVIEWED=1` with a human reviewer, preserve the existing trusted human
receipt path. `AGENT_REVIEWED=1` with `reviewer: user` must be rejected so agents
cannot select the less strict human path.

## Steps

### A001 — Replace the permissive test first

- [x] Rename the current `null` success test to assert rejection.
- [x] Add rejection cases for empty list, dict root, malformed entries, missing
      fields, empty fields, unresolved entries, and invalid review outcome.
- [x] Add rejection for `AGENT_REVIEWED=1` plus `reviewer: user`.

**Verify Adversarial**: focused tests fail against the pre-change parser.

### A002 — Add the smallest valid fixture

- [x] Add a non-empty list containing one resolved review-scope comment with
      id, body, scope, and `resolved: true`; omit optional author to prove it
      is not required.
- [x] Add a resolved line-comment fixture with a non-empty path.
- [x] Assert both satisfy only the agent marker path.

**Verify Positive**: removing or emptying any required field makes the fixture fail.

### A003 — Tighten agent evidence validation

- [x] Reject `None`, all dict roots, and empty lists in `crit_data_errors`.
- [x] Validate every list entry and require all resolved.
- [x] Validate `review_outcome` for agent reviewers.
- [x] Reject agent marker plus non-agent reviewer.
- [x] Preserve repo-local path and valid-JSON checks.
- [x] Reuse Python stdlib and existing helpers; add no new abstraction layer.

**Verify**: each invalid fixture produces a deterministic actionable message.

### A004 — Preserve the human review path

- [x] Run existing `CRIT_REVIEWED=1` human receipt tests unchanged.
- [x] Confirm explicit `CRIT_REVIEW=off` behavior is unchanged.
- [x] Confirm agent reviewers still require `AGENT_REVIEWED=1`.

### A005 — Correct operator instructions

- [x] Update guard output, AGENTS.md, and README.md to use
      `crit status --json` to locate the review file, then
      `crit comments --all --json <review.json>` for evidence.
- [x] Update the managed Codex and Claude instructions emitted by chezmoi to
      the same resolved-comment command so deployed agents can satisfy the gate.
- [x] State that the evidence must contain at least one resolved record. When a
      review has no findings, add one review-scope approval record and resolve it.
- [x] State that this local guard is process evidence, not an authentication boundary.

### A006 — Run acceptance gates

- [x] Run compile, focused tests, and `make unit-test`.
- [x] In an isolated test repo, prove `null` fails and the minimal resolved list passes.
- [x] Mutate the resolved fixture to unresolved and prove it fails.

## Test plan

- Reject: null, empty list, dict, malformed member, missing/empty required field,
  unresolved member, invalid outcome, agent marker with user reviewer, external path.
- Accept: resolved review-scope record and resolved path-bound line record.
- Preserve: human Crit receipt, explicit disable, missing evidence, native marker rules.

## Done criteria

- [x] Agent review cannot be satisfied by `null`, empty, or malformed JSON.
- [x] Agent review requires at least one fully resolved Crit record.
- [x] Agent marker cannot select the trusted human reviewer path.
- [x] Human browser-review and explicit-disable paths remain covered and passing.
- [x] Documentation and guard output use the actual Crit 0.18.0 command sequence.
- [x] Focused, full, and compile checks exit 0.
- [x] No dependency or target-attestation subsystem is added.
- [x] `plans/README.md` is updated only after independent review and CI.

## STOP conditions

- Crit 0.18.0 cannot emit a non-empty resolved list after an explicit review record.
- Tightening agent evidence necessarily breaks the documented human marker path.
- Existing agent workflow cannot add/resolve a review-scope record headlessly.
- The change requires raw review files containing source anchors to be committed.
- A proposed implementation claims reviewer authenticity from self-authored local files.

## Maintenance notes

- Treat new Crit root shapes as invalid until explicitly tested.
- Keep agent and trusted-human marker tests separate.
- Put authenticity enforcement in GitHub settings, not this local Python guard.

## 安全回帰

- Empty or malformed agent evidence fails closed.
- Unresolved comments fail closed.
- Human review remains usable.
- Explicit opt-out remains explicit.
- Evidence stays repo-local and ignored.
- Documentation does not promise security properties the guard cannot provide.
