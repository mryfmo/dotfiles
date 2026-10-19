# Default-deny Anthropic credential check (a05)

Status: one independent pre-push review and one consolidated fix round complete; first push and final-base validation pending. One post-round P2 remains OPEN (a05-worker-verification-1, Markdown list-contained code fence); no surviving P0/P1 observed in bounded verification. This is a Codex seat; all evidence paths are relative to worker-g, in this task directory. Durable report, validation, sandbox and learning records are committed with PR #412 as explicitly requested by the orchestrator and are updated before RESULT. Timestamped plan/todo worklogs remain uncommitted.

Continue PR #412 against main on tools/anthropic-auth-route-structured. Starting head: 325f520bfc8b4dbb25e0744d27878cdf7eab2fd2. Task copy sha256: 5eb78325f3b09c2cd4a762305c25770f58d94cbc1d081dda6672d85c8ca8d925. Historical premises in the exact task copy are unchanged. The sole predecessor change is deletion of the a04 task copy. PR #396 remains the stacked record; PR #389 is superseded. First push is held until the orchestrator sends PR420's merged SHA, then the branch is rebased onto origin/main.

## Resulting behavior

The shell scanner, recursion, quote provenance and wrapper tables are removed. credential_occurrences searches raw text and retained spelling views, carrying original LF locations and unchanged containing lines. allowed_assignment_line is the sole allowance and uses the task's byte-identical, flag-free whole-line regex. Both credential names accept exactly four environment-reference forms, optional exact export prefix and restricted single-space command suffix. Self-references, literal/empty/template values, quoted or encoded names, wrappers, operators and non-LF separators are refused. Comments beginning with # and Markdown prose naming a credential without = emit notes; fenced and indented code remains hard. The historical test method names remain for lineage continuity; their expectations explicitly follow a05.

Tracked home/ and install/ regular files are inspected without executing them or following symlinks. Raw source precedes parsing/rendering; every retained decoded key/string and both template platforms participate. JSON duplicate entries and YAML aliases/complex keys retain their coverage. Required parser absence, malformed UTF-8, malformed documents/templates and failed Git discovery refuse validation. Diagnostics use fixed reasons, never containing lines or decoded payloads; assignment-bearing ancestor labels are decoded/redacted before escaping diagnostic paths. No applied-file edits, dependency, workflow or SECRET_PATTERN change is used to obtain green.

The explicit residual is unchanged: runtime assembly from pieces no retained decoder joins is undetectable. Credential-free dynamic fragments remain no-occurrence controls; contextual cases retain the recorded binding to a credential name. No shell-completeness claim is made.

## Regression and baseline evidence

The initial table contains 414 rows with exact bytes, source kind, provenance, finding class, exit status and diagnostic assertions; the one review correction adds 11 rows for a final 425 (170 hard, 248 no-occurrence/allowed, seven notes). It retains all 188 inherited table inputs and 92 concrete inputs captured from the two superseded scanner test methods, every seven-wrapper expansion, all named local/security reproductions, parser/key-path cases, no-occurrence controls, note-only cases and 48 honest combinations of name/form/export/suffix. Independent review verified the inherited bytes. Every hard row also exercises decoded JSON-string traversal and an actual tracked JSON input. Literal-value and audit_dummy payloads must never appear in diagnostics. corpus-inventory.json records the counts and source/test SHA256s.

Tests were changed before implementation. Against unchanged 325f520b (source blob afbf5d445bf78e59dc1e35745bd24a2a8bc7032b), the 414-row policy comparison recorded 190 mismatches: 32 newly required refusals, 154 former scanner refusals now credential-free controls, and four newly reported notes. The other 224 classifications were already correct. The unseen typeset -x test was already rejected: its baseline passed and is explicitly not RED. Historical a03/a04 and b139995 red results remain historical and are not relabelled as this task's fresh baseline.

Current local module suite: 122 tests passed, PyYAML present, zero skips. The fixed regex is byte-identical to the dispatched regex; the repository's tracked applied-tree auth run passes. Ruff exits 1 with eight unchanged baseline findings at the original relative filenames; formatting passes. Final-base full validation and exact committed-range measurements are pending.

## Inherited finding dispositions (proposed to orchestrator)

| Finding | Historical fixing commit and a05 disposition |
| --- | --- |
| 4305965376 escaped names; 4305965379 main registration | fixed:d3480fc0eaf94ccf9cf6dab9aa8eabdb72aaba91 historically; spelling corpus and real main-entry fixtures retained. |
| Both-platform template CI failure and surviving case-pattern regression | fixed:d3480fc0eaf94ccf9cf6dab9aa8eabdb72aaba91 historically; darwin/linux render assertions and exact case-pattern inputs retained. |
| 4305863865 strict UTF-8 | fixed:65841e68f3ee119adcb8ab130e698256f9268ed0 historically; strict structured decoding/refusal retained. |
| 4302758230 structured escaped keys; 4302758234 single quotes; 4302758239 JSON delimiter | fixed:7ee711ccae781b44aab3a361ae9a19d894d00653 historically; parsers retained, single-quoted forms and credential mapping keys explicitly refused by a05; an allowed decoded value cannot erase raw refusal. |
| local:b139995:1 single-quoted backslash and nested regressions | fixed:a9056299ba965457b569de2d52aa0cbb7abb6e50 historically; exact bytes retained and refused by shared occurrence search. |
| local:b139995:2 following command/operator | fixed:a9056299ba965457b569de2d52aa0cbb7abb6e50 historically; a05 preserves single-space command acceptance but intentionally refuses semicolon/exec and other operators under the fixed whole-line policy. |
| local:a64daf1:1 ANSI-C names; :2 Markdown prose quote state; :3 non-LF separators; :4 diagnostic payloads | Historically reported fixed:325f520b; a05 keeps exact cases and removes shell quote-state decisions. Fresh final-head confirmation pending. |
| a03 review 577ad0f3 vanishing/option-prefix P1 | Historically reported fixed:325f520b; both named tests and context-bound variants retained; a05 occurrence refusal has no prefix table. Fresh final-head confirmation pending. |
| local:c15be6b9:1 wrapper-looking value; :2 redirection operand; :3 unresolved command; :4 arithmetic | Historically reported fixed:325f520b; exact corpus/control bytes retained. Credential-bearing lines refuse; fragments without a detectable spelling are explicit controls, not evaluation. Fresh final-head confirmation pending. |
| local:325f520:1 empty/subscript; :2 builtin -- | Owned by a05, retained as hard rows; final fixing commit pending. |
| local:325f520:3 raw structured comments | Owned by a05: raw inspection now reports comments as notes with exit 0 when no hard finding; TOML/YAML cases retained. Final fixing commit pending. |
| local:325f520:4 heredoc reference | Owned by a05: no heredoc semantics; the unchanged body line accepts exactly when it matches the fixed regex. Final fixing commit pending. |
| local:325f520:5 Markdown line offset | Owned by a05: original example line 4 is asserted without chunk-relative offsets. Final fixing commit pending. |
| security:325f520 unmatched nullglob; builtin -- declaration wrapper | Owned by a05: exact multi-line bytes retained, hard findings without executing shell or expanding glob/options. Final fixing commit pending. |

## Review and delivery

The single independent read-only review assessed clean a99521b446de5796393ce4f9654136fda4f6e95d on merge base 3e41e36abc949acd7e6b4859c1a22df9e665c8d4. Crit status had no existing review data/live session; crit comments --all --json failed because that review file does not exist. AGENTS' independent-agent fallback applies. a05-worker-review.json records the two findings and their addressed status; a05-worker-receipt.md is the receipt. Root read that JSON before AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review, which exited 0.

One consolidated correction, e37be90d9aef1c2371529cf02b7266e1645f597e, addressed a05-worker-review-1 (P1: preserve punctuation-stripped raw/intermediate spellings before destructive ANSI-C decoding) and a05-worker-review-2 (P2: valid closing-fence suffix and quote-container depth). Before source edits the four exact reproductions failed in the corpus; afterwards the 425-row corpus plus unseen shape passed, and all 122 module tests passed with PyYAML/no skips. Both review records propose fixed:e37be90d9aef1c2371529cf02b7266e1645f597e. No second independent review or second correction was performed. The closing-fence rule was checked against the primary CommonMark specification: https://spec.commonmark.org/0.31.2/#fenced-code-blocks.

Post-round bounded verification found a05-worker-verification-1, P2/high confidence, scripts/validate-agent-assets.py:1721: list-item markers preceding a fence are not recognized, so a bare credential name inside that code block is treated as note-only prose. The exact fixture and diagnostic are in post-round-open.json. This remains OPEN, not fixed or silently resolved. It was reported to the orchestrator; a proposed advisory a06 ownership disposition requires the orchestrator to write that task first. No owner disposition is claimed here. No surviving P0/P1 was observed. Further source correction is stopped under the one-round limit; final acceptance belongs to the orchestrator.

No manual Bot request, PR edit, PR comment, thread resolution or merge is performed by this worker. After the authorized first push, CI and the automatic-review window will be recorded on that head. Final feedback, task-level audit, separate security-profile review, acceptance and integration belong to the orchestrator.

