# T27 learning triage

## Candidate

herdr exposes no "registration gone" wait state and a stale registration
reports `idle`, so `herdr agent wait --until idle` cannot detect a released
name. The only release check is polling `herdr agent list` until
`.result.agents[].name` no longer contains the name. When testing such a
bounded poll, expose the poll count and interval as env seams (production
defaults untouched) so the never-clears case runs in milliseconds, and assert
the poll count from the fake's call log — a mutation baseline where the
"gives up" test fails only on the poll-count assertion proves the assertion
is load-bearing.

## Disposition

Candidate only. Do not promote automatically. The herdr API facts are already
recorded in the T27 task file and the herdr-worker-relaunch rule candidate
(Addendum 5, now marked resolved).
