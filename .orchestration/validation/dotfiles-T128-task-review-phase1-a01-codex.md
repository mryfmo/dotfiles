# Codex headless task-file review, round 1 (dotfiles-T128-task-review-phase1-a01, Codex half)

- run: `codex --profile review exec --sandbox read-only -C <main checkout> -c approval_policy=never -o <out> "<prompt>" < /dev/null`, finished 2026-10-12T11:42Z
- reviewed: gate-evidence `cba77a8d…`, playbook-rules `15ae4da2…`, aws-cli-macos `6000f026…` (sha256 of the task files at dispatch); design v18 `7f007ec4…`

### dotfiles-T128-gate-evidence-a01

- P1, high confidence — `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:8`: the receipt points to round 18, while design v18 identifies round 20 as the review of this hash (`dotfiles-T128-regime-v3-a01.md:224`) and plan 007 says the pointer was re-pointed after round 20. The listed round-20 receipts are also absent.
- P1, high confidence — `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:10`: `allowed_files` misses gate invocation touch points found by `rg "PR_FEEDBACK_EVIDENCE|AUDIT_DISPOSITIONS|require-crit-review"`—notably `Makefile:206-211` and SKILL step 10 at `home/dot_agents/skills/agmsg-orchestration/SKILL.md:170`. Requiring `ACCEPTANCE_EVIDENCE` in PR mode is incomplete unless the supported invocation passes and documents it.
- P2, high confidence — `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:45`: premise 3’s exact `grep -P` command fails under the repository’s macOS/BSD `grep`. Its claimed data does hold when rerun portably with `awk`.
- P3, high confidence — `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:16`: threat-table shapes pass: all residual payloads are sentences over 20 characters; there are no closed or out-of-scope rows. Every declared `allowed_files` entry and listed non-path control has a row.
- P3, high confidence — `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:54`: the design-tier invariant check passes: `implementing_tasks` maps this exact task id to `[INV-6]`.
- Premises rerun: premises 1 and 2 matched exactly; premise 3’s command failed, while a portable equivalent reproduced the three claimed ledger rows. No brew or network command applies.
Task-file verdict: dotfiles-T128-gate-evidence-a01: revise

### dotfiles-T128-playbook-rules-a01

- P1, high confidence — `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:8`: the receipt points to round 18, contradicting the design’s round-20 review statement and plan 007’s re-pointing claim; the round-20 receipts are absent.
- P2, high confidence — `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:30`: the threat table combines in-process effects, workflow inputs, interpreter/environment inputs, and new/renamed scripts into one row. That contradicts the row unit this same task introduces at line 63: one row per listed non-path control.
- P3, high confidence — `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:10`: the touch-point greps covered `PINNED_SECTIONS`, `fixtures/regime`, the invariant tokens, the SKILL sections, and AGENTS.md’s trust-boundary bullet. The four concrete source/test entries and fixture glob cover the discovered edits.
- P3, high confidence — `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md:56`: no `implementing_tasks` entry is required because this is explicitly review tier.
- Premises rerun: all three commands reproduced the claimed lines, including SKILL lines 69/71/72/162, AGENTS.md line 78, and the fixture pinning logic.
Task-file verdict: dotfiles-T128-playbook-rules-a01: revise

### dotfiles-T128-aws-cli-macos-a01

- P1, high confidence — `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:8`: the receipt points to round 18, contradicting the design’s round-20 statement and plan 007’s re-pointing claim; the round-20 receipts are absent.
- P1, high confidence — `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:64`: the task says `home/dot_agents/agent-config.yaml` remains untouched and omits `scripts/upgrade-tools.sh`, but plan 007 T715 says `assets.aws-cli` gains a macOS branch and `upgrade-tools.sh` runs `aws update`. The same plan paragraph simultaneously says `aws update` was dropped, so T715 is internally contradictory and the task does not resolve it authoritatively.
- P1, high confidence — `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:15`: plan 007 names `tests/install/macos/common/misc.bats`, while the task allows and specifies `tests/install/macos/common/brew.bats`. The latter sources `install/macos/common/brew.sh`, not `dependencies.sh`, so it is not an existing reader of `BREW_PACKAGES`; the existing reader is `tests/unit/test_aws_cli_acquisition.py:636`.
- P2, high confidence — `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:27`: two distinct `allowed_files` entries are combined into one threat row, and the new/renamed-script control is not separately represented, contrary to the one-row-per-entry/non-path-control rule.
- P3, high confidence — `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md:20`: the closed selector has the required `tests/<file>::<name>` form. All residual payloads exceed 20 characters; there are no out-of-scope rows. No design `implementing_tasks` entry is required because the task declares review tier.
- Premises rerun: the Homebrew dependency command reproduced `awscli` as the installed user of `python@3.14` and the stated dependency list; both local grep commands matched. The network/curl premise was not rerun.
Task-file verdict: dotfiles-T128-aws-cli-macos-a01: revise