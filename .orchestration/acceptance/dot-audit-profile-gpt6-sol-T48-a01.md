# Acceptance: dot-audit-profile-gpt6-sol-T48-a01

Operator request 2026-10-01: the auditor default becomes `gpt-6.1-sol` /
`xhigh`. Orchestrator probe before tasking (headless, audit profile, one
prompt): `gpt-6.1-sol` → `400 The 'gpt-6.1-sol' model is not supported when
using Codex with a ChatGPT account`; `gpt-6-sol` / `xhigh` → answered. The
operator first chose `gpt-6-sol` (AskUserQuestion), then overrode to
`gpt-6.1-sol` / `xhigh` with the rejection known. `~/.codex/auth.json` is
`auth_mode: chatgpt`, no API key.

Dispatched 2026-10-01T00:22:54Z (msg 556, task_rev 7e72b322…); override PING
00:35:42Z (msg 557, task_rev 38a86dd0…). RESULT 00:54:44Z (msg 558): PR #218,
head 8956c3d (81d720f `gpt-6-sol` + 8956c3d override; no force-push, as
forbidden), CI all pass, CLEAN.

## Adversarial review (from git objects and origin refs)

- Diff: 7 files, +19/−13, all within allowed files. Manifest
  `model_profiles.audit.codex`: `gpt-6.1-sol` / `xhigh` / `read-only` / notify
  kept; `security` and `adh` untouched (verified by `git grep gpt-6-astra` at
  the head: only security/adh lines remain, plus the rejected value in the pin
  test).
- Generated `modify_private_audit.config.toml` MANAGED block carries the new
  values; the worker's `--check` says up to date (the auditor confirmed
  byte-for-byte generation).
- Validator pin → `gpt-6.1-sol` / `xhigh` / `read-only` with the API-key note;
  pin test now also rejects `gpt-6-astra`, `gpt-6-sol`, `high`.
- README auditor sentence and `model-selection.md` auditor clause updated with
  the API-key prerequisite. No fallback model anywhere.
- Deviation accepted: `make render-check` does not exist on main (it arrives
  with T43 #214); the worker ran the wrapped command instead and pasted the
  failing `make` too.
- 612 unit tests OK, validate ok, exits captured directly.
- CompactionDB: the worker wrote `ae7ca177…` (`gpt-6-sol`, pre-override) and
  `90843027…` (`gpt-6.1-sol`, current) in the main DB. `ae7ca177…` is retracted
  at acceptance (see below).

## Codex audits (gpt-6-astra high read-only — the profile still active until `chezmoi apply`)

- 81d720f (`…-audit-81d720f.md`): **Verdict: correct**.
- 8956c3d (`…-audit-8956c3d.md`): **Verdict: correct**; the API-key
  prerequisite and the ChatGPT-login failure are disclosed.

## PR #218 feedback sweep (head 8956c3d, 16 items)

Codex GitHub P1 at `agent-config.yaml:61` ("pin to a supported model or
provision API-key auth"): the facts are correct and already documented in
this changeset; the choice is a deliberate operator decision taken after the
probe → `not-applicable` with that reason. Remaining 15 items (runner notices,
brew tap warning, CodeRabbit skip/status, Codex container comment) →
`not-applicable`.

## Known consequence (operator lane)

After `chezmoi apply`, `codex --profile audit` and `herdr-agents --audit <sha>`
request `gpt-6.1-sol` and **fail on this machine until Codex has API-key
authentication**. Until then the acceptance-time audits in this regime cannot
run; the orchestrator records that state per task rather than falling back.

cost: ~25k context tokens (worker counter; no per-task figure)

**Decision: ACCEPTED.** Merge PR #218 (squash, no `--delete-branch`) after the
integration gate; live confirmation (`model: gpt-6.1-sol`, `reasoning effort:
xhigh` in the audit header) is recorded once the operator provisions API-key
auth and applies the dotfiles.

## Post-merge audit of the squash commit 0a34a68 (2026-10-01 01:57Z, run by mistake in a T43 audit loop that enumerated main's merged commits)

`…-audit-0a34a68.md`: **Verdict: incorrect**, one P1 — the pin breaks the
audit lane on the ChatGPT-login deployment until API-key auth is provisioned.
Same fact as the Codex GitHub P1 on #218; disposition unchanged:
**not-applicable (operator decision with the prerequisite documented; API-key
provisioning is the operator lane)**. Recorded here so the finding is not
left undispositioned.
