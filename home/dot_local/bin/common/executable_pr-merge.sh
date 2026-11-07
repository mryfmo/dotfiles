#!/usr/bin/env bash
# @file pr-merge.sh
# @brief Squash-merge a pull request only at a head the program's ledger records as `correct`, or as `carried` from an earlier `correct` head with the same diff, with the unit's `sweep` row at that head, and CI passed, the orchestrator seat's merge lever.
# @description
#   Regime-cutover U71 (finding F010), the orchestrator seat's only merge path: `home/dot_agents/omp/policies/orchestrator.yml`
#   allows `~/.local/bin/common/pr-merge.sh *` and denies the `gh pr merge` command text (a speed bump: text rows do
#   not stop a glob spelling; a seat running `gh` itself is the residual unit U88 removes). `<pr>` is decimal and
#   checked before the first `gh` call. The lever runs in the main checkout (a linked worktree is refused) and reads
#   only that checkout's store: `<toplevel>/.orchestration/orchestrate/<program>/ledger.tsv` (header
#   `ts unit pr head_sha verdict verifier evidence`), `<program>` taken from the pull request body's one
#   `Program-Unit: <program>/U<n>` line, no directory of that chain nor the ledger a symlink, each owned by this user;
#   `--records` must resolve (`pwd -P`) to exactly that store, so a ledger written anywhere else is never read. It reads
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
#   directory of this user and no symlink, and `--records` must resolve inside this checkout to exactly the body's
#   store. The
#   lever reads no local git objects or refs; it decides from `gh` reads and the store alone, and git only names the
#   checkout (`rev-parse --show-toplevel`, `--absolute-git-dir`, `--git-common-dir`). CI is `gh pr checks <pr> --json bucket,name` between two reads of `headRefOid` that must both equal
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
#   state,mergeCommit,baseRefName,headRefOid` decides: `MERGED` into `main` at the audited head prints the receipt (the
#   merge happened; never run the merge twice); another state, another base, or another merged head (a merge someone
#   else made after the pinned one failed) is a failure with no receipt that names both shas. The
#   thread check (`pr-threads-check.sh`) stays a separate step before this lever (`hcom-orchestration` SKILL step 6).
#   Each `gh` call is bounded by PR_LEVER_GH_TIMEOUT seconds (perl `alarm`).
#   Since regime-cutover U147 the lever also requires the unit's `security-audit` sweep at the audited head, and since
#   U244 of every unit (the AGENTS.md Audit sweep rule: every unit and every program milestone gets one sweep before
#   its pull request merges; U147 read the unit's brief for the trust-boundary mark to tell a trust-boundary unit from
#   the rest, and with one class that reading is gone). After `require_verdict_row` and before the checks read and the one
#   write, the checkout's `ledger.py sweep <unit> <audited head>` prints the newest row of the unit or a fix unit of it
#   at the audited head whose verdict starts with the word `sweep` (pr `-`, verifier the skill and its pin, evidence
#   the findings file under the store), or `none`, which is a refusal naming the unit, the head and the rule; an exit-0
#   answer that is neither `none` nor one row of four tab-separated fields with a ts is a refusal naming the reader and
#   the answer. The row must be the exact row the rule defines: pr `-`, verifier the two words `security-audit-skill
#   <pin>` with the pin word, 8 or more lowercase hex, a prefix of the `assets.security-audit-skill.pin` of the
#   manifest the self-check read (one probe, `sweep_pin_probe`, run as `python3 -I -S -c` over `LEVER_MANIFEST`), and
#   evidence whose first `;`-separated field names a findings file `sweeps/<path>.json` that is a regular file of this
#   user under the store (never opened); the reader refuses any other `sweep` row as a malformed store, and a pin that
#   is no prefix or a findings file that is missing, a symlink or another user's is a refusal naming it, so a row
#   written by hand with another verifier admits nothing. The audited head is the one `require_verdict_row` set, so a
#   head moved under a `carried` row needs no second sweep. The lever reads no brief, never the findings file a sweep
#   row names, and judges no sweep's content.
# @arg $1 int The pull request number.
# @option --records <dir> The program store holding `ledger.tsv`, `verdicts/`, `dispositions.tsv` and `units.tsv`
#   (required; must resolve to the checkout's own store, above; a directory outside the checkout is refused).
# @env PR_LEVER_GH_TIMEOUT Seconds per `gh` call (default 60).
# @stdout One receipt line: `merged pr=<pr> head=<head> commit=<merge commit> verdict=<ledger row ts>` (the `carried` row's ts for a carried head).
# @exitcode 0 The pull request is merged at the head.
# @exitcode 1 A `gh` or `git` read, the manifest pin probe (any status but 0 or 2), or the merge, failed.
# @exitcode 2 Refused: usage, the pull request's state, no `correct` or `carried` row for the head, no `sweep` row of
#   the unit or a fix unit of it at the audited head, a sweep answer of the reader that is neither `none` nor one row
#   of four tab-separated fields with a ts, a sweep row whose verifier is not `security-audit-skill <pin>` with the
#   pin word a prefix (8 or more characters) of the manifest's `assets.security-audit-skill.pin`, whose evidence does
#   not name a regular file of this user `sweeps/<path>.json` under the store, or a manifest without that one pin, a
#   ledger the checkout's `ledger.py` cannot read as data (a ts outside `YYYY-MM-DDThh:mm:ssZ` or outside the
#   calendar, a wrong header or column count, an empty required cell, a sweep or audit row whose head is not 40 hex, a
#   `sweep` row that is not the exact row of the Audit sweep rule, pr `-`, verifier `security-audit-skill <pin>` and
#   evidence `sweeps/<path>.json`: the reader's exit 2), no python3 or no `scripts/orchestrator/ledger.py` in the
#   checkout, a `carried` row whose evidence names no `carried <earlier> <head> <sha256>` for this head or whose
#   earlier head has no `correct` row, no verdict file for the audited head, a P2 or P3 finding of weight 10 or more
#   without its `residual` disposition row, a malformed verdict file, `dispositions.tsv` or `units.tsv`, a store path
#   that is a symlink or outside the checkout, CI that is not green on the head, or CI that lists no passing result
#   for a check of REQUIRED_CHECKS (U330).
# @example
#   ~/.local/bin/common/pr-merge.sh 480 --records .orchestration/orchestrate/regime-cutover
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
# @arg $1 int The pull request number.
# @arg $2 string The 40-hex head sha.
ledger_verdict() {
    local out status=0
    out=$("${python}" -I -S "${ledger_reader}" "${store}" verdict "$1" "$2" 2>&1) || status=$?
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

# @description Refuse unless the ledger holds the unit's sweep row at `audited_head` (regime-cutover U147, every unit
#   since U244; the AGENTS.md Audit sweep rule: every unit and every program milestone gets one sweep of the
#   `security-audit` skill before its pull request merges). The row is asked of the checkout's ledger.py (`sweep <unit>
#   <head>`, the one reader, its status read as ledger_verdict reads it and its exit-0 answer read by its shape, `none`
#   or one row of four tab-separated fields with a ts, as require_verdict_row reads a row) at `audited_head`: the head
#   itself, or for a `carried` row the earlier head whose verdict file the merge reads, so a head moved under a
#   carried row needs no second sweep. `none` is a refusal naming the unit, the head and the rule. The row must be the
#   exact row of the rule (Codex thread 4457544811: a row written by hand with verifier `coordinator` admitted the
#   merge): the reader already refuses a `sweep` row whose pr is not `-`, whose verifier is not `security-audit-skill
#   <pin>` or whose evidence is not `sweeps/<path>.json` as a malformed store, and the lever reads the answer by its
#   shape all the same, then requires the pin word to be a prefix of the manifest's `assets.security-audit-skill.pin`
#   (sweep_pin_probe over LEVER_MANIFEST: exit 0 the pin, 2 a refusal carrying its line, anything else a failure) and
#   the findings file to be a regular file of this user under `<store>/sweeps/` (`sweeps/` a directory of this user
#   and no symlink, the file `-f`, `-O`, `! -L`, as the verdict file), never opened; a pin that is no prefix or a file
#   that is missing, a symlink or another user's is a refusal naming it. The lever reads neither the findings file the
#   row names nor the sweep's content.
require_sweep_row() {
    local status=0 row rest verifier evidence pin_word manifest_pin findings_path sweeps_dir findings_file
    row=$("${python}" -I -S "${ledger_reader}" "${store}" sweep "${unit}" "${audited_head}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${row#ledger: }" ;;
    *) fail "${ledger_reader} exited ${status} reading ${ledger} for the sweep row of ${unit}: ${row:-no output}" ;;
    esac
    [[ ${row} != none ]] ||
        refuse "${ledger} has no sweep row for ${unit} (or a fix unit of it) at the audited head ${audited_head}; the AGENTS.md Audit sweep rule says every unit and every program milestone gets one sweep of the security-audit skill before its pull request merges (a row with verdict sweep, pr -, head ${audited_head}); run the sweep and write its row, or wait for it"
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
    # The verifier's two words are the skill's name and the pin word the sweep ran at (round 4): the reader refuses any
    # other sweep row, and the lever reads the answer by its shape all the same before it compares the pin.
    case ${verifier} in
    'security-audit-skill '*) ;;
    *) refuse "the sweep row of ${unit} at ${audited_head} names '${verifier}' as its verifier, not the pinned skill and its pin (security-audit-skill <pin>); the gate admits the row the AGENTS.md Audit sweep rule defines alone" ;;
    esac
    pin_word=${verifier#security-audit-skill }
    pin_word=${pin_word%%[[:space:]]*}
    [[ ${pin_word} =~ ^[0-9a-f]{8,}$ ]] ||
        refuse "the sweep row of ${unit} at ${audited_head} names '${pin_word}' as the skill's pin, not 8 or more lowercase hex characters of it"
    status=0
    manifest_pin=$("${python}" -I -S -c "${sweep_pin_probe}" "${LEVER_MANIFEST}" 2>&1) || status=$?
    case ${status} in
    0) ;;
    2) refuse "${manifest_pin#manifest: }; the sweep row's pin is compared with that pin, so a manifest without it admits no sweep" ;;
    *) fail "the pin probe over ${LEVER_MANIFEST} exited ${status}, neither the pin (0) nor a refusal (2): ${manifest_pin:-no output}" ;;
    esac
    [[ ${manifest_pin} =~ ^[0-9a-f]{40}$ ]] ||
        refuse "the pin probe over ${LEVER_MANIFEST} answered with no 40-hex pin: ${manifest_pin:-nothing}"
    [[ ${manifest_pin} == "${pin_word}"* ]] ||
        refuse "the sweep row of ${unit} at ${audited_head} names pin ${pin_word}, which is not a prefix of the manifest's assets.security-audit-skill.pin ${manifest_pin} (${LEVER_MANIFEST}); the sweep ran at another pin than the one the manifest pins, or the row was written by hand"
    # The findings file is the evidence's first `;`-separated field stripped of whitespace, a relative path under
    # `sweeps/` ending in `.json` with no `..`, `.` or empty component, checked as the verdict file is (the directory,
    # then the file: regular, this user's, no symlink) and never opened.
    findings_path=${evidence%%;*}
    findings_path=${findings_path#"${findings_path%%[![:space:]]*}"}
    findings_path=${findings_path%"${findings_path##*[![:space:]]}"}
    case ${findings_path} in # lint-comparisons: allow the row's store-relative path is judged as the text it is, then the file is stat'ed under the store
    sweeps/*.json) ;;
    *) refuse "the sweep row of ${unit} at ${audited_head} names '${evidence}' as its evidence, not a findings file sweeps/<path>.json under the store" ;;
    esac
    case /${findings_path}/ in # lint-comparisons: allow the same text, its components fenced by slashes
    */../* | */./* | *//*) refuse "the findings file ${findings_path} of the sweep row of ${unit} at ${audited_head} has a '..', '.' or empty path component; the file is read under the store alone" ;;
    esac
    sweeps_dir=${store}/sweeps
    [[ ! -L ${sweeps_dir} && -d ${sweeps_dir} && -O ${sweeps_dir} ]] ||
        refuse "${sweeps_dir} is not a directory of this user (a symlink or missing); the findings file a sweep row names must be in the checkout's own store"
    findings_file=${store}/${findings_path}
    [[ ! -L ${findings_file} && -f ${findings_file} && -O ${findings_file} ]] ||
        refuse "${findings_file}, the findings file the sweep row of ${unit} at ${audited_head} names, is not a regular file of this user (a symlink or missing); a sweep whose findings file is not in the store admits no merge"
}

# @description Set `ledger`, `store`, `units_file` and `unit` to the one store the merge may read (U71, bot P1
#   4370212009: a caller-chosen ledger.tsv could hold a fabricated row): `<toplevel>/.orchestration/orchestrate/
#   <program>/ledger.tsv` of this main checkout, `<program>` and `U<n>` taken from the pull request body's one
#   `Program-Unit: <program>/U<n>` line. No directory from the checkout down and not the ledger is a symlink, each is
#   owned by this user, and `--records` must resolve (`pwd -P`) inside the checkout and to exactly that directory;
#   anything else is a refusal.
# @set ledger The canonical ledger path.
# @set store The canonical store directory.
# @set units_file The store's `units.tsv`, read by unit_row_exists.
# @set unit The body's unit id; a ledger row for the pull request must be it or a `U<n>[a-z]` fix unit of it, and the row's unit names the verdict file (require_verdict_row).
resolve_store() {
    local body markers line program path given part
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
    path=${toplevel}
    for part in .orchestration orchestrate "${program}"; do
        path=${path}/${part}
        [[ -d ${path} && ! -L ${path} && -O ${path} ]] ||
            refuse "${path} is not a directory of this user (a symlink or a missing store); the merge reads only the checkout's own store"
    done
    given=$(cd "${records}" 2> /dev/null && pwd -P) || refuse "--records ${records} is no directory"
    [[ ${given} == "${toplevel}/"* ]] || # lint-comparisons: allow both sides are pwd -P forms
        refuse "--records ${records} resolves to ${given}, outside the checkout ${toplevel}; the merge reads only the checkout's own store"
    [[ ${given} == "${path}" ]] || # lint-comparisons: allow both sides are pwd -P forms
        refuse "--records ${records} is not the program's store ${path} (named by the body's Program-Unit line)"
    store=${path}
    ledger=${path}/ledger.tsv
    units_file=${path}/units.tsv
    [[ -f ${ledger} && ! -L ${ledger} && -O ${ledger} && -r ${ledger} ]] ||
        refuse "${ledger} is not a readable regular file of this user"
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
# The one reader of the ledger (U122 round 6), run from the checkout the store is in, as pr-audit.sh runs the
# checkout's rounds-check.py and audit-carry.py; the lever's awk reader is gone with it.
ledger_reader=${toplevel}/scripts/orchestrator/ledger.py
[[ -f ${ledger_reader} ]] || refuse "no ${ledger_reader} in the checkout; the ledger is read through it alone"

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
require_sweep_row

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
((merge_status == 0)) || echo "${lever}: the merge command exited ${merge_status}, but the pull request is MERGED" >&2
echo "merged pr=${pr} head=${head} commit=${commit} verdict=${verdict_ts}"
