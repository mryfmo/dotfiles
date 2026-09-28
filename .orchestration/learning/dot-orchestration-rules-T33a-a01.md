# T33a learning triage

## Candidates

1. Before editing a "mirror" of a rule, find it through the validator and
   tests, not only by the path a task suggests. `scripts/validate-agent-assets.py`
   (line 804) and `tests/install/common/lifecycle.bats` name
   `home/dot_config/codex/AGENTS.md` as the canonical Codex crit text; the
   suggested grep over `home/dot_agents` / `home/dot_codex` missed it.
2. The fail-closed PONG worked on its first use. I sent a scoped
   `status=blocked` for the out-of-boundary item and kept working on the
   in-boundary items. The ruling came back as a task revision and cost no
   idle time.
3. `test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures`
   failed once (`successful_classifications 0 != 5`) while background
   `gh pr checks --watch` and other load were running, and passed on rerun.
   It is a timing-flake candidate for a future test-hardening task.

4. The flake from candidate 3 happened a second time in revision 3, again on
   the first full run after an edit, and the rerun passed. permgate reads none
   of the edited files; the bench's fake-provider calls run under
   `timeout_seconds` of at most 8. A cold start seems to be the trigger.
5. Before putting an evidence format into rule text, read the validator and
   call it on a hand-written sample. The task text's "`reviewer: <agent>`"
   is narrower in the code: `AGENT_REVIEWERS = {claude, claude-code, codex}`.
   Also, `line`/`file` records need a non-empty `path`.

## Promotion

None. These are candidates only.
