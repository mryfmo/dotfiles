## Summary

Plan 024 P1-4a (`dotfiles-T133-verdict-audit-pool-a01`): the orchestrator's acceptance of a PR becomes one script's nine conditions with a JSON verdict, and audits run from a queue two at a time with structured JSON findings whose classes come from one controlled vocabulary.

- `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]`: reads gh, the acceptance record, the audit JSON, a fresh `pr-feedback.py` sweep against the dispositions, the task file's front matter and Check caps, the counters, the merge-base diff and the security review; writes `<task>-verdict-<sha7>.json` (checked against `.schemas/verdict.json`); exits 0 accept, 10 revise (with the revise line), 20 hold. `--apply` acts on accept only (dispatch.sh, then `gh pr merge --squash --match-head-commit`); `--admin` and `--auto` are refused before anything runs; `--shadow` writes the machine column of `verdict-shadow.tsv`.
- `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2]`: an fcntl-locked queue under the validation directory, one review worktree per slot, schema-valid audit JSON kept and everything else blocked with a `.rejected` reason, 429 retried after 60, 120 and 240 seconds, differential mode off until two shadow rows agree.
- `scripts/orchestrator/orch-audit.sh`: `--head <sha40>`, `--json <out>` (one fenced json block before the Verdict line, extracted and checked by a stdlib checker), `--previous-head`/`--previous-findings`, `ORCH_REVIEW_WORKTREE`, `--validate <schema> <json>`; every existing refusal and the masking kept.
- `.schemas/audit.json`, `.schemas/verdict.json` (JSON Schema 2020-12) and `.schemas/classes.yaml` (137 classes, each with remedy and blast_radius; the audit class enum is generated from it).

## Evidence

`.orchestration/dotfiles-T133-verdict-audit-pool-a01/` holds the task copy (Amendment 1), the report, the validation output, the sandbox record and the learning triage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
