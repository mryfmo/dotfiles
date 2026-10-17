---
task_id: dotfiles-T129-integration-seat-result-gate-cap-a01
seat: claude-standard-dot-a006
code_commit: ec4a300d
---

# Validation: dotfiles-T129-integration-seat-result-gate-cap-a01

Every command ran from the worktree `.claude/worktrees/worker-f` on branch `tools/integration-seat-result-gate-cap`, captured at `ec4a300d` by a runner that prints the command, its verbatim output (mise's cache warnings dropped) and `[exit <status>]`. `MAIN` names the main checkout, `T` the task id and `S` the seat's session scratchpad. `UV_OFFLINE=1` was set, and `GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=init.defaultBranch GIT_CONFIG_VALUE_0=main GIT_CONFIG_KEY_1=commit.gpgsign GIT_CONFIG_VALUE_1=false`, CI's git settings (this host signs commits with a key that is absent and sets no default branch, which the test suites' temporary repositories trip on). §1 to §6 ran inside the sandbox; §7 ran outside it (the sandbox denies the macOS `mktemp` that `herdr-agents --add-worker` and its tests use, so 31 add-worker tests fail inside it on `origin/main` as here).

## 1. Task file and task copy (amendment 2, task_sha256 4e00bf12…)

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
4e00bf122f578a9dbbde8ac36feb025d68cb828009a2e9f009606ad760879081  $MAIN/.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md
4e00bf122f578a9dbbde8ac36feb025d68cb828009a2e9f009606ad760879081  .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/task.md
byte-identical
[exit 0]
```

```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-integration-seat-result-gate-cap-a01.md: OK
[exit 0]
```

## 2. The four premises, replayed against origin/main (59db77bb)

premise 1:

```console
$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -nE 'about three concurrent workers|at most three workers' | cut -d: -f1
31
38
[exit 0]
```

premise 2:

```console
$ printf '%s\n' "$(git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -c '^worker_cap:')" "$(git show origin/main:home/dot_local/bin/common/executable_herdr-agents | /usr/bin/grep -c 'worker_cap')"
0
0
[exit 0]
```

premise 3:

```console
$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c 'The worker resolves no thread'
1
[exit 0]
```

premise 4:

```console
$ git show origin/main:scripts/orchestrator/result-precheck.sh > /dev/null 2>&1 && echo present || echo absent
absent
[exit 0]
```

## 3. Branch and base

The branch was cut at `ce032e14` and rebased, before any push, onto `59db77bb` (#386, which changed `local-advisory.sh` without changing its arguments).

```console
$ git log --oneline -6; git merge-base origin/main HEAD; git rev-parse origin/main
ec4a300d fix(herdr-agents): a host without the deployed manifest reads no worker_cap instead of exiting 1 (T129 F4 item 3)
522cc4b8 fix(orchestrator): result-precheck.sh records (h) and (i) as unavailable (<reason>) when codex cannot run, never missing (T129 F4 amendment 2); a head-mismatch case for (e)
e260d89b feat(orchestrator): integrate-seat.sh runs a PR's integration up to the audit; result-precheck.sh refuses a RESULT whose head is not ready (T129 F4 items 1 and 2)
6c994f2c feat(herdr-agents): worker_cap in the manifest bounds --add-worker; the SKILL and rule name the cap and the integration seat (T129 F4 item 3)
59db77bb fix(orchestrator): local-advisory.sh reads only seven-hex earlier reviews and matches their ids literally (T128 chain-review-scripts followup a04) (#386)
ce032e14 chore(orchestration): boundary (19) records of 2026-10-17 (the #379 audit and the local reviews of #375, #378, #386, the T129 auth-route and load-mechanisms task texts, the assets and lint amendments, the 11:10Z handoff) (#391)
59db77bbab7fe19377bc2b94adc6ec5c576f3ebb
59db77bbab7fe19377bc2b94adc6ec5c576f3ebb
[exit 0]
```

## 4. Red: the new tests against origin/main

The two herdr tests against `origin/main`'s manifest, `herdr-agents`, SKILL and rule, then restored; the integration-seat module with the two new scripts moved aside (they do not exist on `origin/main`), then moved back.

```console
$ for f in home/dot_local/bin/common/executable_herdr-agents home/dot_agents/agent-config.yaml home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/claude/rules/agmsg-orchestration.md; do git show origin/main:$f > $f; done && git diff --stat
 home/dot_agents/agent-config.yaml                   |  3 ---
 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 12 ++++++------
 home/dot_config/claude/rules/agmsg-orchestration.md |  4 ++--
 home/dot_local/bin/common/executable_herdr-agents   | 18 ------------------
 4 files changed, 8 insertions(+), 29 deletions(-)
[exit 0]
```

```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap tests.unit.test_herdr_agents.HerdrAgentsTest.test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat 2>&1 | /usr/bin/grep -E '^(FAIL|ERROR):|^Ran|^FAILED|^OK'
ERROR: test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat)
FAIL: test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap)
Ran 2 tests in 1.796s
FAILED (failures=1, errors=1)
[exit 1]
```

```console
$ git checkout -- home && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to ec4a300d
[exit 0]
```

```console
$ mkdir -p "$S/aside" && mv scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh "$S/aside/" && git status --short -- scripts
 D scripts/orchestrator/integrate-seat.sh
 D scripts/orchestrator/result-precheck.sh
[exit 0]
```

```console
$ set -o pipefail; uv run python -m unittest tests/unit/test_integration_seat.py 2>&1 | /usr/bin/grep -E '^(FAIL|ERROR):|^Ran|^FAILED|^OK'
FAIL: test_integrate_seat_reads_plain_gh_output_under_clicolor_force (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_reads_plain_gh_output_under_clicolor_force)
FAIL: test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges)
FAIL: test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
Ran 3 tests in 3.095s
FAILED (failures=3)
[exit 1]
```

```console
$ mv "$S/aside/integrate-seat.sh" "$S/aside/result-precheck.sh" scripts/orchestrator/ && git diff --quiet && git status --short -- scripts && echo restored to $(git rev-parse --short HEAD)
restored to ec4a300d
[exit 0]
```

## 5. The Check inside the sandbox, and the linters

```console
$ uv run python -m unittest tests/unit/test_integration_seat.py -v
test_integrate_seat_reads_plain_gh_output_under_clicolor_force (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_reads_plain_gh_output_under_clicolor_force) ... ok
test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges) ... ok
test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt) ... ok

----------------------------------------------------------------------
Ran 3 tests in 14.911s

OK
[exit 0]
```

```console
$ shellcheck scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh home/dot_local/bin/common/executable_herdr-agents && echo clean
clean
[exit 0]
```

`shfmt -d` as the Check names it, with the repository's flags (`make format` runs `shfmt --indent 4 --space-redirects --diff`; `.editorconfig` sets `indent_size` without `indent_style`, so bare `shfmt -d` asks for tabs in every script of the repository, `chain-integrate.sh` included):

```console
$ shfmt -d -i 4 -sr scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh && echo clean
clean
[exit 0]
```

```console
$ ruff format --config ruff.toml --check tests/unit/test_integration_seat.py tests/unit/test_herdr_agents.py
2 files already formatted
[exit 0]
```

```console
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
[exit 0]
```

```console
$ make validate-agent-assets 2>&1 | /usr/bin/grep -v '^WARN: regime-boundary'
uv run --offline --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
[exit 0]
```

## 6. Mutation check

Each mutant applied alone as a literal replacement asserted to match once, its test run, the file restored with `git checkout`; then the baseline. The script, `$S/mutate-f4.py`:

```python
"""Apply each mutant alone as a literal replacement (asserted to match once), run its test, restore with git checkout.

Prints one `mutant <n> rc=<test status> <file>: <label> (<test>)` line per mutant (caught is rc=1), then a baseline.
"""

import subprocess
import sys
from pathlib import Path

H = "tests.unit.test_herdr_agents.HerdrAgentsTest."
I = "tests.unit.test_integration_seat.IntegrationSeatTest."
CAP = H + "test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap"
TEXT = H + "test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat"
CHAIN = I + "test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges"
COLOUR = I + "test_integrate_seat_reads_plain_gh_output_under_clicolor_force"
PRE = I + "test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt"
HA = "home/dot_local/bin/common/executable_herdr-agents"
SEAT, PC = "scripts/orchestrator/integrate-seat.sh", "scripts/orchestrator/result-precheck.sh"
MUTANTS = [
    (HA, 'if [[ ${seat_seated} == false ]] && ((seats >= seat_cap)); then', "if false; then", "the cap check dropped", CAP),
    (HA, "((seats >= seat_cap))", "((seats > seat_cap))", "the cap off by one", CAP),
    ("home/dot_agents/skills/agmsg-orchestration/SKILL.md", "(4 in the manifest today) in total", "(3 in the manifest today) in total", "a seat count out of step", TEXT),
    ("home/dot_config/claude/rules/agmsg-orchestration.md", "the rest of integration runs on the integration seat through", "the rest of integration runs on another seat through", "the Delegation bullet without the integration seat", TEXT),
    (SEAT, "export CLICOLOR_FORCE=0 FORCE_COLOR=0 NO_COLOR=1", "export FORCE_COLOR=0 NO_COLOR=1", "CLICOLOR_FORCE inherited", COLOUR),
    (SEAT, '[[ ${ok} == *",${rc},"* ]] || {', "true || {", "a failing step does not block", CHAIN),
    (SEAT, "elif [[ ${p} == P[23] && -n ${owner} ]]; then", "elif [[ -n ${owner} ]]; then", "an unfixed P0/P1 made advisory", CHAIN),
    (PC, "[[ ${f} != ${g} ]] || hit=yes", "hit=yes", "(b) takes any file", PRE),
    (PC, "exit !(o <= max && t <= tmax)", "exit 0", "(c) ignores the caps", PRE),
    (PC, '/usr/bin/grep -q -F -- "${c}" "${d}/validation.md" || bad=1', 'true || bad=1', "(d) ignores the validation file", PRE),
    (PC, '[ "$(gh pr view "${pr}" --json headRefOid --jq .headRefOid)" = "${head}" ] && gh pr checks', "gh pr checks", "(e) not bound to the head", PRE),
    (PC, '/usr/bin/grep -q -E "${id}:${p}:$([[ ${p} == P[01] ]] && echo \'(fixed:[0-9a-f]{7}|open:)\')" "${d}/report.md" || bad=1', '/usr/bin/grep -q -F "${id}" "${d}/report.md" || bad=1', "(g) takes any mention of the id", PRE),
    (PC, 'miss+="code-after-receipt,"', ":", "verify takes code after the receipt", PRE),
    (PC, '[ "${want#task_sha256=}" = "$(shasum -a 256 < "${d}/task.md" | cut -d\' \' -f1)" ]', "true", "(a) takes any task copy", PRE),
]


def test(name):
    return subprocess.run([sys.executable, "-m", "unittest", name], capture_output=True, text=True).returncode


for n, (rel, old, new, label, name) in enumerate(MUTANTS, 1):
    path = Path(rel)
    text = path.read_text()
    assert text.count(old) == 1, (rel, label, text.count(old))
    path.write_text(text.replace(old, new))
    rc = test(name)
    subprocess.run(["git", "checkout", "--", rel], check=True)
    print(f"mutant {n} rc={rc} {rel}: {label} ({name.rsplit('.', 1)[1]})", flush=True)
names = list(dict.fromkeys(name for *_, name in MUTANTS))
rc = subprocess.run([sys.executable, "-m", "unittest", *names], capture_output=True, text=True).returncode
print(f"baseline rc={rc}: the {len(names)} tests on the unmutated tree")
```

```console
$ uv run python "$S/mutate-f4.py"
mutant 1 rc=1 home/dot_local/bin/common/executable_herdr-agents: the cap check dropped (test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap)
mutant 2 rc=1 home/dot_local/bin/common/executable_herdr-agents: the cap off by one (test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap)
mutant 3 rc=1 home/dot_agents/skills/agmsg-orchestration/SKILL.md: a seat count out of step (test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat)
mutant 4 rc=1 home/dot_config/claude/rules/agmsg-orchestration.md: the Delegation bullet without the integration seat (test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat)
mutant 5 rc=1 scripts/orchestrator/integrate-seat.sh: CLICOLOR_FORCE inherited (test_integrate_seat_reads_plain_gh_output_under_clicolor_force)
mutant 6 rc=1 scripts/orchestrator/integrate-seat.sh: a failing step does not block (test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges)
mutant 7 rc=1 scripts/orchestrator/integrate-seat.sh: an unfixed P0/P1 made advisory (test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges)
mutant 8 rc=1 scripts/orchestrator/result-precheck.sh: (b) takes any file (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 9 rc=1 scripts/orchestrator/result-precheck.sh: (c) ignores the caps (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 10 rc=1 scripts/orchestrator/result-precheck.sh: (d) ignores the validation file (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 11 rc=1 scripts/orchestrator/result-precheck.sh: (e) not bound to the head (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 12 rc=1 scripts/orchestrator/result-precheck.sh: (g) takes any mention of the id (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 13 rc=1 scripts/orchestrator/result-precheck.sh: verify takes code after the receipt (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
mutant 14 rc=1 scripts/orchestrator/result-precheck.sh: (a) takes any task copy (test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt)
baseline rc=0: the 5 tests on the unmutated tree
[exit 0]
```

## 7. The Check's two modules, outside the sandbox

197 of 198 pass. The one failure, `test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude` (an attach-mode seat claim that depends on this host's live process ids), fails alike with `origin/main`'s `herdr-agents`, the second block.

```console
$ uv run python -m unittest tests/unit/test_integration_seat.py tests/unit/test_herdr_agents.py -v
test_integrate_seat_reads_plain_gh_output_under_clicolor_force (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_reads_plain_gh_output_under_clicolor_force) ... ok
test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges (tests.unit.test_integration_seat.IntegrationSeatTest.test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges) ... ok
test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt (tests.unit.test_integration_seat.IntegrationSeatTest.test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt) ... ok
test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_accepts_a_claude_trust_dialog_while_spawn_waits) ... ok
test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_defaults_to_the_manifest_worktree_and_refuses_a_non_worktree_path) ... ok
test_add_worker_derives_the_default_herdr_socket_for_spawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_derives_the_default_herdr_socket_for_spawn) ... ok
test_add_worker_emits_no_override_for_an_unparseable_codex_config (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_emits_no_override_for_an_unparseable_codex_config) ... ok
test_add_worker_exits_zero_when_a_timed_out_spawn_still_links (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_exits_zero_when_a_timed_out_spawn_still_links) ... ok
test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array) ... ok
test_add_worker_linkage_failure_prints_the_invocation_and_the_query (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_failure_prints_the_invocation_and_the_query) ... ~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a359c40>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a359d20>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a359fc0>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a35a180>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a35a260>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a35a420>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
~/.local/share/mise/installs/python/latest/lib/python3.15/re/_parser.py:176: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10a35a5e0>
  def append(self, code):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_falls_back_to_the_legacy_record_without_the_resolver) ... ok
test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_delayed_pong_for_another_ping) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_gone_from_the_workspace) ... ok
test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_for_a_pane_that_predates_this_spawn) ... ok
test_add_worker_linkage_ignores_a_placement_record_from_another_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_placement_record_from_another_workspace) ... ok
test_add_worker_linkage_ignores_a_pong_older_than_this_ping (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_ignores_a_pong_older_than_this_ping) ... ok
test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_reads_a_leading_zero_wait_as_decimal) ... ok
test_add_worker_linkage_refuses_a_placement_conflict (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_a_placement_conflict) ... ok
test_add_worker_linkage_refuses_several_orchestrator_identities (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_refuses_several_orchestrator_identities) ... ok
test_add_worker_linkage_resolves_an_id_keyed_placement_record (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_resolves_an_id_keyed_placement_record) ... ok
test_add_worker_linkage_survives_a_non_numeric_pong_wait (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_survives_a_non_numeric_pong_wait) ... ok
test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_linkage_uses_the_spawn_placement_record_not_team_sh) ... ok
test_add_worker_names_the_seat_from_a_codex_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_names_the_seat_from_a_codex_orchestrator_identity) ... ok
test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options) ... ok
test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_a_seat_beyond_the_manifest_worker_cap) ... ok
test_add_worker_refuses_an_undefined_profile_before_any_change (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_an_undefined_profile_before_any_change) ... ok
test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_refuses_before_any_change_when_no_herdr_socket_is_found) ... ok
test_add_worker_rejects_a_worktree_outside_claude_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_rejects_a_worktree_outside_claude_worktrees) ... ok
test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_claude_spawn_without_a_trust_dialog) ... ok
test_add_worker_reports_a_failed_spawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_a_failed_spawn) ... ok
test_add_worker_reports_linkage_ok_after_a_ready_spawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_ok_after_a_ready_spawn) ... ok
test_add_worker_reports_linkage_unreached_after_a_failed_spawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_linkage_unreached_after_a_failed_spawn) ... ok
test_add_worker_reports_shallow_metadata_as_not_granted (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reports_shallow_metadata_as_not_granted) ... ok
test_add_worker_reuses_a_seat_tab_in_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seat_tab_in_the_pair_workspace) ... ok
test_add_worker_reuses_a_seated_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_reuses_a_seated_workspace) ... ok
test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_seats_the_worker_in_a_tab_of_the_pair_workspace) ... ok
test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_spawns_the_seat_in_its_own_workspace_with_profile_args) ... ok
test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_succeeds_for_a_claude_worker_without_a_trust_dialog) ... ok
test_add_worker_without_a_worktree_refuses_an_ambiguous_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_add_worker_without_a_worktree_refuses_an_ambiguous_orchestrator_identity) ... ok
test_added_worker_boot_keeps_the_inherited_github_environment (tests.unit.test_herdr_agents.HerdrAgentsTest.test_added_worker_boot_keeps_the_inherited_github_environment) ... ok
test_agent_name_taken_gives_up_after_bounded_wait (tests.unit.test_herdr_agents.HerdrAgentsTest.test_agent_name_taken_gives_up_after_bounded_wait) ... ok
test_attach_bootstraps_agmsg_without_starting_a_worker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_bootstraps_agmsg_without_starting_a_worker) ... ok
test_attach_complete_workspace_is_idempotent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_complete_workspace_is_idempotent) ... ok
test_attach_completes_bootstrap_on_a_self_named_pair (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_completes_bootstrap_on_a_self_named_pair) ... ok
test_attach_correct_order_does_not_swap (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_correct_order_does_not_swap) ... ok
test_attach_equal_halves_does_not_resize (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_equal_halves_does_not_resize) ... ok
test_attach_from_the_self_named_worker_pane_exits_quietly (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_from_the_self_named_worker_pane_exits_quietly) ... ok
test_attach_from_the_worker_pane_does_not_relabel_it (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_pane_does_not_relabel_it) ... ok
test_attach_from_the_worker_worktree_exits_quietly (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_from_the_worker_worktree_exits_quietly) ... ok
test_attach_ignores_agmsg_bootstrap_failure (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_ignores_agmsg_bootstrap_failure) ... ok
test_attach_ignores_extra_panes_on_other_tabs (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_ignores_extra_panes_on_other_tabs) ... ok
test_attach_in_a_linked_worker_worktree_exits_quietly (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_in_a_linked_worker_worktree_exits_quietly) ... ok
test_attach_leaves_a_self_named_pair_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_leaves_a_self_named_pair_alone) ... ok
test_attach_names_stale_seats (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_names_stale_seats) ... ok
test_attach_noops_for_full_mode_managed_layout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_noops_for_full_mode_managed_layout) ... ok
test_attach_reports_agmsg_skip_when_not_installed (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_reports_agmsg_skip_when_not_installed) ... ok
test_attach_skips_delivery_when_turn_hook_exists (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists) ... ok
test_attach_without_herdr_environment_names_the_seated_worker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_names_the_seated_worker) ... ok
test_attach_without_herdr_environment_prints_the_bring_up_summary (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_prints_the_bring_up_summary) ... ok
test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_without_herdr_environment_stays_quiet_in_the_worker_worktree) ... ok
test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact) ... ok
test_audit_creates_the_audit_tab_once_and_reuses_it (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_creates_the_audit_tab_once_and_reuses_it) ... ok
test_audit_exits_2_without_a_managed_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_exits_2_without_a_managed_workspace) ... ok
test_audit_fails_as_unmasked_when_masking_fails (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_fails_as_unmasked_when_masking_fails) ... ok
test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info) ... ok
test_audit_finds_the_self_named_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_finds_the_self_named_pair_workspace) ... ok
test_audit_gates_on_the_concluding_line_of_the_last_message (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_gates_on_the_concluding_line_of_the_last_message) ... ok
test_audit_marker_detection_reads_unwrapped_snapshots (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_marker_detection_reads_unwrapped_snapshots) ... ok
test_audit_masks_evidence_before_the_verdict_gate (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_before_the_verdict_gate) ... ok
test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_masks_evidence_even_when_the_audit_exit_is_nonzero) ... ok
test_audit_nonzero_exit_marker_fails_the_helper (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_nonzero_exit_marker_fails_the_helper) ... ok
test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker) ... ok
test_audit_quotes_a_non_ascii_out_path_under_the_c_locale (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_quotes_a_non_ascii_out_path_under_the_c_locale) ... ok
test_audit_quotes_the_last_message_path_for_a_non_ascii_out (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_quotes_the_last_message_path_for_a_non_ascii_out) ... ok
test_audit_refuses_a_busy_audit_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_busy_audit_pane) ... ok
test_audit_refuses_a_tracked_masker_missing_from_the_tree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_refuses_a_tracked_masker_missing_from_the_tree) ... ok
test_audit_refuses_an_uncommitted_or_untracked_masker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_refuses_an_uncommitted_or_untracked_masker) ... ok
test_audit_refuses_the_masker_from_the_audited_commit (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_refuses_the_masker_from_the_audited_commit) ... ok
test_audit_rejects_unsafe_arguments_before_calling_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_rejects_unsafe_arguments_before_calling_herdr) ... ok
test_audit_runs_codex_exec_with_the_prompt_and_last_message_file (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_runs_codex_exec_with_the_prompt_and_last_message_file) ... ok
test_audit_runs_in_dir_even_when_the_reused_pane_moved (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_runs_in_dir_even_when_the_reused_pane_moved) ... ok
test_audit_skips_masking_without_a_repo_validator (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_skips_masking_without_a_repo_validator) ... ok
test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard) ... ok
test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff) ... ok
test_audit_task_names_a_txt_artifact_when_no_md_one_exists (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_task_names_a_txt_artifact_when_no_md_one_exists) ... ok
test_audit_task_names_only_the_task_file_when_no_artifact_exists (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_task_names_only_the_task_file_when_no_artifact_exists) ... ok
test_audit_task_normalises_home_paths_with_the_repository_masker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_task_normalises_home_paths_with_the_repository_masker) ... ok
test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_task_refuses_a_missing_task_file_or_merge_base_before_herdr_work) ... ok
test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot) ... ok
test_audit_uses_manifest_audit_codex_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_uses_manifest_audit_codex_args) ... ok
test_audit_verdict_gate_reads_only_the_final_codex_block (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_verdict_gate_reads_only_the_final_codex_block) ... ok
test_audit_waits_for_the_prompt_on_a_new_audit_tab (tests.unit.test_herdr_agents.HerdrAgentsTest.test_audit_waits_for_the_prompt_on_a_new_audit_tab) ... ok
test_bootstrap_accepts_same_identity_in_multiple_teams (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_accepts_same_identity_in_multiple_teams) ... ok
test_bootstrap_adds_claude_worker_merge_denials (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_adds_claude_worker_merge_denials) ... ok
test_bootstrap_leaves_a_foreign_pre_push_hook_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_leaves_a_foreign_pre_push_hook_alone) ... ok
test_bootstrap_only_creates_missing_herdr_log_directory (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_creates_missing_herdr_log_directory) ... ok
test_bootstrap_only_does_not_call_herdr_or_agents (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_does_not_call_herdr_or_agents) ... ok
test_bootstrap_only_never_sets_codex_delivery_in_the_main_checkout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_never_sets_codex_delivery_in_the_main_checkout) ... ok
test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_sets_claude_delivery_once_when_hook_is_missing) ... ok
test_bootstrap_only_skips_all_delivery_when_both_hooks_exist (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_all_delivery_when_both_hooks_exist) ... ok
test_bootstrap_only_skips_home_without_agmsg_calls (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_skips_home_without_agmsg_calls) ... ok
test_bootstrap_only_warns_for_missing_claude_identity_without_joining (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_missing_claude_identity_without_joining) ... ok
test_bootstrap_only_warns_for_multiple_claude_identities (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_only_warns_for_multiple_claude_identities) ... ok
test_bootstrap_removes_its_retired_pre_push_stub (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_removes_its_retired_pre_push_stub) ... ok
test_bootstrap_with_claude_worker_leaves_codex_hooks_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_bootstrap_with_claude_worker_leaves_codex_hooks_alone) ... ok
test_claude_agent_accepts_manifest_profile_arguments_for_e2e (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_agent_accepts_manifest_profile_arguments_for_e2e) ... ok
test_claude_orchestrator_kind_keeps_the_attach_summary (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_orchestrator_kind_keeps_the_attach_summary) ... ok
test_claude_settings_add_herdr_attach_session_hook (tests.unit.test_herdr_agents.HerdrAgentsTest.test_claude_settings_add_herdr_attach_session_hook) ... ok
test_codex_orchestrator_kind_keeps_the_non_seating_modes (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_keeps_the_non_seating_modes) ... ok
test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_leaves_a_worker_worktree_attach_quiet) ... ok
test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_attach_in_another_linked_worktree) ... ok
test_codex_orchestrator_kind_refuses_the_claude_orchestrator_before_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_codex_orchestrator_kind_refuses_the_claude_orchestrator_before_herdr) ... ok
test_directive_looks_up_a_codex_orchestrator_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_directive_looks_up_a_codex_orchestrator_identity) ... ok
test_directive_prints_the_regime_line_without_herdr (tests.unit.test_herdr_agents.HerdrAgentsTest.test_directive_prints_the_regime_line_without_herdr) ... ok
test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_legacy_files_pane_is_not_reused_for_claude_or_split_again) ... ok
test_existing_workspace_matches_canonical_macos_workdir (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_matches_canonical_macos_workdir) ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_restarts_missing_claude_in_empty_pane) ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_splits_when_missing_claude_has_no_empty_pane) ... ok
test_existing_workspace_with_legacy_files_pane_focuses_without_mutation (tests.unit.test_herdr_agents.HerdrAgentsTest.test_existing_workspace_with_legacy_files_pane_focuses_without_mutation) ... ok
test_file_viewer_plugin_config_sets_micro_editor (tests.unit.test_herdr_agents.HerdrAgentsTest.test_file_viewer_plugin_config_sets_micro_editor) ... ok
test_full_mode_does_not_duplicate_a_solo_codex_worker_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_does_not_duplicate_a_solo_codex_worker_seat) ... ok
test_full_mode_heal_never_puts_the_orchestrator_in_the_audit_or_an_added_worker_tab (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_never_puts_the_orchestrator_in_the_audit_or_an_added_worker_tab) ... ok
test_full_mode_heal_with_a_live_orchestrator_starts_nothing (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heal_with_a_live_orchestrator_starts_nothing) ... ok
test_full_mode_heals_nothing_in_a_healthy_self_named_pair (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_nothing_in_a_healthy_self_named_pair) ... ok
test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_heals_the_orchestrator_beside_a_live_added_claude_worker) ... ok
test_full_mode_never_takes_a_normalized_claude_worker_for_the_orchestrator (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_never_takes_a_normalized_claude_worker_for_the_orchestrator) ... ok
test_full_mode_refuses_duplicate_managed_workspaces (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_refuses_duplicate_managed_workspaces) ... ok
test_full_mode_refuses_to_seat_the_orchestrator_in_a_worker_tab (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_refuses_to_seat_the_orchestrator_in_a_worker_tab) ... ok
test_full_mode_skips_agmsg_bootstrap_for_home (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_skips_agmsg_bootstrap_for_home) ... ok
test_full_mode_starts_only_the_orchestrator_in_the_initial_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_full_mode_starts_only_the_orchestrator_in_the_initial_pane) ... ok
test_ghostty_config_does_not_auto_start_herdr_session (tests.unit.test_herdr_agents.HerdrAgentsTest.test_ghostty_config_does_not_auto_start_herdr_session) ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_alt_a_runs_helper_from_active_pane) ... ok
test_herdr_prefix_f_opens_file_viewer_popup (tests.unit.test_herdr_agents.HerdrAgentsTest.test_herdr_prefix_f_opens_file_viewer_popup) ... ok
test_make_update_includes_agmsg_bootstrap_and_upgrade_is_gone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_make_update_includes_agmsg_bootstrap_and_upgrade_is_gone) ... ok
test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_new_pane_waits_for_shell_and_retries_agent_start_once_on_timeout) ... ok
test_orchestrator_kind_comes_from_the_manifest_env_and_is_validated (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_kind_comes_from_the_manifest_env_and_is_validated) ... ok
test_orchestrator_pane_appends_claude_args_after_profile_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_appends_claude_args_after_profile_args) ... ok
test_orchestrator_pane_start_claims_the_seat_with_the_composite_id (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_claims_the_seat_with_the_composite_id) ... ok
test_orchestrator_pane_start_without_a_session_claims_nothing (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_start_without_a_session_claims_nothing) ... ok
test_orchestrator_pane_uses_interactive_profile_args (tests.unit.test_herdr_agents.HerdrAgentsTest.test_orchestrator_pane_uses_interactive_profile_args) ... ok
test_pane_creation_propagates_explicit_fpath (tests.unit.test_herdr_agents.HerdrAgentsTest.test_pane_creation_propagates_explicit_fpath) ... ok
test_regime_boundary_check_accepts_a_clean_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_a_clean_canonical_clone) ... ok
test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_a_seated_main_checkout_off_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_a_seated_main_checkout_off_main) ... ok
test_regime_boundary_check_flags_empty_seats_only (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone) ... ok
test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main) ... ok
test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main) ... ok
test_regime_boundary_check_reports_a_stash_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stash_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone) ... ok
test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi) ... ok
test_registered_agent_not_ready_waits_for_idle_without_duplicate_start (tests.unit.test_herdr_agents.HerdrAgentsTest.test_registered_agent_not_ready_waits_for_idle_without_duplicate_start) ... ok
test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_cleans_up_a_codex_seat_without_a_placement_record) ... ok
test_remove_worker_closes_only_its_tab_in_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_closes_only_its_tab_in_the_pair_workspace) ... ok
test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_despawns_then_turns_delivery_off_leaves_and_closes) ... ok
test_remove_worker_force_retries_a_failed_graceful_despawn (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_retries_a_failed_graceful_despawn) ... ok
test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_force_skips_the_forced_despawn_when_graceful_succeeds) ... ok
test_remove_worker_forces_despawn_when_graceful_reports_needs_force (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_forces_despawn_when_graceful_reports_needs_force) ... ok
test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_keeps_a_worker_tab_that_holds_another_running_agent) ... ok
test_remove_worker_refuses_a_dirty_worktree_without_force (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_refuses_a_dirty_worktree_without_force) ... ok
test_remove_worker_stale_keeps_the_record_when_cleanup_fails (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_keeps_the_record_when_cleanup_fails) ... ok
test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows) ... ok
test_remove_worker_stale_retires_a_seat_whose_pane_is_gone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stale_retires_a_seat_whose_pane_is_gone) ... ok
test_remove_worker_stops_when_a_graceful_despawn_fails (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_a_graceful_despawn_fails) ... ok
test_remove_worker_stops_when_the_forced_retry_also_fails (tests.unit.test_herdr_agents.HerdrAgentsTest.test_remove_worker_stops_when_the_forced_retry_also_fails) ... ok
test_restart_worker_is_retired_and_touches_nothing (tests.unit.test_herdr_agents.HerdrAgentsTest.test_restart_worker_is_retired_and_touches_nothing) ... ok
test_seat_claim_fails_when_a_later_team_is_held_by_another_session (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_fails_when_a_later_team_is_held_by_another_session) ... ok
test_seat_claim_held_by_another_session_fails_without_release (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_held_by_another_session_fails_without_release) ... ok
test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude) ... FAIL
test_seat_claim_replaces_a_same_session_bare_lock (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_bare_lock) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid) ... ok
test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid) ... ok
test_seat_claim_replaces_same_session_bare_locks_in_every_team (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_replaces_same_session_bare_locks_in_every_team) ... ok
test_session_start_attach_bounds_a_trickling_hook_payload (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload) ... ok
test_session_start_attach_claims_the_seat_in_a_managed_pane (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_the_seat_in_a_managed_pane) ... ok
test_session_start_attach_claims_when_the_hook_keeps_stdin_open (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_claims_when_the_hook_keeps_stdin_open) ... ok
test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_no_directive_for_a_pane_that_is_not_the_orchestrator) ... ok
test_session_start_attach_prints_the_regime_directive_with_a_worker_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_prints_the_regime_directive_with_a_worker_seat) ... ok
test_session_start_attach_reads_the_hook_payload_and_herdr_pid (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_reads_the_hook_payload_and_herdr_pid) ... ok
test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator (tests.unit.test_herdr_agents.HerdrAgentsTest.test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator) ... ok
test_start_keeps_node_global_without_mise_tool_install (tests.unit.test_herdr_agents.HerdrAgentsTest.test_start_keeps_node_global_without_mise_tool_install) ... ok
test_start_removes_node_global_agent_clis_shadowing_mise (tests.unit.test_herdr_agents.HerdrAgentsTest.test_start_removes_node_global_agent_clis_shadowing_mise) ... ok
test_start_skips_node_global_removal_without_stray (tests.unit.test_herdr_agents.HerdrAgentsTest.test_start_skips_node_global_removal_without_stray) ... ok
test_successful_agent_start_does_not_poll_agent_list (tests.unit.test_herdr_agents.HerdrAgentsTest.test_successful_agent_start_does_not_poll_agent_list) ... ok
test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_the_skill_and_the_rule_name_the_manifest_worker_cap_and_the_integration_seat) ... ok
test_two_self_named_pair_workspaces_still_refuse (tests.unit.test_herdr_agents.HerdrAgentsTest.test_two_self_named_pair_workspaces_still_refuse) ... ok
test_worker_kind_claude_does_not_require_codex (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_kind_claude_does_not_require_codex) ... ok
test_worker_panes_inherit_the_users_github_login (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_panes_inherit_the_users_github_login) ... ok
test_worker_seat_is_skipped_outside_a_git_main_checkout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_is_skipped_outside_a_git_main_checkout) ... ok
test_worker_seat_label_comes_from_the_worker_worktree_registration (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_seat_label_comes_from_the_worker_worktree_registration) ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback (tests.unit.test_herdr_agents.HerdrAgentsTest.test_yazi_edit_opener_prefers_zed_with_editor_fallback) ... ok
test_zprofile_adds_common_bin_to_login_shell_path (tests.unit.test_herdr_agents.HerdrAgentsTest.test_zprofile_adds_common_bin_to_login_shell_path) ... ok

======================================================================
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "$MAIN/.claude/worktrees/worker-f/tests/unit/test_herdr_agents.py", line 1733, in test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude
    self.assertIn(
    ~~~~~~~~~~~~~^
        f"seat_claim=failed status=held team=dotfiles owner={live_owner}",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        result.stdout.splitlines(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'seat_claim=failed status=held team=dotfiles owner=sid-stdin.9533' not found in ['seat_claim=ok owner=sid-stdin.4343 replaced_stale_lock=yes']

----------------------------------------------------------------------
Ran 198 tests in 302.305s

FAILED (failures=1)
[exit 1]
```

```console
$ cp home/dot_local/bin/common/executable_herdr-agents "$S/herdr-agents.branch" && git show origin/main:home/dot_local/bin/common/executable_herdr-agents > home/dot_local/bin/common/executable_herdr-agents && uv run python -m unittest tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^FAILED|^OK"; cp "$S/herdr-agents.branch" home/dot_local/bin/common/executable_herdr-agents && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
FAIL: test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude (tests.unit.test_herdr_agents.HerdrAgentsTest.test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude)
AssertionError: 'seat_claim=failed status=held team=dotfiles owner=sid-stdin.11386' not found in ['seat_claim=ok owner=sid-stdin.4343 replaced_stale_lock=yes']
Ran 1 test in 0.905s
FAILED (failures=1)
restored to ec4a300d
[exit 0]
```

## 8. Caps

```console
$ git status --porcelain -- scripts tests home; git diff --numstat origin/main...HEAD
3	0	home/dot_agents/agent-config.yaml
6	6	home/dot_agents/skills/agmsg-orchestration/SKILL.md
2	2	home/dot_config/claude/rules/agmsg-orchestration.md
18	0	home/dot_local/bin/common/executable_herdr-agents
122	0	scripts/orchestrator/integrate-seat.sh
110	0	scripts/orchestrator/result-precheck.sh
76	0	tests/unit/test_herdr_agents.py
353	0	tests/unit/test_integration_seat.py
[exit 0]
```

Outside `tests/` and `.orchestration/`, excluding the SKILL and the rule (text): 253 changed lines (amendment 2 sets the cap at 260); under `tests/`: 429 added lines (cap 1000).

## 9. The CompactionDB entry, in the worktree's own database

```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] Plan 023 F4: worker_cap: 4 in agent-config.yaml, read by herdr-agents --add-worker with sed from the deployed ~/.agents/agent-config.yaml (no key or no file: no cap, one stderr line), counting .claude/worktrees/ worktrees with an agmsg identity; scripts/orchestrator/integrate-seat.sh runs a PR from the worker RESULT up to the audit on the integration seat (never audit, gate or merge) and sends AGMSG-RESULT kind=integration; scripts/orchestrator/result-precheck.sh run writes .orchestration/<task>/precheck-<sha7>.md (checks a to i, h and i unavailable without codex) and verify refuses a RESULT whose precheck= receipt is absent, has a missing check or precedes a code change. (T129 F4)"
253b4a23-f87d-4604-8049-e476ade55790
[exit 0]
```
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory search worker_cap
253b4a23-f87d-4604-8049-e476ade55790 [project/decision] [memory:decision] Plan 023 F4: worker_cap: 4 in agent-config.yaml, read by herdr-agents --add-worker with sed from the deployed ~/.agents/agent-config.yaml (no key or no file: no cap, one stderr line), counting .claude/worktrees/ worktrees with an agmsg identity; scripts/orchestrator/integrate-seat.sh runs a PR from the worker RESULT up to the audit on the integration seat (never audit, gate or merge) and sends AGMSG-RESULT kind=integration; scripts/orchestrator/result-prech…
[exit 0]
```
