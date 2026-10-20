Two security findings for [PR #409](https://github.com/mryfmo/dotfiles/pull/409), head `4fe243803971bd5ba8ab45f8ede5cfb4dd37f719`.

1. **P1 · High confidence · `scripts/orchestrator/ci-rerun.sh:60` — Caller-controlled interpreter selection can execute PR code with the operator’s authority.**  
   Calling the trusted helper from a PR checkout leaves `uv` in that checkout. A PR-controlled `.python-version` containing `./pwn` can select an attacker-supplied executable before YAML validation; `--no-project`, `--offline`, and Python’s `-I` do not prevent interpreter selection. That executable inherits the operator’s environment and access to credentials. [uv documents this behavior](https://docs.astral.sh/uv/concepts/python-versions/#python-version-files). Reuse the trusted-directory, pinned-interpreter, configuration and environment controls already present in `scripts/orchestrator/dispatch.sh:203`.

2. **P2 · High confidence · `.github/workflows/remote.yaml:78` — Quoted filenames bypass the new bootstrap relevance filter.**  
   A PR adding `home/run_before_probe".sh` produces a Git pathname beginning with `"`, so `^home/` does not match and all public-bootstrap jobs report success without bootstrapping. Git escapes quotes regardless of `core.quotePath=false`. I verified that the production regex rejects this representation while the base predicate runs it. The unit-test relevance predicate also misses it, leaving applied code without either check. Use NUL-delimited paths and add unusual-filename cases. [Git’s quoting rules](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corequotePath).

Assessment of all 19 threat-table rows, numbered in their listed order:

| Rows | Assessment |
|---|---|
| 1–2, 7: workflow decisions and tests | Incomplete: finding 2 contradicts retained coverage for `home/` paths; existing cases omit quoted filenames. |
| 3–4: private workflow and concurrency | Trigger separation, identical decision scripts, and concurrency expressions hold on inspection. |
| 5: production signatures | Specific signature and positive/negative tests are present; YAML uses `safe_load`. |
| 6: rerun controls | Numeric IDs, freshness checks, classification and persistent atomic reservations are implemented; the stated final-check race remains. |
| 8–9: test controls | Fake-GitHub coverage is present; the permissions-test change is exactly the declared addition. Interpreter selection is untested. |
| 10: evidence | Historical failures are disclosed. Credential-pattern and absolute-home-path scans found no matches; final-head CI remains unverified. |
| 11–13: task copy and metadata | Task hash matches the recorded `68425731…`; external dispatch identity is unverified. The predecessor task remains, as acknowledged in the report. |
| 14–15: effects and environment | Finding 1 defeats the claimed interpreter and process-effect controls. |
| 16: new scripts | The script and extracted workflow are declared. |
| 17–19: orchestrator actions | These are procedural commitments outside this diff; this review cannot certify their execution. |

No additional direct shell injection, unsafe YAML deserialization, or run-ID path traversal was identified. Workflow permissions remain read-only and checkout credentials are not persisted.

📝 まとめ: Completed the read-only security review; two findings require orchestrator disposition.

Not checked: live GitHub state (`gh` connectivity failed), full fixture tests or exploit execution; 18 structural/security tests passed, while one fixture test was blocked by read-only temporary-file restrictions.
Verdict: incorrect