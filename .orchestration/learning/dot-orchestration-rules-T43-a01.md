# T43 learning triage

## Candidates

1. **Re-derive a new gate against the incident it codifies.** When a gate
   script codifies a past failure, run it against that failure's artifact
   (here: c3afc7a vs 72b8901, 8 regressions, exit 1) as well as a clean
   self-compare. This proves the gate catches the real case, not only the
   synthetic one.
2. **Def-like line counts are a cheap proxy.** They explain decreases
   without a parser: a file whose source still has at least the old symbol
   count cannot legitimately lose nodes. This avoids the plugin's
   shell-parser gap that blocked T41's incremental path.

## Promotion

None. These are candidates only.
