# T44: Restructure explicit-marker extraction in vendored CompactionDB

## Objective

Fix the three defects found in live E2E (only the first marker processed;
tag-form content swallowing everything to end-of-prompt; English prompts
degenerating into one giant heuristic "sentence") with one structural change
to `vendor/compactiondb/.claude/contextdb/contextdb/memory.py`, not spot
regex patches.

## Design (required)

Restructure `extract_candidates` for `user_prompt` events into stages:

1. **Enumerate all markers** with `finditer` over a marker regex that matches
   only the bracket itself: `\[(?:memory|記憶)\s*:\s*([^\]]+)\]` (no trailing
   capture group in the regex).
2. **Content boundary rule**: for each marker, if the bracket interior is a
   bare known-kind token (existing `_KIND_ALIASES` check), it is TAG FORM —
   content = the prompt text from the end of that bracket up to the start of
   the NEXT marker, or end of prompt if none (strip whitespace). Otherwise it
   is BRACKET FORM — content = bracket interior, with the existing
   kind-prefix parsing (`kind: …` / `kind — …`) preserved. Every marker with
   non-empty content yields its own explicit candidate (project scope,
   confidence 1.0), in prompt order.
3. **Heuristic isolation**: before the keyword-heuristic pass, remove every
   explicit-marker span (bracket plus its tag-form trailing content) from the
   prompt; run `_sentences` and `_KEYWORDS` only on the residual text.
4. **Sentence splitting**: extend `_SENTENCE_SPLIT` so ASCII terminators
   split too — split after `.` `!` `?` when followed by whitespace, keeping
   the existing full-width behavior. Over-splitting on abbreviations is
   acceptable for this session-scoped best-effort layer (state that in a
   short comment).

Backward compatibility is part of the spec: all 43 existing tests must pass
unchanged — single tag-form marker with trailing content keeps identical
output.

## Regression tests (required, in vendor tests/)

1. The exact E2E prompt
   `Read README.md and summarize it in one line. Record two memories: [memory:decision] Use SQLite for all local storage. And also [memory: constraint — the E2E2 scratch project must never call external networks].`
   yields exactly two explicit candidates, in order:
   - (decision, project) whose content contains "Use SQLite for all local
     storage" and does NOT contain "[memory" or "external networks";
   - (constraint, project) whose content is exactly
     "the E2E2 scratch project must never call external networks".
     And NO heuristic candidate is produced from this prompt (the only
     "never"/keyword text sits inside marker spans).
2. An English two-sentence prompt where only one sentence contains a
   constraint keyword → the heuristic captures only that sentence, not the
   whole prompt.
3. A prompt with three markers (mixed forms) → three candidates.

## Housekeeping

- Regenerate `vendor/compactiondb/MANIFEST.sha256`; add a
  `2.0.0+dotfiles.2` entry to the vendor CHANGELOG describing the
  marker-extraction restructure.
- Update the marker documentation in the vendor README (the section that
  explains `[memory:...]`) to state both forms and the boundary rule in one
  or two sentences.
- Full vendor pytest green and `python3 validate.py` green (except the
  optional claude-executable check). Record outputs.

## Constraints

- Work in this registered worktree only; branch `fix/compactiondb-markers`
  from current `main`; single commit
  `fix(vendor): restructure marker extraction (all markers, bounded content, isolated heuristics)`.
- No push/PR/merge; no changes outside `vendor/compactiondb/` and the T44
  artifact files; package stays stdlib-only.

## Expected artifacts

- report: `.orchestration/reports/T44-marker-extraction-redesign.md`
- validation: `.orchestration/validation/T44-marker-extraction-redesign.md`
- sandbox: `.orchestration/sandboxes/T44-marker-extraction-redesign.md`
- learning: `.orchestration/learning/T44-marker-extraction-redesign.md`
- autoskill: `.orchestration/autoskill/runs/T44-marker-extraction-redesign.md`

## Done signal

`AGMSG-RESULT v1 task_id=T44-marker-extraction-redesign
status=ready_for_review|blocked` with all artifact paths, sent in the same
turn the work completes. Max turns: 15.
