# 操作者 handout: main の ruleset に「pull request 必須」を足す(第 48 条の人間部分、一回)

## 何が測定されたか

試験表 `tests/autonomous-change-flow.tsv` の行 f23(U288、2026-11-06T13:4xZ、実測)。`gh ruleset view 24397953 --repo mryfmo/dotfiles` は rules に `deletion`、`non_fast_forward`、`required_status_checks`(public-bootstrap ×3、regime、test ×3、validate)を返し、`pull_request` rule が無い。GitHub の仕様では、required status checks は push にも適用されるが、「Require a pull request before merging」が無いと main への直接 push 自体は(checks を満たせば)許される。ゴール文の「人手なしに受付から merge まで流れる」は、変更が必ず PR を通ることを前提にしている。

## agent がやった部分

- 測定と、この handout。
- 必要な rule の形: `pull_request` rule、`required_approving_review_count: 0`(coordinator が `gh pr merge --squash` で merge する経路を塞がないため。承認者を要求すると、専用アカウント(M-25)ができるまで merge が止まる)、`dismiss_stale_reviews_on_push: false`、`require_code_owner_review: false`、`require_last_push_approval: false`、`required_review_thread_resolution: false`(thread の disposition は `pr-threads-check.sh` が判定する)。
- 既存の rules は一つも変えない。

## 人間が一回やること

GitHub の repository settings(Rules → Rulesets → 対象の ruleset、id 24397953)を開き、Branch rules に「Require a pull request before merging」を追加し、Required approvals を 0 にして保存する。

CLI で行う場合(`gh` の認証が admin 権限のとき):

```
gh api --method GET repos/mryfmo/dotfiles/rulesets/24397953 > /tmp/ruleset-24397953.json
```

出力の `rules` 配列に次の要素を追加した JSON を作り、`PUT` で送る(他の rule はそのまま):

```
{"type":"pull_request","parameters":{"required_approving_review_count":0,"dismiss_stale_reviews_on_push":false,"require_code_owner_review":false,"require_last_push_approval":false,"required_review_thread_resolution":false}}
```

## agent が実行後に走らせる検証

```
gh ruleset view 24397953 --repo mryfmo/dotfiles
```

期待: rules に `pull_request` が含まれる。その後、coordinator が `tests/run-host-rows.py` を再実行し、f23 行が OK になることを記録する。既存の coordinator の merge(`pr-merge.sh`)が引き続き通ることは、次の PR の merge で確認する。

## 代わりに操作者が言えること

- 「承認 1 件を必須にしてよい」: その場合、専用アカウント(M-25)が承認者になるまで coordinator の merge が止まるので、M-25 と同時に入れる。
- 「ruleset は今のままでよい」: f23 行を operator 判断の残差として表に残す。
