#!/usr/bin/env bash
# @file pr-merge.sh
# @brief Squash-merge a pull request only at a head the program's ledger records as `correct`, or as `carried` from an earlier `correct` head with the same diff, with the unit's `sweep` row at that head when the head's changed paths touch a sweep class (a lever, a policy, credential handling or a deployed executable), when no daily sweep of main's head stands within 24 hours at the lever's last read before the merge request, or when the main ruleset does not require branches to be up to date before merging (U613), and CI passed, the orchestrator seat's merge lever.
# @description
#   Regime-cutover U71 (finding F010), the orchestrator seat's only merge path: `home/dot_agents/omp/policies/orchestrator.yml`
#   allows `~/.local/bin/common/pr-merge.sh *` and denies the `gh pr merge` command text (a speed bump: text rows do
#   not stop a glob spelling; a seat running `gh` itself is the residual unit U88 removes). `<pr>` is decimal and
#   checked before the first `gh` call. The lever runs in the main checkout (a linked worktree is refused) and reads
#   one program store, chosen by one rule with two forms (regime-cutover U216, store move 2 of 5,
#   handoff/07-store-move-design.md): the derived store `${REGIME_STORE_ROOT}/<program>` when that directory exists,
#   the root being the fixed derivation `<physical HOME>/.local/state/regime-store/<slug>` the sourced `regime-env`
#   exports (U215); else, until U221 moves the live store of this program there and removes the form, the checkout's
#   own store `<toplevel>/.orchestration/orchestrate/<program>` (the pre-move form; `store_resolve`, which prints the
#   form chosen on stderr). The store's `ledger.tsv` (header
#   `ts unit pr head_sha verdict verifier evidence`), `<program>` taken from the pull request body's one
#   `Program-Unit: <program>/U<n>` line, no directory of that chain nor the ledger a symlink, each owned by this user;
#   `--records` must resolve (`pwd -P`) to exactly the chosen store (one naming the other form is refused naming
#   both), so a ledger written anywhere else is never read. It reads
#   `gh pr view <pr> --json state,baseRefName,headRefOid,isDraft` and refuses unless the pull request is `OPEN`, not a
#   draft and based on `main`. The verdict is the newest `ledger.tsv` row whose `pr` is `<pr>` and whose `head_sha` is
#   the full 40-hex sha it judged (a short sha never matches); newest by the row's ts column parsed as a time (the
#   later line at an equal ts), never by its place in the file (U122 round 5). The ledger is read by the checkout's
#   `scripts/orchestrator/ledger.py`, the one reader of the ledger (U122 round 6: this lever's own awk checked the ts
#   for its shape alone, so a `carried` row dated hour 25 outranked a valid `incorrect` row), run as `python3 -I -S`
#   with its status read, as `pr-audit.sh` runs the checkout's readers: a store it cannot read as data (a header that
#   is not the store's, a row with another column count or an empty `ts`, `unit`, `pr`, `head_sha` or `verdict`
#   cell, a ts `strptime` does not read as `YYYY-MM-DDThh:mm:ssZ`) is refused naming the file and line, and no
#   python3 on PATH or no reader in the checkout is a refusal too. It must start with the word `correct`, so a later
#   `incorrect` or `blocked` row for the same head voids an earlier `correct`, or with the word `carried` (regime-cutover
#   U122, standing order 38): then its evidence must hold `carried <earlier head> <this head> <sha256>`, the line
#   `scripts/orchestrator/audit-carry.py` printed when this head's diff against its merge base equalled the earlier
#   head's (U180: a note may follow the digest after a space, `;`, `,`, `.` or `)`, and after nothing else), the
#   earlier head is another sha than this one, and the newest row (by ts) for the earlier head must itself
#   be `correct` (the digest lever carries the earlier head's verdict whatever it says, round 5, so a carry from an
#   `incorrect` head is a row this gate refuses naming that head); the verdict file and the dispositions the gate then
#   reads are the earlier head's, since its findings
#   are this head's. That sha is always the current head: there is no silent carry-over (U71 audit round 10), so a
#   head that `pr-update-branch.sh` moved gets a fresh audit or a `carried` row the coordinator wrote from the digest
#   lever's output. The row alone is not enough (U119 round 2, Codex thread 4419039271): since standing order 35 a
#   `correct` verdict may carry P2 and P3 findings, and since U125 filed ones of any priority, so the lever also opens
#   the store's `verdicts/<unit>-<sha8>.md` of
#   the audited head, `<unit>` the ledger row's `unit` column (round 2: the body's unit or a `U<n>b` fix unit of it,
#   standing order 24; a `U71b` row's verdict is `U71b-<sha8>.md`, and a row of any other unit is refused) (absent,
#   a symlink or unreadable is a refusal: a merge needs the verdict file, not only the row)
#   and parses its leading `## Findings` section, from the first `## Findings` line to the next `## ` heading (a later
#   `## Findings` line, in the Notes or a rationale, is text; U119 round 4), the lines pr-audit.sh's reader writes
#   since U125 (`- P<n> (<confidence>) [f<n> s<n>] <path>:<line>: <rationale>`: the frequency and severity scores,
#   each one of 1 to 10, read by value and never second-guessed, then the path, the first token after `] ` that holds
#   no colon and no whitespace, the line the digits after it, and the rationale the free text after the following
#   `: `, or `- none`; a line without the `[f<n> s<n>]` token is refused
#   naming it, since this reader always writes it and a verdict of the unscored reader belongs to a merged unit, never
#   to a merge head). That file is the `verdict.md` of `pr-audit.sh`, the audit route
#   (`hcom-orchestration` SKILL step 4, U119 round 3), copied into the store; a verdict of the retired omp-run.sh
#   audit route has no `## Findings` heading, is refused by name, and belongs to a merged unit, never to a merge
#   head. A finding's weight is its frequency times its severity, and WEIGHT_THRESHOLD (10, the number of the
#   AGENTS.md verdict bullet and of the reader) decides what the gate asks of each line (U125): a line of any priority
#   with weight under the threshold is filed, reported in the verdict and the code left as it is, so it needs no
#   row; every P2 or P3 line at or above it needs a row of the store's `dispositions.tsv` (header `ts unit head_sha
#   priority path line disposition reference`) with the same unit, full head sha, priority, path and line (the
#   finding's whole identity, the key `audit-carry.py` joins by as well; U122 round 3) whose `disposition` is
#   `residual` and whose reference `unit=U<n> gate=<clause>` names a `units.tsv` row, or whose `disposition` is
#   `fixed` and whose reference starts with the 40-hex sha of the head being merged while that head is carried (U180:
#   a `fixed` row holds for the head it judges only when the head being merged is the fixing head under a `carried`
#   row, which can only be a body fix, since a code change would have changed the digest; the sha is the reference's
#   first token, read as 40 hex followed by the end or a character outside hex, and compared whole). A `fixed` row
#   naming any other head, or any `fixed` row when the head being merged is the audited head itself, names the later
#   head that fixed the finding and never satisfies the gate for the head it judges. The first finding without such a
#   row is named in the refusal. A P0 or P1 line at or above the threshold under a `correct` row, a `## Findings`
#   line of another shape or without its scores, a score outside 1 to 10, a line whose first token after `] ` is
#   no `<path>:<line>:` with a path free of colons and whitespace, a verdict file whose last
#   line is not `Verdict: correct`, and a `dispositions.tsv` or `units.tsv` row whose column count is not its
#   header's or whose required column is empty are refusals naming the line (standing order 21); the rows are split
#   by awk on the tab alone, since bash's `read` merges adjacent tabs (U119 round 3). Every store path the lever
#   opens (`ledger.tsv`, `verdicts/`, the verdict file, `dispositions.tsv`, `units.tsv`) must be a regular file or
#   directory of this user and no symlink, and `--records` must resolve to exactly the store `store_resolve` chose for
#   the body's program (the derived store, or the checkout's own store while no derived one exists). The
#   lever reads no local git objects or refs; it decides from `gh` reads and the store alone, and git only names the
#   checkout (`rev-parse --show-toplevel`, `--absolute-git-dir`, `--git-common-dir`); the head's changed paths, which
#   decide whether the sweep is required (below), are the compare API keyed by two shas as data: the tip of `main`
#   read once, `gh api 'repos/{owner}/{repo}/git/ref/heads/main' --jq '.object.sha'` (40 hex, else a failure), then
#   one call, `gh api 'repos/{owner}/{repo}/compare/<main tip>...<head>' --jq '("merge-base " +
#   (.merge_base_commit.sha | if type == "string" then . else error("merge_base_commit.sha is " + type + ", not a
#   string") end)), ((if (.files | type) == "array" then .files else error("files is " + (.files | type) + ", not an
#   array") end) | .[] | [.status, .filename, (if has("previous_filename") then .previous_filename else null end)] |
#   @json)'`, the merge base as its first line and one JSON array per file after it, whose merge base must equal the
#   tip (else the head is refused as not up to date with `main`, naming both shas; round 7), whose completeness the
#   reader takes from the listing itself (300 or more entries, the API's cap, is `required cap`) and whose `files`
#   the jq holds to an array first (round 6: an object, a string, a number, a boolean or null there is the jq's own
#   error and the call's failure, never a listing), `gh` reads like the others. CI is `gh pr checks <pr>
#   --json bucket,name` between two reads of `headRefOid` that must both equal
#   the head (and whose second read must still report base `main`: `--match-head-commit` pins only the head): at least
#   one check, every bucket `pass` or `skipping`, every name of REQUIRED_CHECKS listed with bucket `pass`, and `gh`
#   exiting 0; a pending, failed or cancelled check is a refusal naming it, and a required check that is not listed, or
#   is listed with any bucket but `pass` (`skipping` satisfies only a check that is not required), is a refusal naming
#   it apart from the red ones (`CI has no result for: ...`). REQUIRED_CHECKS (regime-cutover U330) is the eight
#   required status contexts of the main ruleset `main integration gate` (24397953), copied as GitHub names them
#   (measured 2026-11-07T03:34Z, decisions row 2026-11-07T03:35:00Z): a constant in the lever and not a read of the
#   rulesets API at merge time, because that read would be one more `gh` call in the merge window and a ruleset the
#   operator edits is not the program's record of what a merge needs; `tests.unit.test_pr_merge` holds the array equal
#   to the contexts recorded from that measurement, so a drift between the lever and the ruleset fails CI, not a merge.
#   Before U330 the gate asked only that every listed check be green, so PR 708's head 792604f9, which conflicted with
#   main and got none of its `pull_request` workflows (GitHub runs them on the merge ref), would have merged on
#   `regime`, GitGuardian and CodeRabbit alone with no test leg run (decisions row 2026-11-07T01:45:00Z). The one
#   write is `gh pr merge <pr> --squash --match-head-commit <head>`, so GitHub
#   refuses the merge if the head moved after these reads; it never passes `--admin`, `--auto` or
#   `--delete-branch`. After the merge, or after a merge error, `gh pr view <pr> --json
#   state,mergeCommit,baseRefName,headRefOid` decides: `MERGED` into `main` at the audited head, whose merge commit's
#   first parent is the tip of `main` read before the listing (round 8, below), prints the receipt (the
#   merge happened; never run the merge twice); another state, another base, or another merged head (a merge someone
#   else made after the pinned one failed) is a failure with no receipt that names both shas. The
#   thread check (`pr-threads-check.sh`) stays a separate step before this lever (`hcom-orchestration` SKILL step 6).
#   Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
#   Since regime-cutover U147 the lever also requires the unit's `security-audit` sweep at the audited head, since
#   U244 of every unit, and since U597 of a head whose changed paths touch a sweep class (the AGENTS.md Audit sweep
#   rule as the operator set it on 2026-11-18, sweep rule C: a lever, a policy, credential handling or a deployed
#   executable; every other head merges on its Codex audit and CI alone while the standing control stands, one full
#   sweep of main's head per day, whose row this lever reads since round 4; U147 read the unit's brief for the
#   trust-boundary mark, and with one class that reading is gone). After `require_dispositions` the lever reads the
#   tip of `main` once (`gh api 'repos/{owner}/{repo}/git/ref/heads/main' --jq '.object.sha'`, status read, 40 hex)
#   and lists the audited head's changed files through the GitHub compare API keyed by that tip and the head's sha,
#   one call, `gh api 'repos/{owner}/{repo}/compare/<main tip>...<head>' --jq '("merge-base " + (.merge_base_commit.sha
#   | if type == "string" then . else error("merge_base_commit.sha is " + type + ", not a string") end)), ((if (.files
#   | type) == "array" then .files else error("files is " + (.files | type) + ", not an array") end) | .[] | [.status,
#   .filename, (if has("previous_filename") then .previous_filename else null end)] | @json)'`, the response's merge
#   base as the first line and one JSON array per file after it (U597 round 4, the mechanism change after three rounds
#   on a listing keyed by the pull request's number: round 1's `gh pr diff <pr> --name-only` printed a rename's
#   destination alone and kept git's C quoting of a name with a tab; round 2's files endpoint listed both paths of a
#   rename as JSON, and round 3 made each file one array the reader parses and refuses in any other shape, but the
#   files endpoint is keyed by the number alone, so a head reread and a count of the pull request around it never
#   bound the listing to the audited head: the pull request's head can move between the listing and the read; the
#   compare request names the shas, so its answer is that head's diff or a failure, and a listing of another head
#   cannot be substituted; `main` is the base the first view read and required; gh fills `{owner}` and `{repo}` from
#   the checkout's remote). Round 7 (the round-6 P1): `pr merge --squash` lands the diff against `main`'s tip, while
#   the three-dot compare lists the diff from the merge base, and when `main` moved after the branch point the two
#   differ (a base-side rename can carry an exempt edit into a sweep-class path), so the lever pins the tip it read,
#   compares against it and requires the response's `merge_base_commit.sha` to equal it, else refuses naming both
#   shas (rebase the branch onto `main` and re-run the audit); with the head up to date the three-dot diff equals the
#   two-dot diff against the tip, the diff the squash lands, and that invariant is what the listing rests on. Round 5
#   (the round-4 P1 and its first P2): the compare response carries `files` on its first page alone, at most 300
#   entries, and paging walks its commits, not its files (docs.github.com, REST API, commits, compare two commits,
#   read 2026-11-19), so the call is one, with no paging, and completeness is read from the listing itself and from
#   nothing keyed by the number: the reader counts the entries and answers `required cap` for 300 or more (the listing
#   may be cut short, so the per-head sweep stands), the classes decide under 300, and no count of the pull request
#   is read beside it. A response whose `files` is not an array (null for a key missing from a later page or a shape
#   the API changed; an object, a string, a number or a boolean: round 6, the round-5 P1, where `.files // error(...)
#   | .[]` iterated an object's values and read a one-record object as that file's listing) is the jq's own error,
#   `(if (.files | type) == "array" then .files else error("files is " + (.files | type) + ", not an array") end)`,
#   which fails the call and the lever names with the type, never an empty listing; a failed tip read, a tip that is
#   not 40 hex, a failed listing and a first line that is not `merge-base <40 hex>` are failures, an empty listing a
#   refusal: a head that changes nothing is nothing to merge, and a listing cut short is never "not required"
#   (standing order 21). The file lines go on stdin to the checkout's
#   `scripts/orchestrator/sweep-scope.py --files-json`, the one definition of the classes (one frozen tuple of path
#   prefixes per class), run as `python3 -I -S` with its status read: exit 2 is a refusal carrying its line (a line of
#   another shape, a rename without its source, a `previous_filename` that is neither a string nor null, which the jq
#   passes through as it is and never maps to null, round 4), any other non-zero status a failure, and an exit-0
#   answer is read by its shape: `required cap` sets `sweep_class` to `cap` with the cap's reason and keeps the gate
#   below, `required <class>` (the class one lowercase word) keeps the gate below; `not-required` binds
#   the exemption to its standing control (round 4; the round-2 and round-3 P2 at AGENTS.md:71: until then no merge
#   gate read the daily sweep, so a head outside every class could merge with no sweep anywhere near it): the
#   checkout's `ledger.py <store> daily 86400` prints the newest row of the store's `daily-sweeps.tsv` (header `ts
#   head_sha verifier evidence`, written by `ledger-row.py daily` after the coordinator's daily dispatch of the sweep
#   seat at main's head from the kit's brief template `home/dot_agents/regime/daily-sweep-brief.md`, the
#   hcom-orchestration SKILL step 4) whose ts is within the last 86400 seconds, or `none`, read as the ledger is (a
#   malformed file is the reader's exit 2 naming the line and field, a missing file `none`); one row, held to the
#   exact row of the rule as a unit's sweep row is (the pin word a prefix of the manifest's pin, the findings file a
#   regular file of this user under the store), skips the sweep row and prints one stderr line, `sweep: not required
#   (no lever, policy, credential or deployed-executable path changed); the daily sweep of main's head <sha> at <ts>
#   stands within 86400 seconds`; `none` keeps the gate below as for a required head, and its refusal names both: no
#   daily sweep within 24 hours, so the per-head rule stands; any other answer is a refusal naming the reader and the
#   answer. When the sweep row is required, and before the checks read and the one write, the checkout's `ledger.py
#   sweep <unit> <audited head>` prints the newest row of the unit
#   or a fix unit of it at the audited head whose verdict starts with the word `sweep` (pr `-`, verifier the skill
#   and its pin, evidence the findings file under the store), or `none`, which is a refusal naming the unit, the head
#   and the rule; an exit-0 answer that is neither `none` nor one row of four tab-separated fields with a ts is a
#   refusal naming the reader and the answer. The row must be the exact row the rule defines: pr `-`, verifier the
#   two words `security-audit-skill <pin>` with the pin word, 8 or more lowercase hex, a prefix of the
#   `assets.security-audit-skill.pin` of the manifest the self-check read (one probe, `sweep_pin_probe`, run as
#   `python3 -I -S -c` over `LEVER_MANIFEST`), and evidence whose first `;`-separated field names a findings file
#   `sweeps/<path>.json` that is a regular file of this user under the store (never opened); the reader refuses any
#   other `sweep` row as a malformed store, and a pin that is no prefix or a findings file that is missing, a symlink
#   or another user's is a refusal naming it, so a row written by hand with another verifier admits nothing. The
#   audited head is the one `require_verdict_row` set, so a head moved under a `carried` row needs no second sweep.
#   The lever reads no brief, never the findings file a sweep row names, and judges no sweep's content.
#   Round 8 (the round-7 P1 at :1123 and P3 at :782). The two readers the lever runs, `ledger.py` and `sweep-scope.py`,
#   ran from `${toplevel}/scripts/orchestrator/` after an existence check alone while the lever held its own bytes to
#   `claude.levers.sha256.pr-merge.sh`, so a rewritten or stale reader could waive a required sweep whatever the
#   compare listed. Now each reader is copied into a private directory the lever makes (`mktemp -d` under `TMPDIR`,
#   mode 0700, removed on every exit by the EXIT trap), the copy is hashed (sha256sum, else shasum -a 256, as
#   lever_self_check hashes this file) against the reader's `claude.levers.sha256.<name>` pin in the manifest the
#   self-check read, and the copy is what `python3 -I -S` runs (reader_copy; hcom-seat's helper_copy_make and
#   helper_pin_check idiom, U310f): a differing digest or a missing or doubled pin is a refusal naming the reader and
#   both digests before the first `gh` read, and the copy is the one read of the file, so a file swapped after the
#   hash is not the file run; `sweep-scope.py` gets its pin and its deployed twin `~/.local/bin/common/sweep-scope.py`
#   from the generator as `ledger.py` has them (`claude.levers.sha256.sweep-scope.py`). Round 9 (the round-8 P1 at
#   :1282, the second strike of the diff-basis class; the mechanism-change decisions row of 2026-11-19T11:56:54Z):
#   `--match-head-commit` pins the head alone, and no client-side read can hold `main` still between the tip read in
#   require_sweep_scope and the moment GitHub writes the squash, so the classified listing is the landed diff only
#   when the server itself refuses a merge of a head that is not up to date, the main ruleset's
#   `strict_required_status_checks_policy` (require branches to be up to date before merging). The lever reads it
#   once, before the listing (require_ruleset_policy): `gh api "repos/{owner}/{repo}/rulesets"` lists the rulesets
#   (each `id`, `enforcement` and `target`, held to their types by the jq), and for each active branch ruleset the
#   per-id read `gh api "repos/{owner}/{repo}/rulesets/<id>"` gives its `conditions.ref_name.include` and
#   `exclude` lists and the `strict_required_status_checks_policy` of its `required_status_checks` rule; a ruleset
#   applies to `main` the way GitHub decides it (round 10, the round-9 P1 at :921, where a ruleset including
#   `~DEFAULT_BRANCH` and excluding `refs/heads/main` counted, and a glob never did): some include pattern matches
#   `refs/heads/<base>` and no exclude pattern does, `~DEFAULT_BRANCH` matching the default branch, `~ALL` every
#   branch and any other pattern an fnmatch glob over the full ref name (`refs/heads/ma*`, `refs/heads/**`;
#   ref_pattern_matches), and `strict_policy` is `true` when at least one applying ruleset's rule has it true, else
#   `false`. A failed read, a value that is not a boolean, an id that is no number, an enforcement that is none of
#   GitHub's three, two such rules in one ruleset, a shape the jq cannot hold, and no applying ruleset holding the
#   rule at all are failures (exit 1, never read as true). While the policy is `false` (today's value, measured
#   2026-11-19; only the repository's admin can change it, asked in U613) the lever grants no exemption: a
#   `not-required` head reads no daily row, `sweep_reason` names the policy and U613, and require_sweep_row runs as
#   for a required head, so every head gets its per-head sweep as before U597 and the daily machinery is dormant;
#   when it is `true` GitHub refuses a merge of a head behind `main`, the classified listing is the landed diff by
#   construction (the window is closed by the server, not by a check), and the daily rule applies as rounds 4 to 8
#   built it. The post-merge first-parent read (`gh api repos/{owner}/{repo}/commits/<commit> --jq '.parents[0].sha'`,
#   status read, 40 hex) stays as the lever's own record of what it merged onto: a parent other than the tip read
#   earlier is exit 1 with no receipt naming the merge commit, its parent and that tip, and the
#   coordinator sweeps the merge commit (the hcom-orchestration SKILL step 6). Round 9 also reads the daily
#   freshness again right before the merge request, after the CI read and the final pull request reread, with the
#   same window (recheck_daily_sweep): a head that rested on a daily row whose window closed during the checks is
#   refused, never merged on a sweep that no longer stands. The window is measured at that read, the lever's last
#   before the merge request, which precedes GitHub's write by one API round trip (round 10, the round-9 P3 at
#   :1556): the daily sweep stands within 24 hours at the lever's last read before the merge request, not at the
#   moment GitHub writes the squash. And the daily row is read by its own grammar (daily_row_fields), the verifier
#   `security-audit-skill <pin> (full audit mode on the srt worker seat <seat>, run-<n>; TASK daily-<YYYY-MM-DD>)`
#   and the evidence `sweeps/<path>.json; <n> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs
#   PASS; validators sha256 <8 hex> <8 hex> <8 hex>; artifacts sha256 <8 hex> <8 hex>; recorded <ts>`, the three
#   digest prefixes the writer checked (round 10: `report-schema.json`'s too, the round-9 P2 at ledger-row.py:575)
#   held to the manifest's `assets.security-audit-skill.validators_sha256` pins through one probe
#   (validators_pin_probe), and the two artifact digests (the writer's copies of the findings file and the coverage
#   ledger, the bytes its count and PASS words attest; round 10, the P2 at ledger-row.py:574) required by shape alone
#   (two 8-hex words; the lever never opens the findings file), so a row of a unit's sweep shape (`TASK U<n>`, no
#   validators) or one whose validators were held to other pins admits nothing.
# @arg $1 int The pull request number.
# @option --records <dir> The program store holding `ledger.tsv`, `verdicts/`, `dispositions.tsv` and `units.tsv`
#   (required; must resolve to the store `store_resolve` chose: `${REGIME_STORE_ROOT}/<program>` when it exists, else
#   the checkout's own store, above; a directory naming the other form, or any other directory, is refused).
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `merged pr=<pr> head=<head> commit=<merge commit> verdict=<ledger row ts>` (the `carried` row's ts for a carried head).
# @exitcode 0 The pull request is merged at the head.
# @exitcode 1 A `gh` or `git` read (the rulesets listing or a ruleset's read, a ruleset id, enforcement, target,
#   `conditions.ref_name.include` or `exclude` or `strict_required_status_checks_policy` of another shape than the
#   lever reads, two `required_status_checks` rules in one ruleset, no active ruleset applying to the base holding that
#   rule (round 9; round 10: applying by GitHub's include and exclude matching), the tip
#   of `main` that fails or is not 40 hex, the compare listing, a response
#   whose `files` is not an array or whose `merge_base_commit.sha` is no string, and a first line that is not
#   `merge-base <40 hex>` among its failures), the manifest pin probes, the scope reader or the ledger reader (any
#   status but 0 or 2), or the merge, failed; or the merge commit's first parent could not be read, is not 40 hex, or
#   is not the tip of `main` read before the listing (round 8: the merge happened on a moved `main`; no receipt, and
#   the coordinator sweeps the merge commit).
# @exitcode 2 Refused: usage, the pull request's state, no `correct` or `carried` row for the head, a head whose merge
#   base with `main` is not `main`'s tip (not up to date: rebase onto `main` and re-run the audit; round 7), a compare
#   listing that names no file, a scope answer the checkout's `sweep-scope.py` refuses (its exit 2: a listing that is not one
#   JSON array of status, filename and previous_filename per file, a `previous_filename` neither a string nor null, a
#   rename without its source, or a path git would not list) or that is neither `not-required` nor `required
#   <class>` (`required cap`, the listing at the compare API's cap, is a required class to this gate), a `daily-sweeps.tsv` that is
#   a symlink or not a regular file of this user, one the checkout's `ledger.py` cannot read as data (its exit 2
#   naming the line and field), a daily answer of the reader that is neither `none` nor one row of four tab-separated
#   fields with a ts and a 40-hex head, a daily row whose verifier or evidence is not the exact row of the rule (as
#   for a unit's sweep row, below) or not the daily row's own grammar (the verifier's seat, run and `TASK
#   daily-<YYYY-MM-DD>`, the evidence's seven fields, the three validator digest prefixes held to the manifest's
#   `validators_sha256` pins, the two artifact digests by shape; round 9, round 10), a daily row whose window closed
#   between the first read and the merge request (recheck_daily_sweep), no `sweep` row of
#   the unit or a fix unit of it at the audited head when the sweep row is required (a class, no daily sweep of
#   main's head within 86400 seconds, or the main ruleset's `strict_required_status_checks_policy` false, U613,
#   under which no head is exempt), a sweep answer of the reader that is
#   neither `none` nor one row of four tab-separated fields with a ts, a sweep row whose verifier is not
#   `security-audit-skill <pin>` with the
#   pin word a prefix (8 or more characters) of the manifest's `assets.security-audit-skill.pin`, whose evidence does
#   not name a regular file of this user `sweeps/<path>.json` under the store, reached through real directories alone
#   and resolving under the resolved store's `sweeps/` (round 5), or a manifest without that one pin, a
#   ledger the checkout's `ledger.py` cannot read as data (a ts outside `YYYY-MM-DDThh:mm:ssZ` or outside the
#   calendar, a wrong header or column count, an empty required cell, a sweep or audit row whose head is not 40 hex, a
#   `sweep` row that is not the exact row of the Audit sweep rule, pr `-`, verifier `security-audit-skill <pin>` and
#   evidence `sweeps/<path>.json`: the reader's exit 2), no python3 or no `scripts/orchestrator/ledger.py` or
#   `scripts/orchestrator/sweep-scope.py` in the
#   checkout, a reader whose copy's sha256 differs from its `claude.levers.sha256.<name>` pin or whose pin is missing
#   or doubled in the manifest, a private directory or a copy the lever cannot make (round 8), a `carried` row whose evidence names no `carried <earlier> <head> <sha256>` for this head or whose
#   earlier head has no `correct` row, no verdict file for the audited head, a P2 or P3 finding of weight 10 or more
#   without its `residual` disposition row, a malformed verdict file, `dispositions.tsv` or `units.tsv`, a store path
#   that is a symlink or outside the checkout, CI that is not green on the head, or CI that lists no passing result
#   for a check of REQUIRED_CHECKS (U330).
# @example
#   ~/.local/bin/common/pr-merge.sh 480 --records .orchestration/orchestrate/regime-cutover
#   ~/.local/bin/common/pr-merge.sh 480 --records ~/.local/state/regime-store/dotfiles/regime-cutover
set -euo pipefail

# @description Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31):
#   `~/.agents/agent-config.yaml` for the installed copy under ~/.local/bin/common, which a sandboxed session cannot
#   write, else the checkout's home/dot_agents/agent-config.yaml. Every read is checked; a failure exits 2 naming the
#   file. The pin is the `claude.levers.sha256.<name>` line, which `scripts/generate-agent-configs.py` refreshes.
# @set LEVER_MANIFEST The manifest the pin came from.
lever_self_check() {
    local src dir self name pin digest home
    # The directory is split from the path in the shell, so no external producer (dirname) can fail unseen.
    src=${BASH_SOURCE[0]}
    case ${src} in
    */*) dir=${src%/*} ;;
    *) dir=. ;;
    esac
    [[ -n ${dir} ]] || dir=/
    dir=$(cd "${dir}" && pwd -P) || {
        echo "${src##*/}: refused: cannot resolve the script directory of ${src}" >&2
        exit 2
    }
    self=${dir}/${BASH_SOURCE[0]##*/}
    # shellcheck disable=SC2034 # read by the levers that source regime-env from this directory
    LEVER_DIR=${dir}
    name=${self##*/}
    home=$(cd "${HOME}" 2> /dev/null && pwd -P) || home=''             # producer-status: allow the if below takes an empty home as the checkout layout
    if [[ -n ${home} && ${dir} == "${home}/.local/bin/common" ]]; then # lint-comparisons: allow both sides are pwd -P forms
        LEVER_MANIFEST=${HOME}/.agents/agent-config.yaml
    else
        LEVER_MANIFEST=${dir}/../../home/dot_agents/agent-config.yaml
    fi
    [[ -r ${LEVER_MANIFEST} ]] || {
        echo "${name}: refused: manifest unreadable: ${LEVER_MANIFEST}" >&2
        exit 2
    }
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") || {
        echo "${name}: refused: cannot read ${LEVER_MANIFEST}" >&2
        exit 2
    }
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: no single sha256 pin for ${name} in ${LEVER_MANIFEST}" >&2
        exit 2
    }
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    else
        digest=$(shasum -a 256 < "${self}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || {
        echo "${name}: refused: cannot hash ${self}" >&2
        exit 2
    }
    [[ ${digest} == "${pin}" ]] || {
        echo "${name}: refused: sha256 ${digest} of ${self} differs from the pin in ${LEVER_MANIFEST}" >&2
        exit 2
    }
}
lever_self_check
# The isolated git and the environment scrub come from the library beside this script (U113). The checkout is named
# from the cwd alone: a caller's repository-location variables could point git at another checkout's store (U71), so
# every GIT_* and transport variable goes before the first git.
[[ -r ${LEVER_DIR}/git-isolated.sh ]] || {
    echo "pr-merge.sh: refused: git-isolated.sh unreadable beside this script: ${LEVER_DIR}/git-isolated.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/git-isolated.sh
. "${LEVER_DIR}/git-isolated.sh"
# shellcheck disable=SC2119 # no name is kept: every GIT_* and transport variable goes
git_env_scrub

[[ -r ${LEVER_DIR}/read-lib.sh ]] || {
    echo "pr-merge.sh: refused: read-lib.sh unreadable beside this script: ${LEVER_DIR}/read-lib.sh" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/read-lib.sh
. "${LEVER_DIR}/read-lib.sh"

# The store root (regime-cutover U216): the program stores lie under `REGIME_STORE_ROOT`, the root the sourced
# regime-env derives from the physical HOME and this checkout's slug (U215) and holds component by component; the
# helper is sourced from the directory this lever runs from and self-checked like a lever (U33), so a rewritten copy
# stops this lever. The call that derives the root comes after this lever's own checkout checks, below.
[[ -r ${LEVER_DIR}/regime-env ]] || {
    echo "pr-merge.sh: refused: regime-env unreadable beside this script: ${LEVER_DIR}/regime-env" >&2
    exit 2
}
# shellcheck source=scripts/orchestrator/regime-env
. "${LEVER_DIR}/regime-env"

lever='pr-merge.sh'
usage='usage: pr-merge.sh <pr> --records <dir>'
gh_timeout=${PR_LEVER_GH_TIMEOUT:-60}
dispositions_header=$'ts\tunit\thead_sha\tpriority\tpath\tline\tdisposition\treference'
# `units.tsv` as the `hcom-orchestration` SKILL ("Rows") has it; a residual reference's unit must be an `id` of it.
units_header=$'id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote'
# The body's program marker, the grammar regime-ci.py and pr-body-edit.sh read; the unit names the verdict file.
program_unit_re='^Program-Unit: ([a-z0-9][a-z0-9_-]{0,63})/(U[0-9]+)$'
# The checks a merge needs, by name (regime-cutover U330): the required status contexts of the main ruleset `main
# integration gate` (`gh api repos/mryfmo/dotfiles/rulesets/24397953`, the `required_status_checks` rule), the exact
# strings GitHub lists them under (`<job> (<matrix values>)` for a matrix job), measured 2026-11-07T03:34Z (decisions
# row 2026-11-07T03:35:00Z). A constant, not a rulesets API read per merge: the list is the program's record of what a
# merge needs, a ruleset the operator edits is not, and the read would be one more `gh` call in the merge window.
# tests.unit.test_pr_merge holds this array equal to the contexts recorded from that measurement, so a drift between
# the lever and the ruleset fails CI, not a merge; a change to the ruleset is a change here and in that test. Every
# name must be listed by `gh pr checks` with bucket `pass`: a pull request that conflicts with main gets none of its
# `pull_request` workflows (GitHub runs them on the merge ref), and before U330 its three passing checks (`regime`, a
# `pull_request_target` workflow; GitGuardian; CodeRabbit, skipping) satisfied the gate with no test leg run (PR 708
# at 792604f9, decisions row 2026-11-07T01:45:00Z).
REQUIRED_CHECKS=(
    'public-bootstrap (macos-15, client)'
    'public-bootstrap (ubuntu-24.04, client)'
    'public-bootstrap (ubuntu-24.04, server)'
    'regime'
    'test (macos-15, client)'
    'test (ubuntu-24.04, client)'
    'test (ubuntu-24.04, server)'
    'validate'
)
# A finding's weight is its frequency times its severity, each 1 to 10 as pr-audit.sh's schema bounds them. A P0 or
# P1 line at or above this threshold blocks a merge under a `correct` row; a line of any priority under it is filed,
# reported in the verdict with the code left as it is, and needs no dispositions.tsv row (regime-cutover U125). The
# number is the one of the AGENTS.md verdict bullet and of the reader's WEIGHT_THRESHOLD, named once here.
WEIGHT_THRESHOLD=10
# A `## Findings` list line as pr-audit.sh's reader writes it since U125, `- P<n> (<confidence>) [f<n> s<n>]
# <path>:<line>: <rationale>`, read from its structure (U119 round 4, audit of dc08660f): the two scores are the
# text between `[f` and ` s` and between ` s` and the first `]`, each read by value as one of the strings 1 to 10
# (score_re; `0`, `11`, `x` or `05` is a malformed line, never a weight); the path is the first token after `] `
# that holds no colon and no whitespace, the line the digits after its colon, and the rationale everything after
# the `: ` that follows, free text that may hold a `<path>:<line>:` of its own. The first token is the location
# because the writer's grammar puts it first and a disposition row names that first location, so no other location
# can satisfy the row (U207: the path group was `(.+)`, which POSIX gives the longest text the whole match allows, so
# a rationale of the form `Carried P2 at hcom-seat:1548: ...` made the path `hcom-seat:1548: Carried P2 at hcom-seat`
# and the gate refused a well-formed line of the U190 verdict). The character class of the path group is the whole
# path rule, so a path with a colon or a space is a line finding_re does not match, and no second check on the
# matched path exists. A line without the `[f<n> s<n>]` token is refused naming the line: this branch's reader always
# writes it, and a verdict of the unscored reader belongs to a merged unit, never to a merge head.
finding_re='^- (P[0-3]) \((high|medium|low)\) \[f([^]]*) s([^]]*)\] ([^[:space:]:]+):([1-9][0-9]*): '
score_re='^(10|[1-9])$'
# The grammar of the leading `## Findings` section, stated once here and once in audit-carry.py (FINDINGS_GRAMMAR),
# which reads the same files: one `- none` line, or one or more finding_re lines whose scores match score_re; an
# empty section, `- none` beside a finding line, or `- none` twice is a malformed verdict (round 2). The two readers
# are run over one fixture set by tests.unit.test_pr_levers.
findings_grammar="the leading '## Findings' section is one '- none' line, or one or more lines '- P<n> (<confidence>) [f<n> s<n>] <path>:<line>: <rationale>' with scores 1 to 10 and a path free of colons and whitespace; the path is the first such token; the rationale after the line's ': ' is free text"
# The pin the sweep must have run at (U147 round 4, Codex thread 4457544811): `assets.security-audit-skill.pin` of the
# manifest the self-check read (LEVER_MANIFEST), the one place the skill's pin is declared. This probe, run as
# `python3 -I -S -c` with the manifest as its argument, prints the pin or exits 2 with one stderr line, and the lever
# requires the sweep row's pin word to be a prefix of it. `-S` leaves no PyYAML, so the manifest is read as text by one
# indentation rule: a bare `<key>:` line opens a
# mapping and a line indented no deeper closes it, so `security-audit-skill:` counts only under the top-level `assets:`,
# and the pin is the one `pin: <40 hex>` line at the indentation of that asset's first field (the field
# scripts/validate-agent-assets.py:1252-1254 reads as `asset.get("pin")`; a git-commit pin is a 40-hex sha). Nothing
# else of YAML is read: no anchors, no flow style, no quoted keys. Zero or two pin lines, a manifest that cannot be
# read or is not UTF-8, and any other exception are exit 2 naming the manifest (standing order 21: never a pass).
# Single-quoted, so the Python holds no single quote.
sweep_pin_probe='import re
import sys

manifest = sys.argv[1]
MAPPING_KEY = re.compile(r"^(\S+):$")
PIN = re.compile(r"^pin: ([0-9a-f]{40})$")
try:
    try:
        with open(manifest, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        print(f"manifest: cannot read {manifest}: {error}", file=sys.stderr)
        sys.exit(2)
    pins = []
    keys = []
    asset = None
    fields = None
    for line in lines:
        text = line.lstrip(" ")
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        if asset is not None:
            if indent > asset:
                if fields is None:
                    fields = indent
                match = PIN.match(text)
                if match and indent == fields:
                    pins.append(match.group(1))
                continue
            asset = None
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if [key for _, key in keys] == ["assets", "security-audit-skill"]:
                asset = indent
                fields = None
    if len(pins) != 1:
        print(f"manifest: {manifest} holds {len(pins)} assets.security-audit-skill.pin lines of 40 hex, not one", file=sys.stderr)
        sys.exit(2)
except SystemExit:
    raise
except BaseException as error:
    print(f"manifest: cannot read {manifest}: {type(error).__name__}: {error}", file=sys.stderr)
    sys.exit(2)
print(pins[0])'
# The three validator pins of the daily row (U597 round 9; round 10 added the schema's, the round-9 P2 at
# ledger-row.py:575): `assets.security-audit-skill.validators_sha256.<file>` of LEVER_MANIFEST, read by the
# indentation rule of sweep_pin_probe (ledger-row.py's manifest_asset reads the writer's side the same way): under the
# asset's `validators_sha256:` key, the one `<file>: <64 hex>` line of each of `validate-findings.cjs`,
# `validate-coverage-ledger.cjs` and `report-schema.json`, printed as one tab-separated line in that order. A daily row
# carries the first 8 hex of the digests its writer checked (`validators sha256 <8 hex> <8 hex> <8 hex>`), and
# daily_row_fields requires each to be a prefix of the pin here, so a row whose validators or schema were held to other
# pins admits nothing. Zero or two lines of a key, a manifest that cannot be read or is not UTF-8, and any other
# exception are exit 2 naming the manifest and the key (standing order 21). Single-quoted, so the Python holds no
# single quote.
validators_pin_probe='import re
import sys

manifest = sys.argv[1]
VALIDATORS = ("validate-findings.cjs", "validate-coverage-ledger.cjs", "report-schema.json")
MAPPING_KEY = re.compile(r"^(\S+):$")
DIGEST = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*): ([0-9a-f]{64})$")
try:
    try:
        with open(manifest, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        print(f"manifest: cannot read {manifest}: {error}", file=sys.stderr)
        sys.exit(2)
    keys = []
    asset = None
    fields = None
    digests_open = False
    digest_fields = None
    digests = {}
    for line in lines:
        text = line.lstrip(" ")
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        if asset is not None:
            if indent > asset:
                if fields is None:
                    fields = indent
                if indent == fields:
                    digests_open = text == "validators_sha256:"
                    digest_fields = None
                elif digests_open and indent > fields:
                    if digest_fields is None:
                        digest_fields = indent
                    match = DIGEST.match(text)
                    if match and indent == digest_fields:
                        digests.setdefault(match.group(1), []).append(match.group(2))
                continue
            asset = None
            fields = None
            digests_open = False
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if [key for _, key in keys] == ["assets", "security-audit-skill"]:
                asset = indent
                fields = None
    pins = []
    for validator in VALIDATORS:
        found = digests.get(validator, [])
        if len(found) != 1:
            print(f"manifest: {manifest} holds {len(found)} assets.security-audit-skill.validators_sha256.{validator} lines of 64 hex, not one", file=sys.stderr)
            sys.exit(2)
        pins.append(found[0])
except SystemExit:
    raise
except BaseException as error:
    print(f"manifest: cannot read {manifest}: {type(error).__name__}: {error}", file=sys.stderr)
    sys.exit(2)
print("\t".join(pins))'
# The probe's answer: the three pins, 64 hex each, tab-separated.
validators_pins_re="^([0-9a-f]{64})"$'\t'"([0-9a-f]{64})"$'\t'"([0-9a-f]{64})\$"
# The daily row's own grammar (U597 round 9; the round-8 P2 at ledger.py:393: the daily reader applied the sweep row's
# grammar, so a row of a unit's shape, `TASK U9` and no validators, stood as the day's sweep of main's head): the
# verifier as `ledger-row.py daily` composes it, the skill, its pin word (8 or more lowercase hex, a prefix of the
# manifest's pin, held by sweep_row_fields), the seat, the run and the task `daily-<YYYY-MM-DD>`; the evidence's seven
# `; `-separated fields (round 10), the findings file (held by sweep_row_fields), the count, the two validators' PASS
# words, the three digest prefixes the writer checked (8 hex each, prefixes of the manifest's `validators_sha256` pins
# of the two validators and the schema), the two artifact digest prefixes (8 hex each, the writer's copies of the
# findings file and the coverage ledger; required by shape, never compared: the lever opens neither file) and the
# recording time. `ledger.py` refuses any other daily row as a malformed store (parse_daily); the lever holds the row
# by its shape all the same (daily_row_fields), as it holds a unit's sweep row.
daily_verifier_re='^security-audit-skill [0-9a-f]{8,} \(full audit mode on the srt worker seat [^[:space:]]+, run-(0|[1-9][0-9]*); TASK daily-[0-9]{4}-[0-9]{2}-[0-9]{2}\)$'
daily_evidence_re='^sweeps/[^;[:space:]]+\.json; (0|[1-9][0-9]*) findings; validate-findings\.cjs PASS; validate-coverage-ledger\.cjs PASS; validators sha256 ([0-9a-f]{8}) ([0-9a-f]{8}) ([0-9a-f]{8}); artifacts sha256 [0-9a-f]{8} [0-9a-f]{8}; recorded [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
# The reference of a `residual` disposition row, the thread rule's form (pr-threads-check.sh `disposition`).
residual_re='^unit=(U[0-9]+[a-z]?) gate=[^[:space:]]'

# A verdict column that starts with the word `correct` (never `incorrect`): `correct`, `correct (…)`, `correct;…`.
correct_re='^correct($|[[:space:](;,])'
# A verdict column that starts with the word `carried` (U122), and the evidence such a row must hold: the line
# audit-carry.py prints, `carried <earlier head> <this head> <sha256 of the diff>`, as a whole word sequence anywhere
# in the column. The coordinator may write a note after it: the digest ends at the end of the column, whitespace or
# one of `;`, `,`, `.` and `)` (U180: the README's receipt form `carried <a> <b> <digest>; verdicts/...` was refused
# and a row rewritten), and a 65th hex-like character is no digest.
carried_re='^carried($|[[:space:](;,])'
carried_evidence_re='(^|[[:space:]])carried ([0-9a-f]{40}) ([0-9a-f]{40}) ([0-9a-f]{64})($|[[:space:];,.)])'

# @description Print the refusal on stderr and exit 2; nothing was merged.
# @arg $@ string The reason.
refuse() {
    echo "${lever}: refused: $*" >&2
    exit 2
}

# @description Print the failure on stderr and exit 1: a read or the merge failed.
# @arg $@ string The reason.
fail() {
    echo "${lever}: $*" >&2
    exit 1
}

# @description Run `gh` with its wait bounded by PR_LEVER_GH_TIMEOUT seconds.
# @arg $@ string The `gh` arguments.
gh_bounded() {
    perl -e 'alarm shift; exec @ARGV or die "exec gh: $!\n"' "${gh_timeout}" gh "$@"
}

# @description Print `<ts>\t<unit>\t<verdict>\t<evidence>` of the newest ledger row for pull request $1 at the full sha $2, or nothing
#   when no row names that pair, as the checkout's `scripts/orchestrator/ledger.py` answers it (`ledger.py <store>
#   verdict <pr> <head>`, run as `python3 -I -S` with its status read; U122 round 6). Newest by the ts column parsed as
#   a time, never by the row's place in the file (round 5), and the ledger is read whole as data first: a ts the
#   calendar does not hold (hour 25; round 6 P1: this lever's own awk checked the shape alone, so such a `carried` row
#   outranked a valid `incorrect` one), a header that is not the store's, a column count other than the header's or
#   an empty required cell is the reader's exit 2, a refusal naming the file and line; any other failure of the reader
#   exits 1. The reader compares every cell as text, so two different all-digit shas never match (U71 audit round 1).
#   The file run is the lever's pinned copy of the reader, `ledger_copy` (reader_copy, round 8); the refusals name
#   the checkout's path.
# @arg $1 int The pull request number.
# @arg $2 string The 40-hex head sha.
ledger_verdict() {
    local out status=0
    out=$("${python}" -I -S "${ledger_copy}" "${store}" verdict "$1" "$2" 2>&1) || status=$?
    case ${status} in
    0) [[ ${out} == none ]] || printf '%s' "${out}" ;;
    2) refuse "${out#ledger: }" ;;
    *) fail "${ledger_reader} exited ${status} reading ${ledger}: ${out:-no output}" ;;
    esac
}

# @description Refuse unless the newest ledger row (by ts) for pull request ${pr} at sha $1 is `correct`, or is `carried`
#   (U122, standing order 38) with an evidence that names this head and an earlier head whose own newest row (by ts)
#   is `correct`. One gate function decides both: a `carried` row whose earlier head has no `correct` row refuses, and
#   the head whose verdict file and dispositions the merge then reads is the earlier one. The row's `unit` column
#   must be the body's unit or a fix unit of it (`U<n>[a-z]`, standing order 24), and it names the verdict file and
#   the disposition rows the merge reads (round 2: the body's unit opened `U71-<sha8>.md` for a `U71b` row).
# @arg $1 string The 40-hex sha the verdict must name.
# @set verdict_ts The row's ts.
# @set audited_head The head whose verdict file and dispositions hold for $1: $1 itself, or the carried row's earlier head.
# @set audited_unit The unit of the row that judged audited_head, which names its verdict file.
require_verdict_row() {
    local row rest verdict evidence earlier named earlier_row earlier_verdict own_unit_re
    own_unit_re="^${unit}[a-z]?\$"
    row=$(ledger_verdict "${pr}" "$1") || exit $?
    [[ -n ${row} ]] || refuse "${ledger} has no row for pull request ${pr} at head ${1} (a short sha never matches)"
    verdict_ts=${row%%$'\t'*}
    rest=${row#*$'\t'}
    audited_unit=${rest%%$'\t'*}
    rest=${rest#*$'\t'}
    verdict=${rest%%$'\t'*}
    evidence=${rest#*$'\t'}
    audited_head=$1
    [[ ${audited_unit} =~ ${own_unit_re} ]] ||
        refuse "the newest ${ledger} row for pull request ${pr} at ${1} (${verdict_ts}) is unit ${audited_unit}, not the body's unit ${unit} or a fix unit of it (U<n>[a-z]); the row's unit names the verdict file"
    if [[ ${verdict} =~ ${correct_re} ]]; then
        return 0
    fi
    [[ ${verdict} =~ ${carried_re} ]] ||
        refuse "the newest ${ledger} row for pull request ${pr} at ${1} (${verdict_ts}) is not correct: ${verdict}"
    [[ ${evidence} =~ ${carried_evidence_re} ]] ||
        refuse "the carried ${ledger} row for pull request ${pr} at ${1} (${verdict_ts}) names no 'carried <earlier head> <head> <sha256>' in its evidence, the line audit-carry.py printed: ${evidence}"
    earlier=${BASH_REMATCH[2]}
    named=${BASH_REMATCH[3]}
    [[ ${named} == "$1" ]] ||
        refuse "the carried ${ledger} row (${verdict_ts}) carries ${named}, not this head ${1}"
    [[ ${earlier} != "$1" ]] ||
        refuse "the carried ${ledger} row (${verdict_ts}) carries ${1} from itself; a carried head rests on an earlier audited head"
    earlier_row=$(ledger_verdict "${pr}" "${earlier}") || exit $?
    [[ -n ${earlier_row} ]] ||
        refuse "the carried ${ledger} row (${verdict_ts}) rests on ${earlier}, which has no row for pull request ${pr}; a carried head needs the earlier head's correct row"
    rest=${earlier_row#*$'\t'}
    audited_unit=${rest%%$'\t'*}
    rest=${rest#*$'\t'}
    earlier_verdict=${rest%%$'\t'*}
    [[ ${earlier_verdict} =~ ${correct_re} ]] ||
        refuse "the carried ${ledger} row (${verdict_ts}) rests on ${earlier}, whose newest row (${earlier_row%%$'\t'*}) is not correct: ${earlier_verdict}"
    [[ ${audited_unit} =~ ${own_unit_re} ]] ||
        refuse "the carried ${ledger} row (${verdict_ts}) rests on ${earlier}, whose newest row (${earlier_row%%$'\t'*}) is unit ${audited_unit}, not the body's unit ${unit} or a fix unit of it (U<n>[a-z]); the row's unit names the verdict file"
    audited_head=${earlier}
}

# @description Print the data rows of the TSV file $1, CR stripped and the header dropped, when its first line is the
#   header $2, every row has the header's column count and no column numbered in $3 is empty; refuse otherwise,
#   naming the line. awk splits on the tab alone (`-F'\t'`), so an empty field is still a field: bash's `read` with a
#   tab IFS merges adjacent tabs, which let a nine-column row with an empty field pass as eight (U119 round 3). The
#   rows are printed as they are read, so on a refusal the last output line is the reason; a failed read exits 1.
# @arg $1 path The file.
# @arg $2 string The header line, tab-separated.
# @arg $3 string The 1-based numbers of the columns that may not be empty, space-separated.
# @stdout The data rows, one per line.
table_rows() {
    local out status=0
    out=$(TABLE_HEADER=$2 TABLE_REQUIRED=$3 awk -F'\t' '
        BEGIN { required = split(ENVIRON["TABLE_REQUIRED"], column, " ") }
        { sub(/\r$/, "") }
        NR == 1 {
            if ($0 != ENVIRON["TABLE_HEADER"]) { print; exit 3 }
            width = NF
            for (i = 1; i <= NF; i++) name[i] = $i
            next
        }
        NF != width { printf "line %d has %d columns, not %d: %s\n", NR, NF, width, $0; exit 4 }
        {
            for (i = 1; i <= required; i++) {
                if ($(column[i]) == "") { printf "line %d: column %d (%s) is empty: %s\n", NR, column[i], name[column[i]], $0; exit 4 }
            }
            print
        }
        END { if (NR == 0) exit 3 }
    ' "$1") || status=$?
    case ${status} in
    0) printf '%s' "${out}" ;;
    3) refuse "$1 does not start with the header (${2//$'\t'/ }); line 1: ${out##*$'\n'}" ;;
    4) refuse "$1 ${out##*$'\n'}" ;;
    *) fail "cannot read $1" ;;
    esac
}

# @description Succeed when the store's `units.tsv` has a row whose `id` is $1. The table is read once per run and
#   checked as every table is (its header, each row's column count, a non-empty `id`); a symlink or a missing file is
#   a refusal naming it and a failed read exits 1 (standing order 21), never "no row". The cache and its flag are
#   locals of require_dispositions, assigned empty there before this function runs (U119 round 6, audit of 4f9f958a):
#   a `units_rows` the caller exported was taken as the table already read, so a row it held passed the lookup
#   without being in `units.tsv`. Nothing this function reads comes from outside this run.
# @arg $1 string The unit id.
# @set units_rows The table's data rows, read once; the caller's local.
# @set units_read Non-empty once `units_rows` holds the table; the caller's local.
# @exitcode 0 Found. 1 Not found.
unit_row_exists() {
    local row
    if [[ -z ${units_read} ]]; then
        [[ ! -L ${units_file} && -f ${units_file} && -O ${units_file} ]] ||
            refuse "${units_file} is not a regular file of this user (a symlink or missing); a residual's unit is judged against it"
        units_rows=$(table_rows "${units_file}" "${units_header}" '1') || exit $?
        units_read=1
    fi
    while IFS= read -r row; do
        [[ ${row%%$'\t'*} == "$1" ]] && return 0
    done <<< "${units_rows}"
    return 1
}

# @description Set `priority`, `path` and `lineno` from a pending entry of require_dispositions (U119 round 5),
#   `<priority>\t<path>\t<lineno>`, by parameter expansion and no `IFS` write: the fields are the lever's own matched
#   text (finding_re), so none is empty and the path holds no tab.
# @arg $1 string The entry.
# @set priority path lineno The three fields.
pending_fields() {
    priority=${1%%$'\t'*}
    lineno=${1##*$'\t'}
    path=${1#*$'\t'}
    path=${path%$'\t'*}
}

# @description Refuse unless every P2 and P3 finding of the head's verdict file in the store has a holding `residual`
#   row in `dispositions.tsv` (U119 round 2): the ledger row says `correct`, and since standing order 35 `correct` no
#   longer means "no finding". Every read is checked; a failed read exits 1 (standing order 21). Every name the gate
#   reads is a local assigned here before its first read, the `units.tsv` cache of unit_row_exists included, so a
#   caller's environment holds nothing the gate takes for its own data (U119 round 6).
# @arg $1 string The 40-hex head the ledger row named (the audited head).
# @arg $2 string The unit of that ledger row, which names the verdict file and the disposition rows (round 2).
# @arg $3 string The 40-hex head being merged: $1 itself under a `correct` row, the carried head under a `carried` row
#   (U180: a `fixed` row whose reference starts with this sha holds when it differs from $1).
require_dispositions() {
    local head=$1 row_unit=$2 merge_head=$3 verdicts_dir verdict_file dispositions text line section=0 seen=0 last='' n=1 satisfied status
    local findings=() pending=() rows=() cols=() entry priority frequency severity weight path lineno why residual_unit none_seen='' listed=''
    local units_rows='' units_read=''
    # The reference of a `fixed` row as the coordinator writes it: a 40-hex sha first, then prose (U180). The sha is the
    # whole first token (the end or a character outside hex after it), so a 41-hex prefix of another sha never matches.
    local fixed_reference_re='^([0-9a-f]{40})($|[^0-9a-f])'
    verdicts_dir=${store}/verdicts
    [[ ! -L ${verdicts_dir} && -d ${verdicts_dir} && -O ${verdicts_dir} ]] ||
        refuse "${verdicts_dir} is not a directory of this user (a symlink or missing); the verdict file is read from the checkout's own store"
    verdict_file=${verdicts_dir}/${row_unit}-${head:0:8}.md
    [[ ! -L ${verdict_file} && -f ${verdict_file} && -O ${verdict_file} && -r ${verdict_file} ]] ||
        refuse "${verdict_file} is not a readable regular file of this user; a merge needs the verdict file of the head, not only its ledger row"
    text=$(cat -- "${verdict_file}") || fail "cannot read ${verdict_file}"
    # Only the leading `## Findings` section is read (U119 round 4, audit of dc08660f): from the first `## Findings`
    # line to the next `## ` heading. A later `## Findings` line, in the Notes the reader copies from the model or in
    # a rationale, is text, never a second list.
    while IFS= read -r line; do
        line=${line%$'\r'}
        [[ -n ${line} ]] || continue
        last=${line}
        if ((seen == 0)); then
            [[ ${line} != '## Findings' ]] || seen=1 section=1
            continue
        fi
        ((section == 1)) || continue
        if [[ ${line} == '## '* ]]; then
            section=0
            continue
        fi
        findings+=("${line}")
    done <<< "${text}"
    ((seen == 1)) ||
        refuse "${verdict_file} has no '## Findings' section; the gate reads the verdict.md pr-audit.sh writes (a '## Findings' list of '- P<n> (<confidence>) [f<n> s<n>] <path>:<line>: <rationale>' or '- none', then 'Blocking: <n>', 'Filed: <n>' and the last line 'Verdict: <value>'); a verdict of the retired omp-run.sh audit route has no such section and no merge head has one"
    [[ ${last} == 'Verdict: correct' ]] ||
        refuse "the last line of ${verdict_file} is not 'Verdict: correct' although the ledger row for ${head} is: ${last}"
    ((${#findings[@]} > 0)) || refuse "${verdict_file}: the Findings section lists nothing; ${findings_grammar}"
    for entry in ${findings[@]+"${findings[@]}"}; do
        if [[ ${entry} == '- none' ]]; then
            [[ -z ${none_seen} ]] || refuse "${verdict_file}: the Findings section lists '- none' more than once; ${findings_grammar}"
            none_seen=1
            continue
        fi
        listed=1
        [[ ${entry} =~ ${finding_re} ]] ||
            refuse "${verdict_file}: a Findings line is not '- P<n> (<confidence>) [f<n> s<n>] <path>:<line>: <rationale>' with a path free of colons and whitespace, the first such token (the reader writes the frequency and severity scores since U125; a line without them is the unscored reader's, whose verdicts belong to merged units, never to a merge head): ${entry}"
        priority=${BASH_REMATCH[1]} frequency=${BASH_REMATCH[3]} severity=${BASH_REMATCH[4]} path=${BASH_REMATCH[5]} lineno=${BASH_REMATCH[6]}
        [[ ${frequency} =~ ${score_re} ]] ||
            refuse "${verdict_file}: a Findings line's frequency score 'f${frequency}' is not one of 1 to 10, so its weight cannot be read: ${entry}"
        [[ ${severity} =~ ${score_re} ]] ||
            refuse "${verdict_file}: a Findings line's severity score 's${severity}' is not one of 1 to 10, so its weight cannot be read: ${entry}"
        # Both scores matched score_re, so the product is arithmetic on two small decimals the gate itself read.
        weight=$((frequency * severity))
        case ${priority} in
        P0 | P1)
            ((weight < WEIGHT_THRESHOLD)) ||
                refuse "${verdict_file} lists ${priority} at ${path}:${lineno} under a correct ledger row with weight ${weight} (f${frequency} s${severity}); a P0 or P1 of weight ${WEIGHT_THRESHOLD} or more blocks (standing order 35, the AGENTS.md Audit rule), so the row or the file is wrong"
            ;;
        esac
        # Under the threshold the finding is filed (U125): reported, the code left as it is, no disposition row asked.
        ((weight >= WEIGHT_THRESHOLD)) || continue
        pending+=("${priority}"$'\t'"${path}"$'\t'"${lineno}")
    done
    [[ -z ${none_seen} || -z ${listed} ]] || refuse "${verdict_file}: the Findings section lists '- none' beside a finding line; ${findings_grammar}"
    ((${#pending[@]} > 0)) || return 0
    dispositions=${store}/dispositions.tsv
    pending_fields "${pending[0]}"
    [[ ! -L ${dispositions} && -f ${dispositions} && -O ${dispositions} && -r ${dispositions} ]] ||
        refuse "${verdict_file} lists ${priority} at ${path}:${lineno} and ${dispositions} is not a readable regular file of this user; every P2 and P3 finding of a correct verdict needs its residual row before the merge"
    # Every column of a disposition row is required, so a validated row holds no adjacent tabs and `read` splits it
    # into its eight fields; the column count and the empty-field check are awk's (table_rows), never bash's.
    text=$(table_rows "${dispositions}" "${dispositions_header}" '1 2 3 4 5 6 7 8') || exit $?
    while IFS= read -r line; do
        [[ -n ${line} ]] || continue
        n=$((n + 1))
        IFS=$'\t' read -ra cols <<< "${line}"
        case ${cols[6]} in
        residual | fixed) ;;
        *) refuse "${dispositions} line ${n}: disposition '${cols[6]}' is neither residual nor fixed" ;;
        esac
        rows+=("${line}")
    done <<< "${text}"
    for entry in ${pending[@]+"${pending[@]}"}; do
        pending_fields "${entry}"
        why="no ${dispositions} row for unit ${row_unit}, head ${head}, ${priority} at ${path}:${lineno}"
        satisfied=0
        for line in ${rows[@]+"${rows[@]}"}; do
            IFS=$'\t' read -ra cols <<< "${line}"
            [[ ${cols[1]} == "${row_unit}" && ${cols[2]} == "${head}" && ${cols[3]} == "${priority}" && ${cols[4]} == "${path}" && ${cols[5]} == "${lineno}" ]] || # lint-comparisons: allow the path column is matched as the text the reader wrote, never resolved
                continue
            if [[ ${cols[6]} == fixed ]]; then
                # U180: under a carried row the head being merged differs from the audited head, and a fix at a
                # carried head can only be a body fix (a code change would have changed the digest), so a `fixed`
                # row whose reference names the head being merged holds for the audited head it judges.
                if [[ ${head} != "${merge_head}" && ${cols[7]} =~ ${fixed_reference_re} ]] &&
                    [[ ${BASH_REMATCH[1]} == "${merge_head}" ]]; then
                    satisfied=1
                    break
                fi
                why="the row at ${cols[0]} says fixed in ${cols[7]}, which is not this head; merge the head that fixed it"
                continue
            fi
            [[ ${cols[7]} =~ ${residual_re} ]] || {
                why="the row at ${cols[0]} is residual but its reference is not 'unit=U<n> gate=<clause>': ${cols[7]}"
                continue
            }
            residual_unit=${BASH_REMATCH[1]}
            status=0
            unit_row_exists "${residual_unit}" || status=$?
            if ((status == 0)); then
                satisfied=1
                break
            fi
            why="the row at ${cols[0]} is residual for ${residual_unit}, which is not a row of ${units_file}"
        done
        ((satisfied == 1)) ||
            refuse "${verdict_file} lists ${priority} at ${path}:${lineno} without a holding disposition: ${why}; write the residual row (unit=U<n> gate=<clause>, U<n> a units.tsv row) or fix it in a new head"
    done
}

# @description Whether one `conditions.ref_name` pattern of a ruleset matches a ref the way GitHub matches it
#   (regime-cutover U597 round 10; the round-9 P1 at :921, where require_ruleset_policy compared each include and
#   exclude entry with the two literals `~DEFAULT_BRANCH` and `refs/heads/<base>` alone, so a ruleset including
#   `~DEFAULT_BRANCH` and excluding `refs/heads/main` counted, one including `refs/heads/ma*` never did, and a strict
#   rule that did not apply to `main` could grant the exemption without the server-side protection it rests on).
#   GitHub's documented syntax for ruleset targets (docs.github.com, "Creating rulesets for a repository", read
#   2026-11-19): `~DEFAULT_BRANCH` matches the default branch (`main`, the base this lever requires at the top),
#   `~ALL` matches every branch, and any other pattern is an fnmatch glob over the full ref name, `refs/heads/ma*`,
#   `refs/heads/**`, where `**` matches across `/`. The two tilde words are handled first; the glob is bash's own
#   `[[ == ]]` pattern match over the ref with `**` turned into `*`: bash's pattern `*` has no `/` boundary either, so
#   `*` already crosses `/` and the two spell one match (`?` and `[...]` are fnmatch's in both), and the right-hand
#   side stays unquoted on purpose, since it is the pattern.
# @arg $1 string The pattern as GitHub lists it.
# @arg $2 string The ref name, `refs/heads/<base>`.
# @exitcode 0 The pattern matches the ref.
# @exitcode 1 It does not.
ref_pattern_matches() {
    local pattern=$1 ref=$2
    case ${pattern} in
    '~DEFAULT_BRANCH') [[ ${ref} == "refs/heads/${base}" ]] ;; # lint-comparisons: allow the ref name is compared as the text GitHub lists, never resolved
    '~ALL') return 0 ;;
    *)
        # shellcheck disable=SC2053
        [[ ${ref} == ${pattern//\*\*/\*} ]] # lint-comparisons: allow the ref name is matched against GitHub's glob as text, never resolved
        ;;
    esac
}

# @description Read the main ruleset's up-to-date policy once, before the listing (regime-cutover U597 round 9; the
#   round-8 P1 at :1282, the second strike of the diff-basis class, and the mechanism-change decisions row of
#   2026-11-19T11:56:54Z): the lever classifies the diff against a snapshot of `main`, and no client-side read can pin
#   `main` at the moment GitHub writes the squash, so the only pre-merge control is the server's own, the main
#   ruleset's `strict_required_status_checks_policy` (require branches to be up to date before merging). The rulesets
#   are listed once, `gh api "repos/{owner}/{repo}/rulesets"` with a jq that holds the response to an array and each
#   ruleset's `id` to a number, `enforcement` and `target` to strings (`<id>\t<enforcement>\t<target>` per ruleset);
#   an enforcement that is none of `active`, `evaluate` or `disabled` is a failure, and the active branch rulesets are
#   read one by one, `gh api "repos/{owner}/{repo}/rulesets/<id>"` with a jq that prints `include <ref>` for each entry
#   of `conditions.ref_name.include` (an array of strings, else its error), `exclude <ref>` for each of `exclude`
#   (an array of strings; null read as none; else its error), and `strict <true|false>` for each
#   `required_status_checks` rule's `strict_required_status_checks_policy` (a boolean, else its error). A ruleset
#   applies to the base when some include pattern matches `refs/heads/<base>` and no exclude pattern does, each
#   pattern read as GitHub reads it (ref_pattern_matches, round 10: `~DEFAULT_BRANCH`, `~ALL`, else a glob over the
#   full ref name); `strict_policy` is `true` when at least one applying ruleset's rule has it true, else `false`.
#   Two such rules in one ruleset, a line the lever did not ask for, a failed read and no applying ruleset holding
#   the rule at all are failures (exit 1): the policy is never read as true from a shape the lever does not know,
#   and never read as false by default either, since an unread policy would hide a ruleset the operator set
#   (standing order 21). The value is printed once on stderr.
# @set strict_policy `true` or `false`, the policy as read; nothing else (every other outcome is a failure).
require_ruleset_policy() {
    local listing line id enforcement target rules kind value includes excluded strict rest listed='' with_rule=''
    local ref="refs/heads/${base}"
    listing=$(gh_bounded api "repos/{owner}/{repo}/rulesets" --jq '(if type == "array" then . else error("rulesets is " + type + ", not an array") end) | .[] | [(.id | if type == "number" then tostring else error("id is " + type + ", not a number") end), (.enforcement | if type == "string" then . else error("enforcement is " + type + ", not a string") end), (.target | if type == "string" then . else error("target is " + type + ", not a string") end)] | @tsv') ||
        fail "cannot list the rulesets (gh api repos/{owner}/{repo}/rulesets), or the listing is not an array of rulesets with a numeric id and string enforcement and target (the jq's own error names the field); whether the main ruleset requires branches to be up to date before merging (strict_required_status_checks_policy) decides whether any head is exempt from its per-head sweep, so an unread policy admits no exemption and no merge"
    strict_policy=false
    # One ruleset per line, `<id>\t<enforcement>\t<target>`, each cell the text up to the next tab.
    while IFS= read -r line; do
        [[ -n ${line} ]] || continue
        id=${line%%$'\t'*}
        rest=${line#*$'\t'}
        enforcement=${rest%%$'\t'*}
        target=${rest#*$'\t'}
        [[ ${id} =~ ^[1-9][0-9]*$ ]] ||
            fail "the rulesets listing (gh api repos/{owner}/{repo}/rulesets) names a ruleset id that is not a decimal number: '${id}'; the policy is read from a shape the lever knows alone"
        case ${enforcement} in
        active) ;;
        evaluate | disabled) continue ;;
        *) fail "the rulesets listing names an enforcement that is none of active, evaluate or disabled for ruleset ${id}: '${enforcement}'; the policy is read from a shape the lever knows alone" ;;
        esac
        [[ ${target} == branch ]] || continue
        rules=$(gh_bounded api "repos/{owner}/{repo}/rulesets/${id}" --jq '((.conditions.ref_name.include | if type == "array" then . else error("conditions.ref_name.include is " + type + ", not an array") end) | .[] | "include " + (if type == "string" then . else error("a ref_name.include entry is " + type + ", not a string") end)), ((.conditions.ref_name.exclude | if type == "array" then . elif . == null then [] else error("conditions.ref_name.exclude is " + type + ", not an array") end) | .[] | "exclude " + (if type == "string" then . else error("a ref_name.exclude entry is " + type + ", not a string") end)), ((.rules | if type == "array" then . else error("rules is " + type + ", not an array") end) | .[] | select(.type == "required_status_checks") | "strict " + (.parameters.strict_required_status_checks_policy | if type == "boolean" then tostring else error("strict_required_status_checks_policy is " + type + ", not a boolean") end))') ||
            fail "cannot read ruleset ${id} (gh api repos/{owner}/{repo}/rulesets/${id}), or its shape is not the one the lever reads (conditions.ref_name.include and exclude arrays of strings, rules an array whose required_status_checks rule has a boolean strict_required_status_checks_policy; the jq's own error names the field); the policy decides whether any head is exempt from its per-head sweep, so an unread policy admits no exemption and no merge"
        includes='' excluded='' strict=''
        while IFS= read -r line; do
            [[ -n ${line} ]] || continue
            kind=${line%% *}
            value=${line#* }
            case ${kind} in
            include) ! ref_pattern_matches "${value}" "${ref}" || includes=1 ;;
            exclude) ! ref_pattern_matches "${value}" "${ref}" || excluded=1 ;;
            strict)
                case ${value} in
                true | false) ;;
                *) fail "ruleset ${id} answered a strict_required_status_checks_policy that is neither true nor false: '${value}'; the policy is never read as true from a shape the lever does not know" ;;
                esac
                [[ -z ${strict} ]] ||
                    fail "ruleset ${id} holds two required_status_checks rules; the lever reads one strict_required_status_checks_policy per ruleset and takes no side"
                strict=${value}
                ;;
            *) fail "the read of ruleset ${id} (gh api repos/{owner}/{repo}/rulesets/${id}) printed a line the lever did not ask for: '${line}'" ;;
            esac
        done <<< "${rules}"
        # The ruleset applies to the base as GitHub applies it: some include pattern matches the ref and no exclude
        # pattern does (round 10).
        [[ -n ${includes} && -z ${excluded} ]] || continue
        listed+="${listed:+, }${id}"
        [[ -n ${strict} ]] || continue
        with_rule+="${with_rule:+, }${id}"
        [[ ${strict} != true ]] || strict_policy=true
    done <<< "${listing}"
    [[ -n ${with_rule} ]] ||
        fail "no active branch ruleset applying to ${ref} (an include pattern matching it, ~DEFAULT_BRANCH, ~ALL or a glob, and no exclude pattern matching it; applying: ${listed:-none}) holds a required_status_checks rule, so strict_required_status_checks_policy cannot be read (gh api repos/{owner}/{repo}/rulesets); the policy decides whether any head is exempt from its per-head sweep, and an unread policy admits no exemption and no merge (the main ruleset 'main integration gate', 24397953, holds the rule; U613 asks the operator to set it)"
    echo "${lever}: ruleset: strict_required_status_checks_policy ${strict_policy} (active ruleset(s) on ${base} with a required_status_checks rule: ${with_rule})" >&2
}

# @description Decide whether the head needs its sweep row (regime-cutover U597, the operator's sweep rule C of
#   2026-11-18): the audited head's changed files as data, the diff the squash lands, listed by the GitHub compare
#   API keyed by two shas. First the tip of the base is read once, `gh api "repos/{owner}/{repo}/git/ref/heads/${base}"
#   --jq '.object.sha'`, with its status read and the value held to 40 hex (anything else, `null` for a missing
#   object included, is a failure; round 7). Then one compare call, `gh api
#   "repos/{owner}/{repo}/compare/${base_tip}...${head}" --jq '("merge-base " + (.merge_base_commit.sha | if type ==
#   "string" then . else error("merge_base_commit.sha is " + type + ", not a string") end)), ((if (.files | type) ==
#   "array" then .files else error("files is " + (.files | type) + ", not an array") end) | .[] | [.status,
#   .filename, (if has("previous_filename") then .previous_filename else null end)] | @json)'`, whose first line is
#   `merge-base <sha>`, the response's `merge_base_commit.sha`, and whose other lines are one JSON array per file.
#   The merge base must equal the base tip, else the head is refused naming both shas: `pr merge --squash` lands the
#   diff against the base's tip, while the three-dot compare lists the diff from the merge base, and when the base
#   moved after the branch point the two differ (round 7, the round-6 P1: a base-side rename can carry an exempt
#   edit into a sweep-class path, and rounds 4 to 6 compared `main...<head>` with neither check nor pin of the tip).
#   With the head up to date (the merge base the tip itself) the three-dot diff equals the two-dot diff against the
#   tip, the diff the squash lands, and the compare keyed by the two shas is that listing or a failure. Round 4 (the
#   mechanism change): rounds 1 to 3 listed the pull request's files by its number, `gh pr diff --name-only` and then
#   the files endpoint, and no reread around a number-keyed listing binds it to the audited head, since the pull
#   request's head can move between the listing and the read; the compare request names the shas, so its answer is
#   that head's diff or a failure, and a listing of another head cannot be substituted. `base` is the pull request's
#   base the first view read and required to be `main`, `head` the pinned full sha. Round 5 (the round-4 P1 and its
#   first P2): the compare response carries `files` on its first page alone, at most 300 entries, and `per_page`
#   pages its commits, not its files (docs.github.com, REST API, commits, compare two commits, read 2026-11-19), so
#   the call is one, with no paging, and completeness is read from the listing itself: the reader counts the entries
#   and answers `required cap` for 300 or more, a listing that may be cut short, which this function treats as
#   `required <class>` does (`sweep_class=cap`, the cap's reason), and under 300 the listing is whole and the classes
#   decide; the pull request's file count of rounds 3 and 4 was a read keyed by the pull request's number that no pin
#   bound to the audited head, and it is gone with the reader's count option. A response whose `files` is not an
#   array (null for a key missing from a later page or a shape the API changed; an object, a string, a number or a
#   boolean) is the jq's own error, `(if (.files | type) == "array" then .files else error("files is " + (.files |
#   type) + ", not an array") end)`, so the call fails and the failure names it with the type, never an empty listing
#   read as "not required" (round 6, the round-5 P1: round 5's `(.files // error("no files key")) | .[]` iterated an
#   object's values, so a response whose `files` was one file record as an object was read as a listing of that one
#   file; the type is checked before anything iterates), and a `merge_base_commit.sha` that is no string is the jq's
#   error the same way. This lever reads no local git object, so no planted replace ref or graft can narrow the
#   listing. A listing that fails is a failure, a first line that is not `merge-base <40 hex>` a failure, and a
#   listing that names no file a refusal (standing order 21: a head that changes nothing is nothing to merge, and a
#   listing cut short is never "not required"). The file lines go on stdin to the checkout's
#   `sweep-scope.py --files-json`, the one definition of the classes, run as `python3 -I -S` as the ledger reader is, with its status
#   read as ledger_verdict reads it: 2 a refusal carrying its line (a line of another shape, a rename without its
#   source, a `previous_filename` that is neither a string nor null, which the jq passes through as it is and never
#   maps to null, round 4), any other non-zero a failure. The exit-0 answer is read by its shape: `required cap` sets
#   `sweep_class` to `cap` and `sweep_reason` to the cap's clause; `required <class>` with the class one lowercase
#   word (letters and hyphens) sets `sweep_class` to it and `sweep_reason` to the class clause; `not-required` alone
#   sets `sweep_class` empty and, while `strict_policy` is `true`, asks require_daily_sweep whether the standing
#   control stands (round 4: the exemption is bound to the daily sweep; round 9: and to the main ruleset's up-to-date
#   policy, read by require_ruleset_policy before this function runs, since the classified listing is the landed diff
#   only while the server refuses a merge of a head behind `main`; while the policy is `false` the daily row is not
#   read, `sweep_reason` names the policy and U613, and require_sweep_row runs as for a required head, so no head is
#   exempt); anything else, a second line included, is a refusal naming the reader and the
#   answer. The lever reads the listing as text it passes on and judges no class itself. The reader run is the
#   lever's pinned copy, `scope_copy` (reader_copy, round 8); the refusals name the checkout's path.
# @set base_tip The tip of the base read before the listing, 40 hex; after the merge the merge commit's first parent must equal it (round 8).
# @set sweep_class The class that requires the sweep (`credential`, `policy`, `lever`, `deployed-executable`), `cap` for a listing at the compare API's cap, or empty when none does.
# @set sweep_reason Why require_sweep_row runs, named in its refusal: the class clause, the cap clause, or the missing daily sweep (require_daily_sweep); empty when the head skips the row.
require_sweep_scope() {
    local status=0 listing merge_base files answer class
    base_tip=$(gh_bounded api "repos/{owner}/{repo}/git/ref/heads/${base}" --jq '.object.sha') ||
        fail "cannot read the tip of ${base} (gh api repos/{owner}/{repo}/git/ref/heads/${base}); the head's changed paths are listed against it, so the listing is the diff the squash lands"
    [[ ${base_tip} =~ ^[0-9a-f]{40}$ ]] ||
        fail "the tip of ${base} read from gh api repos/{owner}/{repo}/git/ref/heads/${base} is not 40 hex: '${base_tip}'; the head's changed paths are listed against it, so the listing is the diff the squash lands"
    listing=$(gh_bounded api "repos/{owner}/{repo}/compare/${base_tip}...${head}" --jq '("merge-base " + (.merge_base_commit.sha | if type == "string" then . else error("merge_base_commit.sha is " + type + ", not a string") end)), ((if (.files | type) == "array" then .files else error("files is " + (.files | type) + ", not an array") end) | .[] | [.status, .filename, (if has("previous_filename") then .previous_filename else null end)] | @json)') ||
        fail "cannot list the changed paths of the head ${head} of pull request ${pr} (gh api repos/{owner}/{repo}/compare/${base_tip}...${head}); the sweep scope is decided from them, and a response whose files is not an array (null for a key missing from a later page or a shape the API changed; an object, a string, a number or a boolean) or whose merge_base_commit.sha is no string is this failure through the jq's error(\"files is <type>, not an array\") or error(\"merge_base_commit.sha is <type>, not a string\"), never an empty listing"
    merge_base=${listing%%$'\n'*}
    [[ ${merge_base} =~ ^merge-base\ ([0-9a-f]{40})$ ]] ||
        fail "the compare API (gh api repos/{owner}/{repo}/compare/${base_tip}...${head}) answered with a first line that is not 'merge-base <40 hex>': '${merge_base}'; the merge base is read beside the files, in the same call, so the listing can be held to the diff the squash lands"
    merge_base=${BASH_REMATCH[1]}
    [[ ${merge_base} == "${base_tip}" ]] ||
        refuse "the head ${head} of pull request ${pr} is not up to date with ${base} (merge base ${merge_base}, ${base} tip ${base_tip}); rebase the branch onto ${base} and re-run the audit, so the listing is the diff the squash lands"
    files=''
    [[ ${listing} != *$'\n'* ]] || files=${listing#*$'\n'}
    [[ -n ${files} ]] ||
        refuse "the compare API (gh api repos/{owner}/{repo}/compare/${base_tip}...${head}) listed no changed path of the head ${head} of pull request ${pr}; a head that changes nothing is nothing to merge, and a listing cut short is never 'not required' (standing order 21)"
    answer=$("${python}" -I -S "${scope_copy}" --files-json <<< "${files}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${answer#sweep-scope: }" ;;
    *) fail "${scope_reader} exited ${status} reading the changed paths of the head ${head} of pull request ${pr}: ${answer:-no output}" ;;
    esac
    case ${answer} in
    not-required)
        sweep_class=''
        if [[ ${strict_policy} == true ]]; then
            require_daily_sweep
        else
            # Round 9: while the main ruleset does not hold `main` still at the merge, the classified listing is not
            # known to be the landed diff, so no head is exempt and the daily row is not read (U613).
            sweep_reason="this head changes no sweep-class path, but the main ruleset does not require branches to be up to date before merging (strict_required_status_checks_policy false), so the diff the squash lands is not the diff classified and no head is exempt; the per-head sweep stands (U613)"
        fi
        ;;
    'required cap')
        # The listing is at the compare API's cap (round 5): 300 or more entries, so it may be cut short and the
        # per-head sweep stands, as for a class.
        sweep_class=cap
        sweep_reason="the head changes 300 or more files, the compare API's cap, so the listing may be cut short and the per-head sweep stands"
        ;;
    'required '*)
        class=${answer#required }
        [[ ${class} =~ ^[a-z][a-z-]*$ ]] ||
            refuse "${scope_reader} answered the sweep scope question for pull request ${pr} with 'required ${class}', not required <class> with the class one lowercase word"
        sweep_class=${class}
        sweep_reason="this head changes a ${sweep_class} path"
        ;;
    *) refuse "${scope_reader} answered the sweep scope question for pull request ${pr} with neither not-required nor required <class>: ${answer:-nothing}" ;;
    esac
}

# The window of the daily sweep (U597 round 4): a row of the store's `daily-sweeps.tsv` whose ts is within this many
# seconds of now stands for a head outside every class; the rule's one day, named once here and in the reader's call.
DAILY_SWEEP_MAX_AGE=86400

# @description Read the daily sweep of main's head within the window (regime-cutover U597 round 4; round 9 split it
#   from require_daily_sweep so that recheck_daily_sweep reads the same way right before the merge write): the rows
#   live in the store's `daily-sweeps.tsv` (header `ts head_sha verifier evidence`; `ledger-row.py daily` writes them
#   after the coordinator's daily dispatch, the hcom-orchestration SKILL step 4), held as the ledger is when the file
#   exists (a readable regular file of this user, no symlink; a missing file is `none` to the reader), and read by the
#   lever's pinned copy of `ledger.py` (`<store> daily <seconds>`, the one reader), run as `python3 -I -S` with its
#   status read as ledger_verdict reads it: 2 a refusal carrying its line (a malformed file naming the line and field,
#   standing order 21), any other non-zero a failure. The exit-0 answer is read by its shape: `none`, or one row of
#   four tab-separated fields (ts, head_sha, verifier, evidence) with a ts and a 40-hex head, whose verifier and
#   evidence are then held to the exact row of the rule as require_sweep_row holds a unit's row (sweep_row_fields:
#   the pin word a prefix of the manifest's pin, the findings file a regular file of this user under the store, never
#   opened) and to the daily row's own grammar (daily_row_fields, round 9: the seat, the run, the daily task, the
#   validators' PASS words and the three digest prefixes held to the manifest's `validators_sha256` pins, the two
#   artifact digests by shape; round 10); any other
#   answer is a refusal naming the reader and the answer.
# @set daily_row `none`, or the row as the reader printed it.
# @set daily_ts daily_head daily_verifier daily_evidence The row's four cells when daily_row is a row.
daily_sweep_read() {
    local status=0 daily_file rest subject
    daily_file=${store}/daily-sweeps.tsv
    if [[ -L ${daily_file} || -e ${daily_file} ]]; then
        [[ ! -L ${daily_file} && -f ${daily_file} && -O ${daily_file} && -r ${daily_file} ]] ||
            refuse "${daily_file} is not a readable regular file of this user (a symlink or another kind of entry); the daily sweep rows are read from the store alone"
    fi
    daily_row=$("${python}" -I -S "${ledger_copy}" "${store}" daily "${DAILY_SWEEP_MAX_AGE}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${daily_row#ledger: }" ;;
    *) fail "${ledger_reader} exited ${status} reading ${daily_file} for the daily sweep of main's head: ${daily_row:-no output}" ;;
    esac
    [[ ${daily_row} != none ]] || return 0
    # The answer is read by its shape, as require_sweep_row reads a row: one line of four tab-separated fields,
    # `<ts> <head_sha> <verifier> <evidence>`, with a ts and a 40-hex head.
    case ${daily_row//[!$'\t']/} in
    $'\t\t\t') ;;
    *) refuse "${ledger_reader} answered the daily sweep question with neither none nor one row of four tab-separated fields (ts, head_sha, verifier, evidence): ${daily_row:-nothing}" ;;
    esac
    daily_ts=${daily_row%%$'\t'*}
    rest=${daily_row#*$'\t'}
    daily_head=${rest%%$'\t'*}
    rest=${rest#*$'\t'}
    daily_verifier=${rest%%$'\t'*}
    daily_evidence=${rest#*$'\t'}
    [[ ${daily_row} != *$'\n'* && -n ${daily_ts} && ${daily_head} =~ ^[0-9a-f]{40}$ ]] ||
        refuse "${ledger_reader} answered the daily sweep question with text beside the row, an empty ts or a head that is not 40 hex, not one row of four tab-separated fields: ${daily_row}"
    subject="the daily sweep row of ${daily_ts} at main's head ${daily_head}"
    sweep_row_fields "${subject}" "${daily_verifier}" "${daily_evidence}"
    daily_row_fields "${subject}" "${daily_verifier}" "${daily_evidence}"
}

# @description Bind the exemption to its standing control (regime-cutover U597 round 4; the round-2 and round-3 P2 at
#   AGENTS.md:71): a head outside every sweep class skips its per-head sweep row only while the store holds a daily
#   sweep of main's head within the last DAILY_SWEEP_MAX_AGE seconds (24 hours), the standing control rule C rests on,
#   which until round 4 no merge gate read, so an exempt head could merge with no sweep anywhere near it; since round
#   9 only while require_ruleset_policy read the main ruleset's up-to-date policy as `true` (the caller's test). The
#   row is daily_sweep_read's: `none` sets `sweep_reason` so that require_sweep_row runs as for a required head (its
#   refusal names both: no daily sweep within the window, so the per-head rule stands); a row skips the per-head row
#   with one stderr line naming the daily row's ts and head, and recheck_daily_sweep reads the file again right
#   before the merge write.
# @set sweep_reason Empty when the daily sweep stands; the reason require_sweep_row names otherwise.
require_daily_sweep() {
    daily_sweep_read
    if [[ ${daily_row} == none ]]; then
        sweep_reason="this head changes no sweep-class path, but ${store}/daily-sweeps.tsv holds no daily sweep of main's head within the last ${DAILY_SWEEP_MAX_AGE} seconds (24 hours), so the per-head rule stands until the day's sweep runs and its row is written (ledger-row.py daily)"
        return 0
    fi
    sweep_reason=''
    echo "${lever}: sweep: not required (no lever, policy, credential or deployed-executable path changed); the daily sweep of main's head ${daily_head} at ${daily_ts} stands within ${DAILY_SWEEP_MAX_AGE} seconds" >&2
}

# @description Read the daily freshness again right before the merge request (regime-cutover U597 round 9; the round-8
#   P3 at :1282): the first read came before the CI read and the final pull request reread, and a row whose window
#   closed during those calls still authorized the merge after the 24 hours were over. The same read, the same window
#   (daily_sweep_read, DAILY_SWEEP_MAX_AGE): a row within the window, the one rested on or a newer one, stands and is
#   named on stderr; `none` is a refusal naming the row this head rested on, with no merge. This is the lever's last
#   read before the merge request, and the window is measured here: the request follows it by one API round trip,
#   and GitHub writes the squash after that, so the daily sweep stands within 24 hours at the lever's last read before
#   the merge request, not at the write (round 10, the round-9 P3 at :1556; no client-side read can sample the
#   server's clock at the write).
recheck_daily_sweep() {
    local rested_ts=${daily_ts} rested_head=${daily_head}
    daily_sweep_read
    [[ ${daily_row} != none ]] ||
        refuse "the daily sweep of main's head ${rested_head} at ${rested_ts}, which this head rested on, no longer stands within ${DAILY_SWEEP_MAX_AGE} seconds (24 hours) at the merge write: its window closed during the checks, so the per-head rule stands; run the day's sweep and write its row (ledger-row.py daily), or write the unit's sweep row, then run the lever again"
    echo "${lever}: sweep: the daily sweep of main's head ${daily_head} at ${daily_ts} still stands within ${DAILY_SWEEP_MAX_AGE} seconds at the merge write" >&2
}

# @description Hold a daily sweep row to its own grammar (regime-cutover U597 round 9; the round-8 P2 at ledger.py:393:
#   the daily reader applied the sweep row's grammar alone, so a recent row of a unit's shape, `TASK U9`, a pinned
#   verifier and an existing findings path, qualified as the day's sweep of main's head with no daily task and no
#   validator result), after sweep_row_fields held the fields the two rows share. The verifier is the one
#   `ledger-row.py daily` composes (daily_verifier_re: the skill, its pin word, the seat, the run, `TASK
#   daily-<YYYY-MM-DD>`), the evidence its seven fields (daily_evidence_re: the findings file, `<n> findings`, the two
#   validators' PASS words, `validators sha256 <8 hex> <8 hex> <8 hex>`, `artifacts sha256 <8 hex> <8 hex>`, `recorded
#   <ts>`; round 10), and each validator digest prefix must be a prefix of the manifest's
#   `assets.security-audit-skill.validators_sha256` pin of its file (validate-findings.cjs, validate-coverage-ledger.cjs
#   and, since round 10, report-schema.json: the round-9 P2 at ledger-row.py:575, where a row validated under another
#   schema still authorized an exemption), read through validators_pin_probe over LEVER_MANIFEST (exit 0 the three
#   pins, 2 a refusal carrying its line, anything else a failure), so a row whose validators or schema were held to
#   other pins than the manifest's admits nothing. The artifact digests are required by shape alone (two 8-hex
#   words), never compared: they are the writer's attestation that its count and PASS words were earned over one set
#   of bytes (the round-9 P2 at ledger-row.py:574), and the lever opens neither the findings file nor the coverage
#   ledger. `ledger.py` already refuses a daily row of another shape as a malformed store; the lever reads the answer
#   by its shape all the same. Every other shape is a refusal naming the row and the field.
# @arg $1 string The row, as the refusals name it (`the daily sweep row of <ts> at main's head <head>`).
# @arg $2 string The row's verifier.
# @arg $3 string The row's evidence.
daily_row_fields() {
    local subject=$1 verifier=$2 evidence=$3 status=0 pins findings_pin coverage_pin schema_pin findings_digest coverage_digest schema_digest
    [[ ${verifier} =~ ${daily_verifier_re} ]] ||
        refuse "${subject} names '${verifier}' as its verifier, not the daily row's own 'security-audit-skill <pin> (full audit mode on the srt worker seat <seat>, run-<n>; TASK daily-<YYYY-MM-DD>)' as ledger-row.py daily writes it; a row of a unit's sweep shape (TASK U<n>) is no daily sweep of main's head"
    [[ ${evidence} =~ ${daily_evidence_re} ]] ||
        refuse "${subject} names '${evidence}' as its evidence, not the daily row's own 'sweeps/<path>.json; <n> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; validators sha256 <8 hex> <8 hex> <8 hex>; artifacts sha256 <8 hex> <8 hex>; recorded <ts>' as ledger-row.py daily writes it; a row without the validators' results, the digests they were held to and the digests of the bytes they validated is no daily sweep of main's head"
    findings_digest=${BASH_REMATCH[2]}
    coverage_digest=${BASH_REMATCH[3]}
    schema_digest=${BASH_REMATCH[4]}
    pins=$("${python}" -I -S -c "${validators_pin_probe}" "${LEVER_MANIFEST}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${pins#manifest: }; the daily row's validator digests are compared with those pins, so a manifest without them admits no daily sweep" ;;
    *) fail "the validators pin probe over ${LEVER_MANIFEST} exited ${status}, neither the pins (0) nor a refusal (2): ${pins:-no output}" ;;
    esac
    [[ ${pins} =~ ${validators_pins_re} ]] ||
        refuse "the validators pin probe over ${LEVER_MANIFEST} answered with no three 64-hex pins: ${pins:-nothing}"
    findings_pin=${BASH_REMATCH[1]}
    coverage_pin=${BASH_REMATCH[2]}
    schema_pin=${BASH_REMATCH[3]}
    [[ ${findings_pin} == "${findings_digest}"* ]] ||
        refuse "${subject} names validators sha256 ${findings_digest} for validate-findings.cjs, which is not a prefix of the manifest's assets.security-audit-skill.validators_sha256.validate-findings.cjs ${findings_pin} (${LEVER_MANIFEST}); the sweep's validators were held to other pins than the manifest's, or the row was written by hand"
    [[ ${coverage_pin} == "${coverage_digest}"* ]] ||
        refuse "${subject} names validators sha256 ${coverage_digest} for validate-coverage-ledger.cjs, which is not a prefix of the manifest's assets.security-audit-skill.validators_sha256.validate-coverage-ledger.cjs ${coverage_pin} (${LEVER_MANIFEST}); the sweep's validators were held to other pins than the manifest's, or the row was written by hand"
    [[ ${schema_pin} == "${schema_digest}"* ]] ||
        refuse "${subject} names validators sha256 ${schema_digest} for report-schema.json, which is not a prefix of the manifest's assets.security-audit-skill.validators_sha256.report-schema.json ${schema_pin} (${LEVER_MANIFEST}); the sweep's validators were held to another schema than the manifest's, or the row was written by hand"
}

# @description Hold a sweep row's verifier and evidence to the exact row of the AGENTS.md Audit sweep rule (U147 round
#   4, Codex thread 4457544811: a row written by hand with verifier `coordinator` admitted the merge), one function
#   for the unit's row (require_sweep_row) and the daily row (require_daily_sweep, U597 round 4): the verifier's two
#   words are the skill's name and the pin word the sweep ran at, 8 or more lowercase hex, which must be a prefix of
#   the manifest's `assets.security-audit-skill.pin` (sweep_pin_probe over LEVER_MANIFEST: exit 0 the pin, 2 a
#   refusal carrying its line, anything else a failure); the findings file is the evidence's first `;`-separated
#   field stripped of whitespace, a relative path under `sweeps/` ending in `.json` with no `..`, `.` or empty
#   component, checked as the verdict file is (`sweeps/` a directory of this user and no symlink, then every
#   directory component between `sweeps/` and the file a directory of this user and no symlink, walked one by one
#   with `-L` on each, then the file `-f`, `-O`, `! -L`, then the realpath of the file's directory, `cd` and `pwd -P`,
#   under the realpath of the store's `sweeps/`; round 5: `-f` on the file alone followed a symlinked directory
#   between them, so a row could name a findings file outside the store) and never opened. The reader already refuses
#   a row of another shape as a malformed store; the lever reads the answer by its shape all the same. A pin that is
#   no prefix or a file that is missing, a symlink, another user's, behind a symlinked component or resolving outside
#   the store's `sweeps/` is a refusal naming it and the row.
# @arg $1 string The row, as the refusals name it (`the sweep row of U<n> at <head>`, `the daily sweep row of <ts> at main's head <head>`).
# @arg $2 string The row's verifier.
# @arg $3 string The row's evidence.
sweep_row_fields() {
    local subject=$1 verifier=$2 evidence=$3 status=0 pin_word manifest_pin findings_path sweeps_dir findings_file
    local relative component_dir resolved_store resolved_dir
    case ${verifier} in
    'security-audit-skill '*) ;;
    *) refuse "${subject} names '${verifier}' as its verifier, not the pinned skill and its pin (security-audit-skill <pin>); the gate admits the row the AGENTS.md Audit sweep rule defines alone" ;;
    esac
    pin_word=${verifier#security-audit-skill }
    pin_word=${pin_word%%[[:space:]]*}
    [[ ${pin_word} =~ ^[0-9a-f]{8,}$ ]] ||
        refuse "${subject} names '${pin_word}' as the skill's pin, not 8 or more lowercase hex characters of it"
    manifest_pin=$("${python}" -I -S -c "${sweep_pin_probe}" "${LEVER_MANIFEST}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${manifest_pin#manifest: }; the sweep row's pin is compared with that pin, so a manifest without it admits no sweep" ;;
    *) fail "the pin probe over ${LEVER_MANIFEST} exited ${status}, neither the pin (0) nor a refusal (2): ${manifest_pin:-no output}" ;;
    esac
    [[ ${manifest_pin} =~ ^[0-9a-f]{40}$ ]] ||
        refuse "the pin probe over ${LEVER_MANIFEST} answered with no 40-hex pin: ${manifest_pin:-nothing}"
    [[ ${manifest_pin} == "${pin_word}"* ]] ||
        refuse "${subject} names pin ${pin_word}, which is not a prefix of the manifest's assets.security-audit-skill.pin ${manifest_pin} (${LEVER_MANIFEST}); the sweep ran at another pin than the one the manifest pins, or the row was written by hand"
    findings_path=${evidence%%;*}
    findings_path=${findings_path#"${findings_path%%[![:space:]]*}"}
    findings_path=${findings_path%"${findings_path##*[![:space:]]}"}
    case ${findings_path} in # lint-comparisons: allow the row's store-relative path is judged as the text it is, then the file is stat'ed under the store
    sweeps/*.json) ;;
    *) refuse "${subject} names '${evidence}' as its evidence, not a findings file sweeps/<path>.json under the store" ;;
    esac
    case /${findings_path}/ in # lint-comparisons: allow the same text, its components fenced by slashes
    */../* | */./* | *//*) refuse "the findings file ${findings_path} of ${subject} has a '..', '.' or empty path component; the file is read under the store alone" ;;
    esac
    sweeps_dir=${store}/sweeps
    [[ ! -L ${sweeps_dir} && -d ${sweeps_dir} && -O ${sweeps_dir} ]] ||
        refuse "${sweeps_dir} is not a directory of this user (a symlink or missing); the findings file a sweep row names must be in the checkout's own store"
    # Every directory component between sweeps/ and the file, walked one by one (round 5): a symlinked directory
    # there carried a findings file from outside the store into the row, since `-f` on the file follows it.
    relative=${findings_path#sweeps/}
    component_dir=${sweeps_dir}
    while [[ ${relative} == */* ]]; do # lint-comparisons: allow the row's store-relative path is split as the text it is; each component is then stat'ed under the store
        component_dir=${component_dir}/${relative%%/*}
        relative=${relative#*/}
        [[ ! -L ${component_dir} && -d ${component_dir} && -O ${component_dir} ]] ||
            refuse "${component_dir}, a directory component of the findings file ${findings_path} that ${subject} names, is a symbolic link or not a directory of this user; the file is read under the store's sweeps/ through real directories alone"
    done
    findings_file=${store}/${findings_path}
    [[ ! -L ${findings_file} && -f ${findings_file} && -O ${findings_file} ]] ||
        refuse "${findings_file}, the findings file ${subject} names, is not a regular file of this user (a symlink or missing); a sweep whose findings file is not in the store admits no merge"
    # The resolved file lies under the resolved store's sweeps/ (round 5): the realpath of the file's directory and of
    # the store, `cd` and `pwd -P`, the lever's physical form; each read with its status.
    resolved_store=$(cd "${store}" 2> /dev/null && pwd -P) || fail "cannot resolve the store ${store} to its physical path"
    resolved_dir=$(cd "${findings_file%/*}" 2> /dev/null && pwd -P) || fail "cannot resolve the directory of the findings file ${findings_file} to its physical path"
    [[ ${resolved_dir}/ == "${resolved_store}/sweeps/"* ]] || # lint-comparisons: allow both sides are pwd -P forms
        refuse "the findings file ${findings_file} that ${subject} names resolves to ${resolved_dir}/${findings_file##*/}, outside the store's ${resolved_store}/sweeps/; a sweep whose findings file is not in the store admits no merge"
}

# @description Refuse unless the ledger holds the unit's sweep row at `audited_head` (regime-cutover U147, every unit
#   since U244, and since U597 only when require_sweep_scope found a class, `sweep_class`, or, since round 4, when a
#   head outside every class has no daily sweep of main's head within 24 hours to rest on (require_daily_sweep;
#   `sweep_reason` names which); the AGENTS.md Audit sweep rule: a head whose changed paths touch a lever, a policy,
#   credential handling or a deployed executable gets one sweep of the `security-audit` skill before its pull request
#   merges). The row is asked of the checkout's ledger.py (`sweep <unit> <head>`, the one reader, its status read as
#   ledger_verdict reads it and its exit-0 answer read by its shape, `none` or one row of four tab-separated fields
#   with a ts, as require_verdict_row reads a row) at `audited_head`: the head itself, or for a `carried` row the
#   earlier head whose verdict file the merge reads, so a head moved under a carried row needs no second sweep.
#   `none` is a refusal naming the unit, the head, the rule and the reason. The row must be the exact row of the rule
#   (Codex thread 4457544811: a row written by hand with verifier `coordinator` admitted the merge): the reader
#   already refuses a `sweep` row whose pr is not `-`, whose verifier is not `security-audit-skill <pin>` or whose
#   evidence is not `sweeps/<path>.json` as a malformed store, and the lever reads the answer by its shape all the
#   same, then holds the verifier and the evidence as sweep_row_fields does (the pin word a prefix of the manifest's
#   `assets.security-audit-skill.pin`, the findings file a regular file of this user under `<store>/sweeps/`, never
#   opened). The lever reads neither the findings file the row names nor the sweep's content.
require_sweep_row() {
    local status=0 row rest verifier evidence
    row=$("${python}" -I -S "${ledger_copy}" "${store}" sweep "${unit}" "${audited_head}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${row#ledger: }" ;;
    *) fail "${ledger_reader} exited ${status} reading ${ledger} for the sweep row of ${unit}: ${row:-no output}" ;;
    esac
    [[ ${row} != none ]] ||
        refuse "${ledger} has no sweep row for ${unit} (or a fix unit of it) at the audited head ${audited_head}; the AGENTS.md Audit sweep rule says a head whose changed paths touch a lever, a policy, credential handling or a deployed executable gets one sweep of the security-audit skill before its pull request merges, and ${sweep_reason} (a row with verdict sweep, pr -, head ${audited_head}); run the sweep and write its row, or wait for it"
    # The answer is read by its shape, as require_verdict_row reads a row (round 2, finding 3): one line of four
    # tab-separated fields, `<ts> <unit> <verifier> <evidence>`, with a ts. The tab count is the row with every other
    # byte removed, read as a word; the ts is the text before the first tab.
    case ${row//[!$'\t']/} in
    $'\t\t\t') ;;
    *) refuse "${ledger_reader} answered the sweep question for ${unit} at ${audited_head} with neither none nor one row of four tab-separated fields (ts, unit, verifier, evidence): ${row:-nothing}" ;;
    esac
    [[ ${row} != *$'\n'* && -n ${row%%$'\t'*} ]] ||
        refuse "${ledger_reader} answered the sweep question for ${unit} at ${audited_head} with text beside the row or an empty ts, not one row of four tab-separated fields: ${row}"
    # The row's columns as the reader prints them (ts, unit, verifier, evidence), each the text up to the next tab.
    rest=${row#*$'\t'}
    rest=${rest#*$'\t'}
    verifier=${rest%%$'\t'*}
    evidence=${rest#*$'\t'}
    sweep_row_fields "the sweep row of ${unit} at ${audited_head}" "${verifier}" "${evidence}"
}

# @description Choose the program store this lever reads (regime-cutover U216, store move 2 of 5,
#   handoff/07-store-move-design.md; U215 gave regime-env the root): the derived store `${REGIME_STORE_ROOT}/<program>`
#   when that directory exists, the root being the fixed derivation `<physical HOME>/.local/state/regime-store/<slug>`
#   the sourced regime-env exports after holding every component of it; else the pre-move form
#   `<toplevel>/.orchestration/orchestrate/<program>`, this main checkout's own store, which stands until U221 moves the
#   live store of this program to the root and removes this form. One rule, two forms: while the derived store exists
#   the checkout form is refused (the caller refuses a path naming it, naming both forms), and while it does not the
#   checkout form is read as before U216. The per-component holds of the chain walk (U71) stay and apply to the form
#   chosen: a symbolic link at `<root>/<program>` is refused by name before anything is read through it, an entry
#   there that is not a directory of this user is refused by name, and only an absent one falls through to the
#   checkout chain, whose three components are each a directory of this user and no symlink. The root's own
#   components are held by regime-env (`regime_store_root`). Nothing is written. The form chosen is printed once on
#   stderr (`store: derived <dir>`, or `store: checkout <dir> (pre-move form, removed by U221)`), the line the
#   coordinator reads after the deploy. The same text stands in pr-close.sh (two levers, standing order 36: no helper
#   file).
# @arg $1 string The program name.
# @set store The chosen store, `pwd -P` form (the root and the toplevel are both physical).
# @set store_form `derived` or `checkout`.
# @set store_derived The derived candidate `${REGIME_STORE_ROOT}/<program>`.
# @set store_checkout The checkout candidate `<toplevel>/.orchestration/orchestrate/<program>`.
store_resolve() {
    local program=$1 path part
    [[ -n ${REGIME_STORE_ROOT:-} ]] ||
        refuse "regime-env derived no store root for ${toplevel}; the program store is judged under it (U216)"
    store_derived=${REGIME_STORE_ROOT}/${program}
    store_checkout=${toplevel}/.orchestration/orchestrate/${program}
    [[ ! -L ${store_derived} ]] ||
        refuse "${store_derived} is a symlink; the derived program store is a plain directory of this user under the store root ${REGIME_STORE_ROOT}, and nothing is read through a link"
    if [[ -e ${store_derived} ]]; then
        [[ -d ${store_derived} && -O ${store_derived} ]] ||
            refuse "${store_derived} exists but is not a directory of this user; the derived program store under ${REGIME_STORE_ROOT} is read only as one"
        store=${store_derived}
        store_form=derived
        echo "${lever}: store: derived ${store}" >&2
        return 0
    fi
    path=${toplevel}
    for part in .orchestration orchestrate "${program}"; do
        path=${path}/${part}
        [[ -d ${path} && ! -L ${path} && -O ${path} ]] ||
            refuse "${path} is not a directory of this user (a symlink or a missing store); no derived store ${store_derived} exists, so ${lever} reads only the checkout's own store (the pre-move form, until U221)"
    done
    store=${store_checkout}
    store_form=checkout
    echo "${lever}: store: checkout ${store} (pre-move form, removed by U221)" >&2
}

# @description Set `ledger`, `store`, `units_file` and `unit` to the one store the merge may read (U71, bot P1
#   4370212009: a caller-chosen ledger.tsv could hold a fabricated row): the store `store_resolve` chooses for
#   `<program>` (U216: the derived store under `REGIME_STORE_ROOT` when it exists, else this main checkout's own
#   store, the pre-move form), `<program>` and `U<n>` taken from the pull request body's one
#   `Program-Unit: <program>/U<n>` line. No directory of the chosen chain and not the ledger is a symlink, each is
#   owned by this user, and `--records` must resolve (`pwd -P`) to exactly that directory: one that names the other
#   form is refused naming both forms, one outside the checkout while the checkout form stands is named as such, and
#   anything else is refused as not the program's store.
# @set ledger The canonical ledger path.
# @set store The canonical store directory.
# @set units_file The store's `units.tsv`, read by unit_row_exists.
# @set unit The body's unit id; a ledger row for the pull request must be it or a `U<n>[a-z]` fix unit of it, and the row's unit names the verdict file (require_verdict_row).
resolve_store() {
    local body markers line program given
    body=$(gh_bounded pr view "${pr}" --json body --jq .body) || fail "cannot read the body of pull request ${pr}"
    markers=''
    while IFS= read -r line; do
        line=${line%$'\r'}
        [[ ${line} == Program-Unit:* ]] && markers+="${line}"$'\n'
    done <<< "${body}"
    markers=${markers%$'\n'}
    [[ -n ${markers} && ${markers} != *$'\n'* && ${markers} =~ ${program_unit_re} ]] ||
        refuse "the body of pull request ${pr} must hold exactly one line 'Program-Unit: <program>/U<n>'; it holds: ${markers:-none}"
    program=${BASH_REMATCH[1]}
    unit=${BASH_REMATCH[2]}
    store_resolve "${program}"
    given=$(cd "${records}" 2> /dev/null && pwd -P) || refuse "--records ${records} is no directory"
    if [[ ${given} != "${store}" ]]; then # lint-comparisons: allow both sides are pwd -P forms (the root and the toplevel are physical)
        case ${store_form} in
        derived)
            [[ ${given} != "${store_checkout}" ]] || # lint-comparisons: allow both sides are pwd -P forms
                refuse "--records ${records} resolves to the checkout store ${given}, the pre-move form, but the derived store ${store} exists and is the program's store (U216); the checkout form is refused while it exists, until U221 removes it"
            ;;
        *)
            [[ ${given} == "${toplevel}/"* ]] || # lint-comparisons: allow both sides are pwd -P forms
                refuse "--records ${records} resolves to ${given}, outside the checkout ${toplevel}; no derived store ${store_derived} exists, so the merge reads only the checkout's own store (the pre-move form, until U221)"
            ;;
        esac
        refuse "--records ${records} is not the program's store ${store} (named by the body's Program-Unit line; the ${store_form} form)"
    fi
    ledger=${store}/ledger.tsv
    units_file=${store}/units.tsv
    [[ -f ${ledger} && ! -L ${ledger} && -O ${ledger} && -r ${ledger} ]] ||
        refuse "${ledger} is not a readable regular file of this user"
}

# @description Make the private directory the readers' copies live in (regime-cutover U597 round 8; the round-7 P1 at
#   :1123): `mktemp -d` under TMPDIR (the system temporary directory when unset) with `umask 077`, a directory of this
#   user and no symlink, mode 0700, removed on every exit by reader_copies_remove through the EXIT trap, which the
#   signal traps reach too. A directory that cannot be made or held is a refusal naming the place; nothing was read
#   from GitHub yet.
# @set reader_dir The directory, empty until made and after its removal.
reader_copies_make() {
    local base=${TMPDIR:-/tmp}
    reader_dir=$(umask 077 && mktemp -d "${base%/}/pr-merge.readers.XXXXXX") ||
        refuse "cannot make the private directory for the readers' copies under ${base} (mktemp -d); the readers run from copies held to their pins alone"
    [[ -n ${reader_dir} && ! -L ${reader_dir} && -d ${reader_dir} && -O ${reader_dir} ]] ||
        refuse "the private directory ${reader_dir} for the readers' copies is not a directory of this user"
    chmod 0700 "${reader_dir}" || refuse "cannot set mode 0700 on the private directory ${reader_dir} for the readers' copies"
}

# @description Remove the readers' copy directory (reader_copies_make) when one exists; a removal that fails is named,
#   and the function returns 0 either way, so the status the lever exits with is the gate's. Idempotent: the variable
#   is cleared first, so a refusal inside a removal cannot recurse into it (hcom-seat's helper_copy_remove).
reader_copies_remove() {
    local dir=${reader_dir:-}
    [[ -n ${dir} ]] || return 0
    reader_dir=''
    rm -rf -- "${dir}" || echo "${lever}: the readers' copy directory ${dir} remains after its removal; remove it by hand" >&2
}

# @description Read the reader $2 once into the lever's own copy `<reader_dir>/$1` (0600 under `umask 077`), hash the
#   copy and refuse unless its sha256 equals the `claude.levers.sha256.$1` pin of LEVER_MANIFEST, the manifest the
#   self-check read, with the readers lever_self_check uses (sed for the pin line; sha256sum, else shasum -a 256;
#   hcom-seat's helper_copy_make and helper_pin_check, U310f). What is hashed is what runs (`python3 -I -S <copy>`,
#   `ledger_copy` and `scope_copy`), and the path beside the checkout is never read again, so a file swapped after the
#   hash is not the file run (round 8; until then the lever ran the checkout's readers after an existence check alone,
#   so a rewritten reader could waive a required sweep). A copy that cannot be made, a pin that is missing or doubled,
#   a copy that cannot be hashed and a digest that differs from the pin are refusals naming the reader and, for a
#   differing digest, both digests.
# @arg $1 string The reader's name, the key of its pin.
# @arg $2 string The reader's path in the checkout, named in the refusals.
# @set reader_copy_path The copy, the file the lever runs.
reader_copy() {
    local name=$1 origin=$2 copy pin digest
    copy=${reader_dir}/${name}
    (umask 077 && cat -- "${origin}" > "${copy}") ||
        refuse "cannot copy the reader ${origin} into ${reader_dir}; the reader runs from a copy held to its pin alone"
    pin=$(sed -n -E "s/^      ${name//./\\.}: ([0-9a-f]{64})\$/\\1/p" "${LEVER_MANIFEST}") ||
        refuse "cannot read ${LEVER_MANIFEST} for the pin of ${name}"
    [[ ${pin} =~ ^[0-9a-f]{64}$ ]] ||
        refuse "no single sha256 pin for ${name} in ${LEVER_MANIFEST} (claude.levers.sha256.${name}); the reader ${origin} runs only from a copy held to that pin"
    if command -v sha256sum > /dev/null; then
        digest=$(sha256sum < "${copy}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    else
        digest=$(shasum -a 256 < "${copy}") || digest='' # producer-status: allow the regex test below refuses an empty digest
    fi
    digest=${digest%% *}
    [[ ${digest} =~ ^[0-9a-f]{64}$ ]] || refuse "cannot hash the reader ${origin} (its copy ${copy})"
    [[ ${digest} == "${pin}" ]] ||
        refuse "sha256 ${digest} of the reader ${origin} (hashed as its copy ${copy}) differs from the pin ${pin} of claude.levers.sha256.${name} in ${LEVER_MANIFEST}; the reader is not the pinned one, so the lever does not run it"
    reader_copy_path=${copy}
}

[[ $# -ge 1 ]] || refuse "${usage}"
pr=$1
shift
[[ ${pr} =~ ^[1-9][0-9]{0,9}$ ]] || refuse "the pull request is not a decimal number: ${pr}"
[[ $# -eq 2 && $1 == --records && -n $2 ]] || refuse "${usage}"
records=$2
[[ ${gh_timeout} =~ ^[1-9][0-9]*$ ]] || refuse 'PR_LEVER_GH_TIMEOUT must be a positive integer'
python=$(command -v python3) || refuse 'no python3 found (it runs the ledger reader, scripts/orchestrator/ledger.py)'
# The checkout the lever runs in, by its physical path, and it must be the main checkout: a linked worktree (a
# worker's clone) holds a copy of the store that is not the orchestrator's record (U71, bot P1 4370212009).
toplevel=$(git_isolated rev-parse --show-toplevel 2> /dev/null) || refuse 'run from the repository checkout that holds the program store'
[[ -n ${toplevel} && -d ${toplevel} ]] || refuse 'run from the repository checkout that holds the program store'
toplevel=$(cd "${toplevel}" && pwd -P) || refuse "cannot resolve ${toplevel}"
git_dir=$(git_isolated -C "${toplevel}" rev-parse --absolute-git-dir) || refuse 'cannot read the git directory'
common_dir=$(git_isolated -C "${toplevel}" rev-parse --path-format=absolute --git-common-dir) ||
    refuse 'cannot read the git common directory'
git_dir=$(cd "${git_dir}" && pwd -P) || refuse "cannot resolve ${git_dir}"
common_dir=$(cd "${common_dir}" && pwd -P) || refuse "cannot resolve ${common_dir}"
[[ ${git_dir} == "${common_dir}" ]] || # lint-comparisons: allow both sides are pwd -P forms
    refuse "${toplevel} is a linked worktree; run from the main checkout, where the orchestrator keeps its store"
# U216: regime-env derives `REGIME_STORE_ROOT` for this checkout (its own refusals name this lever). This lever reads
# nothing in the hcom store, so the store's `origin` binding is not asked of it (`--unbound-ok`; the dotfiles program
# runs on the pre-U33 store pair and its derived hcom store `~/.local/state/hcom/dotfiles` carries no `origin`, so the
# bound form would stop every merge on this host); the collision refusal (an `origin` naming another checkout) and
# every store-root hold stay. The helper's refusal (return 1) is this lever's refusal status, exit 2.
regime_env pr-merge.sh --unbound-ok || exit 2
# The one reader of the ledger (U122 round 6), run from the checkout the store is in, as pr-audit.sh runs the
# checkout's rounds-check.py and audit-carry.py; the lever's awk reader is gone with it.
ledger_reader=${toplevel}/scripts/orchestrator/ledger.py
[[ -f ${ledger_reader} ]] || refuse "no ${ledger_reader} in the checkout; the ledger is read through it alone"
# The one definition of the sweep classes (U597), run from the checkout as the ledger reader is.
scope_reader=${toplevel}/scripts/orchestrator/sweep-scope.py
[[ -f ${scope_reader} ]] || refuse "no ${scope_reader} in the checkout; whether a head needs its sweep row is read through it alone"
# The readers run from the lever's own copies, each held to its `claude.levers.sha256.<name>` pin (round 8): the copies
# are made and hashed here, before the first `gh` read, and the directory goes on every exit.
reader_dir=''
trap reader_copies_remove EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
reader_copies_make
reader_copy ledger.py "${ledger_reader}"
ledger_copy=${reader_copy_path}
reader_copy sweep-scope.py "${scope_reader}"
scope_copy=${reader_copy_path}

view=$(gh_bounded pr view "${pr}" --json state,baseRefName,headRefOid,isDraft \
    --jq '[.state, .baseRefName, .headRefOid, (.isDraft | tostring)] | @tsv') || fail "cannot read pull request ${pr}"
IFS=$'\t' read -r state base head draft <<< "${view}"
[[ ${state} == OPEN ]] || refuse "pull request ${pr} is ${state:-unreadable}, not OPEN"
[[ ${base} == main ]] || refuse "pull request ${pr} targets ${base:-nothing}, not main"
[[ ${draft} == false ]] || refuse "pull request ${pr} is a draft (isDraft=${draft:-unreadable})"
[[ ${head} =~ ^[0-9a-f]{40}$ ]] || fail "pull request ${pr} has no readable head: ${head}"
resolve_store

require_verdict_row "${head}"
require_dispositions "${audited_head}" "${audited_unit}" "${head}"
# The main ruleset's up-to-date policy, read once before the listing (round 9): while it is false no head is exempt.
require_ruleset_policy
require_sweep_scope
[[ -z ${sweep_reason} ]] || require_sweep_row

status=0
checks=$(gh_bounded pr checks "${pr}" --json bucket,name --jq '.[] | [.bucket, .name] | @tsv') || status=$?
# The second read checks the base as well as the head (U71 audit round 7): `--match-head-commit` pins only the head,
# and a pull request retargeted from main with the same head would otherwise merge into the new base.
again=$(gh_bounded pr view "${pr}" --json headRefOid,baseRefName --jq '[.headRefOid, .baseRefName] | @tsv') ||
    fail "cannot read the head and base of ${pr} again"
IFS=$'\t' read -r again again_base <<< "${again}"
[[ ${again} == "${head}" ]] || refuse "the head of pull request ${pr} moved from ${head} to ${again:-unreadable} during the checks"
[[ ${again_base} == main ]] || refuse "pull request ${pr} was retargeted from main to ${again_base:-unreadable} during the checks"
[[ -n ${checks} ]] || {
    ((status == 0)) && refuse "no check is reported on the head ${head}"
    fail "gh pr checks ${pr} failed (exit ${status}) and printed nothing"
}
red=''
while IFS=$'\t' read -r bucket name; do
    case ${bucket} in
    pass | skipping) ;;
    *) red+="${red:+, }${name}=${bucket}" ;;
    esac
done <<< "${checks}"
[[ -z ${red} ]] || refuse "CI is not green on the head ${head}: ${red}"
# The named checks (U330): every REQUIRED_CHECKS name must be listed with bucket `pass`. The listing is scanned once
# per required name and the name compared whole (a check whose name only starts with a required one is no result for
# it); a name listed twice is `pass` only when every line of it is, so `skipping` beside `pass` is no result either.
# An absent required name is named bare, one listed with another bucket with that bucket, so the refusal tells a
# workflow that never ran from a job that skipped. Every listed check is `pass` or `skipping` here (the red check
# above), so a required check that is not `pass` is `skipping`.
missing=''
for required in "${REQUIRED_CHECKS[@]}"; do
    found=''
    while IFS=$'\t' read -r bucket name; do
        [[ ${name} == "${required}" ]] || continue
        case ${bucket} in
        pass) [[ -n ${found} ]] || found=pass ;;
        *) found=${bucket} ;;
        esac
    done <<< "${checks}"
    [[ ${found} == pass ]] || missing+="${missing:+, }${required}${found:+=${found}}"
done
[[ -z ${missing} ]] ||
    refuse "CI has no result for: ${missing}; every check of REQUIRED_CHECKS (the main ruleset's required contexts) must pass on the head ${head}, and a pull request whose pull_request workflows never ran (a conflict with main) lists none of them"
((status == 0)) || fail "gh pr checks ${pr} exited ${status} although every listed check passed"
# The daily freshness again, right before the merge request (round 9; the round-8 P3 at :1282): a head that rested on
# a daily row (an empty `sweep_reason`) rests on it only while it is still within the window after the CI read and the
# reread above; a row that expired meanwhile is a refusal, never a merge. This read is the lever's last before the
# request, and the window closes here, one API round trip before GitHub's write (round 10).
[[ -n ${sweep_reason} ]] || recheck_daily_sweep

merge_status=0
gh_bounded pr merge "${pr}" --squash --match-head-commit "${head}" >&2 || merge_status=$?
after=$(gh_bounded pr view "${pr}" --json state,mergeCommit,baseRefName,headRefOid \
    --jq '[.state, (.mergeCommit.oid // ""), .baseRefName, .headRefOid] | @tsv') ||
    fail "cannot read pull request ${pr} after the merge command (exit ${merge_status}); read it before anything else"
IFS=$'\t' read -r state commit merged_base merged_head <<< "${after}"
[[ ${state} == MERGED && ${commit} =~ ^[0-9a-f]{40}$ ]] ||
    fail "pull request ${pr} is ${state:-unreadable} after the merge command (exit ${merge_status})"
# A merge this lever did not make (U71 audit round 9): when the pinned merge failed and someone else merged a later
# head, MERGED alone would credit the audited head with that merge, so the merged head must be the audited one.
[[ ${merged_head} == "${head}" ]] ||
    fail "pull request ${pr} merged at head ${merged_head:-unreadable} as ${commit}, not at the audited head ${head} (merge command exit ${merge_status}); that merge is not this verdict's; tell the operator"
# gh pr merge takes no base (`gh pr merge --help`), so a retarget between the second read and the merge call is
# reported here, loudly, with the base it landed on; it cannot be undone by the lever.
[[ ${merged_base} == main ]] ||
    fail "pull request ${pr} merged into ${merged_base:-an unreadable base}, not main: it was retargeted after the last read; tell the operator"
# The merge landed on the tip the listing was classified against (round 8; the round-7 P3 at :782): `--match-head-commit`
# pins the head alone. While the main ruleset's `strict_required_status_checks_policy` is false (round 9: read before
# the listing by require_ruleset_policy, and no head is exempt then) nothing server-side holds `main` still between the
# tip read in require_sweep_scope and the merge; when it is true GitHub refuses a merge of a head behind `main` and this
# check never fires. The merge commit's first parent is the `main` the squash landed on, read with its status and held
# to 40 hex, and it must be the tip read earlier; a merge onto a moved `main` is exit 1 with no receipt naming the
# commit, its parent and that tip, since the classified listing may not be the landed diff and the coordinator must
# sweep the merge commit (the hcom-orchestration SKILL step 6): the lever's own record of what it merged onto.
parent=$(gh_bounded api "repos/{owner}/{repo}/commits/${commit}" --jq '.parents[0].sha') ||
    fail "pull request ${pr} is MERGED as ${commit}, but the first parent of that commit could not be read (gh api repos/{owner}/{repo}/commits/${commit}); whether the merge landed on the tip ${base_tip} of main the listing was classified against is unknown, so the classified listing may not be the landed diff: the coordinator must sweep the merge commit ${commit}"
[[ ${parent} =~ ^[0-9a-f]{40}$ ]] ||
    fail "pull request ${pr} is MERGED as ${commit}, but its first parent read from gh api repos/{owner}/{repo}/commits/${commit} is not 40 hex: '${parent}'; whether the merge landed on the tip ${base_tip} of main the listing was classified against is unknown, so the classified listing may not be the landed diff: the coordinator must sweep the merge commit ${commit}"
[[ ${parent} == "${base_tip}" ]] ||
    fail "pull request ${pr} merged as ${commit}, whose first parent ${parent} is not the tip ${base_tip} of main read before the listing: main moved between the tip read and the merge, so the classified listing may not be the landed diff; the coordinator must sweep the merge commit ${commit}"
((merge_status == 0)) || echo "${lever}: the merge command exited ${merge_status}, but the pull request is MERGED" >&2
echo "merged pr=${pr} head=${head} commit=${commit} verdict=${verdict_ts}"
