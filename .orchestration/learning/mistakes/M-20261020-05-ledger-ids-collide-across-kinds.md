---
id: M-20261020-05
date: 2026-10-20
classes: [records-form, gate-bypass]
severity: P1
---

# The JSON-ledger id mapping collapsed rows of different kinds, so the gate's S1 undercounted

**What happened.** D-024-42 (09:31Z) mapped every prose finding row `<kind>:<sha7>:<n>` to the gate id `audit:<sha7>:<n>` so the gate grammar accepts it. Rows of different kinds on one head share the id: in the a06-checker record `ci:b8bf806:1`, `worker:b8bf806:1` and `security:b8bf806:1` became one entry, and the sync reported `ledger +0` for the security row (10:02Z). The JSON ledger therefore held 61 entries for 64 prose rows, and the classes `evidence-integrity` and `approval-binding` were under-counted; worker-write-boundary-a02 has three such collisions. The gate's S1 rule (three rows of one class need a re-plan) reads the JSON ledger only, so a class could reach three rows in prose and pass the gate.

**What the rules say.** Plan 020 step 4 and C-59: every finding row counts toward its class; the gate is the single authority on the record's rows (pr-integration rule); D-024-42 kept the provenance prefix in prose for that reason.

**Why the rules did not fire.** The mapping was designed for the gate's grammar, not for injectivity; the sync prints the number of added rows but did not compare it with the number of prose rows, and the orchestrator read `+0` as "already present".

**Mechanism.** (1) `record-json-sync.py` maps injectively with a per-kind offset and accepts digit-bearing class slugs; `--rebuild` drops the old `audit:` ids and re-adds every prose row, and the sync line now shows the count to compare with the prose rows (C-114). (2) The proper fix is a provenance slot in the gate grammar and in `acceptance-front-matter.py`, written as a task. (3) The re-plan check after every sync prints the classes at three or more rows without a `replans` entry; it found `lint-detection-gap` x9 without a re-plan in the #432 record while that chain was running, and the line was added before the record step (11:04Z).
