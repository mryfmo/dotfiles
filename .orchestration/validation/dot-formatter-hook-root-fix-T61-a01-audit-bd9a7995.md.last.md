No findings in `bd9a7995`. `.github/workflows/test.yaml:290` and `Makefile:158` consistently select the root configuration, matching [Ruff’s documented behavior](https://docs.astral.sh/ruff/configuration/). Read-only probes with pinned Ruff confirmed vendor exclusion while unformatted owned Python still fails. No introduced security, regression, or rule-compliance issue was found.

Exact-SHA CI remains unverified: GitHub access failed, and saved success logs concern later commits.

📝 まとめ: 指定 commit の監査を完了し、指摘はありません。対象 SHA の CI は未確認です。

Verdict: correct