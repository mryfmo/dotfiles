---
task: dotfiles-T129-integration-seat-result-gate-cap-a01
pr: 393
head: fa14b3748ebeb940533fed2c695ed678d045543e
---

- a ok: `check_a`

```
626823fbf25a2a48bad0ae1e05792e6ea5f25ea4d1e4c710e973da64b62d1864  .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/task.md
```

- b ok: `check_b`

```
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/autoskill.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/learning.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/precheck-2d61e22.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/report.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/sandbox.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/task.md
yes .orchestration/dotfiles-T129-integration-seat-result-gate-cap-a01/validation.md
yes home/dot_agents/agent-config.yaml
yes home/dot_agents/skills/agmsg-orchestration/SKILL.md
yes home/dot_config/claude/rules/agmsg-orchestration.md
yes home/dot_local/bin/common/executable_herdr-agents
yes scripts/orchestrator/integrate-seat.sh
yes scripts/orchestrator/result-precheck.sh
yes tests/fixtures/regime/worker-step-15.md
yes tests/unit/test_agmsg_orchestration_docs.py
yes tests/unit/test_herdr_agents.py
yes tests/unit/test_integration_seat.py
```

- c ok: `check_c`

```
outside 257 (cap 260), tests 510 (cap 1000)
```

- d ok: `check_d`

```
uv run python -m unittest tests/unit/test_integration_seat.py tests/unit/test_herdr_agents.py -v
shellcheck scripts/orchestrator/integrate-seat.sh scripts/orchestrator/result-precheck.sh home/dot_local/bin/common/executable_herdr-agents
shfmt -d
make validate-agent-assets
git diff --numstat origin/main...HEAD
```

- e ok: `check_e`

```
public-bootstrap (macos-14, client)	pass	9m0s	https://github.com/mryfmo/dotfiles/actions/runs/39045758391/job/117434030424	
public-bootstrap (ubuntu-24.04, client)	pass	10m26s	https://github.com/mryfmo/dotfiles/actions/runs/39045758391/job/117434030611	
public-bootstrap (ubuntu-24.04, server)	pass	8m18s	https://github.com/mryfmo/dotfiles/actions/runs/39045758391/job/117434030585	
test (macos-14, client)	pass	7m57s	https://github.com/mryfmo/dotfiles/actions/runs/39045758387/job/117434030561	
test (ubuntu-24.04, client)	pass	8m38s	https://github.com/mryfmo/dotfiles/actions/runs/39045758387/job/117434030391	
test (ubuntu-24.04, server)	pass	6m4s	https://github.com/mryfmo/dotfiles/actions/runs/39045758387/job/117434030579	
validate	pass	2m5s	https://github.com/mryfmo/dotfiles/actions/runs/39045758390/job/117434030271	
```

- f ok: `check_f`

```
- **The round-3 head, `fa14b374`:** CI passed, 13 rows; bot: none on fa14b37 (the step-15 wait of 15 minutes from the push at 15:35:59Z, no further `@codex review`).
```

- g ok: `check_g`

```
4302868172 P1
4302868177 P1
4302868180 P1
4302959624 P1
4302959629 P2
```

- h unavailable (no local review of fa14b37 here; a Claude seat cannot run codex review): `check_h`

```
local-review: unavailable (no local review of fa14b37 here; a Claude seat cannot run codex review)
```

- i ok: `check_i`

```
Audited `fa14b37` against merge base `59db77b` from a clean checkout.

- [P1] High confidence, correctness — `scripts/orchestrator/integrate-seat.sh:33`: RESULT consumption never invokes `result-precheck.sh verify`; the new receipt gate has no workflow caller.
- [P1] High confidence, security — `scripts/orchestrator/result-precheck.sh:33`: A receipt without `head:` passes verification because the failing `git diff` is swallowed by `|| true`; reproduced with exit 0.
- [P1] High confidence, security — `scripts/orchestrator/result-precheck.sh:33`: The artifact exemption matches substrings, allowing later code changes such as `scripts/.orchestration/<task>/unsafe.sh`; reproduced with exit 0.
- [P1] High confidence, integrity — `scripts/orchestrator/result-precheck.sh:51`: Check (a) hashes the working copy rather than `<head>:<task path>`, allowing a correct local task copy to conceal a different committed copy.
- [P1] High confidence, security — `scripts/orchestrator/integrate-seat.sh:24`: HEAD equality permits modified scripts and configuration in the integration checkout, so subsequent execution is not guaranteed to use trusted `origin/main` content.
- [P2] High confidence, evidence — `scripts/orchestrator/result-precheck.sh:76`: Check (d) accepts command-name occurrences without validation output or successful execution; both a failed transcript and a bare command name passed the reproduction.
- [P2] High confidence, compliance — `scripts/orchestrator/result-precheck.sh:92`: An unresolved P0/P1 marked `open:` passes without the required `bot_rounds=2`; reproduced for P1.
- [P2] High confidence, compliance — `scripts/orchestrator/integrate-seat.sh:100`: Bot findings can receive advisory ownership and be resolved without checking that the owner task exists or recording their required ownership rows.
- [P2] High confidence, correctness — `scripts/orchestrator/integrate-seat.sh:94`: Dispositions cover only the earlier RESULT’s thread list; a P2 arriving during the Bot wait remains undispositioned and blocks integration instead of following the specified advisory path.

Shell syntax and Python compilation passed. Full suites and live-seat execution were not run; latest CI for [PR #393](https://github.com/mryfmo/dotfiles/pull/393) could not be verified because GitHub API access failed.

📝 まとめ: 指定差分の監査で9件の問題を確認しました。受付検査の迂回と統合処理の不足について修正・再監査が必要です。
Verdict: incorrect
```

