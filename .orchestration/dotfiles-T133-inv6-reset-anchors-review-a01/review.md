# INV-6 reset anchors — twelve-lineage independent design review

Task: dotfiles-T133-inv6-reset-anchors-review-a01
Dispatched task SHA256: 38a321efb523666bcae78814b05f25a4efa2f31a9036e832daea2b0c234992fb

Scope: named main-checkout file bytes, reset_of, predecessor acceptance findings and relative permission/trust boundaries. All twelve digests were independently computed with /usr/bin/shasum -a256; read-checks.json preserves exact argv, output, exits and acceptance hashes. scope-comparison.json preserves old/new allowlists. All reviewed task/acceptance and compared predecessor-task hashes were rechecked unchanged after review. No source, Git state, PR, network, deployment or implementation test was changed/run.

Crit status exited0 with no review file, daemon or session. Per AGENTS, three independent fresh security-profile contexts reviewed rounds1–4,5–8,9–12. Parent read their findings, checked cited clauses and C3 semantics, and reconciled cross-batch deletion-ownership treatment. The round12 initial approval was superseded by the independent addendum after that check. dotfiles-T133-inv6-reset-anchors-review-a01-worker-crit.json and dotfiles-T133-inv6-reset-anchors-review-a01-worker-review-receipt.md record this process. Resolved evidence records mean the review disposition was completed; reject findings remain unfixed in the pinned design bytes.

Outcome: accept rounds1,3,5,7,9,11; reject rounds2,4,6,8,10,12. Hash/reset metadata are OK for all twelve. This is a design-anchor review, not implementation, dispatch, security-audit, merge or operator approval. A rejected hash cannot be silently accepted by referring to these results.

Boundary interpretation: distinguish metadata capacity/test/helper additions from execution or worker-write authority. A newly delegated out-of-allowlist deletion fails the no-widening check; a transition already in the predecessor is described as inherited, not newly approved. C3 requires threat-table references to task copies and grants no write permission. Narrow orchestrator-directed bookkeeping does not establish OS permission growth, but it changes which actor may write the task paths.

## Results

| Round | Old lineage | Redesign | Verdict |
| --- | --- | --- | --- |
| 1 | dotfiles-T133-python-pin-a01 | dotfiles-T133-python-pin-a02 | accept |
| 2 | dotfiles-T133-regime-ci-fixture-grammar-a01 | dotfiles-T133-regime-ci-fixture-grammar-a02 | reject |
| 3 | dotfiles-T133-result-precheck-a01 | dotfiles-T133-result-precheck-a02 | accept |
| 4 | dotfiles-T133-result-precheck-a02 | dotfiles-T133-result-precheck-a03 | reject |
| 5 | dotfiles-T133-result-precheck-a03 | dotfiles-T133-result-precheck-a04 | accept |
| 6 | dotfiles-T133-task-generator-plan-check-a02 | dotfiles-T133-task-generator-plan-check-a03 | reject |
| 7 | dotfiles-T133-task-generator-plan-check-a03 | dotfiles-T133-task-generator-plan-check-a04 | accept |
| 8 | dotfiles-T133-task-generator-plan-check-a05-checker | dotfiles-T133-task-generator-plan-check-a06-checker | reject |
| 9 | dotfiles-T133-permission-guard-gate-a01 | dotfiles-T133-permission-guard-gate-a02 | accept |
| 10 | dotfiles-T133-permission-guard-gate-a03 | dotfiles-T133-permission-guard-gate-a04 | reject |
| 11 | dotfiles-T133-ci-efficiency-a01 | dotfiles-T133-ci-efficiency-a02 | accept |
| 12 | dotfiles-T133-ci-efficiency-followup-a02 | dotfiles-T133-ci-efficiency-followup-a04 | reject |

## Round 1 — dotfiles-T133-python-pin-a01 → dotfiles-T133-python-pin-a02

- Hash: OK; 95c7e7c7bf0007e2da931017867883cd60ad47b9b7f40226595a03cdd37d92c6 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-python-pin-a02.md:4; exactly [dotfiles-T133-python-pin-a01].
- Predecessor: .orchestration/acceptance/dotfiles-T133-python-pin-a01.md; SHA256 2d3e2f414db6d8eb8b51fe1c31e9ad99d0ae0966945baaa29be5c463a702bfb9. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_1_4.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Prior S2 and omitted ledger/re-plans: new:4,94–95,146 explicitly reset and preserve historical records; predecessor closing synchronization is recorded in that acceptance record.
- OK — Failed probe and interpreter mismatch: new:41–89,117–121,154–156 bind successful observations and execute the same fixed interpreter, without claiming worker/RESULT operations were probed.
- OK — Environment/shims/discovery/imported-repository and chezmoi concerns: new:22,105–126,163 specify clean environments, bound Python/gh and direct test-file scope; other tests remain CI work.
- OK — Mutable local refs/Git configuration/compare truncation: new:127–136,160–162,168 use isolated fixed-host/repository API evidence, full SHAs and completeness refusal.
- OK — Version grammar and missing design threat rows: new:27–37,148 retain all eleven design items and ASCII fullmatch/negative cases.
- OK — Wrong gh path, invalid Git command, executable-block prose and circular prerequisite: new:123–136,155,161 use observed binary/API calls and place compare work at RESULT.
- OK — Line cap and repeated secret-pattern fixture text: new:128–136,163,179 use the amended variable form and190-line cap; actual design183lines.

Permission/trust boundary check: OK: same three non-artifact paths; new:146–150 narrows work to evidence and preserves predecessors. Sandbox-only/no-bypass, operator deployment and orchestrator integration remain at167–174. No new execution authority.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 2 — dotfiles-T133-regime-ci-fixture-grammar-a01 → dotfiles-T133-regime-ci-fixture-grammar-a02

- Hash: OK; fd9ff2123d96bebdabfea725bcc7c8412b3f1275bbaac2858da143d9a0ff1303 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md:6; exactly [dotfiles-T133-regime-ci-fixture-grammar-a01].
- Predecessor: .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md; SHA256 3528e18d3374d4cf5aa886c13724e86a96aac49a6bfdaef46c1eb6590f41d145. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_1_4.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Wrong amendment counts/S2 continuation: new:6,47,74 explicitly reset and record two amendments/two questions.
- OK — Unstated excluded send: new:63,67 demand per-command inside/excluded reporting, but name an unsupported outside-sandbox send.sh exception (R02-F1).
- OK — push -u/shared configuration write: new:65 removes -u and names the destination ref.
- OK — Unmeasured Check command, cap/fixture attribution and stale task copy: new:51,53,57,59,63,69 retain the measured uv/TMPDIR/proxy direct-run form, exact ROWS removal, cap12 and dispatched-copy SHA.
- OK — CI-watch propagation/JSON-ledger synchronization issues remain orchestration-owned; new:53,59 prevents implementation expansion.

Permission/trust boundary check: FAIL in text only: production scope is unchanged and implementation/evidence are otherwise frozen; a documented agmsg-dispatch exclusion is not evidence that bare send.sh is approved outside the worker sandbox. No actual deployed bypass is claimed.

- R02-F1 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md:67: The task names send.sh/Stop-hook delivery as permitted outside the sandbox, while predecessor sandbox.md:31, historical cd47e1b manifest and the installed Skill step11 authorize agmsg-dispatch. Narrow the text to the documented delivery route; acknowledgement of that existing route would not itself widen authority. Supporting references: Old task:59; old acceptance:36; home/dot_agents/agent-config.yaml:285–290; agmsg-orchestration Skill Worker Playbook step11.

Verdict: reject

## Round 3 — dotfiles-T133-result-precheck-a01 → dotfiles-T133-result-precheck-a02

- Hash: OK; fda18e21e738bb222a50ebd29be302fa009fd1a2822b660311abe81aa1397e61 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-result-precheck-a02.md:14; exactly [dotfiles-T133-result-precheck-a01].
- Predecessor: .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md; SHA256 e97ec7aabb5d5a786dedc80564612b272ab7285effa85ed7ddbff0ecc7236567. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_1_4.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — S2: new:69–73 explicitly reset and preserve prior counters/evidence.
- OK — Binary-marked/push-range skipped content: new:97,109,111–113 require every changed blob in every pushed commit, including added-then-removed, NUL/binary and clean controls.
- OK — Failed commands/ok:false: new:103,115–123 require nonzero/error propagation and strict refused invalid evidence.
- OK — Malformed/missing/duplicate checks and requested selectors: new:119–123 require exact complete names/booleans and negative fixtures.
- OK — Index/working-tree divergence and CI formatting scope: new:85,95,109,131–133 retain exported index content/configuration and exact CI scope.
- OK — Sandbox full-suite failures and invalid historical red: new:89,133–135 require unchanged-baseline comparison, current test source against old production and executed assertion failure, never import/missing-test failure.

Permission/trust boundary check: OK: same five code/test paths, artifacts change identity only. Old/new cap increases do not grant privileges. New:71,127 leave predecessor removal with orchestrator and worker edits inside allowed_files; live hook config/workflows/host/schema changes stay excluded. Warning default is inherited.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 4 — dotfiles-T133-result-precheck-a02 → dotfiles-T133-result-precheck-a03

- Hash: OK; d8048ef508676f65c5eaee82cc69a9f83f04b4418ed3e61bb9e4803d5c0a32ba equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-result-precheck-a03.md:14; exactly [dotfiles-T133-result-precheck-a02].
- Predecessor: .orchestration/acceptance/dotfiles-T133-result-precheck-a02.md; SHA256 ccea41ea17d82e115e228ff61fc30c905bf90a966b422c7fb44b8457948670ef. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_1_4.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — S1 repeated secret-scan bypass: new:69,75,91,107,129,133–135 replace concatenation with unchanged per-blob input, preserving token boundary/JSON/UTF-16 decoding and old regressions.
- OK — Undecodable input and mistaken red proof: new:101,109,129,137,159,179 require fail-closed decode and one exact executed assertion-failing test without import/error substitution.
- OK — Stale RESULT before revise: new:111,117,139–141 require correct ordering and subsequent requested proof.
- OK — Home-path normalization counted as secrets: new:93,143–145 separates secret detection and limits home-path classification to original .orchestration paths.
- OK — Earlier range/index/failure/record controls and advisory ownership: new:105–109,125–129,167 retain controls and absorb the two named P2.

Permission/trust boundary check: FAIL: old a02:71,127 leaves predecessor removal with orchestrator; new a03 delegates two exact task-copy deletions to worker outside its declared allowlist. Bounded artifact bookkeeping only; no arbitrary cleanup, host or production privilege expansion is asserted.

- R04-F1 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-result-precheck-a03.md:71: Worker must delete the a02 task.md and a01 task.md if present, absent from frontmatter allowed_files:6–12; threat row:28–29 and completion:165 repeat the delegation. Keep actual deletions orchestrator-side as predecessor specifies. C3 threat-row coverage does not grant write authority. Supporting references: Old task:71,127; Skill Worker Playbook step3 and Pitfalls262; main checker:8,64–67; design-quality:61.

Verdict: reject

## Round 5 — dotfiles-T133-result-precheck-a03 → dotfiles-T133-result-precheck-a04

- Hash: OK; e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-result-precheck-a04.md:15; exactly [dotfiles-T133-result-precheck-a03].
- Predecessor: .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md; SHA256 7552e91466414e29979f1b2f00d83a3841ceaa2b94da52371e99804572a430e7. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_5_8.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Masker failure/raw credential output and symlinked evidence destinations: new:164–170 suppress both streams, remove raw/partial captures, lstat every component and use safe atomic replacement with sentinel regressions.
- OK — Discarded sender/recipient identity and inherited HOME: new:172–178 bind authoritative identities and use temporary HOME before subprocesses, preserving honest historical fixture reds.
- OK — Blob traversal/truncation and early-exit raw logs: new:180–186 validate before redirection and install cleanup before captures, retaining failure status.
- OK — Code/evidence/integration head confusion: new:112–114,188–192 bind trees/ancestry/evidence-only changes and authenticated update-branch provenance plus final-head checks.
- OK — Dispatch trusted premise digest/warnings: new:194–198 forward existing TASK authority and warnings, refusing mismatches without deriving digest from branch.
- OK — Earlier baseline/selector/index/push-range/failure/record concerns: new:78,96–120,128,138–144,216,226,230–232 preserve controls and ownership/evidence provenance.

Permission/trust boundary check: OK relative to a03: same four production/hook paths; added test_orchestrator_tools.py is restricted to existing dispatch argv assertions/stub checker at240. The inherited worker predecessor-copy transition narrows from two copies to one at74; no new actor category is introduced here. Live hooks/workflows/policy/merge/sandbox remain excluded; warning default inherited at130,253.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 6 — dotfiles-T133-task-generator-plan-check-a02 → dotfiles-T133-task-generator-plan-check-a03

- Hash: OK; 1dd4538ac9edf5f35d55ddb585e7911d4e6e7fe9fcfd5692524101b060fb7e3c equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:18; exactly [dotfiles-T133-task-generator-plan-check-a02].
- Predecessor: .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md; SHA256 d4727a8aa3184fd44b4134e98faf9f1fc7ccd10d89050e810fbcb8296fc91e6d. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_5_8.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Generator executes plan commands, checkout bin/bash despite digest and output symlink: new:147–177,181–203 prohibit plan/shell/source execution, use fixed read-only probes and require confined O_EXCL output without symlink following.
- OK — Escaping glob enumeration and C11 class-qualified selector: new:205–223 requires grammar/confinement before inspection and meaningful class-selector historical red.
- OK — Hostile uv/venv/config/cache, Git filters/includes/submodules/lazy fetch/core.worktree: new:149–159,225–239 retain isolated offline bindings, effective-config checks, explicit worktree binding/refusal and marker regressions.
- OK — Earlier twelve audit P2/parser-gap lineage and detection residual: new:161,263–267 retain explicit ownership and accurate delayed records-PR detection.
- OK — Deployment prerequisite is inconsistent within this same Codex task (R06-F1).

Permission/trust boundary check: No demonstrated runtime widening: same nine non-artifact paths and security:true; execution/path contracts tighten. FAIL is an unresolved dispatch contract, not a claim D-024-25 grants extra sandbox privilege.

- R06-F1 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:295: New:133 invokes D-024-25 to dispatch this Codex task before P1-15 but the same paragraph requires that task's merge/deployment;295 says this task is not dispatched before deployment and301 demands pre-dispatch verification. Explicitly reconcile these opposite prerequisites; an implicit override cannot certify one consistent contract. Supporting references: New:133,295,301; predecessor acceptance:297–317.

Verdict: reject

## Round 7 — dotfiles-T133-task-generator-plan-check-a03 → dotfiles-T133-task-generator-plan-check-a04

- Hash: OK; b325fe161c1e2cab2183cc0f8110ad185153b6cde15dbeaf9b894d5efe9e3e0c equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a04.md:18; exactly [dotfiles-T133-task-generator-plan-check-a03].
- Predecessor: .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a03.md; SHA256 195bb6431f701b7c0a388870e16fb4cefdafe9d780efb5cc87e773f376a2f19f. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_5_8.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Host install-root assumptions/StopIteration and missing resolver: new:177–199,241–247 replace discovery with validated parent bindings, named refusals and real caller tests; no new resolver dependency/install-tree fallback.
- OK — Regime fixture missing absolute cache/offline provisioning: new:199,255–257 require independent fixture caches/tool bindings; provisioning stays separately recorded and final regressions cannot pass via skip at289.
- OK — Python3.12 glob.translate absence: new:231–235 specifies compatible component matching, grammar cases and behavioral floor-runtime red.
- OK — Five R4 lint hits: new:259–261 require meaningful normalization and changed-file regression with no suppression/baseline workaround.
- OK — Premature cap/runner claims and denied environment operations: new:92–115,201–209,267–271,303–307,343 record actual observations, contexts, final arithmetic and no-bypass/block reporting.

Permission/trust boundary check: OK: same nine non-artifact paths. Parent toolcache bindings retain realpath/executable/worker-root/clean environment checks; canonical reads use fixed repository API/pinned SHA at167–171. Workflow prefixes/deployment external at205–209,275;209 explicitly resolves the Codex/P1-15 exception.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 8 — dotfiles-T133-task-generator-plan-check-a05-checker → dotfiles-T133-task-generator-plan-check-a06-checker

- Hash: OK; b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:15; exactly [dotfiles-T133-task-generator-plan-check-a05-checker].
- Predecessor: .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md; SHA256 ffeb54abd51b402a9687e625bc2ba568b5a562ea1dd93b282b1da3b2b6bcf047. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_5_8.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — cedc7f5 original Unicode confinement/internal directory aliases/multi-item C16 rows: new:129–143,176–178,184 preserve original targets, reject directory aliases and count each occurrence with exact regressions.
- OK — 06ffefb normalized pruning/resolved literal C16 and repeated input-validation: new:129–143,179–188 require one pipeline across consumers plus invariant/collision/one-file controls.
- OK — Source cap exceeded by held unverified draft: new:95–97,211–216 supplies measured450/720 caps and honest continuation/diff arithmetic.
- OK — Recurring glob-filter and token argv defects: new:123,135–136,161,165 prohibit argv tokens and require post-cleanup magic rejection/prefix confinement.
- OK — C6 ambiguity/canonical prerequisite/exemption: new:103–107,125–127,140–141 retain exact field name, fixed-host API bytes and resolved-target classification.
- OK — Parent/cache risks and old withdrawn generator/parser findings: new:55,62,93–99,119 preserve external ownership/no-closure boundaries.
- OK — R4 lint/evidence/runtime/network concerns: new:97,192–207,224–234 retain validated tools, committed evidence and owner transport without escape.
- OK — The text-defect checker/long-Checks prevention or explicit owner disposition is missing (R08-F1).

Permission/trust boundary check: No execution/permission widening: same checker/two tests; predecessor directory remains unchanged at16–17,29,145; cap growth is capacity only. Parent/cache risks remain externally owned. Reject is omitted predecessor obligation rather than a claim current source is unsafe.

- R08-F1 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:218: The new260-line convention does not retain the predecessor text-defect re-plan's checker-side authored-cap counting plus long-Checks fixture, or an explicit a06 owner row if the cap prevents implementation. Preserve one of those outcomes. This concerns the allowed checker or ownership disposition, not excluded generator/templates. Supporting references: Predecessor acceptance:243–247,273; new task:99,218.

Verdict: reject

## Round 9 — dotfiles-T133-permission-guard-gate-a01 → dotfiles-T133-permission-guard-gate-a02

- Hash: OK; 8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md:25; exactly [dotfiles-T133-permission-guard-gate-a01].
- Predecessor: .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a01.md; SHA256 fe1f3b458baa2b6e7bca527e35b47c6ad4c165c421fbacd106ad8eca5b8463c0. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_9_12.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Three question-PONG authority ambiguities: new:140–152 bind deployed sandbox-unwritable Workspace anchor/realpaths/primary repo, implicit record identity and operation-specific merge/ready/draft/update rules without schema extension.
- OK — Stale dependency and misleading heredoc trigger: new:108,186 consistently name#412;136,168–172 require nonexecuting command-position recognition and both observed heredoc/compound/actual-command regressions.
- OK — Stopped history and prior reproduction/closure confusion: new:106–112,124,166,188 preserve records and distinguish reproduction from final-head proof.

Permission/trust boundary check: OK: unchanged production scope and intended three ask-rule replacements. New140–152 narrows authority;172 adds no new allow form. Workflows/ruleset writes/policies/deployment/permgate excluded at176. Actual predecessor removal remains orchestrator-owned at110.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 10 — dotfiles-T133-permission-guard-gate-a03 → dotfiles-T133-permission-guard-gate-a04

- Hash: OK; 17a1795fbbafe55339dfa28b8c5a7d779408e615c1679262a591b9030ebef0cb equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md:25; exactly [dotfiles-T133-permission-guard-gate-a03].
- Predecessor: .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a03.md; SHA256 154fd1e2b74125d345810b5edc9b2f20f8044844cef61979ab911725426ec684. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_9_12.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Legacy records/missing comparison status/body-file disclosure/missing progress ledger: new:146–150,168–176,182,202 retain bounded record selection, refusal, regular contained bodies and optional explicit progress writes.
- OK — Mise shims before validation: new:224–230 require trusted-root absolute non-shim binaries, private PATH, excluded caller configuration and sentinel regressions.
- OK — Case-sensitive Git metadata exclusion: new:232–236 require resolved filesystem identity and deterministic case-insensitive negative cases.
- OK — PR supplies its own approval ledger: new:238–244 anchors the default and rejects PR-tree overrides, but external provenance remains unbound (R10-F1).
- OK — Cap779/780 leaves no space for three regressions: new:106,206–212,266 increases room but disagrees on900/950 (R10-F2).
- OK — Old fixture/order/alias/reporting repairs and history: new:134,202,270,276–288 preserve controls and honest historical failures.
- OK — New worker predecessor-copy deletion also widens declared edit authority (R10-F3).

Permission/trust boundary check: Production grammar/path scope otherwise unchanged and tool/body/default-ledger checks tighten. FAIL: external ledger lacks trusted provenance, and predecessor orchestrator-side deletion becomes worker-side outside declared allowlist. No deployed-policy change is claimed.

- R10-F1 — [P1] high confidence — .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md:240: An explicit --decisions path may lie anywhere outside the PR worktree after checkout/repository checks;244 expects an external fixture ledger to pass. Those checks do not authenticate that file. A matching forged row in worker-writable /tmp can meet stated predicates. Remove the production override or bind it to independently trusted provenance and reject external worker-writable ledgers. Supporting references: New:138,142,238–244; predecessor acceptance:52,55 and security report:7.
- R10-F2 — [P3] high confidence — .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md:106: The reset gives a900 test cap here but950 at266 (171 lines remaining). Resolve the operative budget explicitly because cap exhaustion caused this reset. This is secondary; meeting the stricter900 would satisfy both. Supporting references: New:106,266; predecessor acceptance:59–60.
- R10-F3 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md:110: Worker must delete a03/task.md absent from allowed_files:6–23, where predecessor:112,214 assigns removal to orchestrator. New:62,276 repeats the delegation. Keep actual deletion orchestrator-side; ownership wording does not preserve the hard worker edit boundary. Supporting references: Skill Worker Playbook step3/Pitfalls262; main checker C3:8,64–67; design-quality:61.

Verdict: reject

## Round 11 — dotfiles-T133-ci-efficiency-a01 → dotfiles-T133-ci-efficiency-a02

- Hash: OK; 684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md:18; exactly [dotfiles-T133-ci-efficiency-a01].
- Predecessor: .orchestration/acceptance/dotfiles-T133-ci-efficiency-a01.md; SHA256 547ed7dfba40909f44135ae5b9da8167daf78a7df6af1c3eb714c6ba51187b8e. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_9_12.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Continued past S2: new:87–89 resets through another context and preserves history;153 stops again at amendment/revise limit.
- OK — Superseded PR heads and failure-conclusion eligibility: new:111,113 check before reservation/rerun and classify failed/timed-out/cancelled signatures with no-write negative cases.
- OK — Unexecuted production flake registry and broad Markdown skip: new:115 loads actual registry/engine and mutation negatives;117 retains macOS for home/install and narrows root Markdown.
- OK — Checkout-wide lock and rerun races: new:119 requires atomic per-run persistent reservations, same/different-run concurrency and failure/interruption retention.
- OK — Unsupported CI13/13 and earlier path gates: new:103,121 retain chezmoi/vendor coverage and calculate separate status/check/required counts from feedback JSON;109 retains read-only security expectation.

Permission/trust boundary check: OK: same amended allowlist/artifact identity change only;101 retains private bootstrap/isolated HOME/pinned actions/read-only permissions,103–109 retain required-context reporting. Existing rerun write is tighter, not expanded. Predecessor removal remains orchestrator-owned at41,89.

- Approval: the reset-triggering findings have substantive requirements and evidence obligations; no new permission/trust authority was identified in this relative reset review.

Verdict: accept

## Round 12 — dotfiles-T133-ci-efficiency-followup-a02 → dotfiles-T133-ci-efficiency-followup-a04

- Hash: OK; 3eba74bfa6104d3c89aeb0e57e823b87da672863d844fe04855031d918d5c975 equals the requested SHA256.
- reset_of: OK at .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:14; exactly [dotfiles-T133-ci-efficiency-followup-a02].
- Predecessor: .orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a02.md; SHA256 d77d59b73a6843acc0fb3ad58cdc8cdfbb8370e5601aa5c1cc18710ae0cff808. Independent reviewer read the full record and full redesign.
- Independent context: /root/reset_anchor_rounds_9_12.

Predecessor findings → redesign requirements (new means the redesign named above):

- OK — Attacker .python-version/.venv/absolute PATH and missing mise fallback: new:109–137,147,157 replaces discovery/fallback with fixed-declaration/passwd-home resolution, isolated uv/cache and hostile activated-PATH regressions.
- OK — Pre-pin EXIT rm and R4 rebase lint: new:22–23,127,141,159 retains absolute cleanup and normalizes new comparisons without broad baseline escape.
- OK — Two amendments/exhausted rounds and owner self-reference: new:77–81,79,212,214–216 reset class-level mechanism and retain explicit separate owner/stopped counters.
- OK — Draft/new PR confusion: new:75,208,218–222 continues existing PR/final-head checks; Git-quoted-path and timezone observations remain assigned to existing owners rather than claimed repaired.
- OK — Exact declaration/checker/deployed protection/caller migration/CI prerequisites stay explicit holds at87–93,174–176, but prerequisite identity needs reconciliation (R12-F2).
- OK — C3 is incorrectly claimed as authority for worker deletion outside allowlist (R12-F1).

Permission/trust boundary check: Resolver/test additions are bounded implementation scope, not permission to write protected declarations/installations/workflows/caches. New:220 requires individual in-sandbox commands/no bypass. FAIL is the newly delegated out-of-allowlist deletion, not OS sandbox expansion. Dispatch remains held independently.

- R12-F1 — [P2] high confidence — .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:208: The worker is directed to delete predecessor a02/task.md absent from allowed_files:6–12, and the text calls C3 authority for it. C3 only checks threat-table references to task copies; it grants no edit/deletion authorization. Predecessor granted no such worker deletion. Keep transition orchestrator-owned. Supporting references: New:31,204,208; main checker:8,64–67; Skill Worker Playbook step3/Pitfalls262; design-quality:61.
- R12-F2 — [P3] high confidence — .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:91: This dispatch prerequisite still names worker-write-boundary-a01 while frontmatter after names worker-write-boundary-a02. Reconcile before dispatch along with the explicitly held pin/protection/caller/CI prerequisites. This is secondary to R12-F1 and no dispatch-readiness claim is made. Supporting references: New:13,87–93.

Dispatch remains held: exact declaration/grammar, required checker revision, deployed protection, caller clean-prefix migration, CI provisioning and measurements must be established by their owners. Any changed design bytes need a new digest/review; this review authorizes no worker prerequisite repair.

Verdict: reject

## Evidence and limits

- read-checks.json: task/acceptance hashes and all24 independently executed shasum command outputs; all twelve expected hashes/reset_of values match.
- scope-comparison.json: predecessor/new allowlists, added test/helper scope and after fields.
- crit-status.json: unavailable Crit data and no running session.
- dotfiles-T133-inv6-reset-anchors-review-a01-worker-crit.json / dotfiles-T133-inv6-reset-anchors-review-a01-worker-review-receipt.md: independent agent process evidence and parent dispositions.
- review-data.json: machine-readable round/hash/verdict/finding map and supporting source hashes.
- Reported design requirements and historical test/CI results were not executed or independently revalidated in this text-only task.
- No source edit, commit, PR, push, network access, local Bats, live-host settings inspection or deployment verification. No task dispatch is authorized by this report.
- The unreviewed live runtime and inherited host/cache/credential risks remain outside scope.

cost: n/a
