📝 まとめ: Audited [PR #432](https://github.com/mryfmo/dotfiles/pull/432) at `6434c27c762aecc134f075bd220a34c0d6e20037` without modifying files. The task-copy hash matches, 14 fixture replays pass, and 147 tracked targets parse without stale baseline rows; the following problems remain.

- [P1] high conformance `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/sandbox.md:18` — Records `agmsg-dispatch` running outside the sandbox through `excludedCommands`, directly contradicting the task’s application of design §5.14 item 10 to every worker command.
- [P2] high implementation `scripts/lint-comparisons.py:226` — Acceptance searches raw source lines, including heredoc data: `[[ $path == /x ]] && cat <<EOF` followed by a body containing `realpath` suppresses R1; replacing that body text restores R1. This violates the required heredoc exclusion.
- [P2] high implementation `scripts/lint-comparisons.py:240` — Checking only the first command word drops wrapped tests: `command [ "$path" = "$other" ]` produced R1 at the merge base and produces no finding at this head.
- [P2] high implementation `scripts/lint-comparisons.py:247` — Pipeline detection requires an immediate `CallExpr` producer, so `(ps aux) | grep needle` loses the R5 finding emitted at the merge base.
- [P2] high implementation `scripts/lint-comparisons.py:254` — Removing expansions before classifying options turns `"$name-x"` into `-x`; consequently `pgrep -f "$name-x"` is mistaken for options and loses its existing R5 finding.
- [P2] high implementation `scripts/lint-comparisons.py:262` — The jq locator still searches raw text in every argument: `echo "$(jq -r .name input)" 'select(.url == $p)'` incorrectly emits R3, while the actual command `j"q" 'select(.url == $p)'` is missed.
- [P2] high implementation `scripts/lint-comparisons.py:140` — ANSI-C decoding handles only a few escapes: `jq $'select(.url \x3d\x3d $p)'` receives `==` from Bash but produces no R3 because the scanner decodes it incorrectly.
- [P2] high implementation `scripts/lint-comparisons.py:285` — Identifier presence is mistaken for normaliser application: `def canonical_path: error("unused"); {canonical_path: "/x"} == {canonical_path: $p}` is exempted even though neither operand invokes the function.
- [P2] high implementation `scripts/lint-comparisons.py:310` — Fully escaped concatenations regress: `re.search(f"{re.escape(prefix) + re.escape(name)}", text)` now emits R6 despite containing no unescaped fragment.
- [P2] high evidence `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/validation.md:42` — The recorded CompactionDB invocation uses `uv run --no-project <script>` without `-I` or an explicit interpreter, contradicting sandbox.md:22’s assertion that every Python invocation used both.
- [P2] high orchestration `.orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-pr-feedback.json:178` — Three findings use `fixed:c4aa5ac4…`, but that commit changes only records. The required disposition must identify the commit that actually fixes the root cause.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md:217` — A finding explicitly labelled P3 is dispositioned as “advisory P2” and deferred to a05. The permitted advisory exception applies to P2; changing the disposition label does not change the finding’s priority.
- [P3] high implementation `scripts/lint-comparisons.py:286` — Reasonless jq comments never enter R0 collection: `jq '. # lint-comparisons: allow'` passes silently, while a comparison followed by that comment emits R3 instead of R0.
- [P3] high evidence `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/validation.md:583` — Mutation evidence discards stdout and truncates stderr to four selected lines, contrary to the requirement to preserve validation outputs; M14b retains only an error count, without its diagnostic.

INV-6: holds `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a04/report.md:16` — One documented correction round and one amendment; the predecessor’s exhausted history is preserved.

Orchestration findings: 2

Not rerun: full suites or Bats. Live GitHub verification failed through both `gh` and web access; CI success relies on the supplied final-head JSON.
Verdict: incorrect