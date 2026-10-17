---
task_id: dotfiles-T129-assets-omp-hcom-a01
round: 2
amendment: 4
bot_fix_round: 1
status: revised-source-approved-local-validated
---

make update gains omp18.11.3 and hcom0.7.30 as https-download assets whose versions, exact artifact URLs and SHA256 values are recorded in agent-config.yaml. Each function downloads a tarball/platform wheel, verifies its SHA256 before npm/uv receives that local file, checks the installed managed binary's version and records success. Matching managed installs skip; missing package managers and unsupported hcom platforms skip. Function-local subshell EXIT traps remove temporary artifacts on success and error. check-tools reports the owned binaries beside their pins and records genuine absence warnings without required failures.

The operator runs the real make update after merge. No real package, binary or dependency was installed by the worker; fake installers write scripts only. No actual artifact/registry request was made for the current task amendments. Registry facts/hashes come from the dispatched task; comparisons verify every URL/hash and omp integrity against it. Top-level artifacts are pinned; actual package-manager compatibility, transitive dependency behavior, host PATH integration and future uv upgrades are untested.

The generator rejects files.<platform> URL render values as non-plain pins. The explicit task fallback therefore keeps the four URLs in assets.hcom.files and mirrors them beside existing updater URL constants; version/hash constants are generated. Other manifest/model/permission data, mise config, validator and its tests, original installer helpers and existing Bats cases remain unchanged. No new production script or dependency.

Tests are the two required installer methods plus test_updates_use_managed_binaries_when_path_is_shadowed. The first two were RED before implementation. The third was RED in all4 subcases against initial head6b9c5d970f22d37b95516aebe9700615c7d4383b and GREEN after four explicit managed-path pre/post version probes. All11 named installer/doctor/updater methods pass in18.969s. The3 installer methods cover46 isolated invocations, including all4 hcom platforms, matching/stale PATH shadows with absent managed targets, verified-file argv/bytes, idempotence, hash/version refusal with no success receipt, missing managers, unsupported platforms and cleanup. Two new Bats cases remain CI-only.

First independent review found two P2 doctor regressions, addressed by lazy data-only pin reads and the true warning-count expectation1to3. Amendments3/4 authorize that test update and three main-caller fixture stubs; no previous assertion was removed. Initial source approval, ten-method independent run21.927s and validator success are preserved as historical evidence. Broader runtime-health Ruff reports17 diagnostics identical to baseline by code/message/source line; no unrelated lint change. Current revised source passes ShellCheck-x, shfmt, new-module Ruff and both-module formatting. Its independent security re-review explicitly approves the revised seven source hashes: three installer methods pass in6.459s, and all4 shadow failures are independently reproduced against the old updater. The refreshed full clean-index validator exits0 with all7 source hashes matching the approved candidate; earlier approval is not reused for changed source hashes.

PR388 first Bot review reported P2 thread4302479678: a foreign PATH binary could falsely satisfy the installed-version check or reject a good managed install. The orchestrator sent status=revise with previous_head/check (revise.yaml). This authorized first fix replaces only four bare version lookups with ~/.local/bin/omp and ~/.local/bin/hcom. No thread reply/resolution by the worker. RESULT will identify the observed fixing commit; final-head CI/Bot, task audit, feedback dispositions, acceptance/gate and merge remain separate requirements.

Baseline35ab0e95a7fe27c501db3478d4f37e69a514d532; branch feat/pinned-omp-hcom. Production162/200 changed lines, tests226/1000 additions. Task copy SHA256c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85. Seven source/test paths and nine canonical records (including revise.yaml) are committed before RESULT; timestamp worklogs/raw observers/superseded evidence remain untracked. Publishing head/CI/Bot are recorded after push in raw publishing evidence referenced by RESULT to avoid self-referencing commit claims.

The full validator uses a clean staged-index export with source hashes bound to the candidate because unrelated historical untracked logs fail the worker-root secret scan. No checker, ignore rule or old raw log was changed. Verbatim earlier traces retain trailing whitespace; source/test whitespace checking is separate. Crit has no review file/daemon/session, so AGENTS.md's independent read-only review fallback is used. No browser, Plan Mode, publish, local Bats, sandbox/profile/permission change, release retry, login/provider/bus/relay setup, AutoSkill or project-memory promotion.

Source SHA256:

- home/dot_agents/agent-config.yaml: e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310
- scripts/check-tools.sh: 45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224
- scripts/lib/installer-pins.sh: a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091
- scripts/update-agent-assets.sh: 80066713c6dc4e3c2d30ee0405e8a9477f38942a2d0401ed12a26d7f9a4aaea4
- tests/install/common/check_tools.bats: 9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed
- tests/unit/test_runtime_health.py: 0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6
- tests/unit/test_update_agent_assets.py: 75f275085b4eb8ac9069c3b4de4329b9abff8363ff86e9e21076785e920ec92b

Graph940a3a2b intentionally stale; summaries queried then targeted rg, no graph update. No durable project decision created. effects=none. cost: n/a
