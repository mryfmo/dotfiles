Two threat-table findings in [PR #425](https://github.com/mryfmo/dotfiles/pull/425), reviewed at `380e7f4` against `205fe85c`:

- **P2 · High confidence · `.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md:33`** — The workflow-input control claims no workflow is allowed to change, but line 8 permits `regime.yml` and this diff changes its executable-code selection; replace that false exclusion with the actual target-branch trust assumptions and checkout protections.
- **P3 · High confidence · `.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md:31`** — The claimed fake-PATH isolation does not exist: `test_regime_ci.py` invokes real Git and uv with inherited environment variables; document the actual temporary-repository isolation and remaining tool/environment effects.

I found no new exploitable injection, authorization, secret-handling, unsafe-deserialization, or path-traversal regression in the runtime diff. `github.base_ref` identifies the PR’s target branch, and this value enters an action input rather than shell source. The fetched head remains data; execution uses the checked-out base with Python isolation, disabled uv configuration, read-only repository permissions, and no persisted checkout credentials. [GitHub context reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context)

The remaining threat rows have corresponding path coverage or procedural controls. Dispatch authenticity, evidence provenance, and merge/update/removal enforcement cannot be authenticated from branch records alone.

Validation: nine workflow-security tests passed; both changed test modules parsed successfully; the verifier is unchanged.

📝 まとめ: 指定差分のセキュリティレビューを完了し、threat_table の不正確な制御記述を2件指摘しました。受け入れ判断は orchestrator に委ねます。

Not checked: repository-writing integration tests or live CI (`gh` API access failed); those results remain unverified.
Verdict: incorrect