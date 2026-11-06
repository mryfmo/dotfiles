# Architecture: dotfiles, scoped to d1ecd495..d1fd54ba (U244)

## Product, principals, protected resources

A dotfiles repository that also carries the orchestration levers of an agent "regime". An orchestrator seat merges unit pull requests only through `scripts/orchestrator/pr-merge.sh`, deployed as `~/.local/bin/common/pr-merge.sh`. The seat's policy allows that lever and denies `gh pr merge` text.

The protected resource is `main`: a merge must follow a recorded audit verdict, a sweep row and green CI.

Principals:

- **The operator and orchestrator seat.** They write the program store, `.orchestration/orchestrate/<program>/` (`ledger.tsv`, `verdicts/`, `dispositions.tsv`, `units.tsv`, `sweeps/`, `briefs/`).
- **Worker seats.** They push branches but do not write the main checkout's store.
- **The pull request body.** It carries the `Program-Unit:` line.
- **GitHub.** It answers `gh` reads, and the lever pins its one write with `--match-head-commit`.

## Comparable baseline

None source-grounded beyond the repository's own Audit rule (AGENTS.md, Audit section).

## Stack and limits

- Bash (`set -euo pipefail`), with Python 3 probes run as `python3 -I -S`.
- `scripts/orchestrator/ledger.py` is the one ledger reader.
- Tests are `unittest` modules.
- This run is source-only; no target code is executed.

## Entry surfaces and paths in scope

The lever's inputs at the head:

- **The body's one `Program-Unit:` line** (pr-merge.sh:206, 691-701). It selects the store, `<toplevel>/.orchestration/orchestrate/<program>`. Each directory is a non-symlink directory of this user, and `--records` must resolve to it (702-712).
- **`ledger.py verdict`** (`require_verdict_row`, 344-393), **the verdict file and `dispositions.tsv`** (`require_dispositions`, 468-595), and **`ledger.py sweep`** (`require_sweep_row`, 613-677).
- **The manifest pin probe** (`sweep_pin_probe`, 243-290) over `LEVER_MANIFEST`, the manifest the self-check trusted (124-179).
- **The findings file stat** under `<store>/sweeps/` (661-676).
- **CI**: `gh pr checks` between two head and base reads (758-779), then the merge (782) and the post-merge read (783-798).

What U244 changed:

- It deletes the brief reading: `trust_probe`, which compiled and executed `brief-check.py`; the `briefs/` glob; and the `3) return 0` branch that skipped the sweep for a brief without `TRUST`.
- Every unit now needs its sweep row.
- The pin of both byte-identical lever copies (agent-config.yaml levers block, generated-agent-outputs.json), the Audit sentence in AGENTS.md and its regime template, the README row and the tests follow.

## Trust boundaries and their strongest controls

| Boundary | Strongest control |
| --- | --- |
| Body into store | An anchored grammar for the program (one component) and unit (`U<digits>`), owner and no-symlink checks, and the `--records` equality. |
| Store rows into the gate | `ledger.py` as the one strict reader, its status mapped 0/2/other, and the answer read by shape. The verdict row's unit must be the body's or a fix unit. The sweep row must be the rule's exact row, with the pin a prefix of the manifest pin and the findings file a regular file of this user. |
| Lever integrity | The self-check sha256 pin. Both copies hash to `5e235e90…`, which is the manifest value. |

## Starting paths

`scripts/orchestrator/pr-merge.sh`, `home/dot_local/bin/common/executable_pr-merge.sh`, `scripts/orchestrator/ledger.py` (unchanged, read for context), `home/dot_agents/agent-config.yaml`, `tests/unit/test_pr_merge.py`, `tests/unit/test_pr_levers.py`.

## Prior coverage

The previous run is run-3 (U236, the U224 head `dfb763ce`). Its 26 units are carried with the same IDs as `out_of_scope`, because that change is not in this head. There are no prior records.

## Companion selection

- **ATTACK-CLASSES.md:** Access control (the merge gate), Injection (body-selected names), Business logic (the pin probe, policy text, tests), Chained vulnerabilities and trust boundaries (the removed brief reading), Obvious things.
- **SUPPLY-CHAIN-AND-RELEASE.md:** Generated-source and codegen provenance gaps (the deployed copy and its pin), with Core discipline, Universal moves and Validation rules.
- **Excluded:** AI, local IPC, cloud and web companions; no such boundary is in the changed paths.
