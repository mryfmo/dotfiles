# Learning

[memory:failure] Generated templates must be changed through the manifest and checked with the generator validator (T1 CI revision).
[memory:failure] MISE_CONFIG_DIR alone does not isolate upgrade lifecycle subprocesses that load a live config symlink. Observed and reconciled native-generated spill; lifecycle fix deferred to separate scope.
[memory:decision] Exact-version consumers in tests, smoke script, and CI must move with generated statusline pins. Confirmed by 1/21 failing before consumer update and 25/25 passing afterward.
No automatic rule/skill promotion.
