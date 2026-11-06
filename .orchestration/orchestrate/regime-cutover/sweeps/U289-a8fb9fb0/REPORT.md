# Security audit: dotfiles at a8fb9fb0c072c03de2e69a6707bdae6026c6cabc (U276d head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | The four U276 paths at `a8fb9fb0` (`scripts/deploy-kit.sh`, the Makefile target, the README paragraph, the tests). U276 merged as `29439083` (#698), identical over those paths to the run-11 head `114b974b`. Round 4 (U276d), `29439083..a8fb9fb0`, changes 3 of them, +345 −62. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `a8fb9fb0` on `fix/deploy-kit-verify-and-recheck`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- **The brief's GOAL and hunt focus describe U251** (`dsh-srt`), which is not in this head. The head the brief names, `a8fb9fb0`, is U276d, round 4 of `make deploy-kit`, so this run sweeps U276 to U276d.
- The output directory is **run-12**. The brief's run-11 already holds this seat's U285 sweep and is left untouched.
- The brief's prior "run-113" does not exist; the previous run is run-11, this unit's round 3.

**Prior run.**

- All 58 run-11 units are carried with the same IDs.
- The candidate `deploy-kit:named-apply-skips-dirty-source-guard` is unchanged in substance.
- The 6 covered units were re-read with their lines re-mapped.
- The 51 out-of-scope units stay out of scope; the two dsh-srt candidates among them are not in this head.
- There are no prior records.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran.
- The candidate **stays unvalidated in the coverage ledger and is not a finding**; findings.json holds no record.
- No critic ran, so this report makes **no clean-coverage claim**.

### Unvalidated candidate (ledger only; not a finding, no severity)

| Fingerprint | Ledger unit (surface; boundary; class) | Status |
| --- | --- | --- |
| `deploy-kit:named-apply-skips-dirty-source-guard` | `scripts/deploy-kit.sh#apply`; `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`; Chained vulnerabilities and trust boundaries | Carried from run-11, unvalidated |

**Claim.** The narrow deploy installs the levers and their pins from a chezmoi source that nothing checks against the merged main.

**Trace.**

- `make update`'s whole apply (Makefile:124) runs the source's `run_before_00-refuse-dirty-source`. It refuses a source whose `home/`, `install/` or `scripts/` differ from origin/main as last fetched (run_before_00-refuse-dirty-source.sh.tmpl:4-14), "so changes reach the host only through a merged pull request" (README.md:358-361).
- `deploy-kit` applies the pending kit targets by name (deploy-kit.sh:293-298). By its own statement, a named apply does not run the source's `run_` scripts (24-25). It pulls nothing (README.md:203), and round 4 adds no comparison with a merged ref.
- Round 4's re-reads (the roots after status, 221-233; the managed set after the apply, 314-329) bound which names are applied and verified, not which content they carry. `chezmoi apply` installs whatever the checkout holds at apply time, and `chezmoi verify` compares the target with that same checkout.
- Its targets include `~/.local/bin/common/pr-merge.sh`, which the orchestrator policy allows (orchestrator.yml:36-37), and `~/.agents/agent-config.yaml`, which holds the pin that lever's self-check reads.
- The contained orchestrator seat can write that source: its write roots begin with the checkout (hcom-seat:1367, 1373).
- The tests have no case for a dirty source (test_deploy_kit.py:187 is the only guard reference, a fixture row).

**Blockers.**

- That chezmoi's named apply runs no `run_before_` script. This is the script's statement, not measured here.
- Where the coordinator runs `deploy-kit`.
- Whether the main checkout can hold an unmerged lever change at that moment.

**Bounded local check.**

- In a scratch HOME and a scratch clone with an origin/main ref, edit `executable_pr-merge.sh` and its pin without committing.
- Run `chezmoi apply` (expect the guard's refusal), then `deploy-kit.sh`.
- An installed lever equal to the edit confirms the claim.

**Owner check.** Where `make deploy-kit` runs, and that the checkout holds only merged main when it does.

**Smallest fix.** Run the guard's comparison (or the guard script by path) before the named apply and refuse on a dirty source. Alternatively, apply from a clean export of origin/main.

## 2. Security posture

Round 4 tightens the apply and its verification:

- The roots are read again after the status read; a root that changed, or now fails the physical check, refuses naming it.
- A status row on a root itself is refused unless it is a plain pending change, so a root replaced by a link (`MM`) or removed by the source (`D`) stops the run.
- `chezmoi apply` and `chezmoi verify` run with `--recursive=false`, so a pending directory is applied as its own entry and a child the managed listing never named is not installed.
- A retired target is verified by its absence (a dangling link counts as present), and every other applied name is verified only after a fresh managed read still lists it; that re-read fails closed.

The carried gap is unchanged: no check that the source being deployed is the merged one.

## 3. Confirmed findings

None. No candidate could be independently validated; see section 1.

## 4. Confirmed finding details

None.

## 5. Needs validation

No `needs_validation` record. The open lead is the unvalidated candidate in section 1, and it is not a record.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes:

- **Root swap after the re-read.** The root re-read (deploy-kit.sh:221-233) closes the swap window up to the status read, not up to the apply (293-298). A root replaced after the re-read is applied through. The kit roots are no seat write root (hcom-seat:1373), so only an uncontained process of the operator could race it. A re-check after the apply, beside the retired-target check, would make the window observable.
- **Retired targets and the managed listing.** A `D` row must pass `in_kit_set` (247-248), so it needs `chezmoi managed` to list the retired (`.chezmoiremove`) target. That was not measured: no chezmoi command may read the target source in this run. If chezmoi does not list it, every `D` row is refused as unmanaged and nothing is applied, which fails closed. That is a robustness question, not a security one. The fixture lists it by default (test_deploy_kit.py:69-71).
- **The pstack external.** It pins its own sha256 (common.yaml.tmpl:54-61). With `--refresh-externals=never`, a missing cache entry is fetched by chezmoi without `make update`'s bounded prefetch (Makefile:123). That is a robustness gap, not an integrity one.
- **The README promise.** README.md:199-200 still promises a post-merge deploy without checking the merge.

Positive patterns:

- Fail-closed producers, each tested, including the post-apply managed re-read (test_deploy_kit.py:232, 246, 436).
- Physical root checks before and after the status read (267, 370).
- The root-row refusal (386) and the non-recursive apply (406).
- Retired-target verification by absence, dangling links included (334, 355).
- Idempotence (320).

## 7. Coverage summary (coverage-ledger.json, 58 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 6 | In scope. |
| candidate | 1 | The carried unvalidated candidate. |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 51 | Carried. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
