# Learning
- Candidate (not promoted): for push timelines, use `gh api repos/<owner>/<repo>/activity?ref=refs/heads/<branch>` (lists every ref update with before/after and push vs pr_merge). The events API dropped 6 of 22 main updates in this range (f78666a, d6cfed2, 3a8c7d3, 127e27b, d906b00, 3303fbc).
- Candidate (not promoted): locally created merge commits for dependabot PRs make one push carry several commits; count commits per ref update (22 updates -> 27 commits here) instead of assuming one push per commit.
- Observation: `git log --all --find-object=<blob>` quickly shows whether a Web-UI-uploaded binary duplicates a blob already on another branch (PRD_ADR_BDD.zip / TestSuite.zip = d3281de on W1/W2) or is unique history bloat (jev-all-engines.zip, 17,606,234 bytes).
No rule or skill promotion.
