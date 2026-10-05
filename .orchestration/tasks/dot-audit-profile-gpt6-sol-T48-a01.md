# AGMSG-TASK dot-audit-profile-gpt6-sol-T48-a01

## Objective

Operator decision 2026-10-01: the auditor's default model is **`gpt-6-sol` at
`xhigh`** (was `gpt-6-astra` / `high`). The operator first asked for
`gpt-6.1-sol`; the orchestrator probed it under the audit profile and the
ChatGPT-login account rejected it (`400 The 'gpt-6.1-sol' model is not
supported when using Codex with a ChatGPT account`), while
`codex exec --profile audit -m gpt-6-sol -c model_reasoning_effort=xhigh`
answered normally. Model IDs live only in `model_profiles`
(`home/dot_config/claude/rules/model-selection.md`); everything else renders
from there or quotes it.

Deliver, in one commit on `fix/audit-profile-gpt6-sol` from `origin/main`:

1. `home/dot_agents/agent-config.yaml` `model_profiles.audit.codex`:
   `model: gpt-6-sol`, `model_reasoning_effort: xhigh`; keep
   `sandbox_mode: read-only` and `notify`. Update the comment above it (it says
   "Auditor tier (監査役)") only if it names the model. Do not touch the
   `security` or `adh` profiles.
2. Regenerate: `uv run --with pyyaml scripts/generate-agent-configs.py`
   (`make render-check` green). Commit the regenerated
   `home/dot_codex/modify_private_audit.config.toml` (and any other file the
   generator rewrites for this change; list them in the report).
3. `scripts/validate-agent-assets.py:752-760`: the operator pin for the audit
   profile becomes `gpt-6-sol` / `xhigh` / `read-only`, comment "Operator pin
   (2026-10-01): the auditor is codex gpt-6-sol xhigh, read-only
   (gpt-6.1-sol is rejected under ChatGPT login)". Leave the security pin
   (`gpt-6-astra` / `high`) as is.
4. Docs that quote the auditor model: `README.md:265` ("The auditor uses the
   `audit` profile (Codex `gpt-6-astra`, …)") and
   `home/dot_config/claude/rules/model-selection.md:3` ("auditor=`audit`
   (Codex gpt-6-astra high, read-only sandbox)") → `gpt-6-sol xhigh`. Grep
   `gpt-6-astra` outside `.orchestration/` and `reviews/` (READ-ONLY baseline,
   never edit) and update every remaining auditor-specific mention; leave
   mentions that belong to the `security` or `adh` profiles
   (`scripts/check-agent-runtime.py`, generator/validator defaults for `adh`).
5. Tests: update any test pinning the audit profile values
   (`tests/unit/test_validate_agent_assets.py`,
   `tests/unit/test_generate_agent_configs.py` — grep `audit`); add none unless
   a pin test is missing for the new values.
6. Validation (verbatim output, exit codes captured directly):
   `make render-check`, `make unit-test`, `make validate-agent-assets`,
   `git grep -n gpt-6-astra -- . ':!.orchestration' ':!reviews'` (only
   security/adh mentions may remain; paste them), `gh pr view <n> --json
url,headRefOid,mergeStateStatus`, the CompactionDB command below.
7. PR (English) from `fix/audit-profile-gpt6-sol`; push without `-u`.

Out of scope: launching the auditor (the orchestrator verifies the live lane
with `herdr-agents --audit <sha>` after `chezmoi apply`), the `security`
profile, `~/.agents/model-profiles.env` (`MODEL_PROFILE_AUDIT_CODEX_ARGS` stays
`--profile audit`), herdr-agents.

[memory:decision] T48: the auditor (`audit` profile) runs Codex `gpt-6-sol`
at `xhigh`, read-only; `gpt-6.1-sol` is rejected under the ChatGPT-login
account (operator decision 2026-10-01, probe recorded in the T48 task file).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`;
  start only after your T43 r5 RESULT is sent. `git fetch`, then branch
  `fix/audit-profile-gpt6-sol` from `origin/main`. Leave
  `feat/orchestration-rules-T43` and `fix/sandbox-unix-sockets` untouched.
- Sandbox deny-mount stubs (nobody-owned zero-byte char devices) are not dirt;
  explicit-path `git add` only. Config-writing git outside the sandbox; push
  without `-u`; never remove `.git/*.lock`. Ignore the Understand-Anything
  hook (record "hook fired; not acted on").

## Allowed files

- `home/dot_agents/agent-config.yaml` (audit profile block only)
- `home/dot_codex/modify_private_audit.config.toml` and any other generator
  output changed by this manifest edit
- `scripts/validate-agent-assets.py` (audit pin only)
- `README.md` (auditor sentence only), `home/dot_config/claude/rules/model-selection.md` (auditor clause only)
- `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_generate_agent_configs.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-audit-profile-gpt6-sol-T48-a01.md` (main checkout)
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Any other profile or model value; `reviews/**`; `model-profiles.env`;
  sandbox settings; pane reads; merge; force-push; `--delete-branch`;
  `.orchestration/acceptance/**`; local `bats`; running the auditor.
- Escalating outside the sandbox/allowlist for approval: fail, PONG blocked
  with the exact command and boundary.

## Validation commands

- `make render-check`
- `make unit-test`
- `make validate-agent-assets`
- `git grep -n gpt-6-astra -- . ':!.orchestration' ':!reviews'`
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=25. done_signal=AGMSG-RESULT v1.

## Orchestrator amendment (2026-10-01 00:4xZ, operator override; supersedes the model value above)

Operator decision: the auditor default is **`gpt-6.1-sol` / `xhigh`**, not
`gpt-6-sol`. Apply every deliverable above with `gpt-6.1-sol` in place of
`gpt-6-sol`:

- `model_profiles.audit.codex.model: gpt-6.1-sol`,
  `model_reasoning_effort: xhigh`, `sandbox_mode: read-only` unchanged.
- Validator pin: `gpt-6.1-sol` / `xhigh` / `read-only`, comment "Operator pin
  (2026-10-01): the auditor is codex gpt-6.1-sol xhigh, read-only; this model
  needs API-key auth (rejected under ChatGPT login: 400 'not supported when
  using Codex with a ChatGPT account', probe 2026-10-01)".
- README auditor sentence and `model-selection.md` auditor clause:
  `gpt-6.1-sol xhigh`, plus one clause that the audit lane requires Codex
  API-key authentication (the ChatGPT-login account rejects the model).
- No fallback model anywhere (no-fallback principle of the manifest).
- `[memory:decision]` text: replace `gpt-6-sol` with `gpt-6.1-sol` and add
  "requires API-key auth; ChatGPT login rejects it".

Known consequence, recorded by the orchestrator: on this machine
`~/.codex/auth.json` is `auth_mode: chatgpt` with no API key, so
`herdr-agents --audit` will fail at the model call until the operator
configures API-key auth for Codex. That is the operator's lane; do not add a
fallback or a conditional.
