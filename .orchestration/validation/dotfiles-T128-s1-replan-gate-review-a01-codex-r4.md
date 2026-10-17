[P1] high .orchestration/tasks/dotfiles-T128-s1-replan-gate-a01.md:73 The existing `test_s6_searches_entry_must_equal_the_recomputed_records_search` expects success for three-row `scope` and `absent` ledgers (tests/unit/test_require_crit_review.py:1349), but `write_record` supplies no re-plan line (:420), so the new refusal breaks both cases despite the shared-fixture update; permit adding valid re-plan lines while retaining their S6 assertions.

📝 まとめ: Hash matched; premises replayed `2/2/0`; checker returned `OK`; mask found zero matches; template checks passed.

Implementation tests and CI were not run; this was a read-only specification review.
Task-file verdict: dotfiles-T128-s1-replan-gate-a01: revise