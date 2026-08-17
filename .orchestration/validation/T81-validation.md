# T81 validation

## Exact delta and contract invariants

- Reconstructed the pre-T81 skill by removing the exact new Worker Playbook
  line and computed a unified diff against the post-T81 file.
- Result: `added_lines=1`, `removed_lines=0`.
- The addition contains all required meanings: `cost:`, observed session
  token/cost figures, runtime availability, `cost: n/a`, T76, and the
  `AGMSG-ACCEPTANCE v1` cost line.
- Message Contract pre/post bytes are identical.
- Message Contract SHA-256:
  `aa48267ed63f6ef1b2a13149e6a9c74be3be73699f4dae6610d1627fe7be8700`.
- Slim rule files were outside the allowed edit set and received no T81 delta:
  - Claude agmsg rule: 1,358 bytes,
    `6c20067178b83b84487c5c0b1f8ed291f09c3fc50415a5b0a24ccc9d244fac72`.
  - Codex AGENTS: 8,697 bytes,
    `09ad0f73b074c4512909b2acc932784321b94321c55df69a77238aee6b24565d`.

## Command validation

| Command | Result |
|---|---|
| `make format` | PASS — shfmt diff empty |
| `env UV_CACHE_DIR=/private/tmp/t80-uv-cache uv run python -m unittest discover -s tests/unit -p 'test_*.py' -q` | PASS — 336 tests in 28.575s |
| `env UV_CACHE_DIR=/private/tmp/t80-uv-cache uv run --with pyyaml scripts/validate-agent-assets.py` | PASS — `agent asset validation ok` |
| `git diff --check` | PASS |
| one-line delta / contract / rule static assertions | PASS |

The unit output's four `ERROR:` lines are expected negative-fixture messages;
the unittest runner ended `OK` with exit 0.

## Plan-quality gate

- Manual checklist: passed.
- Validator / Make target: unavailable.
- Hook: unavailable.
- Subagent definition: unavailable.
- Template and CI entrypoint: unavailable.
- Unavailable exact command:
  `uv run python scripts/validate_plan_quality.py .agents/worklog/codex/plan/20260817_170515_plan.md`.

## Crit gate

- Initial `make require-crit-review`: expected block for shared skill/broad diff.
- Crit review: finding-free resolved record `r_beed82`.
- Receipt: `.agents/worklog/codex/review/T81-receipt.md`.
- Final command:
  `env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/T81-receipt.md make require-crit-review`.
