---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a07
kind: code
security: true
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/**
  - Makefile
after: [dotfiles-T133-worker-write-boundary-a01]
reset_of: [dotfiles-T129-anthropic-auth-route-check-followup-a05]
threat_table:
  - control: "scripts/validate-agent-assets.py (applied-file classification, structured-template substitution, decoded occurrence inspection, Markdown fence classification and diagnostic redaction)"
    disposition: "residual: the fixed whole-line regex remains the entire acceptance predicate; structured-template decoding closes the recorded parser gap, but runtime-assembled names that no retained decoder joins remain undetectable"
  - control: "tests/unit/test_validate_agent_assets.py (the inherited corpus, parser and entry-point fixtures, intermediate-view redaction and three new regression tests)"
    disposition: "residual: temporary tracked repositories exercise the real discovery path; fixture coverage does not establish shell-language completeness, and the final-head audit compares the review reproductions with the actual fixture bytes and assertions"
  - control: "scripts/lint-comparisons-baseline.tsv (the inherited amendment-1 comparison-lint repair)"
    disposition: "residual: preserve the row for the moved comparison at the starting head's line 1626; any necessary maintenance is limited to this PR's changed lines, and tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline rejects unbaselined hits and stale rows"
  - control: "Makefile (unit-test provisioning through the existing UV_PYYAML cache-first probe)"
    disposition: "residual: the existing PyYAML dependency is supplied deterministically to unit-test; unavailable cache and failed dependency resolution remain command failures, never permission to skip YAML validation"
  - control: ".orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts are data, stay in this task's directory and distinguish inherited observations from final-head commands, revisions, outputs and exit statuses"
  - control: "the task-file copy .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md"
    disposition: "residual: the orchestrator compares the complete a07 copy byte-for-byte with the dispatched text and binds its own sha256 to TASK and RESULT"
  - control: "the reset_of copy .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md"
    disposition: "residual: the first push deletes only the a05 task copy as the sole reset-bookkeeping exception; all other predecessor evidence remains intact"
  - control: "the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/"
    disposition: "residual: report, validation, sandbox, learning, autoskill, measurement and worker-review records preserve provenance and disclose no credential payload; committed predecessor evidence remains historical and is not rewritten"
  - control: "applied-file inputs under home/ and install/"
    disposition: "residual: raw source is inspected before any transformation, structured kinds are decoded without executing their contents, and an allowed later view never erases an earlier finding; unsupported runtime assembly remains outside detection"
  - control: "task metadata"
    disposition: "residual: the orchestrator checks the dispatched front matter and its allowed-file boundary before dispatch and at acceptance; whole-file byte comparison detects changes to metadata or body"
  - control: "metadata separators"
    disposition: "residual: the first YAML document supplies front matter and the orchestrator's whole-file comparison covers both separators and all remaining bytes"
  - control: "in-process effects"
    disposition: "residual: fixed regex matching, stateless spelling transformations and data parsers inspect bytes without shell evaluation or applied-script execution; temporary fixtures do not modify the live home directory"
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: only the declared Makefile unit-test invocation changes, using the existing cache-first PyYAML probe; workflows, interpreter selection, credentials and global environments are unchanged, and missing required parsing still refuses validation"
  - control: "new or renamed scripts"
    disposition: "residual: none are authorized; the final inventory and audit reject new or renamed executables or an undeclared helper script"
  - control: "orchestrator effect merge"
    disposition: "residual: the orchestrator alone integrates PR 412 through the final-head feedback sweep, task-level audit, separate security review, acceptance and gate before gh pr merge --squash --match-head-commit"
  - control: "orchestrator effect update-branch"
    disposition: "residual: an update moves the head, so the orchestrator refreshes CI, feedback, local review, task-level audit and security evidence before the integration gate"
  - control: "orchestrator effect forced worker removal"
    disposition: "residual: ordinary removal refuses a dirty worktree; a forced removal is an orchestrator decision recorded with the exact uncommitted state it discards"
  - control: "design 5.14 item 1 — write boundary"
    disposition: "residual: a012 uses the Codex sandbox, whose configured writable roots bound all tool writes; record those roots in sandbox.md and keep repository writes within allowed_files and the sole reset exception; no Claude seat is used, and this does not isolate other same-UID processes"
  - control: "design 5.14 item 2 — sanitized inputs"
    disposition: "residual: item 1 removes every inherited GIT_* variable for every remaining Git root-confirmation command, supplies the fixed environment and configuration overrides, and binds Git directories to the verified repository root; filesystem discovery includes ignored and untracked regular files and refuses failed, empty or home-less walks; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_sanitizes_git_root_probes_and_walks_regular_files exercises these controls; executable identity and the rest of the startup environment are not authenticated and are not claimed closed"
  - control: "design 5.14 item 3 — trusted-path checks of the validator's own inputs"
    disposition: "residual: item 1 requires a real .git directory, canonical agreement of the expected root and sanitized Git root and directory probes, an unset core.worktree and regular in-root trusted inputs, with case-aware identity and containment comparisons on a case-insensitive filesystem; it enumerates every regular input by walking fixed home/ and install/ roots without following symlinks, reports skipped symlinks and gives Git no listing or exclusion authority; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_verifies_its_root_and_regular_input_paths exercises the root and trusted-input checks; this worker-checkout input validation does not establish the orchestrator's trusted-root exclusion or eliminate same-UID replacement races"
  - control: "design 5.14 item 4 — execute what was verified"
    disposition: "residual: the validator reports on the snapshot it read and does not bind consumption (chezmoi apply) to that snapshot; no test is claimed to close this item"
  - control: "design 5.14 item 5 — output and lock identity"
    disposition: "residual: the validator holds no lock and writes no artifact; its outputs are stdout, stderr and the exit status, so no artifact-name or lock-identity control is implemented or claimed closed"
  - control: "design 5.14 item 6 — honest residuals"
    disposition: "residual: unclosed risks are explicitly stated as residuals; parser coverage, canonical path checks and sandbox restrictions do not establish executable identity, bind later consumption or isolate hostile same-UID processes"
  - control: "design 5.14 item 7 — verification"
    disposition: "residual: this table has one separate row for each item 1 to 10; item 1 adds local Git-environment and trusted-input tests; the shared test helper belongs to P1-6 and does not exist yet, and this task neither creates it nor claims the four shared red-to-green checks, PATH-shim exclusion or consumption binding"
  - control: "design 5.14 item 8 — committed ledger"
    disposition: "residual: committed-ledger acquisition is not applicable to this validator because it reads no ledger and makes no permission or approval decision; no local ledger is treated as approval"
  - control: "design 5.14 item 9 — private caches"
    disposition: "residual: uv run --with pyyaml resolves PyYAML from the worker's cache; the worker's UV_CACHE_DIR binding belongs to P1-15 and may be absent at implementation time, so dependency provisioning does not establish private-cache isolation"
  - control: "design 5.14 item 10 — sandbox enforcement"
    disposition: "residual: every worker command runs inside the Codex sandbox; anything that cannot complete there requires AGMSG-PONG v1 status=blocked with the exact command, exit status and boundary, followed by waiting for re-tasking; no sandbox escape or alternate execution route is authorized"
premises: []
---

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-followup-a07 — structured-template decoding and list-fence classification reset (plan 024 D; INV-6; PR #412)

This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a05 acceptance record’s last decision resets the lineage after the security review of `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab` found P1 `security:2b6fc7f:1` (`template-classification-gap`) and P2 `security:2b6fc7f:2` (`markdown-fence-note`). The review is `.orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a05-security-2b6fc7f.md.last.md`. The worker’s pre-push fix round plus revise 1 reached the C-61 cap; this is an INV-6 reset, not a third a05 correction round. The amendment-1 rebase repair remains a rebase repair under D-024-24.

Worker: **a012, Codex, worktree `.claude/worktrees/worker-g`**. Continue branch `tools/anthropic-auth-route-structured` from `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab`, using the existing main-target PR **#412**. Preserve the a05 implementation, its revise-1 redaction fix, its rebase repair and all committed evidence. The first push deletes `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md` and adds the byte-identical dispatched a07 text at `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md`. Deleting that a05 task copy is the sole reset-bookkeeping exception to `allowed_files`; no other predecessor artifact or canonical task text is changed.

PR #396 stays open as the stacked record until #412 merges. PR #389 is superseded and supplies no merge precondition. This reset creates neither a fresh branch nor another implementation PR. The dispatch supplies the deadline.

Section **5.14 of `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`** is context only: **uncommitted; the quoted sentences are normative** (C-86; C18). The execution-contract sentences relied on here are copied verbatim below so that the reviewed task bytes carry the contract; later edits to that local path do not change this task.

Design 5.14 item 2: “最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。” “git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。” “`-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。”

Design 5.14 item 3: “仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.”

Design 5.14 item 4: “検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。”

The threat rows give one disposition per item 1 to 10 and distinguish this validator's implemented controls from the quoted contract's residual requirements. This read-only validator performs no fetch, so its Git invocation retains `protocol.allow=never` without an HTTPS exception. Its own verified worker-checkout inputs are not orchestrator trusted roots. Full startup-environment and executable authentication, the orchestrator's worker-root exclusion and binding later chezmoi consumption remain residual; local checks do not establish isolation between hostile processes sharing a UID.

The a06 row `a05-worker-verification-1` moves into item 10 of this task. It is the same list-container fence reproduction as `security:2b6fc7f:2`, not an additional deferred finding. **The a06 owner keeps nothing of that row.** The orchestrator records the transfer in the acceptance records; the worker does not edit the a06 text or those records.

## Goal

The Anthropic credential check defaults to denial without understanding shell. Every credential-name occurrence in raw applied text and each retained decoded view is a finding unless its unchanged containing line matches the fixed allowlist of four environment-reference assignments. A comment beginning with `#` and Markdown prose naming a variable without `=` produce reported `note` findings with exit 0 when no hard finding exists; code fences, including list-container fences, receive no prose exception. `docs/` remains outside applied-file discovery.

Structured templates are structured inputs: `.toml.tmpl`, `.yaml.tmpl`, `.yml.tmpl` and `.json.tmpl` are parsed as their corresponding structured kinds after inert directive substitution. An input that still cannot be decoded is refused. Diagnostics disclose no assignment payload, including payloads in intermediate decoded key views.

## Files and items

1. `scripts/validate-agent-assets.py` retains `validate_anthropic_auth_route()` in the real `main()` beside `validate_no_obvious_secrets()`. Discovery walks the filesystem under the fixed `home/` and `install/` roots; Git is consulted only to confirm the repository root and metadata, never to enumerate files or authorize exclusions. Run every remaining Git command with a sanitized environment: remove every inherited `GIT_*` variable, then set `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and pass `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never`. Derive the expected repository root from the validator's location, not inherited Git state; use explicit `--git-dir=<root>/.git` and `--work-tree=<root>` arguments with explicit `-C` for every Git command. Verify that sanitized `git rev-parse --show-toplevel` canonically identifies that expected root before walking or reading inputs; a mismatch is exit 2 with `ERROR: anthropic auth-route discovery refused: repository root mismatch`. No Git command relies on `-C` alone.

   Authenticate Git metadata before walking or reading inputs. Before any Git command, `<root>/.git` must be a real directory checked without following a symlink: a symlink, a gitfile pointer, a missing path or any other file type refuses. With the sanitized environment and explicit bindings above, resolve both `git rev-parse --git-common-dir` and `git rev-parse --git-dir` through realpath, resolving relative output against the explicit `-C` root; both must equal the canonical `<root>/.git`. Run `git config --show-origin --get core.worktree` with the same environment and bindings; the effective setting must be unset, meaning exit 1 and empty stdout. Any configured value, including an empty value or the expected root, refuses; any unexpected metadata-probe failure also refuses. These failures exit 2 with `ERROR: anthropic auth-route discovery refused: invalid Git metadata`. A matching `--show-toplevel` alone never authenticates metadata. Linked-worktree gitfiles receive the same refusal. For the required successful real-tree checks, the worker uses the continuing branch's exact tested head in a temporary standalone checkout with a real `.git` directory inside its sandbox, records the source head and checkout identity, and leaves worker-g's metadata unchanged.

   Require the baseline TSV `scripts/lint-comparisons-baseline.tsv` and manifest `home/dot_agents/agent-config.yaml` to resolve to regular files inside the verified root before consuming them. Resolve symlink components before identity and containment comparisons, and make those comparisons case-aware on a case-insensitive filesystem; missing, non-regular or outside-root inputs refuse with exit 2 and `ERROR: anthropic auth-route discovery refused: invalid trusted input`, naming only the safe repository-relative input label. Separately, skipping applied-file symlinks and non-regular files is input filtering, not the trusted-path control.

   Use `os.walk` with `followlinks=False` under the verified root's fixed `home/` and `install/` paths. Inspect root and descendant entries without following symlinks; never traverse a symlinked root or directory, skip each symlink as an input, and report skipped symlinks by count and safe repository-relative labels in the summary. Enumerate and scan every regular file, whether tracked, untracked or ignored, through the existing extension and chezmoi-attribute classification; do not prune ignored or untracked directories. Preserve the existing non-regular-file filtering. A filesystem-listing or walk error refuses with exit 2 and `ERROR: anthropic auth-route discovery refused: filesystem listing failed`; an empty regular-file inventory refuses with exit 2 and `ERROR: anthropic auth-route discovery refused: empty filesystem listing`; a missing `home/` root or an inventory without any regular file under `home/` refuses with exit 2 and `ERROR: anthropic auth-route discovery refused: missing home/ root`. Error diagnostics name only safe repository-relative labels, never file contents. Remove Git-based file listing, the walk/listing cross-check and all ignore-rule and ignore-inventory logic; no Git listing or exclusion result authorizes omitting an input.

   This is the design-tier re-plan for the third pre-dispatch security review, `.orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-066254d.md.last.md`, whose P1 at line 106 is the third finding in the Git-input-enumeration family (`GIT_INDEX_FILE`, redirected `.git`, then working-tree ignore rules). The refreshed design 5.14 item 3 quotation above is the normative discovery contract (C-88); replacing exclusion authority with direct inspection addresses the family rather than adding another ignore-rule check.

   Add `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_sanitizes_git_root_probes_and_walks_regular_files` before implementation. In a temporary repository containing a forbidden credential assignment under `home/`, export `GIT_INDEX_FILE` naming a nonexistent file and assert the same credential finding and outcome as with that variable absent, never a clean pass; the file list no longer comes from Git. At unchanged `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab` this reproduces the silent zero-path bypass. Assert that every remaining Git root-confirmation invocation removes inherited `GIT_*` inputs, including directory and configuration overrides, and receives the specified environment, configuration and root bindings. Exercise empty and home-less filesystem inventories and a walk failure and assert exit 2 with their named messages. Record the red command, revision, output and exit status before the fix and the green equivalents on the final head; a bogus index must not change discovery or credential refusal.

   Extend that same discovery selector before implementation with a clean tracked `home/` control and an untracked credential-bearing `home/hidden.sh`, matched by a newly added, uncommitted `~` rule in the tracked root `.gitignore`. Assert a hard credential finding naming the untracked file, no clean pass and no payload disclosure; a discovery-error refusal alone is insufficient. Cover an untracked regular file under `install/` too. Clean ignored and untracked regular files pass, and credential-bearing regular files remain findings regardless of root or nested ignore rules, negation, an untracked `.gitignore`, `.git/info/exclude` or global excludes; none supplies an exclusion decision. Assert that no Git file-listing or ignore probe runs, traversal begins only after root and metadata verification, symlinked files and directories are skipped without following them and are reported in the summary, and a regular file inside an ignored directory is scanned. Preserve red-then-green commands, revisions, outputs and exit statuses for the new cases; an already-correct control remains a baseline pass.

   Add `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_verifies_its_root_and_regular_input_paths` before implementation. It exercises canonical root mismatch and both trusted inputs as missing files, directories and symlinks escaping the root, plus ordinary in-root regular-file controls and case-aware identity and containment on case-insensitive filesystems. Assert the named exit-2 refusal for invalid inputs and preserve successful clean controls. Record red-then-green commands, exact revisions, outputs and exit statuses; record an already-correct control honestly as a baseline pass. Reuse and update the existing tracked-fixture helper to supply the required in-root files; an unrelated incomplete fixture must not cause refusal. The shared `tests/unit/trusted_exec_contract.py` helper belongs to P1-6 and does not exist yet; this task does not add it.

   Extend the root-and-input selector before implementation with separate fixtures planting a `.git` gitfile pointing at another repository, a symlinked `.git` pointing at another repository and an effective `core.worktree` setting. The other repository has a nonempty innocuous tracked `home/` tree while the expected root contains the forbidden fixture, so an empty filesystem inventory cannot explain the result. Assert the named exit-2 metadata refusal at the root check before traversal, with a gitfile or symlink refused before any Git invocation, even when explicit `--work-tree` would make `--show-toplevel` report the expected root. Cover both Git-directory probe mismatches and an empty configured `core.worktree` value; a real `.git` directory with both canonical probes matching and an unset setting remains a passing control. Record each new case's red command, exact revision, output and exit status before implementation and its green equivalents on the final head.

   Measure retained corpus coverage at unchanged a05 head `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab` and at the final head using `rows = anthropic_a03_cases()`: record `len(rows)` as the corpus row count and `sum(row["group"] == "honest" for row in rows)` as the honest-form count in `validation.md`. Both counts must stay the a05 head's, and every inherited row keeps its fixture bytes, finding class, exit status, redaction and location assertions. The new discovery regressions belong to the discovery selectors and do not replace or shrink the corpus or honest-form coverage.

   `applied_file_format` retains the chezmoi-attribute classification for JSON, TOML, YAML, template and script sources, with item 9 correcting structured-template classification. The check inspects raw source before parsing or rendering can discard comments, then inspects every decoded key and string value and both existing `darwin` and `linux` template outputs. A later allowed view never erases an earlier finding.

2. `credential_occurrences(text) -> [(line_no, line, decoded_form)]` remains the shared occurrence search. It finds `ANTHROPIC_API_KEY`, `ANTHROPIC_OAUTH_TOKEN`, decoded spellings of either name and identifiers that become either name after removing quote characters, backslashes, braces and the punctuation of `${…}`. It searches occurrences rather than shell assignment positions. LF alone separates lines; U+2028, U+2029, vertical tab and carriage return remain part of a containing line. The tuple retains the unchanged containing line and its one-based LF line number; `decoded_form` identifies the decoded spelling without becoming printable diagnostic content. Normalization does not trim or rewrite the line passed to the allowlist. Original source locations remain associated with decoded views, and Markdown examples retain their original offsets.

   Existing JSON, TOML and YAML readers, `parsed_entry` traversal, `json_strings` where applicable and `render_template_text(path, os_name)` are reused. The view pipeline retains ANSI-C and backslash character transformations and concatenated-piece handling without restoring the deleted shell-token or provenance interface. Percent and Unicode escape views participate in the same stateless occurrence search using existing primitives and the standard library. Raw text and the text after each transformation are inspected. Decoding covers data and spelling transformations, never variable evaluation, arithmetic, commands or shell expansion. Duplicate mapping entries remain visible and YAML aliases cannot multiply traversal. Strict UTF-8, malformed structured-input refusal, missing-PyYAML refusal and malformed-template refusal remain intact. No new library dependency is introduced; deterministic provisioning of the existing PyYAML dependency is specified below.

3. `allowed_assignment_line(line) -> bool` remains the only acceptance predicate for a credential-bearing line. `NAME` is either credential name and `VAR` is an ASCII identifier other than either credential name. The four forms are `NAME=$VAR`, `NAME="$VAR"`, `NAME=${VAR}` and `NAME="${VAR}"`, each optionally preceded by the exact text `export ` and optionally followed by ` <command words>`. A command word is a nonempty run of ASCII letters, digits, `_`, `.`, `/` or `-`; words are separated by one ASCII space. The suffix contains no credential-name occurrence. The complete fixed Python regex is matched without flags against the unchanged line:

   `\A(?:export )?(?:ANTHROPIC_API_KEY|ANTHROPIC_OAUTH_TOKEN)=(?P<q>"?)\$(?:\{(?!ANTHROPIC_(?:API_KEY|OAUTH_TOKEN)\})[A-Za-z_][A-Za-z0-9_]*\}|(?!ANTHROPIC_(?:API_KEY|OAUTH_TOKEN)(?![A-Za-z0-9_]))[A-Za-z_][A-Za-z0-9_]*)(?P=q)(?: (?!.*ANTHROPIC_(?:API_KEY|OAUTH_TOKEN))[A-Za-z0-9_./-]+(?: [A-Za-z0-9_./-]+)*)?\Z`

   No substring match, whitespace stripping, decoded replacement of the original line or additional value allowlist broadens this regex. A quoted or encoded left-hand name, credential self-reference, empty value, template-valued assignment, suffix literal, fallback, compound or subscripted assignment, arithmetic form, wrapper, `env` or `builtin` form has no exception. Heredoc syntax has no dedicated allowance or expansion analysis; its raw credential-bearing lines face this same predicate. The four forms continue to replace the earlier broader R1/R2 acceptance grammar.

4. The deleted `auth_shell_words` scanner, recursive shell parsing, quote state, word boundaries, command-prefix tables and provenance-based decisions remain deleted. The two shared functions govern applied script inspection, Markdown inspection and decoded-content inspection. Markdown prose and code classification does not evaluate shell; prose and fences cannot suppress a code-line occurrence. A `#` at the beginning of a line makes its occurrences `note` findings, and a Markdown prose line naming a credential without `=` makes its occurrences `note` findings. Credential-bearing code and structured data receive no prose exception. Notes are printed and leave exit 0 when no hard finding exists. `docs/` is not added to discovery. Every other non-allowlisted occurrence is a hard finding.

   Reporting names a source, location, rule or note class and fixed reason; it prints neither the containing line nor `decoded_form`. Preserve revise 1: every original and intermediate decoded key view is redacted before any diagnostic, including assignment-bearing mapping keys and ancestor paths, and log-line escaping follows redaction. `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_diagnostics_never_contain_a_decoded_payload_of_a_sensitive_key` remains green.

5. `tests/unit/test_validate_agent_assets.py` retains the consolidated table-driven `test_anthropic_check_bypass_corpus`: the three local reviews, the worker’s `anthropic_a03_cases()` corpus and pre-push regressions remain represented. Each row records provenance, source kind, exact fixture bytes, expected finding class and exit status, plus redaction and location assertions. Rows continue to exercise raw applied text and decoded structured-string views through temporary tracked fixtures. No inherited credential-bearing bypass disappears. A dynamic-name fragment retains its original bytes and credential-binding context; a fragment containing no detectable spelling remains a no-occurrence control, not a claim of variable evaluation.

   The retained lineage rows and verdicts are:

   | Provenance | Raw fixture or retained context | Expected result |
   | --- | --- | --- |
   | `local:b139995:1` | `NAME=ANTHROPIC_API_KEY; printf '%s' '\'; export "$NAME"=literal-value` | Hard finding. |
   | `local:b139995:1` worker regression | `NAME=ANTHROPIC_API_KEY; out=$(printf '%s' '\'; export "$NAME"=literal-value)` | Hard finding. |
   | `local:b139995:1` worker regression | `NAME=ANTHROPIC_API_KEY; out="$(printf '%s' '\'; export "$NAME"=literal-value)"` | Hard finding. |
   | `local:b139995:2` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY client` | Allowed form. |
   | `local:b139995:2` | `export ANTHROPIC_API_KEY=\"$DEPLOYED_KEY\"; exec client` | Hard finding under the whole-line policy. |
   | `local:a64daf1:1` | `export $'ANTHROPIC_API_\x4bEY'=literal-value` | Hard finding. |
   | `local:a64daf1:1` OAuth equivalent | `export $'ANTHROPIC_OAUTH_\x54OKEN'=literal-value` | Hard finding. |
   | `local:a64daf1:2` | `Don't store credentials.\n\n` followed by a fence containing `NAME=ANTHROPIC_API_KEY; export "$NAME"=literal-value` | Hard finding at the original example line. |   | `local:a64daf1:2` control | `Never store credentials.\n\n` followed by the same fenced example | The same hard finding. |
   | `local:a64daf1:3` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\u2028literal-value` | Hard finding. |
   | `local:a64daf1:3` worker extension | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\u2029literal-value` | Hard finding. |
   | `local:a64daf1:3` | `ANTHROPIC_API_KEY=$DEPLOYED_KEY\vliteral-value` | Hard finding. |
   | `local:a64daf1:4` | `{"ANTHROPIC_API_KEY=literal-value": "unused"}` | Hard finding with payload redacted. |
   | `local:a64daf1:4` TOML regression | `"ANTHROPIC_API_\u004bEY=literal-value" = "unused"` | Hard finding with payload redacted. |
   | `local:a64daf1:4` ancestor regression | `{"parent=literal-value": {"ANTHROPIC_API_KEY": "literal-value"}}` | Hard finding with every assignment-bearing path component redacted. |
   | a03 worker review, `577ad0f3` | `NAME=ANTHROPIC_API_KEY; EMPTY=; env $EMPTY "$NAME"=literal-value client` | Hard finding. |
   | a03 worker review, `577ad0f3` | `NAME=ANTHROPIC_API_KEY; OPTION=-i; env "$OPTION" "$NAME"=literal-value client` | Hard finding. |
   | a03 unresolved-prefix class | `env $opts NAME=literal` with its recorded credential-binding context | Hard finding in that context. |
   | a03 quoted-leading-blank regression | `ANTHROPIC_API_KEY=\" $DEPLOYED_KEY\"` | Hard finding. |
   | a03 escaped-leading-blank regression | `ANTHROPIC_API_KEY=\ $DEPLOYED_KEY` | Hard finding. |
   | a03 concatenation regressions | `ANTHROPIC_API_KEY=$DEPLOYED_KEY''` and `ANTHROPIC_API_KEY=''$DEPLOYED_KEY` | A hard finding for each. |
   | a03 encoded-key regressions | `{"ANTHROPIC_API_KEY$'\x3d'literal-value": "unused"}` and `{"ANTHROPIC_API_KEY$'\072'literal-value": "unused"}` as correctly JSON-escaped fixture bytes | A hard finding for each, with payload redacted. |
   | a04 worker review, `c15be6b9` | `ANTHROPIC_API_KEY=/usr/bin/env`, `ANTHROPIC_API_KEY=/usr/bin/export` and the retained wrapper-value rows | A hard finding for each. |
   | a04 worker review, `c15be6b9` | `NAME=ANTHROPIC_API_KEY; env >env "$NAME"=literal-value client` and `NAME=ANTHROPIC_API_KEY; env >export "$NAME"=literal-value client` | A hard finding for each. |
   | a04 worker review, `c15be6b9` | `NAME=ANTHROPIC_API_KEY; TOOL=env; "$TOOL" "$NAME"=literal-value client` | Hard finding. |
   | a04 worker corpus | `NAME=ANTHROPIC_API_KEY; env "$NAME"=/usr/bin/env client` | Hard finding. |
   | `local:325f520:1` | `export ANTHROPIC_API_KEY=; ANTHROPIC_API_KEY[1]=literal-value` | Hard finding. |
   | a02 subscript variant | `ANTHROPIC_API_KEY[0]=literal-value` | Hard finding. |
   | `local:325f520:2` | `NAME=ANTHROPIC_API_KEY; builtin -- export "$NAME"=literal-value` | Hard finding. |
   | `local:325f520:3`, TOML and YAML | `# export ANTHROPIC_OAUTH_TOKEN=x` | Reported note and exit 0 without a hard finding. |
   | `local:325f520:4` honest reference body | `ANTHROPIC_API_KEY=$DEPLOYED_KEY` | Allowed only by the raw-line regex, with no heredoc exception. |
   | `local:325f520:5` | A Markdown example whose `ANTHROPIC_API_KEY=literal-value` line is line 4 | Hard finding at line 4. |
   | security review of `325f520`, unmatched glob | `shopt -s nullglob\nNAME=ANTHROPIC_API_KEY\nenv /__codex_audit_no_such_dir__/* "$NAME"=audit_dummy /usr/bin/printenv ANTHROPIC_API_KEY` | Hard finding. |
   | security review of `325f520`, declaration wrapper | `NAME=ANTHROPIC_API_KEY\nbuiltin -- export "$NAME"=audit_dummy` | Hard finding. |

   In this table, `\"` denotes the presentation-escaped assignment quote retained from a05; `\n`, `\t`, `\u2028`, `\u2029` and `\v` denote the corresponding fixture characters where specified. Shell ANSI-C escapes remain literal fixture bytes.

   Retain every concrete expansion of the seven-prefix corpus for `env`, `exec`, `command`, `nohup`, `sudo`, `xargs` and `time`: unknown and attached options, vanishing and special-parameter expansions, dynamic names, redirection operands, numbered and brace file descriptors, descriptor duplication, append and process redirection, path-qualified env and unresolved executable paths. Retain quoted, backslash-escaped, ANSI-C, locale, brace-assembled, continued-name, nested-substitution, case-pattern, heredoc, encoded-ancestor and YAML complex-key fixtures. Credential-bearing bypasses remain findings; credential-free scanner-only refusal cases remain no-occurrence controls. Historical allowed rows outside the four forms remain explicit rejection rows.

   Percent-escaped, Unicode-escaped and concatenated-piece spellings and an allowed-looking prefix followed by a second literal credential assignment remain covered. Hard rows assert refusal and absence of `literal-value` and `audit_dummy` from diagnostics; note rows assert reporting without refusal. The existing selector is `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_bypass_corpus`.

6. Retain `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_refuses_an_unseen_shape_without_a_new_rule`: `typeset -x ANTHROPIC_API_KEY=literal` is refused through the shared occurrence search and unchanged regex, without a `typeset` branch, wrapper entry, parser rule or fixture override. Preserve its historical baseline observation against `325f520b`; a pre-existing rejection is never relabelled red. Its final-head result continues to prove shape-independent refusal.

7. Retain honest-form coverage for both credential names, all four forms, the exact optional `export ` prefix and command-word suffixes such as ` client` and ` client --flag`, using a non-credential identifier. Allowed forms pass; credential-free ordinary names and shell text remain passing controls. Self-references to either credential name, quoted or decoded left-hand names, empty values, assignment templates, tabs, operators and wrappers remain explicit findings. A suffix cannot hide a second credential occurrence.

   Comment and prose fixtures assert notes; code fixtures assert hard findings; `docs/` remains excluded. The real-entry fixture still proves `main()` registration, `home/` and `install/` coverage, `scripts/` exclusion, failed-listing refusal and symlink skipping. Parser fixtures retain malformed-byte, malformed-document, duplicate-key, alias and redaction coverage. Both existing platform renderings remain exercised. An honest decoded assignment passes exactly when it meets the same regex and no raw or other decoded view has a hard finding. Keep the existing unchanged-line, parser, entry-point and platform-rendering tests.

8. The real applied-tree run calls `validate_anthropic_auth_route()` on this repository’s tracked `home/` and `install/` files and records command, source head, output and exit 0. `make validate-agent-assets` is also green with main’s current templates. Honest forms through templates face the same allowlist. Obtain green without a per-path waiver, scanner fallback, applied-file edit or credential-rule baseline.

9. **Structured templates use their structured parser before decoded values are scanned.** Classify applied `.toml.tmpl`, `.yaml.tmpl`, `.yml.tmpl` and `.json.tmpl` as TOML, YAML, YAML and JSON respectively after the existing chezmoi filename-attribute handling. Preserve script-source exclusions such as `modify_` and `run_`; a script does not become a data document merely because its name contains a structured extension.

   For a structured `.tmpl` source, replace every complete chezmoi directive `{{ … }}`, including `{{- … -}}` trim forms and directives spanning lines, with the single inert ASCII token **`0`** before parsing. `0` is valid both inside a string and as a bare value in JSON, TOML and YAML. Replacement inspects text only: it executes neither chezmoi nor directive expressions. Scan the unchanged raw source first, so replacement cannot hide a raw credential occurrence. An incomplete directive or any substituted document that still cannot be parsed is a finding, never a raw-only fallback or a pass.

   Parse the substituted result with the existing parser for its classified kind and traverse every decoded key and string value. Each decoded string faces the same occurrence search and fixed honest-form regex as a `.toml` value. Preserve existing platform-specific inspection of managed template sources; inert substitution does not erase either platform’s findings or introduce template execution. Parser failures name the file, kind and parser error after the existing diagnostic redaction and escaping; no raw source excerpt, assignment payload or intermediate key view may leak.

   Add these two tests before implementation:

   - `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_parses_toml_templates_before_scanning_values` reproduces `security:2b6fc7f:1` using the reviewer’s exact applied-file content:

     ```toml
     [tasks.audit]
     run = """export ANTHROPIC_API_\
       KEY=audit_dummy"""
     ```

     The `.toml.tmpl` case must be red at unchanged `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab`, where validation incorrectly returns 0, and green on the final head, where it is a hard finding because TOML joins the credential name. Its byte-identical `.toml` sibling stays a finding at both revisions. Assert the source file and refusal without disclosure of `audit_dummy`.

   - `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_substitutes_structured_template_directives_and_refuses_parse_failures` covers all four structured-template suffixes, ordinary and trim directives, multiline directives, substitution inside strings and at bare value positions, and refusal after unsuccessful decoding. Include a clean `.toml.tmpl` whose bare directive makes it parse only after substitution: it passes when all decoded values are clean. Include malformed structured templates that remain unparseable after substitution and assert a finding naming the file and safe parser error without payload disclosure. Retain strict UTF-8 refusal and the missing-PyYAML refusal. Use the existing tracked-fixture helper and adjust its empty JSON-template fixture initialization where necessary; an unrelated empty fixture must not be the reason a case refuses.

10. **List-container fences are code fences.** Treat list indentation and an opening list marker before the fence as container syntax when recognizing the opening and matching closing fence. A fence within a list has the same code class as a top-level fence; a bare credential name inside it is a hard finding, never a prose note. Preserve original source offsets and the existing top-level, blockquote, fence-marker and indented-code behavior.

    Add `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_treats_list_container_fences_as_code` before implementation. It owns `a05-worker-verification-1` and `security:2b6fc7f:2`, including the exact reproduction ``- ```sh\n  ANTHROPIC_API_KEY\n  ``` `` with actual LF characters. Record its red result at unchanged `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab` and green result on the final head. Exercise the closing fence with list indentation, both credential names and the retained fence classes in this test; assert a hard finding at the original credential line. A prose-only control remains a note. The a06 owner retains no part of this fix or its test.

## Deterministic unit-test environment

At `2b6fc7fc`, required job `test (macos-14, client)` fails 338 of 1276 tests with `ERROR: home/key.yaml: cannot be parsed as yaml (ImportError); PyYAML is required`, while the same job passed at `53642ace`, `eda0354b` and `33ea990f` and the Ubuntu unit jobs pass at `2b6fc7fc`. The inherited log is `.claude/worktrees/worker-g/.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/rebase-repair-1-ci-job-117920404520.log`.

The cause is that `Makefile:185-186` runs `uv run python -m unittest discover -s tests/unit -v` without installing PyYAML; YAML fixtures therefore depend on whether the runner’s interpreter happens to carry it. The comment at the starting validator’s lines 227–228 relies on that accidental environment.

Change the `unit-test` recipe to `$(UV_PYYAML) python -m unittest discover -s tests/unit -v`, reusing the existing cache-first `UV_PYYAML` probe already used by `validate-agent-assets`. This runs `uv run --offline --with pyyaml` when its import probe succeeds and otherwise `uv run --with pyyaml`; do not duplicate the probe, install globally or edit a workflow. Update the stale validator comment so it no longer says that `make unit-test` does not install PyYAML.

**No test is required to keep passing without PyYAML installed.** Under default denial, an undecodable YAML input remains a finding. Do not obtain green by skipping YAML fixtures or treating unavailable parsing as clean. Preserve the existing mocked missing-PyYAML refusal test, `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_refuses_parse_failures_and_missing_yaml_without_disclosing_payloads`, and run the YAML parser fixtures with PyYAML present.

## Preserved rebase repair

Keep amendment 1’s repair from `2b6fc7fc`: the comparison moved to line 1626 has its baseline row, and the authored comparison at line 1817 uses the normalizer. `scripts/lint-comparisons-baseline.tsv` remains allowed only for this PR’s affected comparison rows, including necessary stale-row maintenance if an authorized edit changes a hit. Add no unrelated baseline entry or suppression. Preserve the revise-1 redaction fix and its 36 regression combinations. Historical evidence is not rewritten as a07 evidence.

## Measured size budget

The 06:26:39Z PONG measures 232/300 source lines at `2b6fc7fc`; 232 + about 40 for structured-template classification and substitution + about 10 for list-fence classification + about 6 for the Makefile and stale-comment edits + about 45 net for item 1's Git sanitization, metadata authentication, trusted-input checks and filesystem-only discovery = about 333 changed source lines, within the retained source cap of 350. Item 1's revised net estimate is about 15 below the previous 60: removing the Git listing, cross-check and ignore-rule logic offsets part of the filesystem walk. Only item 1's implementation estimate changes; the source cap stays 350.

The same PONG measures 967/1000 test lines at `2b6fc7fc`; 967 + about 90 for the three new tests + about 120 net for item 1's two new tests and required fixture updates = about 1177 changed test lines, within the retained test cap of 1200. Replacing listing and ignore-authorization assertions with filesystem-discovery regressions lowers item 1's previous 130-line estimate by about 10; the test cap stays 1200.

These are planning measurements, not claims that the final diff or implementation checks already pass.

## Out of scope

The omp auth-store probe, PR #404, manifests, rendered settings, workflows, live credentials and applying files to the user’s home directory are outside this task. Do not change `SECRET_PATTERN`, its placeholder allowlist, the honest-form regex, permission policies, execution boundaries or dependency declarations. The only dependency-provisioning change is supplying the existing PyYAML dependency through the Makefile’s existing probe. Do not add scripts, another parser, shell evaluation, template execution, per-path exceptions or another implementation PR.

## Check

`make unit-test` is green through the existing cache-first PyYAML invocation, and the validator module is also green under `uv run --with pyyaml python -m unittest tests/unit/test_validate_agent_assets.py -v` or its cache-first offline equivalent. Paste the commands, actual outputs and exit statuses in `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/validation.md`. YAML parser cases run with PyYAML present; no dependency-related skip substitutes for their execution. The retained mocked missing-PyYAML case still proves refusal.

`make validate-agent-assets` exits 0 on the continuing branch with main’s current templates, with output and exit status in the same validation file. Item 8’s real applied-tree auth run is green. The table-driven corpus remains green with every inherited bypass and provenance accounted for. Record raw, structured-decoded, rendered-template, spelling-decoded and note-only cases separately, including both platform outputs, original Markdown offsets and redaction.

The three new selectors are green on the final head:

- `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_parses_toml_templates_before_scanning_values`
- `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_substitutes_structured_template_directives_and_refuses_parse_failures`
- `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_anthropic_check_treats_list_container_fences_as_code`

Write those tests before their fixes. Record red and green commands, exact tested revisions, outputs and exit statuses. The reviewer’s `.toml.tmpl` reproduction and the list-container reproduction are red at unchanged `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab` and green on the final head; the `.toml` sibling remains a finding. A clean template requiring placeholder substitution passes, and an unparseable template is refused. Record any already-correct control honestly as a baseline pass.

Preserve the a05 historical red provenance against `325f520bfc8b4dbb25e0744d27878cdf7eab2fd2`, the six a03 redesign tests, the two a04 command-prefix tests, both `b139995` regressions and revise 1’s redaction evidence. Give their retained behaviors fresh final-head green results without fabricating new historical failures. The unseen-shape test still passes without a shape-specific implementation change, and the fixed regex remains byte-identical.

Record `ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py`, the changed-file comparison-lint result and `git diff --numstat origin/main...HEAD`. Inherited Ruff findings retain their actual exit status and comparison against the unchanged baseline at the original filenames; add no suppression or unrelated fix. A failing command is never labelled passing.

The diff contains at most **350 changed lines, added plus deleted, outside `tests/` and `.orchestration/`**.

The diff contains at most **1200 changed lines, added plus deleted, under `tests/`**, including fixtures.

`measure.md` records actual totals and the complete changed-file inventory for the continuing PR. Do not remove validation, redaction or required corpus coverage to fit. Do not run Bats locally.

On the final head, required unit job **`test (macos-14, client)` and the Ubuntu unit jobs are green**, with their job identities, head SHA and results recorded. The Makefile change must supply PyYAML deterministically; previous green runs or an interpreter that happens to carry it do not establish completion. All other ruleset-required checks are also green.

The **orchestrator** runs `scripts/orchestrator/task-consistency-check.py` with PyYAML before dispatch and at acceptance, covering C1 to C10 and C7b, and verifies C11’s closed-row selectors and C18’s section-5.14 reference. It records which checks were automated and which were checked manually rather than claiming an unimplemented checker rule ran.

The **orchestrator** obtains the independent **C-80 pre-dispatch security review** of this exact task text, addresses its findings within the applicable task-authoring process and dispatches only the reviewed bytes. This text itself claims no completed C-80 review.

The **orchestrator** verifies the first-push inventory and performs the whole-file byte comparison between the dispatched a07 text and `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md`, checking the TASK and RESULT sha256 values. The first push deletes only the a05 task copy and adds the a07 copy; all other predecessor evidence remains intact.

## Completion

One branch and one continuing implementation PR complete this task. PR #412 remains the main-target PR on `tools/anthropic-auth-route-structured`, continuing from `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab`. PR #396 remains open as the stacked record until #412 merges. The first push contains the a05 task-copy deletion and the byte-identical a07 task copy. No second implementation PR or fresh branch is created.

The following embedded Completion clause applies with **`dotfiles-T129-anthropic-auth-route-check-followup-a08`** as the owner of new advisory P2 findings and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md>` in the RESULT. This task’s continuing branch, existing PR, round limits, default-deny policy, bounded automatic-review wait and sandbox command restrictions govern the corresponding steps. The orchestrator writes the advisory owner’s task before recording its first owned row. Item 10’s transferred a06 finding is required work here, not an a08 advisory.

One PR continues on `tools/anthropic-auth-route-structured` from `2b6fc7fcf6c4db3c698aab67cfaae8ba7cecc6ab`. The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-anthropic-auth-route-check-followup-a08`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-anthropic-auth-route-check-followup-a08` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md>` and the evidence paths.

One PR continues on `tools/anthropic-auth-route-structured`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The third finding of one class stops further rounds until the orchestrator's re-plan.

The RESULT identifies the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. It carries the precheck evidence required by the applicable RESULT procedure.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and refusal.

The findings `local:a64daf1:1` through `local:a64daf1:4`, the a03 command-prefix P1, the a04 worker’s `local:c15be6b9:1` through `local:c15be6b9:4`, `local:325f520:1` and `local:325f520:2` remain owned by this reset lineage. The a04 raw-comment, heredoc and Markdown-location findings retain explicit dispositions against the changed policy and final-head evidence. The unmatched-glob and `builtin --` reproductions remain in the corpus. Both `security:2b6fc7f:1` and `security:2b6fc7f:2`, including the latter’s `a05-worker-verification-1` identity, receive fixing commits and final-head regression evidence.

Preserve the a02 through a05 acceptance histories, worker-side fix counts, revise-1 redaction evidence and D-024-24 rebase-repair evidence. **Every worker-side fix round counts toward INV-6, including one before the first push or RESULT.** The a05 cap is the reason for this reset; its history is not erased.

The worker performs at most one independent pre-push review and one consolidated worker-side fix round. Any orchestrator revise is allowed only while INV-6’s two-round total permits it. Verification after the worker fix round records a surviving P0/P1 as **`open:<id>`** and stops for the orchestrator’s decision; the worker does not fix it a second time. Local identifiers retain their review provenance; Bot findings use `open:<thread id>` or `open:review-<review id>`. This applies before the first push or RESULT as well as afterward. A third finding of one class stops rounds for a new orchestrator re-plan.

The RESULT names `pr=412`, final head, base, branch, changed files, tests, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/task.md>`. It records every inherited and new finding with its fixing commit or proposed evidence-backed disposition and distinguishes policy changes from historical fixes. Retain both `b139995` findings with their `a9056299` provenance and the separator verdict; retain 4305965376 and 4305965379 with fixing commits, the template CI fix and surviving-case regression, and the dispositions of 4302758230, 4302758234, 4302758239 and 4305863865. Name the retained corpus, unseen-shape test, note behavior, honest forms, real applied-tree run, three new regressions, deterministic PyYAML invocation and final-head unit jobs. A surviving P0/P1 remains explicitly open.

Write new evidence under `.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a07/` in the worker’s worktree, using those same relative paths and saying so in the report and RESULT. Commit the task’s branch evidence before the RESULT. Keep inherited a05 outputs distinct from unchanged-`2b6fc7fc` regression observations and final-head checks. Worker review evidence uses the required `-worker-` infix and follows the repository’s JSON-evidence, receipt and review-gate rules. The report, validation, sandbox, learning, autoskill and measurement records state their actual status.

`security: true` requires a task-level audit and a separate security-profile review on the final head before integration. The orchestrator follows Orchestrator Playbook step 10 for final-head feedback collection, audit dispositions, acceptance, the integration gate and merge. A changed head requires refreshed final-head evidence.

**Every `gh` command and every Git write runs as an individual command inside the worker’s sandbox**, without shell chaining or a wrapper combining writes. The worker requests no sandbox escape, changes no execution boundary and obtains no agent-to-agent permission approval. For any required operation that cannot complete there, send `AGMSG-PONG v1 status=blocked` naming the exact command, exit status and boundary, preserve the evidence and wait for the orchestrator to re-task; do not substitute an out-of-sandbox route.

The worker posts **no `@codex review` request** and runs no `gh pr edit` or `gh pr comment`. Await CI and automatic reviews within the existing bounded window, starting from the push rather than the end of CI. Record absent automatic Bot review as `bot: none` when the window ends. Thread replies and resolutions remain the orchestrator’s responsibility.

Where the inherited P1-14 text-writing restriction remains applicable, strings containing `gh pr merge` or `gh pr create` are written with the file-edit tool, never a Bash heredoc or `echo`. It grants no authority to create another PR or merge this one.

This read-only redesign runs no implementation tests or live CI and claims no new green result.
Runtime-assembled names that no retained decoder joins remain undetectable; local evidence does not establish a hostile same-UID execution boundary.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```