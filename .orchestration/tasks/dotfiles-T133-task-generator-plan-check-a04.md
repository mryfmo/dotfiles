---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a04
kind: code
security: true
allowed_files:
  - scripts/orchestrator/task-from-plan.py
  - scripts/orchestrator/plan-check.py
  - scripts/orchestrator/task-consistency-check.py
  - scripts/orchestrator/task-template.md
  - tests/unit/test_task_from_plan.py
  - tests/unit/test_plan_check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_regime_ci.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a04/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a03]
threat_table:
  - control: "scripts/orchestrator/task-from-plan.py (committed plan data, unverified commands and exclusive output creation)"
    disposition: "residual: generation executes no plan or Check command, binds its checker and template independently of inspected data, and refuses existing or redirected output; trusted-parent authority and concurrent same-UID replacement remain residual."
  - control: "scripts/orchestrator/plan-check.py (form, drift, invariants and confined glob enumeration)"
    disposition: "residual: Python-3.12-compatible matching retains root confinement, rejects escaping patterns and matches, and never follows directory symlinks; fixtures do not establish host isolation or live GitHub correctness."
  - control: "scripts/orchestrator/task-consistency-check.py (fixed C14 probes, selector grammar and shared trusted launches)"
    disposition: "residual: C14 parses and hashes the same bytes and interprets only its fixed vocabulary; parent-supplied launch bindings replace install-root discovery, while caller authority and same-UID host access remain residual."
  - control: "scripts/orchestrator/task-template.md (bundled rows, unverified Check text and Completion)"
    disposition: "residual: the bundled template supplies defaults without authorizing command execution or inventing observations; generation fixtures retain its use without reading sibling task records."
  - control: "tests/unit/test_task_from_plan.py (generation, output, Git configuration and comparison regressions)"
    disposition: "residual: temporary repositories and marker files verify non-execution, confinement and retained behavior without touching canonical records, live credentials or deployment state."
  - control: "tests/unit/test_plan_check.py (confined matching and retained form, drift and invariant fixtures)"
    disposition: "residual: fixtures exercise recursive and single-component matching, hostile paths and stubbed GitHub responses; supported-version claims distinguish actual interpreter runs from source-level compatibility."
  - control: "tests/unit/test_task_consistency_c11_c15.py (parent inputs, clean launches, digest and selector fixtures)"
    disposition: "residual: successful fixtures supply absolute temporary caches and trusted interpreter bindings; invalid-input fixtures assert named refusal before subprocess or cache access; hostile PATH, virtualenv and configuration markers remain absent."
  - control: "tests/unit/test_regime_ci.py (temporary launch inputs and retained reset-lineage behavior)"
    disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_supplies_absolute_parent_launch_inputs_to_the_checker"
  - control: "tests/unit/test_task_checkers.py (historical fixtures and expected check sets)"
    disposition: "residual: inherited C4, C11 and C15 fixture dispositions remain; successful checker invocations receive explicit temporary launch inputs without granting historical command text premise authority."
  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a04/** (this reset's branch artifacts)"
    disposition: "residual: artifacts distinguish inherited observations, new red proofs and final-head results; acceptance compares dispatched bytes, tested revisions, implementation, evidence and CI."
  - control: "the task-file copy at .orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md replaces .orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md"
    disposition: "residual: the first push deletes only the named predecessor copy and adds the byte-identical dispatched a04 copy; TASK and RESULT bind the a04 copy's own SHA256 and acceptance verifies the replacement."
  - control: "the evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a04/ (report.md, validation.md, sandbox.md, learning.md, measure.md and worker review evidence)"
    disposition: "residual: evidence records commands, stdout, stderr, exits, source hashes and actual execution contexts without secrets or unmasked home-directory paths; historical a03 implementation and evidence remain available."
  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    disposition: "residual: structural checks and dispatched-byte comparison bind scope; integration evidence binds the final head, and authoritative approval and gate evidence are obtained through GitHub at the authenticated SHA."
  - control: metadata separators
    disposition: "residual: the first document separators delimit YAML front matter and the dispatched-copy digest covers the complete document."
  - control: in-process effects
    disposition: "residual: generation reads committed plan data and exclusively creates one confined file; C14 interprets authorized read-only probes without a shell; plan-check writes no records."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: every script requires parent-supplied absolute UV_CACHE_DIR and TRUSTED_PYTHON, validates the interpreter as a regular trusted executable, and preserves both through env -i; executable bindings come from the trusted parent's private PATH, never an inspected checkout or an install-root search."
  - control: new or renamed scripts
    disposition: "residual: the inherited generator, plan checker and bundled template remain the new production-file inventory; this reset adds no production file outside allowed_files."
  - control: "CI parent launch prefixes and validate wiring in the existing workflows (P1-11 owner; no workflow edit is authorized here)"
    disposition: "out-of-scope: dotfiles-T133-regime-ci-a02"
  - control: "5.14 item 0: host threat model"
    disposition: "residual: host controls reduce accidents and prompt injection rather than isolate same-UID seats; shared GitHub credentials leave detection on the next acceptance-record PR, not prevention, with P1-11 owning ci:detection:1 and separate-user or separate-host isolation remaining P1-16."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: this Codex seat uses its effective workspace-write boundary; Claude file-tool and managed-setting guarantees require P1-15 deployment and verification, and no fixture result establishes them; this task changes no seat, hook, exclusion or permission setting."
  - control: "5.14 item 2: sanitized environment and private executable PATH"
    disposition: "residual: the trusted parent supplies clean launch inputs and verified absolute executable bindings; children enter env -i, use the private binary-link PATH and Python -I, and receive the prescribed Git controls; arbitrary inherited PATH and GIT_* values supply no executable authority."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: executable, helper, template, snapshot and output bindings retain realpath, worker-root and filesystem-identity checks; fixture trusted roots are separate from inspected repositories; same-UID replacement and undeployed Claude protections remain residual."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: validated realpaths execute without rediscovery, consumed content uses unique mode-0600 trusted-root snapshots with last-use SHA256 checks, and C14 hashes the bytes it parses; parent authority and native execution remain trusted residuals."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: output creation retains O_EXCL and refuses existing files and symlinks; new head-specific resources use the full 40-character head; this task adds no reservation protocol or physical-slot lock."
  - control: "5.14 item 6: honest residuals"
    disposition: "residual: trusted-parent decisions, native loaders, shared credentials, processes outside seat sandboxes and concurrent filesystem changes remain explicit residuals; tests establish behavior, not deployment or malicious-worker isolation."
  - control: "5.14 item 7: trusted-execution verification"
    disposition: "residual: named regressions retain hostile PATH, injected Git environment and configuration, worker-root binding and replaced-content cases; P1-6 owns tests/unit/trusted_exec_contract.py, which this task neither creates nor edits."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: these scripts grant no permission or merge approval; canonical main is resolved through gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha, and approval and authoritative evidence are read through repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>; local remotes, URL rewrites, refs, records and the shared object database supply no approval authority."
  - control: "5.14 item 9: private uv caches"
    disposition: "residual: scripts require the parent's absolute cache and interpreter inputs and compute no defaults; orchestrator, worker and fixture parents select their own private caches; uv launches retain --no-config --no-project --offline --python and Python -I, while cache write protection remains conditional on verified seat deployment."
  - control: "5.14 item 10: worker commands remain inside the sandbox"
    disposition: "residual: this Codex worker performs every command inside its sandbox and reports unavailable operations as blocked; it gains no escape, exclusion or Herdr socket authority; broader Claude guarantees remain conditional on P1-15 deployment."
  - control: orchestrator effect merge
    disposition: "residual: the worker has no merge assignment; integration follows Orchestrator Playbook step 10 and pins the squash merge to the audited final head; shared credentials leave unauthorized merges detectable rather than prevented."
  - control: orchestrator effect update-branch
    disposition: "residual: a changed head requires fresh applicable CI, feedback, audit and security-review evidence before acceptance and the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; dirty-worktree protections remain and acceptance records any operator-authorized discarded state."
premises:
  - claim: the read-only authoring checkout is main 51ba5801 and the continuing implementation head is 82fd9b12
    command: git rev-parse HEAD 82fd9b12 | paste -sd ' ' -
    output: "51ba580149fcace54a912358e7e87c5b07cd8760 82fd9b12f79073ac706423f2716eac701feaebb3"
  - claim: current additions plus deletions against the lineage comparison base are 801 source lines and 1065 test lines
    command: >-
      git diff --numstat b22a5580 82fd9b12 | awk 'BEGIN{s=0;t=0} $3 ~ /^tests\// {t+=$1+$2;next} $3 !~ /^\.orchestration\// {s+=$1+$2} END{printf "source=%d; tests=%d\n",s,t}'
    output: "source=801; tests=1065"
  - claim: the unit workflow supplies uv with setup-uv and uses mise for statusline and formatting tools, without installing Python through that mise step
    command: >-
      /usr/bin/awk '/os: \[|system: \[|os: ubuntu-26.04|jdx\/mise-action|astral-sh\/setup-uv|enable-cache: false|install: false|mise -C .* install|make unit-test/{sub(/^[ \t]+/,"");printf "%s%d:%s",sep,NR,$0;sep="; "}END{print ""}' .github/workflows/test.yaml
    output: '34:os: [ubuntu-24.04, macos-14]; 35:system: [client, server]; 43:- os: ubuntu-26.04; 225:uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4; 229:install: false; 236:mise -C "${RUNNER_TEMP}/statusline-mise" install node; 238:mise -C "${RUNNER_TEMP}/statusline-mise" install npm:ccstatusline npm:ccusage; 239:mise -C "${RUNNER_TEMP}/statusline-mise" install ruff npm:prettier; 335:uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0; 337:enable-cache: false; 349:make unit-test'
  - claim: agent-assets validate runs on Ubuntu with setup-uv and its existing validator command
    command: >-
      /usr/bin/awk '/runs-on:|astral-sh\/setup-uv|enable-cache: false|run: uv/{sub(/^[ \t]+/,"");printf "%s%d:%s",sep,NR,$0;sep="; "}END{print ""}' .github/workflows/agent-assets.yml
    output: '25:runs-on: ubuntu-24.04; 37:uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0; 39:enable-cache: false; 42:run: uv run --with pyyaml scripts/validate-agent-assets.py'
  - claim: test.yaml has an OS/system matrix, not an explicit Python-version matrix or setup-python step
    command: >-
      /usr/bin/awk '/python-version|actions\/setup-python/{n++} END{printf "test.yaml explicit Python-version/setup-python lines=%d\n",n}' .github/workflows/test.yaml
    output: "test.yaml explicit Python-version/setup-python lines=0"
  - claim: agent-assets.yml has no explicit Python version, setup-python or mise step
    command: >-
      /usr/bin/awk '/python-version|actions\/setup-python|jdx\/mise-action/{n++} END{printf "agent-assets.yml explicit Python-version/setup-python/mise lines=%d\n",n}' .github/workflows/agent-assets.yml
    output: "agent-assets.yml explicit Python-version/setup-python/mise lines=0"
  - claim: the Linux failure log records setup-uv's toolcache executable and Python 3.12, outside the a03 uv resolver's listed roots
    command: >-
      rg -m 1 'fixture-seed UV_CACHE_DIR=' .claude/worktrees/worker-g/.orchestration/dotfiles-T133-task-generator-plan-check-a03/ci-required-linux-failure-completed.log | sed 's/^.*fixture-seed /fixture-seed /'
    output: "fixture-seed UV_CACHE_DIR=/tmp/a03-pyyaml-y61co94e ['/opt/hostedtoolcache/uv/0.13.1/x86_64/uv', 'run', '--no-config', '--no-project', '--python', '/usr/bin/python3.12', '--with', 'pyyaml', 'python', '-I', '-c', 'import yaml'] exit=0"
  - claim: the macOS failure log records its toolcache uv and Homebrew Python 3.14, rather than a pinned mise Python
    command: >-
      rg -m 1 'fixture-seed UV_CACHE_DIR=' .claude/worktrees/worker-g/.orchestration/dotfiles-T133-task-generator-plan-check-a03/ci-required-macos-failure.log | sed 's/^.*fixture-seed /fixture-seed /'
    output: "fixture-seed UV_CACHE_DIR=/var/folders/s6/5hzmn6lx4dz5nxs7k_0slzph0000gn/T/a03-pyyaml-jq71ja76 ['~/hostedtoolcache/uv/0.13.1/aarch64/uv', 'run', '--no-config', '--no-project', '--python', '/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/bin/python3.14', '--with', 'pyyaml', 'python', '-I', '-c', 'import yaml'] exit=0"
  - claim: the main checkout still lacks the five originally new implementation and dedicated-test files
    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    output: "0"
  - claim: the main checkout's format-2 checker documents eleven checks before this lineage's additions
    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    output: "11"
  - claim: the plan group remains eleven files
    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    output: "11"
  - claim: the todo table remains fifteen P1 rows
    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    output: "15"
  - claim: the relied-on design is uncommitted in the authoring checkout
    command: git status --short -- .orchestration/plans/024-design-quality.md
    output: "?? .orchestration/plans/024-design-quality.md"
  - claim: this digest identifies the design bytes read for the verbatim C-88 quotations below
    command: shasum -a 256 "$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md" | awk '{print $1}'
    output: "c77d9dd4a1fedf8208fd6df2eb1f89c4aa780fc29db092a5b050c2aa2ed0df1f"
  - claim: both the P1-11 owner and the unchanged advisory owner have task files
    command: /bin/ls .orchestration/tasks/dotfiles-T133-regime-ci-a02.md .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md | wc -l
    output: "2"
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a04 — INV-6 reset on PR #417 (plan 024 P1-12; worker a012, Codex, worker-g)

This text is the independent redesign by a review-profile context other than the author of a03. The a03 acceptance record stops that artifact at the C-61 cap: its one pre-push review round and one correction batch are consumed, and required Linux and macOS CI fail at `82fd9b12f79073ac706423f2716eac701feaebb3`. This is the a04 reset, not another a03 correction batch.

Read `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md` through Amendment 3, `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a03.md`, and the worker's `ci-required-linux-failure-completed.log` and `ci-required-macos-failure.log` under `.orchestration/dotfiles-T133-task-generator-plan-check-a03/` in worker-g. The logs and acceptance record identify the uv install-root resolver, missing regime-fixture cache, Python-3.13-only glob API and five comparison-lint hits. The first three are this task's execution-environment defects; the fourth is the D-024-24 repair after PR #415 landed.

Worker a012 fetches and continues `tools/task-generator-plan-check-a01` on PR #417 from `82fd9b12f79073ac706423f2716eac701feaebb3`, incorporating current main through the prescribed update-branch procedure. The authoring checkout is main `51ba580149fcace54a912358e7e87c5b07cd8760`; do not implement there. The a03 implementation and evidence stay. There is one implementation branch and one PR.

The first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a03/task.md` and adds this complete dispatched text byte-identically at `.orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md`. That exact predecessor-copy deletion is the orchestrator-directed reset-bookkeeping exception outside `allowed_files`. Do not delete the a03 directory, fixture-a02-task.md, logs or other evidence. Every other worker edit stays within `allowed_files`.

The a01–a03 task texts, acceptance histories, amendments, observations and counters remain historical. Fresh premises above describe their named sources and revisions. Complex probe commands are read-only authoring evidence, not additions to C14's execution vocabulary; structural runs pass no trusted digest, and an authorized C14 run rejects unsupported forms without a shell fallback.

## Goal

Retain the generator's format-2 skeleton, bundled template, proposed scope and unverified command text; C11–C15 and the inherited checks; and plan-check's form, drift, invariant and confined-overlap reporting. Repair launch selection and fixtures so this behavior runs with the actual CI-provided tools rather than assumptions about the orchestrator host.

Section 5.14 items 0–10 of `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` apply by reference. The inspected checkout supplies data and no executable authority. The relied-on sentences are quoted verbatim from the uncommitted design, rather than recalled or attributed to main (C-88).

Item 2:

> 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。

> Python は `-I`。PATH 探索で実行するものは無い。

Item 4:

> 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。

Item 8 (refreshed uncommitted design SHA256 `bc42c39e28b4e816a6298787450910d682113ae966bd2905535c35c1e3900334`; the design digest in premises remains the earlier observation):

> The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`.

Every canonical-main baseline and every ledger read, including validation and integration evidence, resolves and validates one full 40-hex main SHA through that fixed API endpoint, then reads each path only through `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>` at that same SHA. This includes the checker's main-based presence/content probes and plan-check's F6 decisions.tsv and permissions.ask baseline. Use the retained trusted read-only gh binding and clean launch; failures produce a named refusal without falling back to git ls-remote, local refs, git show or the shared object database. Local plan inputs, C14's explicitly authorized revision probes and Check's local numstat remain data and confer no canonical-main or approval authority.

Item 9:

> Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19).

> A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.

The three scripts consume `UV_CACHE_DIR` and `TRUSTED_PYTHON` from the environment their trusted parent supplies. Before any subprocess or cache access, each refuses an absent or relative cache with nonzero exit and `refused: UV_CACHE_DIR must be set to an absolute path`. Each refuses an absent, relative, nonexistent or non-regular interpreter with nonzero exit and `refused: TRUSTED_PYTHON must be set to an absolute regular file`. A valid interpreter also passes the retained executable, realpath, shim and worker-root checks; path existence alone supplies no trust.

Every Python subprocess uses the validated `TRUSTED_PYTHON` binding, including uv's `--python` argument; it never substitutes `sys.executable`, discovers `.venv`, runs mise, scans an install tree or derives an interpreter from HOME. Each script explicitly preserves the validated cache and interpreter through its clean child environments. There is no cache default from the inspected root, trusted root, cwd or home.

The trusted parent resolves uv, Git and any needed gh once and supplies their verified absolute bindings as named links in a single private executable directory. Scripts consume those bindings, validate their realpaths and execute those realpaths without searching install roots, ordinary caller PATH, shims or checkout bin directories. An absent binding produces a named refusal, not StopIteration or a fallback. A toolcache location is neither rejected merely for differing from mise nor accepted merely because it is a toolcache: the trusted parent establishes its binding. The scripts do not construct a second host-specific uv resolver.

Every subprocess starts under `env -i`; PATH contains only the private links and Python uses `-I`. Every retained uv launch uses `run --no-config --no-project --offline --python "$TRUSTED_PYTHON"`, followed by the existing dependency arguments and `python -I`. Hostile cwd or ancestor `.venv`, uv.toml, loader variables, PYTHON* and injected GIT_* supply no launch authority.

Every Git call retains explicit `-C`, `--git-dir=<checkout>/.git`, `--work-tree=<checkout>`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_LAZY_FETCH=1`, and `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c submodule.recurse=false -c protocol.allow=never -c protocol.https.allow=always`. Status uses `--no-optional-locks` and status/diff use `--ignore-submodules=all`; diff/show use `--no-ext-diff --no-textconv -c core.attributesFile=/dev/null -c core.sshCommand=false`.

Before Git reads, retain the `.gitmodules` refusal, effective `core.worktree` refusal with origin and key, and realpath equality of `rev-parse --show-toplevel` with the inspected checkout. Before every substantive Git invocation, retain the clean-environment effective-config probe `config --show-origin --get-regexp '^filter\.|^core\.worktree$'`, including local includes and enabled config.worktree; any matching filter or worktree key refuses before status/diff. Missing objects start no lazy fetch or configured credential helper.

Trusted helper, template, executable and snapshot bindings retain realpath, worker-root rejection and filesystem-appropriate identity comparison. Consumed file snapshots remain unique, mode 0600, under the trusted root, with SHA256 checked immediately before use and recorded in evidence. Same-UID replacement, native loaders, trusted-parent decisions and shared credentials remain residuals.

## Execution contexts and CI ownership

On the orchestrator host, the trusted parent prefix supplies `UV_CACHE_DIR="$HOME/Workspace/dotfiles/.agents/worklog/uv-cache"` and the absolute interpreter resolved from the pinned mise installation. The parent performs resolution; none of these scripts requires the not-yet-landed resolver file or implements its own substitute.

In worker-g, the launcher and every recorded validation command explicitly supply `UV_CACHE_DIR="$HOME/Workspace/dotfiles/.claude/worktrees/worker-g/.uv-cache"` and `TRUSTED_PYTHON=<the pinned absolute regular interpreter available to that worker>`. Record its actual realpath and version. The a03 record observed Python 3.15.0; that observation is not a CI Python-version guarantee.

Fixture parents supply a temporary absolute cache, the absolute regular interpreter they run on, and the private executable bindings before invoking any of the three scripts. Regime fixtures do this independently of the outer runner's cache. Tests deliberately remove or replace individual inputs only in their refusal cases. The existing single online PyYAML seed per private fixture cache remains provisioning, recorded separately; script launches remain offline. Provisioning failure is a named skip locally, never a passing or red regression proof.

The workflow probes establish an OS/system matrix: Ubuntu 24.04 client/server and macOS 14 client, plus the non-required Ubuntu 26.04 client canary. They establish no Python-version matrix. The observed required-job interpreters are Linux Python 3.12 and macOS Python 3.14; the glob implementation must also be available on Python 3.13. Do not describe 3.12/3.13 as workflow matrix entries or infer mise Python installation from the statusline step.

In `.github/workflows/test.yaml`, setup-uv is lines 333–337 and `Run Python unit tests` is lines 339–349, ending in `make unit-test`; mise at lines 223–239 has `install: false` and explicitly installs node, npm tools, ruff and prettier, not Python. In `.github/workflows/agent-assets.yml`, setup-uv is lines 36–39 and validation is lines 41–42; that workflow has no mise or setup-python step. Neither current step supplies these scripts' parent-input contract.

Any direct CI invocation of these scripts needs a trusted job-step prefix after setup-uv and before execution: select and validate the runner's absolute uv/Python bindings in that parent, set `UV_CACHE_DIR="${RUNNER_TEMP}/<job-private-cache>"`, set `TRUSTED_PYTHON` to that selected absolute regular Python, construct the private executable bindings, and preserve the values through the clean launch. For unit CI the insertion point is before test.yaml line 349; for agent-assets direct checker wiring it is before agent-assets.yml line 42 or in its separately added checker step. The existing regime workflow's verifier step at lines 40–43 also needs that contract before invoking a landed checker which requires it.

Those workflow and verifier-launch integration edits belong to P1-11, `dotfiles-T133-regime-ci-a02`, whose scope the orchestrator must update before assigning them. They are not authorized here. This task repairs the allowed fixtures so current required unit jobs invoke the scripts through fixture parents supplying the inputs. The report names pending production wiring and makes no deployment claim.

D-024-25 permits this Codex seat before P1-15; `after: []` adds no P1-15 dispatch dependency. Do not turn that exception into a claim about Claude protections. P1-15's managed settings, failIfUnavailable, exclusions, hooks and effective deployment remain separately verified conditions; this worker keeps every command inside its actual sandbox.

## Files

1. `scripts/orchestrator/task-consistency-check.py` retains C14's dispatched-SHA gate, hashing and parsing the same bytes. A missing or mismatching digest executes no probe and retains `C14: not run (no trusted sha)`. Only the orchestrator supplies the dispatched digest; acceptance never recalculates authorization from a branch copy.

   The complete authorized vocabulary remains `git rev-parse <ref>`, `test -e <path>`, `test -f <path>` and `grep -c <pattern> <path>`. Only the first starts a subprocess, using the validated absolute Git and prescribed flags; its ref is one revision operand, never an option. Test and fixed-string matching-line counts are interpreted in-process after path confinement. Shell expansion, chaining, pipes, redirection, substitution, arbitrary Git subcommands, Python file operands and source commands fail with the unsupported form printed and no execution.

   Retain whitespace normalization, supported-probe output mismatch reporting, C10 literal operands after `git grep -e`, and C6 design confinement. Unsupported forms remain failures rather than absent-tool warnings or network skips. Retain `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_interprets_the_probe_vocabulary_without_a_shell`, including both test flags, fixed-string counts, confinement, hostile forms, marker absence, clean Git launches and consumed-byte identity.

2. `scripts/orchestrator/task-from-plan.py` retains its CLI, committed eleven-file plan-group reads, bundled template, whole-token wave selection, program-item extraction, scope proposals, grep provenance and threat-row generation. The staged/unstaged/untracked clean-plan check establishes provenance, not permission to execute plan text.

   Generation executes no extracted plan command and no bundled or plan-derived Check command. Recognized commands remain text with explicit `verify:` wording that execution and verification are pending; no stdout or exit status is fabricated and absent observation remains distinct from observed empty output. No scratch Check worktree or execution-only cleanup returns.

   The trusted checker is invoked without `--premises-sha`; structural findings and the C14 warning remain visible, and the generated file remains available for editing. `scripts/orchestrator/task-template.md` retains its task-copy, evidence, non-path, effect, Check and Completion defaults with this unverified wording. Retain `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_never_executes_a_plan_command`: committed marker-writing plan and bundled Check text remain unexecuted, no scratch worktree appears and no generated digest becomes premise authority.

3. Generator output remains confined to `<root>/.orchestration/tasks/`, with realpath checks of root, directory and destination, refusal of existing ordinary files and all existing symlinks, including dangling and inside-target links, and `O_EXCL` creation. Write through that exclusively opened descriptor without reopening the leaf. Existing targets and outside-root markers remain unchanged; same-UID parent-directory races remain residual.

   Retain `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_the_generator_refuses_a_symlinked_or_existing_output`, covering existing files, existing/dangling symlinks, outside destinations, symlinked parents and fresh confined creation.

4. `scripts/orchestrator/plan-check.py` retains F1–F6, eleven-file scope, timestamped acceptance drift, per-occurrence PR comparisons, forbidden-pattern checks, trusted read-only gh, no record writes, exit 1 for violations and exit 0 for clean results. Dedicated drift/invariant fixtures use no live GitHub service.

   Replace `glob.translate` with a translator available on Python 3.12 and 3.13. Using `fnmatch.translate` per path component is sufficient if `**` is handled explicitly: `*`, `?` and bracket classes match within one component; a whole `**` component matches zero or more components, so `scripts/**/*.py` includes both direct and nested children. Preserve hidden-file inclusion and trailing `/**` behavior.

   Validate patterns before enumeration; absolute and parent-traversal patterns escaping the root fail. Never follow directory symlinks, even to inside-root directories, and never enter one before checking it. Realpath-check matches before inspection/reporting; outside filenames are not collected or disclosed. Retain concrete overlap and literal-versus-glob behavior. Retain `tests/unit/test_plan_check.py::PlanCheckTest::test_globs_never_resolve_outside_root`.

   Add `tests/unit/test_plan_check.py::PlanCheckTest::test_glob_translation_works_without_glob_translate`. Its table covers direct and nested `**`, zero-component `**`, trailing `/**`, single-component `*`, `?`, positive/negative bracket cases, hidden files, nonmatches across `/`, and the retained confinement/symlink cases. Exercise the real scope/overlap path with glob.translate unavailable; the production implementation must not call that API. Establish a behavioral red against 82fd9b12 on Python 3.12, not an import or unavailable-runner failure.

5. C11 retains both `tests/<path>::<test>` and `tests/<path>::<Class>::<test>` with identifier class/test segments; malformed selectors remain findings. Retain `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c11_accepts_the_pytest_node_id_with_a_class`, including function form, class form, spaces and extra-segment rejection. Keep the historical a02 fixture under the retained a03 evidence path and use a filename matching its task id.

   Retain C1–C10, C7b, C12, C13 and C15 apart from shared launch repairs. C11/C14 docstrings state their contracts. Existing out-of-scope owner checks, residual length and disposition grammar remain; the twelve audit P2 remain with their owner.

6. Apply the parent-input contract once in the existing shared launch code and update all callers in the three scripts and allowed tests. Preserve the same validated cache and interpreter in every clean child. Preserve complete uv flags and isolated Python without rediscovering either executable or interpreter. Remove the install-tree scan responsible for StopIteration; no new resolver script, host-root allowlist expansion or fallback is added.

   Retain `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_uv_launches_ignore_a_hostile_venv_and_uv_config`, `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_all_three_scripts_refuse_an_unset_uv_cache_dir` and `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_all_three_scripts_refuse_a_relative_uv_cache_dir`. All successful fixtures supply the other valid inputs; refusal fixtures prove no subprocess/cache access or fallback.

   Add `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_all_three_scripts_use_parent_supplied_launch_bindings`. A fixture parent supplies the actual absolute runner tools, temporary cache and interpreter while install-root discovery is unavailable; all three scripts reach their intended behavior. Trace the generator's checker child and assert the exact supplied interpreter, cache, flags, clean environment and resolved executable binding. Plant PATH shims, .venv and uv.toml markers and assert none executes. No fixture requires a real /opt/hostedtoolcache directory or a writable host install root.

   Add `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_all_three_scripts_refuse_an_unset_trusted_python` and `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_all_three_scripts_refuse_an_invalid_trusted_python`. The latter covers a relative path, nonexistent absolute path and absolute directory. For every script supply all other valid inputs and assert the exact interpreter refusal, nonzero exit, no child/cache access and no fallback. Retain separate worker-root and shim binding refusals with their actual messages.

7. Retain the four Git marker regressions: `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_refuse_repository_local_filters_before_status_or_diff`, `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_refuse_a_checkout_with_gitmodules`, `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_refuse_a_redirected_worktree` and `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_disable_lazy_fetch_for_missing_objects`.

   Preserve local, worktree-scoped and included filter cases with matching origins/keys; submodule-filter marker absence and plain-checkout success; core.worktree refusal plus explicitly bound Git toplevel equality; and missing-object behavior with GIT_NO_LAZY_FETCH and absent credential-helper marker. Their valid parent inputs must prevent an unrelated launch refusal from supplying a false green.

   Add `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_all_three_scripts_ignore_git_url_rewrites_for_canonical_main`. In a temporary repository set `remote.origin.url=https://github.com/mryfmo/dotfiles.git` and `url.https://rewrite.invalid/.insteadOf=https://github.com/`, and supply valid private parent inputs. A fake trusted gh records endpoint paths and returns a canonical 40-hex main SHA plus distinct pinned contents. Trigger each script's applicable main/ledger reads, including the generator's checker child, checker baselines and plan-check's F6 ledger and invariant baseline. Assert `repos/mryfmo/dotfiles/git/ref/heads/main` is requested with `--jq .object.sha`, every contents endpoint is `repos/mryfmo/dotfiles/contents/<path>?ref=<that sha40>`, and the expected verdict consumes those contents rather than conflicting local refs/ledger bytes. Trace Git calls and assert no ls-remote, remote resolution or fetch occurs and no URL-rewrite destination is consulted. The fake gh rejects any other repository or unpinned contents endpoint; a launch refusal or stubbed success is not proof. Record its behavioral red at 82fd9b12 and final green under Check's evidence rules.

8. `tests/unit/test_regime_ci.py` creates an absolute temporary UV_CACHE_DIR in its fixture setup, supplies the fixture's absolute regular TRUSTED_PYTHON and executable bindings, and passes them to every verifier/checker child. Do not borrow or silently default to the outer runner's cache. Retain inherited reset-lineage fixture dispositions and the complete existing module.

   Add `tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_supplies_absolute_parent_launch_inputs_to_the_checker`. With the outer cache/interpreter variables absent, the fixture parent supplies valid temporary inputs and the base's real checker reaches its expected verdict. Assert the cache is absolute and temporary and the binding reaches the checker; a stubbed checker success or an unrelated failure is not proof.

9. Normalize the five PR #415 R4 hits at the 82fd9b12 locations `task-consistency-check.py:47,110` and `task-from-plan.py:56,106,125` through the lint's accepted normalizers. This is D-024-24 rebase repair within the task's files. Existing filesystem identity comparisons use realpath/resolve or samefile as appropriate; comparisons of logical relative-name tokens use an explicit normalise_/normalize_ operation preserving their grammar. Do not apply filesystem resolution to Git refs or wildcard semantics.

   No baseline, lint implementation, allow marker, dummy normalizer or identifier renaming suppresses a hit. Retained confinement, command recognition, scope proposal and generation fixtures stay green. Add `tests/unit/test_task_from_plan.py::TaskFromPlanTest::test_task_scripts_have_no_unbaselined_comparison_hits`, invoking the landed lint over the three production Python files with those paths explicitly treated as changed, and assert exit 0 with no hits. The red identifies the five R4 findings, not missing lint code.

The allowed modules reuse their existing temporary-repository and cache fixtures. Existing tests whose historical names mention executed commands retain their actual non-execution assertions. No test changes an expected set merely to conceal a regression. P1-6's separately owned common helper remains untouched.

## Measurement and out of scope

The executed `git diff --numstat b22a5580 82fd9b12` measures 801 changed source lines outside tests/ and .orchestration/; adding 120 estimated for parent-input/launch repair, 60 for compatible glob translation, 30 for comparison normalization and 89 margin gives a source cap of 1100 changed lines.

The same measurement gives 1065 changed lines under tests/; adding 240 estimated for launch/refusal and regime-fixture coverage, 120 for glob coverage, 35 for comparison coverage, 60 for canonical-main URL-rewrite coverage and 80 margin gives a test cap of 1600 changed lines.

These are additions plus deletions across the complete inherited implementation, fixtures and bundled template. The reset does not restart measurement at 82fd9b12. `.orchestration/` artifacts remain outside both totals.

`dotfiles-T133-task-generator-plan-check-followup-a01` remains the unchanged advisory owner of `audit:8a09b93:1` through `audit:8a09b93:12`: C15 local-design acceptance; C12 instruction coverage and confinement; generator root-file omission, directory-child rows, normalization and unavailable-command recognition; F1 completion parsing; edited-file SHA evidence; selector grammar; template feedback and parser-gap search. Reconcile this lineage's C11 fix evidence with that owner rather than implementing the correction twice.

Dispatch SHA/warning forwarding remains with P1-5/P1-6 after result-precheck; CI regime/validate wiring and trusted job prefixes remain P1-11; reset-task.sh remains C-69. Ruleset tooling, permission policy, seat settings, managed deployment, credential separation, agmsg hardening and reservation locks remain outside scope.

Canonical task, plan, progress, acceptance, owner and approval-ledger records remain outside worker edits. The orchestrator performs reset/ownership bookkeeping. The named predecessor-copy deletion is the sole exception. These scripts read local data without treating it as permission approval or integration authority.

## Check

`.orchestration/dotfiles-T133-task-generator-plan-check-a04/validation.md` records commands, verbatim stdout/stderr, exits, revisions, interpreter realpaths/versions, parent executable bindings and cache paths. Every worker validation invocation explicitly carries the worker cache prefix and `TRUSTED_PYTHON`; supplied values survive clean launch boundaries.

Run `make unit-test`, `make format`, and the trusted absolute uv with `run --no-config --no-project --offline --python "$TRUSTED_PYTHON" python -I -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v`, with the required dependencies already provisioned. All four task modules are green.

Run the complete `tests.unit.test_regime_ci` module and separately its `RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage` invocation through the same trusted launch. The new absolute-input regime regression and retained fixtures are green.

Retain the twelve a03 regression proofs against `8a09b9365932f23b09df8aa2385a93d0b3016a3e`, with their regression-source SHA256, exact commands, outputs and exits, and rerun their final green tests. They are historical red evidence, not new failures attributed to 82fd9b12. Every complete selector named in Files maps to its unittest class/method invocation.

Write the new launch-binding, interpreter-refusal, glob, regime-input and comparison regressions before their fixes and establish behavioral red against production at `82fd9b12f79073ac706423f2716eac701feaebb3`, then green on the final implementation. Record production revision, current regression-source SHA256, command, output, exit and interpreter version. The comparison red uses the landed lint from main against the named head's files; the glob red uses Python 3.12. Missing methods, import failures, unavailable tools, zero-test runs or unrelated environment refusals are not red proofs. Final required regressions are not skipped for provisioning failure.

Run the trusted interpreter with `-I scripts/lint-comparisons.py scripts/orchestrator/task-consistency-check.py scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py --changed scripts/orchestrator/task-consistency-check.py scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py`; require exit 0 and no hits, with no baseline or suppression edit.

Run the trusted uv with `run --no-config --no-project --offline --python "$TRUSTED_PYTHON" --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-*.md`; preserve complete output and exit. Account for C1–C15 and C7b separately from C14 warnings and known owner findings.

Without `--premises-sha`, record C14 as not run with its warning. An authorized rerun uses only the orchestrator's dispatched digest and fixed vocabulary. Unsupported historical or new authoring probes fail with their forms printed; record actual results, tested root and revision without granting shell fallback or replacing the trusted digest from branch bytes.

Run the trusted uv with the same clean flags and `--with pyyaml python -I scripts/orchestrator/plan-check.py` once; preserve output and exit. Report real-plan violations for the orchestrator. Dedicated fixtures exercise --drift and --invariants without live GitHub access and cover the complete glob/selector grammar cases in Files.

Reproduce an inherited full-suite or formatting failure against the unchanged base in the same sandbox and record the comparison; never label it green or repair outside allowed_files. The four named CI defects are assigned repairs, not inherited-failure exemptions. Required final-head GitHub jobs `test (ubuntu-24.04, client)`, `test (ubuntu-24.04, server)`, `test (macos-14, client)` and `validate` are green before RESULT; Linux and macOS unit execution is recorded, not replaced by a skip or local result. Record the actual Python versions and distinguish the Ubuntu 26.04 canary from required jobs.

Orchestrator executions use the trusted parent, main-checkout private cache, pinned absolute interpreter and complete launch contract. Worker runs use worker-g/.uv-cache and its supplied interpreter inside the sandbox. Successful script fixtures use temporary absolute caches and explicit interpreter bindings; invalid inputs occur only in refusal fixtures. Evidence records actual commands rather than this text's placeholders.

The complete final diff against the merge-base with `origin/main` (three-dot) has at most 1100 changed lines outside `tests/` and `.orchestration/`.

The complete final diff against the merge-base with `origin/main` (three-dot) has at most 1600 changed lines under `tests/`.

Record `git diff --numstat b22a5580 HEAD` and `git diff --numstat origin/main...HEAD` through the prescribed trusted Git invocation. `measure.md` and RESULT contain comparison identities, per-file numstat, both totals and the complete changed-file inventory.

Before dispatch, the orchestrator runs the format-2 checks and obtains the required C-80 security-profile review of this complete text; no passing result is presumed here. At acceptance it verifies the predecessor-copy replacement and byte identity, evidence, actual parent-input behavior and honest deployment residuals. Any P1-15 deployment claim requires make update and effective-setting evidence. Local Bats tests do not run; GitHub Actions supplies required Bats results.

## Completion

One branch, `tools/task-generator-plan-check-a01`, continues PR #417 from `82fd9b12f79073ac706423f2716eac701feaebb3`. The first push contains the a03 task-copy deletion and byte-identical a04 copy. No second implementation branch or PR is created; a03 implementation, evidence and stopped-round history remain.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's scope, comparison base, 1100/1600 caps, continuing branch and review restrictions. This text's continuation, automatic-review window and prohibition on a requested Codex review govern the reset.

`dotfiles-T133-task-generator-plan-check-followup-a01` owns every advisory P2 assigned from this task and retains the twelve a02 audit P2. Before integration the orchestrator records each advisory ownership disposition against that existing task and reconciles C11 fix evidence before its later dispatch.

RESULT carries `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md>` and `precheck=<the precheck evidence hash>` when PR #411 has merged and the applicable precheck ran; otherwise it carries `precheck=pending-411`.

RESULT names final head, base, branch, changed files, new production-file inventory, exact selectors, inherited/new red proofs, final greens, measured caps, feedback dispositions and evidence paths. It records trusted roots and executable realpaths, parent input provenance, private PATH, Git flags, fixed probes, uv arguments, cache, interpreter/version, input digests, comparison normalization and supported-version evidence. It names pending P1-11 launch wiring and dispatch SHA/warning forwarding as externally owned and records verified P1-15 deployment or its actual residual.

The worker's pre-push review is one round at most. A surviving P0/P1 appears open in RESULT for the orchestrator and operator. An inherited Bot P0/P1 receives its actual root-cause disposition or remains open; threads use `open:<thread id>` and review-body findings `open:review-<review id>`.

Every worker-side fix round counts toward INV-6 and C-61, including CI repair before RESULT. Start no additional private correction/review cycle. Keep a01–a03 stopped histories and amendment accounting; a third non-advisory finding of one class stops the artifact under plan 006 and requires recorded search and redesign.

The Codex seat writes required evidence at these relative paths in its own worktree and states that location in RESULT. Review evidence uses the `-worker-` infix; the orchestrator copies it by absolute path before acceptance. The report maps the four a04 causes to fixes and tests, retains earlier finding dispositions and distinguishes observations from deployment claims.

Crit remains agent-side: repository-compliant crit-data evidence and receipt, with no browser review, publication or human review request. This task is security: true; the orchestrator obtains the final-head task audit and separate security-profile review before the integration gate.

Final-head CI, complete feedback sweep, dispositions, task audit, acceptance record and gate follow Orchestrator Playbook step 10 in order, using PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and the required review receipt. A changed head receives fresh applicable evidence. Run make require-crit-review before completion and the integration gate before `gh pr merge --squash --match-head-commit <audited head>`. The worker has no merge assignment.

Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window; record absence as `bot: none`. Every feedback item has its proposed disposition and surviving P0/P1 remains open for the operator's decision.

Every gh command and Git write is a separate command without chaining or a wrapper combining writes. All worker commands stay inside the sandbox. A denial or unavailable operation produces a blocked PONG with exact command, output and boundary; no alternative tool, API or command bypasses it. Until P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written with the file-edit tool, never Bash heredoc or echo.

The report states user-visible behavior: generation keeps commands unverified; existing output/symlinks are refused; C14 interprets fixed probes without a shell; launch inputs come from the trusted parent; hostile virtualenv/config discovery is ignored; C11 accepts class selectors; and confined glob checks work without Python-3.13-only APIs. No merge alone establishes deployment.

Local Bats, production workflow-prefix deployment and the advisory owner's twelve findings are outside this worker's checks. Trusted-parent authority, same-UID host access and shared GitHub credentials remain residual risks.

## Amendment 1 (2026-10-19T20:2xZ)

The caps are measured against the merge-base with `origin/main` (three-dot diff), not against the historical base: a rebase or update-branch brings main's own changes into a two-dot diff and would exhaust the cap before any new code. The worker may use the Python 3.12 runtime it installed with uv under its private temporary directory, by absolute path, for the 3.12 compatibility runs; the optional `~/.local/bin/python3.12` alias the installer could not create is not needed (the sandbox refusal is recorded in sandbox.md, not repaired). Nothing else changes.

## Checks (pasted by the orchestrator before each send)

```
dispatch (reset of a03), 2026-10-19T20:1xZ; task-consistency-check.py: OK; C-80: .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-text-security-545281d.md.last.md Verdict: correct (round 2; round 1: the ls-remote P1 and the row selector); D-024-25 (Codex seat before P1-15)
task=dotfiles-T133-task-generator-plan-check-a04 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=none..none (-) source=live
detail: pr=none authors=- tasks=- results=- questions=- withdrawn=- bot_heads=- source=live
```