# Security audit: dotfiles at 491085954cbb16c1aac1b7bfd7ab2f477bfa1d36 (U276 head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U276 commit, `4525d339..49108595`: 4 paths, +393 (`scripts/deploy-kit.sh`, the Makefile target, the README paragraph, the tests). The dirty-source guard, hcom-seat's write roots and the orchestrator policy were read as context. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `49108595` on `feat/make-deploy-kit`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- **The brief's GOAL and hunt focus describe U251** (`scripts/orchestrator/dsh-srt`). That change is not in this head; `dsh-srt` is absent here. The head the brief and the TASK name, `49108595` on `feat/make-deploy-kit`, is U276, so this run sweeps U276.
- The output directory is **run-9**. The brief's run-8 already holds this seat's U271 sweep and is left untouched.
- The brief's prior "run-83" does not exist; the previous run is run-8.
- The brief's base and CONTEXT diff line were not used.

**Prior run.**

- run-8's 51 units are carried with the same IDs as `out_of_scope`.
- Its two dsh-srt candidates (`dsh-srt:self-check-helpers-from-caller-path`, `dsh-srt:dsh-home-write-root-run-by-updater`) cover source that is not in this head. They are not re-checked here and stay open for that branch.
- There is no prior record.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran.
- The one candidate **stays unvalidated in the coverage ledger and is not a finding**; findings.json holds no record.
- No critic ran, so this report makes **no clean-coverage claim**.

### Unvalidated candidate (ledger only; not a finding, no severity)

| Fingerprint | Ledger unit (surface; boundary; class) | Status |
| --- | --- | --- |
| `deploy-kit:named-apply-skips-dirty-source-guard` | `scripts/deploy-kit.sh#apply`; `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`; Chained vulnerabilities and trust boundaries | New, unvalidated |

**Claim.** The narrow deploy installs the levers and their pins from a chezmoi source that nothing checks against the merged main. This drops the guarantee `make update` keeps: "changes reach the host only through a merged pull request".

**Trace.**

- `make update` runs a whole `chezmoi apply` (Makefile:124). The source's `run_before_00-refuse-dirty-source` refuses that apply when `home/`, `install/` or `scripts/` differ from origin/main: uncommitted, untracked, unmerged, not yet pulled, or a pushed but unmerged branch (run_before_00-refuse-dirty-source.sh.tmpl:4-14).
- `deploy-kit` applies the pending kit targets by name (deploy-kit.sh:44, 135-145). By its own statement, a named apply does not run the source's `run_` scripts (16-18). It pulls nothing (Makefile:166, README.md:203), and it makes no comparison of its own.
- Its targets include `~/.local/bin/common/pr-merge.sh`, the merge gate the orchestrator policy allows (orchestrator.yml:36-37), and `~/.agents/agent-config.yaml`, which holds the pin that lever's self-check reads. A lever and its pin from the same unmerged source therefore deploy together, and the self-check passes.
- The contained orchestrator seat can write that source: its write roots begin with "the checkout for the orchestrator" (hcom-seat:1367, 1373).
- So an edit made from inside the seat reaches the installed merge gate through a `deploy-kit` run outside srt, where `make update` would have refused the dirty source.
- The tests have no case for a dirty or unmerged source (test_deploy_kit.py:44-137).

**Blockers.**

- That chezmoi's named apply runs no `run_before_` script. This is the script's statement, not measured here.
- Where the coordinator runs `deploy-kit`.
- Whether the main checkout can hold an unmerged lever change at that moment.

**Bounded local check.**

- In a scratch HOME and a scratch clone with an origin/main ref, change `home/dot_local/bin/common/executable_pr-merge.sh` and its pin in `home/dot_agents/agent-config.yaml` without committing.
- Run `chezmoi apply` (expect the guard's refusal), then `scripts/deploy-kit.sh` with chezmoi pointed at that source.
- An installed `pr-merge.sh` equal to the uncommitted edit confirms the claim.

**Owner check.** Where `make deploy-kit` runs, and that the checkout holds only merged main when it does.

**Smallest fix.** Run the same comparison before the named apply: source the guard's logic, or call the guard script by path, and refuse on a dirty source. Alternatively, apply from a clean export of origin/main instead of the working tree.

## 2. Security posture

`deploy-kit` is careful about what it applies:

- three roots, matched by prefix
- every chezmoi read status-checked
- a refusal on two-sided drift
- targets passed as quoted words, with stdin closed
- a verify after the apply
- the same asset updater as `make update`

The one gap is where its input comes from. It deploys the working tree's levers and pins without the merged-source check that `make update`'s apply enforces.

## 3. Confirmed findings

None. No candidate could be independently validated; see section 1.

## 4. Confirmed finding details

None.

## 5. Needs validation

No `needs_validation` record. The open lead is the unvalidated candidate in section 1, and it is not a record.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes:

- The README calls this "the narrow deploy an agent runs after a pull request merges" (README.md:199-200), but nothing checks that the source is that merge. That gap is the candidate.
- `make update` prefetches and verifies the chezmoi externals before applying (Makefile:123); `deploy-kit` does not. No external lands under the kit roots in `home/.chezmoiexternal.yaml.tmpl` at this head, so nothing is affected today.

Positive patterns:

- The root table is one constant.
- Two-sided drift refuses the whole run.
- A dry run gives the same verdict.
- A second run is idempotent.
- Operator targets never reach apply (tested at test_deploy_kit.py:92-120).

## 7. Coverage summary (coverage-ledger.json, 58 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 6 | In scope. |
| candidate | 1 | The unvalidated candidate above. |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 51 | Carried from run-8, including the 10 dsh-srt units. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
