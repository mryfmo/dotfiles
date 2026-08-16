# T67: Pi model-access verification — headless harness + operator procedure (π1 前段)

task_id: T67
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 3)
depends: T65 (accepted); T66 (accepted — extension will be loaded in any real run)

[memory: decision — Pi model access is verified in two lanes: a headless API-key/local-provider RPC round-trip that gates T68, and an operator-run subscription-auth checklist (Fable-family availability, thinking levels, gpt-5.6 availability, terms comfort) that decides the model_profiles pi values and the π4 comparison setup.]

## Goal

Produce (1) a runnable headless verification script and (2) an operator
procedure + result form. NO real Pi run happens in this task unless the
headless lane can run fully offline-safe (see below) — the first real
execution is performed BY THE ORCHESTRATOR using the deliverables.

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_pi-model-access-check (NEW, bash,
  shdoc): runs the headless lane against an ALREADY-INSTALLED pi binary
  (checks `command -v pi` and exact version 0.84.2; refuses otherwise).
  Steps: (a) `pi --version`; (b) `pi -p 'Reply with exactly OK'
--mode json` against a provider selected by env
  (PI_CHECK_PROVIDER/PI_CHECK_MODEL; no key material handled by the
  script — it only checks the documented env var for the chosen provider
  is set and otherwise SKIPS with a clear message); (c) an RPC one-shot:
  spawn `pi --mode rpc`, send a `prompt`, await the agent-end event,
  print the envelope KINDS observed (this doubles as the plan's
  RPC-envelope confirmation step for T68); (d) verify the permgate
  extension loaded (grep the observed events/logs for the extension name
  or use `get_commands` if it lists extension commands — investigate the
  pinned source read-only and choose a reliable signal; cite it).
  Every step prints PASS/SKIP/FAIL lines; exit nonzero only on FAIL.
- .orchestration/validation/T67-model-access.md (NEW: operator procedure
  - result form): numbered steps for `/login` Anthropic and OpenAI
    subscription auth, then recording (a) whether Fable-family models are
    listed, (b) thinking-level options incl. xhigh-equivalent, (c) gpt-5.6
    family availability, (d) operator's terms-of-use judgment, (e) the
    chosen models for the future model_profiles pi section. Include the
    exact commands/UI paths per the pinned docs (cite them).
- tests/unit/ (script logic tests with a FAKE pi stub — the stub speaks
  the version/print/RPC envelopes; no real pi needed)
- Your artifact paths (T67 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; installing
or running the REAL pi binary; handling or echoing any API key material;
editing model_profiles (values are decided after the operator lane).

## Validation (record in validation artifact)

1. make format / bash -n / unit-test / validate-agent-assets green.
2. Fake-pi transcript covering PASS, SKIP (no provider env), FAIL, and
   the RPC envelope-kind listing.
3. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T67 set); memory add with the decision fact; effects=none.
Orchestrator then runs the real headless lane (after the T72-preceding
pin+install chore) and hands the operator form to the user.
Reply `AGMSG-RESULT v1 task_id=T67 status=ready_for_review`. max_turns=20.
