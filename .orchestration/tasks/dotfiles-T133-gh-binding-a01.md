---
format: 2
task_id: dotfiles-T133-gh-binding-a01
kind: code
security: true
dispatch_status: blocked-pre-anchor
design_review: {design: .orchestration/plans/024-design-quality.md}
requires_decision: [D-024-69]
after: []
allowed_files:
  - home/dot_mise/config.toml
  - home/dot_agents/agent-config.yaml
  - scripts/validate-agent-assets.py
  - scripts/orchestrator/chain-integrate.sh
  - scripts/orchestrator/orch-gate.sh
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_*.py
  - .orchestration/dotfiles-T133-gh-binding-a01/**
threat_table:
  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "scripts/validate-agent-assets.py", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_chain_integrate_authenticated_decoy"}
  - {control: "scripts/orchestrator/orch-gate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_orch_gate_authenticated_decoy"}
  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_local_review_authenticated_decoy"}
  - {control: "tests/unit/test_*.py", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence-integrity automation; limit edits to Item 6's four modules and independently inspect assertions and red/green logs."}
  - {control: ".orchestration/dotfiles-T133-gh-binding-a01/** including task.md", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence automation; compare anchored bytes, task-copy digest and literal full head against the independently audited PR."}
  - {control: "pin", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
  - {control: "declaration", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "consumer binding", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_consumer_binding_matrix"}
  - {control: "minimal environment", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_gh_environment_is_minimal"}
  - {control: "gh configuration inputs", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_protected_gh_configuration"}
  - {control: "trusted parent before first instruction", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns automatic parent binding; authenticated use stays disabled until the orchestrator measures a clean, absolutely bound parent and private namespace for every non-gh process in the route."}
  - {control: "task metadata", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns dispatch automation; reviewed inventory and populated Checks must match the complete anchored task before dispatch."}
  - {control: "metadata separators", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns byte-integrity automation; compare all front matter, separators and Checks, with no paste after anchor."}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_git_environment_cannot_redirect_fixture_writes"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns uv/Python/Node, permgate and launcher binding; unchanged resolvers run only inside Item 3's measured parent namespace, otherwise authenticated use is blocked."}
  - {control: "new or renamed scripts; future gh routes", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns adoption by absent chain-finish and future checker gh routes; create no consumer here and require their own positive authenticated fixtures before claiming closure."}
  - {control: "remaining git/date/mise executable provenance", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns permanent remaining-tool binding; today's resolver algorithms remain, constrained by the measured parent namespace and token-free discovery, with no authenticated fallback."}
  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns integration follow-through; only the orchestrator integrates the exact audited head through Playbook step 10."}
  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence refresh; rerun CI, feedback, audit, acceptance and gate for every changed head."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns teardown records; none is planned and no dirty state may be discarded without separate authorization."}
  - {control: "orchestrator effect owner-stub amendment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns every residual assigned here; the orchestrator expands its existing stub before anchor, outside worker scope."}
  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns measurement automation; gh-free private-clone evidence and trusted-parent observations must precede a fresh review of the complete populated bytes."}
  - {control: "orchestrator effect installation and deployment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment follow-through; separately verify the pinned install, protected configuration and real authenticated consumer probes before enabling acceptance reads."}
  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns the unchanged item 0 residual; this task establishes no same-UID or credential-separation boundary."}
  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns host protection evidence; item 1 must cover the declaration, binary, configuration source and parent namespace before authenticated use."}
  - {control: "design 5.14 item 2", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 2 integration; the measured trusted-parent compensating control is mandatory now."}
  - {control: "design 5.14 item 3", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 3 integration; apply it to this task's gh inputs without certifying other runtime boundaries."}
  - {control: "design 5.14 item 4", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 4 integration; checked gh identity is consumed directly and same-UID replacement remains item 0's residual."}
  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns unchanged item 5 obligations; retain full head identities and introduce no lock or reservation changes."}
  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment verification; distinguish fixture success, CI and observed host execution under item 6."}
  - {control: "design 5.14 item 7", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns wider item 7 coverage; independently check behavioral assertions and never count setup failure or absent routes as closure."}
  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns future canonical-reader adoption; apply item 8 to active gh routes and do not certify the current local-object checkers."}
  - {control: "design 5.14 item 9", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 9 integration; measured isolated runtimes and the parent's absolute UV_CACHE_DIR remain mandatory."}
  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns denial records; item 10 applies and any denied command stops work with a blocked PONG."}
premises: []
---

# AGMSG-TASK dotfiles-T133-gh-binding-a01 — bind gh on the measured host

D-024-69 supersedes the 2026-10-21 owner stub and pulls this remedy ahead of slices 2-5; pins-a01 merged as #449, after remains empty, and later tool declarations use sibling entries. TASK names worker a012, a Codex seat.
Seven refused C-80 rounds: a07-checker 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1; regime-ci-followup-a02 a232baf/a18a67d. Unbound gh can forge canonical main, design, merge state and PR data and read forwarded credentials.
Design 5.14 items 0-10 apply by reference, particularly 2-4/9; do not restate their trusted-execution contract.
R1 references below identify original lines of .orchestration/tasks/dotfiles-T133-gh-binding-a01.md: 39→Item 3; 76→Item 4; 38/80→Item 6; 105→Item 0; 110→Anchor.

## Items

0. Reviewed baseline amendment for R1:105: local HEAD and origin/main are 7da0cdfab9de9fbea673b82379acd4e317115065; chain-finish.sh is absent, and regime-ci.py/task-consistency-check.py currently use Git, not gh lookups. These are local observations, not authenticated canonical facts.
   Implement the three present shell routes, including their actual gh descendants; do not invent a finish script or add canonical-network behavior to either checker. Future gh adoption belongs to dotfiles-T133-gh-binding-followup-a01 and requires positive authenticated fixtures in those owners.
   This explicit inventory amendment requires C-80 approval with gh-free canonical confirmation before dispatch. If the canonical baseline differs, reauthor and review the whole inventory and threat table; never silently widen scope or claim six routes were closed.
1. Pin "github:cli/cli" = "2.102.0" in home/dot_mise/config.toml, with one adjacent English reason comment following pins-a01; extend the exact-version assertion and retain unrelated pins.
2. Add trusted_tools.gh with version "2.102.0" and path "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh" to agent-config.yaml; later uv/Python/Node bindings extend sibling entries.
   validate-agent-assets.py checks version equals the mise pin, the spelling is normalized and home-anchored, expansion is absolute under the real user's trusted home, and neither spelling nor resolved path is under shims. Refuse missing/malformed declarations, traversal, forged HOME and mismatched identities; one refusal test per rule.
   Runtime reads the protected deployed ~/.agents/agent-config.yaml as data using existing parsing facilities under the measured isolated interpreter; never source/eval it or read a PR/worker copy. Chezmoi already deploys this plain source file; no generated artifact is needed, so leave generate-agent-configs.py and its tests unchanged.
3. Replace gh discovery in chain-integrate.sh and orch-gate.sh, and bind local-review.sh's descendant namespace to the declaration. Cover pr-feedback/gate collectors and review descendants without editing their sources or adding wrappers.
   Require the declared version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target without rediscovery. Missing/mismatching identity emits exactly "refused: gh binding", exits nonzero and performs no canonical operation; no PATH/mise/latest fallback for gh.
   gh api uses --hostname github.com and fixed repos/mryfmo/dotfiles endpoints; other subcommands use --repo github.com/mryfmo/dotfiles or a full fixed-host URL under item 8. Do not add the unsupported --hostname flag to gh pr; version probes make no network call.
   R1:39: before any script, loader, resolver or parser runs with credentials, the orchestrator supplies and measures the trusted parent required by items 2/9, binding Bash, mise, git, uv, Python, Node and every other non-gh executable the selected route can execute.
   Keep today's non-gh resolver algorithms, but constrain their execution and outputs to that preverified private namespace; discovery receives no tokens. A PATH- or mise-selected unchecked parent is forbidden. No self-reexec, sentinel or child cleanup counts as pre-exec evidence; without this compensating control authenticated operation stays blocked.
4. R1:76: launch every bound gh, including identity probes, with a constructed allowlist and protected GH_CONFIG_DIR=/var/empty on this host; verify its resolved directory and ancestors are protected, it is empty and contains no symlink/config payload. Missing/unsafe configuration refuses, without default-home fallback or directory creation.
   Only the call's explicitly supplied token is inherited, normalized to GH_TOKEN; never fetch credentials implicitly from home config/keychain. Supply required nonsecret constants explicitly, including trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output; probes get no token.
   Reject ambient GH_HOST/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git configuration overrides. Apply items 2/9 to the parent and descendants too; every env -i contract carries UV_CACHE_DIR. Record the complete allowed-name set without token values.
   Test planted home/XDG gh config with http_unix_socket, aliases and alternate hosts; neither transport nor child execution may change. Test refusal of unsafe configuration and a positive authenticated operation using the controlled source. Sources: [gh config](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).
5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver algorithm or acceptance-semantic change. No new/renamed executable or executable evidence. Future checkers and missing consumers remain explicitly owned, never represented as implemented here.
6. The test wildcard authorizes only test_supply_chain_policy.py, test_chain_glue.py, test_regime_ci.py and test_task_checkers.py; reuse trusted_exec_contract.py without modifying it and preserve existing assertions.
   R1:38: fix reused chain/regime/checker fixture Git helpers before any init/add/commit/reset/fetch: construct fresh environments, explicit fixture roots and neutralized configuration; do not merge os.environ. Plant GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and hostile local includes/hooks; a second disposable repository's refs/index/bytes and external markers must stay unchanged. See [Git environment](https://git-scm.com/docs/git).
   R1:80: each active route needs a successful authenticated-operation fixture through the declared target, with a synthetic credential, expected fixed host/repository, response consumption and descendant coverage; separately test missing/version/path refusals. Identity refusal can never satisfy a success or decoy assertion.
   Put an executable gh decoy on the lookup path and a hostile mise answer; prove neither is executed or receives the synthetic credential. The trusted-parent fixture binds non-gh tools but must not prebind gh and thereby mask the production defect.
   Implement every closed selector above; the policy test uses separate subtests per refusal rule, and the consumer/environment/configuration matrices cover all three active routes. Absent future routes are not passing matrix entries.
   Write fixtures first; for each behavioral case record red against origin/main production bytes and green at the fix commit, with selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and exit status. Red must reach its intended assertion, not import/setup/missing-tool failure; inventory-only requirements use diff evidence, not fabricated red tests.

## Check

The final diff has at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 700 under `tests/`.
Measure with git diff --numstat <merge-base40> <head40>.
Caps are PR-wide additions plus deletions from git merge-base <authenticated-main40> <head40> (C-123), not round deltas. Record dispatch measurement_base40, final full SHAs, every numstat row and both totals; recount after update-branch. Expected width is about 200/400; headroom covers parent/configuration fixtures and one Bot fix round. The a07 rewrite's 446/709 grants no exemption; an overrun blocks.
Run uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_supply_chain_policy tests.unit.test_chain_glue tests.unit.test_regime_ci tests.unit.test_task_checkers -v with measured absolute uv/Python, item 9 isolation and a temporary absolute UV_CACHE_DIR; record the expanded invocation.
Run bash -n, shellcheck and shfmt --indent 4 --space-redirects --diff on all three changed shells; run ruff check --config ruff.toml and ruff format --check --config ruff.toml on changed Python. Run make validate-agent-assets and the existing review gate. Never run Bats locally.
Host resolution probe: /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv; repeat with python and paste actual outputs, never guess a uv/bin path. These discovery observations alone do not establish trusted-parent deployment.

## Execution and evidence

Worker Playbook step 4 applies: every command sandboxed; any denial sends AGMSG-PONG v1 task_id=dotfiles-T133-gh-binding-a01 status=blocked with exact command, exit status and boundary, then holds. Never escalate, probe Herdr sockets or retry through another surface.
Create tools/gh-binding-a01 from origin/main with git switch -c tools/gh-binding-a01 --no-track origin/main. Push HTTPS with git push https://github.com/mryfmo/dotfiles.git tools/gh-binding-a01, never -u or shared config changes; open one draft PR. Follow step 15's CI/Bot wait, at most one worker Bot fix round; surviving P0/P1 stops for the operator. Worker never merges.
Under .orchestration/dotfiles-T133-gh-binding-a01/ write task.md byte-identical to the complete anchored dispatch, report.md, validation.md with verbatim command stdout/stderr and real exit statuses, sandbox.md, learning.md, autoskill.md and result.txt; keep artifacts non-executable and secret-free.
Every evidence item names its producer/seat: worker (Codex seat), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat, sandboxed exec) for the observations below. report.md maps rows/selectors, scope, counts, red/green pairs and limitations; sandbox.md records denials, learning.md triage, autoskill.md actual use/not-used, cost n/a unless measured.
Write AGMSG-RESULT v1 before sending: task_id, status, pr, literal head=<full40>, authenticated_main=<full40>, merge_base=<full40>, source_cap=350, test_cap=700, source_changed/test_changed, every red/green SHA pair, task_copy=<repo-local task.md>, task_copy_sha256 and artifact paths. ready_for_review requires passing CI.
Keep plan/todo/learn updated and uncommitted, one active todo per owner. Use agent-side Crit data/evidence only; no browser or publication. Satisfy make require-crit-review and its receipt before RESULT. The orchestrator alone follows Playbook step 10's feedback, audit, acceptance, gate and integration order.

## Anchor

R1:110: the observed Checks below explicitly block anchoring; no canonical clone or trusted-parent deployment was measured in this read-only authoring context. They are not an approval or substituted canonical evidence.
Before C-80/anchor, the orchestrator expands the gh-binding-followup-a01 owner stub for every assigned residual and the three future consumers; confirms Item 0's amended inventory; obtains main40/design digest from a fresh private HTTPS bare clone of the fixed repository, gh-free and independent of the shared object store.
Record exact sanitized producer commands/outputs and item 2/9 parent/namespace protection evidence separately; paste their observed identifiers and the host pin/version lines into the five payload lines below. Change dispatch_status only after all observations exist, then review and anchor the entire resulting bytes; any later paste invalidates that anchor.
Installation is separate from code/CI: the orchestrator records the declared pinned install and protected config, then positive real consumer probes under the measured parent before enabling authenticated acceptance reads. a07/regime-ci future routes remain unclosed until their own adoption evidence exists.

## Checks

