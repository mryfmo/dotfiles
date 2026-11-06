# Architecture: dotfiles at 1a4d712f (scoped to unit U249, round 2)

## Product, principals and resources

A personal dotfiles repository whose `scripts/orchestrator/` holds the orchestration levers of the regime-cutover program.

`brief-check.py` is the orchestrator seat's brief gate. The coordinator runs it on a written brief before sending the brief's TASK line. It reads one brief and its own manifest and writes nothing. Exit codes: 0 passes, 1 refuses with reason lines, 2 means it cannot read the brief, the brief is not in the grammar, or the lever self-check failed.

**Deployment.** The generator writes byte-identical copies to `home/dot_local/bin/common/executable_brief-check.py`, which chezmoi installs as `~/.local/bin/common/brief-check.py`. Its sha256 is pinned under `claude.levers.sha256` in `home/dot_agents/agent-config.yaml`, and the script refuses to run unless its own digest equals that pin (`brief-check.py:79-121`).

**Principals.** The coordinator writes briefs and runs the checker. Workers receive briefs, but cannot write them: the store belongs to the coordinator. No lower-trust principal supplies brief text. The protected resource is the integrity of the gate decision, which decides whether a TASK is sent.

## The change under hunt (main cf68daf6..1a4d712f; round 2 effff558..1a4d712f merges main and rewords one docstring line)

U249 adds a rule. When SCOPE names a repository path, ACCEPTANCE must name a lint gate and a test gate.
- `GATES` (`:248-257`) is a table of (class, name, term) rows; `GATE_CLASSES` (`:258`) are `lint` and `test`. `GATE_WORDS` (`:287`) compiles each class's terms through `word_pattern` (`:267-278`): escaped, whole-word, any case.
- `scope_paths` (`:378-388`) yields backticked, whitespace-free SCOPE spans split at `/`.
- `in_repository` (`:405-411`) counts a span as a repository path when it is relative, is not `~`, `..` or `$VAR`, and names more than a bare word.
- `gates` (`:414-423`) returns one reason per missing class, or "no ACCEPTANCE section" if there is none.
- `judge` applies the rule at `:452-453`.

Supporting changes: the deployed copy, the new pin `7be650074d4b159f9bd7e85a0a6e0515d0b35285b8b2d2dd8fc881f1bbc7af3c` (`agent-config.yaml:894`), `scripts/generated-agent-outputs.json:403`, one README paragraph (`scripts/orchestrator/README.md:118`), and tests (`tests/unit/test_brief_check.py:478-531`).

## Comparable baseline

A lint rule over a document's text, run by the document's own author. The pattern's known limit is that it checks wording, not behaviour. The docstring says so itself (`:35`): whether a gate actually ran is read from the pasted lines by the coordinator.

## Stack and limits

Python 3, standard library only, run under `python -I`. No target code ran, by task rule. The copy and the pin were compared over committed blobs with `git cat-file`, `cmp` and `shasum`.

## Entry surfaces and paths

1. ACCEPTANCE text → `gates` → `GATE_WORDS`. Can a brief satisfy the rule without naming a gate?
2. SCOPE text → `scope_paths` → `in_repository`. Can it switch the rule on or off wrongly, or crash?
3. Malformed brief text → `main` exit codes (`:457-475`). Can it crash the checker into an exit code the levers misread?
4. Deployed copy and pin. Does the self-check compare the bytes that were reviewed?
5. Tests and README.

## Trust boundaries and strongest controls

- **Brief author to gate decision.** Same principal (the coordinator). Controls: compiled, escaped whole-word patterns, and fail-closed exit codes.
- **Repository source to deployed copy.** A byte-identical generated copy, a sha256 pin, and a self-check that refuses with exit 2 on a mismatch.

## Prior coverage

run-4 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-4`, source effff558) is the U249 round-1 sweep, and its five units are re-checked here. Round 2 changes only `brief-check.py:31` (a docstring line) and the pin, so the code line numbers are unchanged. run-7 (source 1d23154b) is the newest ledger and is carried for every other unit. Its six U227b units are absent at this head (changed source), and the rest stay out of scope. No prior run holds a finding.

## Output directory

The brief names `run-4`, which holds the U255 sweep of the round-1 head. This run writes to `run-8` and leaves `run-4` untouched.

## Companion selection

`SUPPLY-CHAIN-AND-RELEASE.md` is selected, for its generated-source provenance block: the deployed copy and the pin. Every other companion is excluded with its reason in the ledger. The checker is a deterministic parser with no IPC, network or model surface.

## Execution and independence limits of this run

The platform's delegation tool (Task) and eval kernel are denied by policy on this seat. Reconnaissance, hunting and both critic passes ran in the parent, and `run-metadata.json` records the run as incomplete for that reason.
