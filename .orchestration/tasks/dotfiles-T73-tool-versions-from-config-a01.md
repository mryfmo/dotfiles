# AGMSG-TASK dotfiles-T73-tool-versions-from-config-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 3, dotfiles-T73). Dispatched now because its files are disjoint from every in-flight task (T65 stop gate, T66 permgate, T89/T67 herdr-agents). Worker: `claude-standard-dot-a005` in worker-c.

## Objective

Principle 3: a pin is declared once and read everywhere. ccstatusline `2.2.30` and ccusage `20.0.24` are hand-maintained in four places; the awscli GPG fingerprint is hard-coded in a test while the installer already carries it.

1. `.github/workflows/test.yaml` (~216-217 and ~229-230): drop the `@<version>` literals; resolve the tools from the exact config that the job already copies into `${RUNNER_TEMP}/statusline-mise` (`mise -C … install --locked npm:ccstatusline npm:ccusage` and `mise -C … where npm:ccstatusline` / `which`), so the workflow carries no version literal for them.
2. `scripts/check-statusline-tools.py` (`EXPECTED_VERSIONS`, line ~20) and `tests/unit/test_statusline_tools.py` (`EXPECTED_TOOLS` ~23-26, the workflow-literal assertions ~101-111): read the expected versions from `home/dot_mise/config.toml` with `tomllib` (keys `"npm:ccstatusline"`, `"npm:ccusage"`; the script receives the repo path or resolves it relative to its own location, so the CI smoke still works from the checkout). Replace the workflow-literal assertions with an assertion that the workflow contains no `ccstatusline@`/`ccusage@` literal.
3. `tests/unit/test_aws_cli_acquisition.py`: line ~13 hard-codes the fingerprint; read it from `install/ubuntu/common/aws_cli.sh` with a regex, the way line ~15 already reads the version (`AWS_CLI_FINGERPRINT=` or the variable name used there; name it in the report).
4. Nothing else; no pin value changes.

[memory:decision] dotfiles-T73 (operator 2026-10-03): ccstatusline/ccusage versions are read from home/dot_mise/config.toml by the statusline smoke script, its unit test and the CI workflow (no `@version` literals), and the awscli fingerprint test reads the installer; pins have one declaration.

## Repo / branch

- Work ONLY in worker-c. `git fetch origin`; `git switch -c chore/tool-versions-from-config origin/main` (523fda06 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `.github/workflows/test.yaml` (the two statusline install lines and anything they feed)
- `scripts/check-statusline-tools.py`, `tests/unit/test_statusline_tools.py`, `tests/unit/test_aws_cli_acquisition.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T73-tool-versions-from-config-a01.md` (main checkout)

## Forbidden actions

- `home/dot_mise/config.toml`, `mise.lock`, any pin value; other workflows; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rn "2\.2\.30\|20\.0\.24\|FB5DB77F" .github scripts tests; echo "exit=$?"     # expect no matches, exit=1 (adjust the fingerprint prefix to the real one)
uv run python -m unittest tests.unit.test_statusline_tools tests.unit.test_aws_cli_acquisition 2>&1 | tail -3
make unit-test
make validate-agent-assets
gh pr checks <pr-number>       # statusline smoke and canary green
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings and repeat; if the Bot enumerates spellings of a covered class, propose `not-applicable` in the report; close your crit server if Plan Mode opened one; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.
