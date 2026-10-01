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

## Revision 3 triage

1. **A global rule must not call a repo-local script.** Rules under `home/dot_config/**` are
   installed for every repository, so any helper they invoke has to ship through the managed
   PATH (`home/dot_local/bin/common/executable_*`). Candidate check: `validate-agent-assets`
   could flag `scripts/…` paths inside `home/dot_config/*/rules/**` and `home/dot_agents/skills/**`.
   Status: candidate, not promoted.
2. **Evidence for "explained by source" must use the source the new artifact describes.** A
   pre-change base turns every legitimate deletion into a failure. The same trap applies to any
   before/after gate that takes a ref. Status: observation.
3. **`python3 -m py_compile` on a file in `home/**` writes `__pycache__` into the chezmoi
   source tree.** It is git-ignored but can be chezmoi-applied. Prefer
   `python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())' <file>` or
   `PYTHONDONTWRITEBYTECODE=1`. Status: candidate learning, not promoted.

## Revision 4 triage

1. **Absence is not evidence.** A before/after gate that exempts "gone at REF" must first rule
   out a move (rename) using both endpoints, or fail closed without the earlier endpoint. This
   applies to any coverage or regression gate keyed by path. Status: observation.
2. **Managed-agent PATHs must list every managed bin directory explicitly.** Relying on shell
   startup files (`zsh -l`) hides the gap until a runtime switches to `sh -c`. Candidate check:
   `validate-agent-assets` could assert that `shell_environment_policy.set.PATH` includes
   `.local/bin/common` whenever any managed config references a `~/.local/bin/common/…` command.
   Status: candidate, not promoted.
3. The PostToolUse formatter reformats whole files on every Edit in `tests/unit/*.py` that are
   not formatter-clean (seen twice more in this task). Check the diff stat before `git add`.
   Status: reinforces the T47 learning candidate.

## Revision 5 triage

1. **Fix the evidence class, not the grammar.** Each grammar gap (Ruby `private def`, a
   heredoc `def`, a decorator) let an undercount "explain" a loss. Comparing blob ids
   (unchanged source ⇒ no legitimate loss) closes the whole class for the common case of
   graph-only refreshes. Applies to any heuristic count used as an excuse. Status: observation.
2. **One review round per symptom is a signal to look for the shared cause sooner.** r2–r5 each
   closed a fail-open path in the same "explained" branch. A table of every branch that can
   produce `explained` (as listed in the r5 docstring) would have exposed them together.
   Status: candidate learning, not promoted.
