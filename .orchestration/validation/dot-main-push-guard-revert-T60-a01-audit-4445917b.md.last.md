- [P2] high home/dot_local/bin/common/executable_herdr-agents:1573 A shared/global `core.hooksPath` lets cleanup delete a matching hook outside this repository’s common Git directory, although the old installer explicitly refused such locations; reproduced with deletion intercepted. Restore that boundary.
- [P2] high home/dot_local/bin/common/executable_herdr-agents:1575 `hash-object` applies clean filters, so customized hooks can match the retired stub and be deleted; a hook containing an added local check reproduced this. Use `--no-filters` for raw content comparison. [Git documentation](https://git-scm.com/docs/git-hash-object)

[CI for PR #231](https://github.com/mryfmo/dotfiles/actions/runs/37082340714) confirms both changed tests passed; 709 Python tests passed with one skipped. Available RESULT evidence targets a later commit, so its claims were not attributed to this changeset.

📝 まとめ: Audited only `4445917b9a`; found two hook deletion defects. No files changed.
Verdict: incorrect