# Report: dotfiles-T124-wave1-task-validator-a01

- Worker: `claude-standard-dot-a001` (Claude Code, `standard`), worktree `.claude/worktrees/worker-c`.
- Branch: `feat/task-validator`, from `origin/main` `d29ce4c1`.
- PR: #313, head `e6b30e9670569604666730bf1de042b51cf4f2b7` (RESULT round 2). Commits:
  - d680a607: the validator, the shared tiers, the boundary check, `REVIEW_TREE`, the prose and the tests.
  - ce9d3dd2: the gate-command fix. `test_pr_feedback` pins step 10's command string, so every text now writes `make require-crit-review -C <main checkout> REVIEW_TREE=<review worktree>`.
  - f4f845fd: Worker Playbook step 1 runs the validator from the worktree, because the task branch only comes in step 2 (an ordering error my own review caught).
  - 5a17d633: the nine Bot findings on ce9d3dd2 (below).
  - 0d6d5aed: Amendment 3 (the receipt bound to the canonical hash), Amendment 2 (design-reset records) and the seven Bot findings on 5a17d633.
  - 918a91b8: CI's `validate` job on 0d6d5aed failed. The repository's secret scan read `<redacted:secret-pattern>` in the NFA as a committed secret, so the variable is now `piece`. The commit also adds the `kind: chore` case: the mutation run showed that the kind membership rule was pinned only by the type check.
  - 2d2ae688: Amendment 4 (the process tier) and Amendment 5 (the six Bot findings on 0d6d5aed).
  - 4f9627ac: Amendment 6 (`implementing_tasks` hashed) and the four other Bot findings on 2d2ae688.
  - ab0f81eb: the three Bot findings on 4f9627ac.
  - a11e3617: Amendments 7 and 8 (the `redesign` profile) and the other two Bot findings on ab0f81eb. The first RESULT was sent at this head.
  - e6b30e96: revise round 1, the ten Bot findings open at the first RESULT.
- CI: 14/14 checks pass on e6b30e96, as on every head since 5a17d633. 0d6d5aed failed `validate` (the secret scan; fixed in 918a91b8) (validation §8).
- Bot: the Codex Code Review reviewed every head from ce9d3dd2 to e6b30e96 and raised findings on each, 46 threads in all. 43 are fixed and named `fixed:<sha>` in the RESULT, the ten from the first RESULT in e6b30e96. The three on e6b30e96, the round-2 head, are open with proposed handling below; one is a P1, the first Bot P1 on a head after the first RESULT that T126's INV-5(d) counts. The Security Review ran once, on ce9d3dd2, with no finding. Rechecked right before the RESULT (validation §8).
- Status: ready_for_review, with three Bot findings on e6b30e96 open (below)

## Task start

- I read the design and all three of its review receipts.
- Two round-3 notes conflicted with the task as first written: the gate-source routing, and the gate-from-`main` texts. I asked about both with defaults (09:02Z). Amendment 1 (09:01:15Z) had already answered both, the same way as the defaults, and my question was read after it. So I withdrew both questions (09:04Z) and applied Amendment 1 before writing any code.
- The first run of the new validator was on this task's own file: `valid` (validation §1).

## What changed

This section describes the first commit, d680a607. What each later commit added, from Amendment 2 to 8 and the six Bot rounds, is under "Codex Bot threads" and the amendment sections below, and validation §5 lists every rule with the test that pins it.

- **`scripts/lib/high_risk_paths.py` (new).**
  - The **review tier**, `HIGH_RISK_PREFIXES`, `HIGH_RISK_FILES` and `HIGH_RISK_TOKENS`, copied unchanged from the gate. `scripts/require-crit-review.py` is untouched (Amendment 1). `test_the_module_review_tier_equals_the_gate_constants` loads the gate by path and asserts the three lists are equal, until wave 2a switches the gate to the import.
  - The **design tier** is explicit glob patterns, as the round-3 note asked:
    - `install/**` and `setup.sh`;
    - `scripts/lib/github-release.sh`, `scripts/update-agent-assets.sh` and `scripts/upgrade-tools.sh`;
    - the whole of `home/dot_agents/agent-config.yaml`;
    - the four gate scripts;
    - `executable_herdr-agents` and `executable_permgate`;
    - `home/dot_codex/**`, `.claude/hooks/**` and `home/dot_claude/hooks/**`;
    - the rendered `claude-settings-managed.json` and `codex-config-managed.toml`, `modify_private_settings.json` and `permgate-policy.yaml`;
    - the auth helpers.
  - **Auth helpers**, found with `git grep -ln 'gh auth\|credential' -- home install scripts` (validation §6):
    - `home/dot_config/git/config.tmpl`: git's `!gh auth git-credential` helper;
    - `home/dot_local/bin/common/executable_setup-gh`: `gh auth login` and `refresh`;
    - `scripts/gh-auth.sh`: the `make gh-auth` login.

    The other matches are not credential handlers. `install/common/gh_extensions.sh` and `install/ubuntu/common/apparmor_userns.sh` are already under `install/**`, and `scripts/lib/github-release.sh` is listed. `scripts/pr-feedback.py` and `scripts/check-agent-runtime.py` only check `gh auth status`. `scripts/generate-agent-configs.py` writes a comment about Codex's MCP credential store. The README files, `SKILL.md`, `agent-config.yaml` and the rendered settings are prose or already in the tier. `p10k.zsh` mentions Google credentials only in prompt comments.

  - `glob_regex`: `**` and `**/` cross directories; `*` and `?` stay inside one directory.
  - `parse_front_matter`: a strict YAML subset, which the gate imports in wave 2a and which needs no PyYAML. It covers nested maps, lists of scalars, and plain, quoted, `{}` and `[]` scalars. It raises on anything PyYAML would read differently: flow collections, aliases, block scalars, `: ` or ` #` inside a plain scalar, dates, YAML 1.1 booleans, floats, duplicate keys and tabs.

    On every task file in the main checkout that it accepts, it gives the same result as PyYAML (validation §6). It refuses only three legacy headers with unquoted timestamps; PyYAML would turn those into datetimes.

  - `canonical_design_hash`: exactly the task's expression over `invariants`, `threat_model` and `trust_anchors`.
- **`scripts/validate-task.py` (new).** Every rule in task item 2:
  - Paths resolve against the main checkout through `git rev-parse --git-common-dir`. `allowed_files` globs expand against that checkout's tracked files.
  - A file with no `format: 2` is `legacy` with exit 0. That includes a header that fails to parse but does not claim `format: 2`.
  - `--json` prints the whole report. `--print-design-hash` prints the hash of the design named in `design_review.design`. For the design file, which names itself, that is `36ebd76d9bdbd53f3df668d14be353de051e1a8e193f1d5c958ece9829bc8f05`.
  - It runs on Python 3.9, macOS's `/usr/bin/python3`, which the boundary check finds there.
- **`scripts/check-regime-boundary.sh`.** It runs the validator on every `.orchestration/tasks/*.md` in the main checkout. Each failure line of a failing `format: 2` file becomes a `regime-boundary:` violation; legacy files and warnings are skipped. The shdoc lists the new check.
- **`Makefile`.** With `REVIEW_TREE` set, the recipe becomes `cd "$(REVIEW_TREE)" && … "$(CURDIR)/scripts/require-crit-review.py" …`, with the same variables. Without it, `make -n` output is byte-identical to `d29ce4c1` (validation §6). The texts write `make require-crit-review -C <main checkout> REVIEW_TREE=<review worktree>`: GNU make takes `-C` after the target, and that keeps the step 10 string that `test_pr_feedback` pins.
- **Prose.**
  - SKILL step 3: the front matter, the two tiers, and the design review before a security task is dispatched.
  - SKILL step 10.4: the gate from `main`. It is not run while `main` is at the audited head; the gate refuses that case from wave 2a.
  - Worker Playbook step 1: run the validator first, and answer `status=blocked` on a failure.
  - The agmsg rule, in the Routing bullet: "every task file passes `scripts/validate-task.py`; security tasks carry a reviewed design".
  - `pr-integration.md`, `crit-review.md` (which keeps the local pre-completion run, as distinct from the acceptance gate), the AGENTS.md "Agent Review Evidence" section, and one README paragraph under the regime section.

## Codex Bot threads

- **ce9d3dd2**, all fixed in 5a17d633, with tests and mutations in validation §5:
  - 4237190641 (P1): `./install/common/tool.sh` neither matched the design tier nor expanded, so a security task could pass as non-security, and the wave count could be dodged the same way. `allowed_files` entries must now be canonical repository-relative paths: no leading `/` or `./`, no `..`, `//` or trailing `/`.
  - 4237190645 (P1): an absolute or `../` `design_review` path could name a file outside the repository. Both files must now resolve, symlinks included, to a file inside the main checkout.
  - 4237190646 (P1): a security code task could name itself as its design and supply its own threat model, which also skipped the subset rule. `design_review.design` must now be a separate `kind: design` task; only a design task may name itself. A design file without `format: 2` front matter now fails too (it used to be skipped).
  - 4237190648 (P2): `security: 1` passed the membership check, because `1 == True`, and then read as false. `security` must now be a boolean.
  - 4237190649 (P1): with a `REVIEW_TREE` that is not this repository's worktree, the gate skipped and exited 0, or judged another repository. The recipe now compares `git rev-parse --git-common-dir` of the tree with this checkout's and refuses a mismatch before the gate runs.
  - 4237190651 (P1): `format: 2 # current schema` failed to parse but missed the narrow fallback regex, so it passed as legacy. Any header that names a format now fails closed when it does not parse. The same family includes a gap the Bot did not name, which is also closed: a header naming `format: "2"` (a string) or `format: 3` used to pass as legacy; it now fails.
  - 4237190654 (P2): `'it's risky'` was accepted although YAML rejects it. A single-quoted scalar must now double its inner quotes.
  - 4237190656 (P1): the design tier missed security-defining sources. It now adds `scripts/lib/high_risk_paths.py` itself, `scripts/generate-agent-configs.py` (it renders the sandbox and permission settings), `.claude/settings.json`, `.claude/contextdb/**` (the hook implementation), `executable_provision-machine-key` and, of the same class, `executable_setup-gpg`. My credential grep had missed the two key scripts because neither mentions `gh auth` or a credential.
  - 4237190658 (P2): `task_id` now matches the same one-segment pattern the audit path enforces (`herdr-agents:1872`).
- **5a17d633**, the six findings fixed in 0d6d5aed, and 4237230624 by Amendment 3 in the same commit:
  - 4237230621 (P1): a quoted `"format": 2` key made the parser raise, and the fallback regex missed it. It now finds `format` quoted or not, at a line start or after `{` or `,`.
  - 4237230623 (P1): `executable_agmsg-dispatch`, the one command the Claude sandbox excludes and the managed settings pre-allow, was not in the design tier. It is now.
  - 4237230624 (P1): the receipt was only checked to exist. I asked (q1). Amendment 3 chose to bind it now: the receipt's `design:` must end in the design's canonical hash, and its `reviewer:` must be one `-aNNN` identity, which is the stop gate's non-orchestrator rule. The receipt header holds an unquoted timestamp, so the validator reads those two lines directly instead of parsing the header. As Amendment 3 expects, every T124 security task file (the design, waves 1, 1b and 3b) fails until the canonical receipt exists. Its round-3 receipt hashed the whole file (`d31c1bb7…`); the canonical hash is `36ebd76d…`.
  - 4237230627 (P1): `.claude/*/new.py` was not security, because nothing tracked matched it yet. `may_touch_design_tier` now intersects each allowed glob exactly with the tier's literal and `<dir>/**` patterns: an NFA over the glob checks whether any path it can name starts with the tier directory. It refuses any other tier pattern shape rather than guess.
  - 4237230644 (P1): Worker Playbook step 1 ran the worktree's validator, which can still be the previous task's branch. It now runs `<main checkout>/scripts/validate-task.py`; the main checkout stays on `main`.
  - 4237230646 (P1): `REVIEW_TREE=<repo>/.git` shared the common dir and passed. The recipe now also requires `--is-inside-work-tree` to be true and `--show-toplevel` to equal the tree's physical path, which refuses the `.git` directory and any subdirectory.
  - 4237230650 (P2): `kind: []` raised `TypeError`, so `--json` printed no report. `kind` is now type-checked before set membership.
- **0d6d5aed**, all fixed in 2d2ae688 as Amendment 5 directs:
  - 4237298693 (P1): `reset_of` dispatched to reset validation wherever the file was, so a "task" in `.orchestration/tasks/` could skip every task rule. Reset validation now runs only for files in `.orchestration/acceptance/`; `reset_of` in any other file fails.
  - 4237298696 (P1): `home/.chezmoiscripts/**`, the apply-time wrappers that include the private-key decrypt, joins the design tier.
  - 4237298700 (P2): waves that listed today's matches of a glob left the files it can create uncovered. An allowed glob must now appear verbatim in exactly one wave; a plain path must be listed, or matched by a wave glob.
  - 4237298702 (P1): the receipt must carry exactly one `Design verdict: accept` line, as rounds 1–3 and the canonical receipt write it.
  - 4237298704 (P1): one reviewed design could authorize an unrelated security task. A task that names a separate design must be listed in that design's `implementing_tasks`. This key is not hashed, so adding a task needs no new review; the T124 design now lists its three wave tasks.
  - 4237298706 (P2): blank trust anchors are refused.
- **2d2ae688**, all fixed in 4f9627ac:
  - 4237362484 (P1): `implementing_tasks` decided which tasks a design authorizes but was not hashed, so a reviewed design could add a task under the same receipt. I asked (q4); Amendment 6 adds it to the canonical hash keys. The hash of every T124 and T126 design therefore changes, and the orchestrator requests new receipts after this push.
  - 4237362485 (P2): a scalar `implementing_tasks` matched as a substring. It must now be a list of task ids.
  - 4237362488 (P2): a reset could name the abandoned task as its own redesign. `redesign_task` must now differ from `reset_of`.
  - 4237362491 (P2): any repository file with `kind: design` could authorize. `design_review.design` must now be `.orchestration/tasks/<task id>.md` with that `task_id`, which is also the set of files the boundary check scans.
  - 4237362495 (P1): `[i]nstall/**` is `install/**` to a shell but a literal to the tier match. `[`, `]`, `{` and `}` are now refused in allowed paths; only `*`, `**` and `?` are glob syntax.
- **4f9627ac**, all fixed in ab0f81eb:
  - 4237404235 (P2): `home/dot_agents/s*/new.md` was `docs`, although it can create `home/dot_agents/skills/new.md`. Because a wildcard can also create a name carrying a review token (`docs/hooks.md`), any glob entry is now at least `review`; only explicit prose paths are `docs`.
  - 4237404237 (P2): `check-regime-boundary` now also validates `.orchestration/acceptance/*-design-reset.md`.
  - 4237404238 (P1): Worker Playbook step 1 now stops on a `superseded` result as well as on a failure. The validator still exits 0 for a superseded task, as the task's exit rule says; the playbook decides.
- **ab0f81eb**, all fixed in a11e3617:
  - 4237437333 (P1): a task-path symlink to a reset record was judged as the record, because the dispatch resolved the file. A task file must now be a regular file. Reset mode follows the file's own directory, `path.parent.resolve()`, never its link target.
  - 4237437337 (P2): `invariants: {}` passed for a non-security task. Every task now needs at least one `INV-n: sentence`. The task text required one only for a security task, but this is a finding on the task's own wording, so it is fixed, and no current `format: 2` file loses its validity.
  - 4237437341 (P2): `process_tiers.design.profiles.redesign` named an undefined profile. I asked (q5). Amendment 7 defines `model_profiles.redesign` here: `claude-fable-5-1` at `xhigh`, and Codex mirroring `deep`'s `gpt-5.6-sol` at `xhigh`. The renderer then writes `MODEL_PROFILE_REDESIGN_*` and `home/dot_codex/modify_private_redesign.config.toml`. That needed `validate-agent-assets.py` to accept a seventh profile; I reported the scope gap (q6), and Amendment 8 added the validator and its three test lines. `test_the_repository_renders_the_redesign_profile` is the one assertion Amendment 7 allows in `test_generate_agent_configs.py`.
- **My own regression, found while fixing:** since 0d6d5aed the subset rule sat inside the receipt check, so it was skipped whenever the receipt check had already failed. The task was invalid either way, so nothing slipped through; only the report omitted the subset failure. It is back under the design check.
- The worker resolves no thread.

## Amendments 4 and 5

- **Amendment 4, the tier stamp.** `validate-task.py` derives `tier` and prints it with `--print-tier`; `--json` carries it too:
  - `design`: any allowed path can name a design-tier file, or `security: true`;
  - `review`: otherwise, any path matches the review tier (the gate's `high_risk_reason`), or is neither prose nor in a tier;
  - `docs`: every path ends in the gate's low-risk suffixes, `.md` or `.txt`.

  A path that is neither prose nor in a tier counts as `review`, because the T126 table defines `docs` as prose-only. That is my reading; correct it if you meant otherwise.

  `home/dot_agents/agent-config.yaml` gains `process_tiers` with the T126 table's stages, profiles and limits, in the YAML subset. The validator reads the block back from the manifest beside its own script, so `main`'s validator reads `main`'s table. It requires an entry for the derived tier and enforces nothing from it. PyYAML reads the same map (validation §6). The renderer ignores the key: `make render-check` and `validate-agent-assets.py` pass. `agent-config.yaml` is in the task file's `allowed_files` only through Amendment 4's text, not its front matter. The tests:
  - `test_the_tier_is_derived_and_needs_a_process_tiers_entry`, for the three tiers, `--print-tier`, and a validator copy whose manifest lacks the entry;
  - the review-tier equality test, which now covers `LOW_RISK_SUFFIXES` too.

- **Amendment 5:** the six fixes above. Also, the parser now reads a flow list of ids or paths (`[dotfiles-T125-acceptance-automation-a01]`), the way PyYAML does; anything richer is still refused.

## Amendments 2 and 3

- **Amendment 2** (09:27Z). I read it only at 10:08Z, because I did not check the inbox between my questions, and implemented it in 0d6d5aed:
  - `kind: design` is valid without `allowed_files`;
  - a reset record `.orchestration/acceptance/<task id>-design-reset.md` (`reset_of`, `redesign_task`, `redesign_seat`, `reason`) is checked for its shape;
  - the file name must match `reset_of`;
  - `redesign_seat` must contain `-redesign-`;
  - the redesign task must be a `kind: design` task file in the main checkout;
  - it must overlap the abandoned task's `allowed_files`, either through its own `allowed_files` or those of the tasks it lists in `implementing_tasks`. That key name is my choice, because the amendment names no key; rename it if you prefer another;
  - the abandoned task is reported `superseded` when its `superseded_by` names the redesign; otherwise a warning says it is not marked yet;
  - `--help` says the history check is wave 2b's.

  Tests: `test_a_design_reset_record_names_a_redesign_seat_and_an_overlapping_design_task` and `test_a_design_reset_must_overlap_the_abandoned_task`. `check-regime-boundary` does not yet run reset records, because they live in `.orchestration/acceptance/`; that was not asked for.

- **Amendment 3**: q1 is bound now (above). On q2, INV-5(d) (Bot P1 findings on two heads) is met on PR #313. The operator decides between a design reset and a waiver; until then the fixes proceed.

## Main-checkout task files

`dotfiles-T125-acceptance-automation-a01.md` and `dotfiles-T126-regime-v2-a01.md`, which the orchestrator wrote after this task started, fail the validator. T126's line 29 has the same problem as T125's line 10. Line 10, `E1: …(T119: two count corrections)`, holds `: ` inside a plain scalar. PyYAML rejects the line too ("mapping values are not allowed here", validation §6), so the validator is right. `make check-regime-boundary` reports the file until the value is quoted. It is not in `allowed_files`, and I did not touch it.

## Revise round 1 (orchestrator, 2026-10-10): the ten open Bot threads, fixed in e6b30e96

All ten were accepted as proposed in the first RESULT. I first saw the six on 918a91b8 only in the final recheck: I pushed 2d2ae688 before that review arrived, and my later waits looked only at the newest head. That was my miss.

- 4237326681 (P1): `Makefile` joins the design tier, because its `require-crit-review` recipe carries the gate's `REVIEW_TREE` checks.
- 4237326686 (P1): a reset's `redesign_task` must itself validate as a `format: 2` design task. The validator runs on that file, so a legacy-style file, or a design whose receipt does not bind, is refused.
- 4237326688 (P1): a security code task that names a design omits `threat_model` and `trust_anchors`, or carries exactly the design's values. The receipt authenticates only the design.
- 4237326692 (P2): reset overlap now intersects the two globs as automata. `globs_intersect` runs a product of the two glob NFAs over the characters the globs name, `/`, and one stand-in character. So `new/*.sh` and `new/tool.*` overlap even though no such file exists yet. The design tier uses the same function, which replaces the earlier `<dir>/**`-only prefix check.
- 4237326697 (P2): the boundary loop also scans `.orchestration/tasks/.*.md` and dot-prefixed reset records.
- 4237326701 (P1): grandfathering is bound to the checked-in `scripts/legacy-task-ids.txt`. It holds the 310 ids the validator reported `legacy` in the main checkout at e6b30e96, one per line, sorted, and it only shrinks. A formatless file with any other id fails, so a new task cannot opt out.
- 4237495354 (P1): the receipt must be a separate file under `.orchestration/validation/`, never the design or the task itself.
- 4237495358 (P2): an ordinary task validates only when its lexical parent is `.orchestration/tasks/`. That includes a worktree's copy, which the design-review paths still resolve in the main checkout.
- 4237495360 (P1): the recipe refuses a `REVIEW_TREE` whose top level is the checkout running it. The full "the gate checkout is `main` and not at the audited head" rule is W5's.
- 4237495362 (P2): each referenced invariant id keeps the design's sentence.

Each rule has a test that fails when the rule is removed; 72 rules in all (validation §5).

`dotfiles-T124-wave1b-redesign-profile-a01.md`, the orchestrator's file, now fails twice. Its design does not list it in `implementing_tasks`, and its INV-5 sentence differs from the design's (validation §6).

## Open Bot findings on e6b30e96 (named in RESULT round 2, proposed handling)

- 4237594826 (P1): the Bot wants `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and the integration rules in the design tier, because they specify the worker's validator run and the gate invocation. The reviewed design's INV-2 says the opposite: "prose paths are not in the tier", and the review tier already requires review for them. So this is not a fix I can make on my own. Proposed: decide between amending INV-2 (a design change, with a new receipt) and keeping it. If you keep it, the thread is answered with INV-2's text. This is the first Bot P1 on a head after the first RESULT, which T126's INV-5(d) counts.
- 4237594829 (P2): the task-directory check compares only the last two directory names, so `nested/.orchestration/tasks/t-a01.md` passes, and so does a non-`.md` file. Proposed fix: the resolved parent must equal `<the file's own checkout top level>/.orchestration/tasks` (a worktree's copy still passes, a nested one does not), and the file must end in `.md`.
- 4237594831 (P2): a referenced design whose `invariants` is a list makes the sentence comparison raise `TypeError`. Proposed fix: require the design's `invariants` to be a text map before comparing, and report a failure otherwise.

## Scope notes

- **The rule's word budget.** `test_agmsg_orchestration_docs.test_word_budgets` caps `agmsg-orchestration.md` at 450 words, and it had 447. To fit the required invariant clause (11 words), I made three cuts that keep the meaning:
  - I dropped the second "(Worker Playbook step 4)" pointer in Permissions; the bullet still names step 4.
  - "skill, in the sections named below" became "skill sections named below".
  - "in this repository through a task" became "through a repository task".

  None of these is a phrase the test pins. The rule is now at exactly 450 words.

- **The Codex mirror.** The "PR 統合" section of `home/dot_config/codex/AGENTS.md` mirrors `pr-integration.md` and is not in `allowed_files`. It still points to SKILL step 10 for the gate command, which now carries the new form, so it does not contradict the change, but it does not repeat the new sentence. A docs task can mirror it.

## Tests (validation §3, §4, §5)

- `tests/unit/test_validate_task.py` (40 tests at e6b30e96; it started with 17): the cases task item 5 lists, and one or more per Bot finding and amendment. They include the gaming paths for this wave:
  - a single all-encompassing wave;
  - an invariant added after review (the subset rule);
  - a receipt that exists only in the cwd's worktree, not the main checkout;
  - `security: false` on a design-tier path.
- `tests/unit/test_herdr_agents.py`: `test_regime_boundary_check_validates_format_2_task_files_and_skips_legacy`.
- `tests/unit/test_require_crit_review.py`: `ReviewTreeTest`. It runs `make -n` with and without `REVIEW_TREE`, plus a real run in a non-repository tree that the gate then skips.
- **INV-8, one removal per rule family.** Seventy-two rules (twenty from the first commit, the rest from the amendments, the Bot fixes and revise round 1), each removed in a scratch worktree of e6b30e96; each time the pinning test fails, and the tree is restored after each (validation §5).
- **The full unit suite**, inside the sandbox, at the head and at the base `d29ce4c1` (validation §4). Both runs use two stated shims: a `mktemp` that honours `TMPDIR`, and `commit.gpgsign=false` through `GIT_CONFIG_*`, because the host signs commits and the key is unreadable in the sandbox. Base `d29ce4c1`: 925 tests, 54 failing or erroring in the sandbox. Head `e6b30e96`: 968 tests, the same 54 and no other (every intermediate head was run the same way; validation §3–4 says how each went). The first head, d680a607, also failed `test_pr_feedback`'s step 10 string pin, which ce9d3dd2 fixes.

## Invariants

- invariant: INV-1 → tests/unit/test_validate_task.py::test_each_required_key_is_reported, scripts/validate-task.py:245
- invariant: INV-1 → tests/unit/test_herdr_agents.py::test_regime_boundary_check_validates_format_2_task_files_and_skips_legacy, scripts/check-regime-boundary.sh:207
- invariant: INV-2 → tests/unit/test_validate_task.py::test_security_is_derived_from_the_design_tier_only, scripts/validate-task.py:263
- invariant: INV-2 → tests/unit/test_validate_task.py::test_declared_false_on_a_design_tier_path_fails_and_declared_true_is_kept, scripts/validate-task.py:267
- invariant: INV-8 → tests/unit/test_validate_task.py::test_legacy_files_are_grandfathered, scripts/validate-task.py:195

INV-8's rule that every rule has a test that fails when the rule is removed is shown by the 72 removals in validation §5.

INV-1's gate half, "a PR cannot pass `make require-crit-review` unless…", is wave 2a's gate rule. This wave delivers the validator, the worker's first run and the boundary listing.

## Decisions

[memory:decision] dotfiles-T124 wave 1 (orchestrator 2026-10-10): every task is a `format: 2` file validated by `scripts/validate-task.py`; `security` derives from the design tier of `scripts/lib/high_risk_paths.py` (the review tier is the gate's existing lists); a security task names a reviewed design whose canonical key hash the receipt carries; legacy task files are grandfathered.

## CompactionDB

The decision line was added from the main checkout through the permission gate (id `37211877-c628-421f-84ce-7411d1eb77f1`). Validation §7 quotes the command and its output.

## Hooks

- The Understand-Anything stale-graph hook did not fire. `.ua/` is not in `allowed_files`.
- No Plan Mode or Crit plan review server was started.

## Review evidence

The evidence is `.orchestration/validation/dotfiles-T124-wave1-task-validator-a01-worker-crit.json` and `-worker-review-receipt.md`. Crit data was unavailable, so the records hold the independent review (advisor passes before the RESULT), the self-review and the CI and Bot findings: 58 records, 55 resolved, 3 open (the three Bot findings on e6b30e96, each with a proposed handling above; the ten open at the first RESULT were fixed in e6b30e96).

cost: n/a
