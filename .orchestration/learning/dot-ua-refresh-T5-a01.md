# Learning
[memory:failure] meta.json can disagree with graph.project.gitCommitHash and fingerprints.json. The 2.9.7 incremental guard correctly rejects the mismatch before writing a plan, preserving the baseline. Report the three hashes rather than hand-editing metadata or guessing a replacement base. No rule promotion.

## Authorized baseline retry
Using the agreed graph/fingerprint commit permits preparation, but the authoritative structural-change threshold selects FULL_UPDATE. Do not override that action or manually advance metadata.
