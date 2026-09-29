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

## Revision 2 addendum

3. **Check every gate for fail-open inputs.** Any gate that treats a failed
   subprocess as "nothing to check" is fail-open. Verify refs up front and
   separate "absent" (`git ls-tree` empty) from "unreadable" (exit 2). This
   is the second occurrence after T38's `--base`, and it is worth a
   repo-wide sweep of `scripts/*` for `returncode != 0` → benign-default
   patterns.
4. **Explanations must be quantitative.** An explanation such as "the source
   lost definitions" must bound the allowed loss (`new >= min(old, defs)`)
   rather than excuse any decrease once it applies.
