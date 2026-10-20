**P2 · High confidence · `.orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md:39`** — The workflow/environment threat control claims no workflows are allowed, but three workflows are explicitly allowed and changed; this residual control therefore does not address the actual boundary where PR-controlled paths determine required CI execution. Replace it with controls covering filename handling, runner-owned environment inputs, failure behavior, and credential isolation.

For [PR #421](https://github.com/mryfmo/dotfiles/pull/421), the remaining assessment is:

- File-scope controls hold: changes match the two owned fixes; both bootstrap scripts remain identical; no scripts were added or renamed.
- No new injection, authorization bypass, secret exposure, unsafe deserialization, or path-traversal vulnerability was identified. Filenames remain data, the temporary destination is quoted and runner-owned, and private-secret triggers remain unchanged.
- The in-process row describes fake-`gh` testing but omits the changed tests’ execution of workflow scripts; update it alongside the finding.
- Task/evidence controls are only partly verifiable: the task hash matches the report, and the consistency checker uses `yaml.safe_load`; dispatch provenance and acceptance-time comparisons remain the orchestrator’s responsibility.
- Merge, update-branch, and removal controls describe future orchestrator actions; this diff does not implement or demonstrate them.

Ten read-only structural tests passed. Direct filename probes confirmed matching for the targeted unusual `home/` filenames. Existing unit-test quoting and grep-error weaknesses are disclosed in the report and predate this changeset.

📝 まとめ: 指定された差分のセキュリティレビューを完了し、脅威表の不成立な制御を P2 として報告しました。受け入れ判断は orchestrator に委ねます。
Not checked: full write-dependent tests or live CI (`gh` API connection failed); recorded validation was not treated as independently verified.
Verdict: incorrect