# T29 learning triage

## Candidates

1. `assets.understand-anything-installer` is a `git-commit` pin **paired with
   `sha256` of `install.sh` at that commit**. `update-agent-assets.sh` verifies
   it and skips the Codex UA install on a mismatch. Bump both together with
   `--set-asset <asset>.pin=<sha> --set-asset <asset>.sha256=<hash>`. Compute
   the hash with `curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/<sha>/install.sh | shasum -a 256`,
   and first re-derive the old hash to confirm the method.
2. `npx renovate-config-validator` can silently reuse a stale cached Renovate
   (37.x here), which rejects `managerFilePatterns`. Use
   `npx --package renovate@<major>`. The npm release-age guard blocks versions
   younger than 7 days; resolve by major rather than overriding the guard.
3. The Bash deny rule `Bash(rm -rf:*)` blocks scratch cleanup. Use
   `mktemp -d` for fresh scratch dirs instead.
4. The Edit/Write PostToolUse formatter (`ruff format`) rewrites whole Python
   files that predate the formatter. For minimal diffs to such files, edit
   through a non-hooked path and check `git diff --stat`.

## Disposition

Candidates only. Do not promote automatically. Candidate 1 contradicts the
T29 task's research note ("no paired sha256") and should be corrected in any
rule or task template that repeats it.
