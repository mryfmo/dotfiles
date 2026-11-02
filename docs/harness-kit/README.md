# docs/harness-kit

The design documents of the TechnoPro Harness Agent Kit (THAK): the plan to run this repository as a reproducible harness kit for Claude Code, Codex, the omp seats and, optionally, a DeepSeek Harness seat, by integrating or deliberately not integrating eight open-source repositories.

## What the directory holds

| Path            | Content                                                                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `PRD.md`        | The product requirements: problem, personas, goals, capabilities, the requirement table (`R-01` onwards), rollout, open questions.            |
| `adr/`          | One architecture decision record per one-way door, `ADR-001` to `ADR-007`. `ADR-003` was written last, after the eighth research note landed. |
| `bdd/`          | One Gherkin feature per capability. Each scenario carries a requirement tag (`@R-nn`) and `@holds-today` or `@target`.                        |
| `research/`     | The research notes, one per candidate repository, with sources. The input the ADRs cite.                                                      |
| `decisions.tsv` | The coordinator's decision trail, appended as the program ran. Append-only; never rewrite a row.                                              |
| `check.py`      | The consistency check over the files above, and the runner for the scenarios that hold today.                                                 |

## How to read it

Start with `PRD.md` for the shape and the requirement table. Each requirement names its source ADR and the scenario tag that verifies it. Read an ADR for the facts behind a decision, the alternatives it rejected and the units it creates; every factual claim about an upstream project cites a research file and section, and every claim about this repository cites a path. Read a feature file for the observable behaviour a requirement asks for. A scenario tagged `@holds-today` is true of the repository now and is proved by a command in `check.py`; one tagged `@target` is a goal for a later unit.

## Running the check

From the repository root:

```bash
python3 -I docs/harness-kit/check.py
python3 -I docs/harness-kit/check.py --holds-today
```

The first form checks that every research note starts with `# <owner>/<repo>` and has a sources heading, that every ADR the PRD names exists with its title, status and date lines and its five sections, that every requirement in the PRD table has a scenario and every scenario tag has a requirement, that every scenario carries exactly one of `@holds-today` and `@target`, that `decisions.tsv` has the six-column header and six cells per row, and that the `@holds-today` scenarios and the `HOLDS_TODAY` table of the script name the same titles. The second form also runs each `HOLDS_TODAY` command from the repository root and prints pass or fail per scenario. Both exit 1 on any failure. The script uses the standard library only.

CI formats Markdown with prettier and Python with ruff:

```bash
mise x npm:prettier -- prettier --check docs/harness-kit
scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check
```

## Adding an ADR

1. Take the next number: `adr/ADR-008-<slug>.md`.
2. Use the same shape: a title line `# ADR-008: <title>`, a `Status: proposed` or `Status: accepted` line, a `Date: YYYY-MM-DD` line, then the sections `## Context`, `## Decision`, `## Alternatives considered`, `## Consequences` and `## Verification`.
3. Add its requirements to the PRD table and tag at least one scenario per requirement in a feature file. A `@holds-today` scenario needs a `HOLDS_TODAY` row in `check.py` with the command that proves it.
4. Run `check.py` in both modes, then prettier and ruff.

## The decision trail

`decisions.tsv` is written by the coordinator through the records logger, one row per decision, with the columns `ts`, `phase`, `decision`, `why`, `evidence` and `result`. The seven `design` rows are the ADR decisions in their original wording. Rows are appended, never edited; a reversed decision gets a new row that names the one it reverses.
