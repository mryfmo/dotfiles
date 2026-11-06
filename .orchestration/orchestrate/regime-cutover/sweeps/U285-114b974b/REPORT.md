# Security audit: dotfiles at 114b974bb041b3134237088b062ad85345e85a7a (U276c head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U276, U276b and U276c commits, `4525d339..114b974b`: 4 paths (`scripts/deploy-kit.sh`, the Makefile target, the README paragraph, the tests). `scripts/update-agent-assets.sh` is back to its base content. Round 3 alone is `837d5996..114b974b`, 5 paths, +135 −158. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `114b974b` on `feat/make-deploy-kit`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- **The brief's GOAL and hunt focus describe U251** (`dsh-srt`), which is not in this head. The head the brief names, `114b974b`, is U276c, round 3 of `make deploy-kit`, so this run sweeps U276 to U276c.
- The output directory is **run-11**. The brief's run-10 already holds this seat's U282 sweep and is left untouched.
- The brief's prior "run-103" does not exist; the previous run is run-10, this unit's round 2.

**Prior run.**

- All 58 run-10 units are carried with the same IDs.
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
| `deploy-kit:named-apply-skips-dirty-source-guard` | `scripts/deploy-kit.sh#apply`; `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`; Chained vulnerabilities and trust boundaries | Carried from run-10, unvalidated |

**Claim.** The narrow deploy installs the levers and their pins from a chezmoi source that nothing checks against the merged main.

**Trace.**

- `make update`'s whole apply (Makefile:124) runs the source's `run_before_00-refuse-dirty-source`. It refuses a source whose `home/`, `install/` or `scripts/` differ from origin/main as last fetched (run_before_00-refuse-dirty-source.sh.tmpl:4-14), "so changes reach the host only through a merged pull request" (README.md:351-354).
- `deploy-kit` applies the pending kit targets by name (deploy-kit.sh:209-219). By its own statement, a named apply does not run the source's `run_` scripts (21-23). It pulls nothing (README.md:203), and round 3 adds no comparison with a merged ref. The new managed-set check (95-101, 176-177) compares two listings of the same source tree, so it does not bear on whether that tree is merged.
- Its targets include `~/.local/bin/common/pr-merge.sh`, which the orchestrator policy allows (orchestrator.yml:36-37), and `~/.agents/agent-config.yaml`, which holds the pin that lever's self-check reads.
- The contained orchestrator seat can write that source: its write roots begin with the checkout (hcom-seat:1367, 1373).
- The tests have no case for a dirty source (test_deploy_kit.py:138 is the only guard reference, a fixture row).

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

Round 3 narrows the deploy to the chezmoi apply of the kit roots:

- It runs no updater step, so no download, `pnpm install` or build runs from it; a structural test refuses the updater's name.
- The physical-HOME read now fails closed, like the root reads.
- A pending name that `chezmoi managed` did not list under the kit roots refuses by name.
- `chezmoi apply` runs with stdin closed, so a target changed after the status read fails instead of prompting.
- The listings are split without a here-string or process substitution.

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

- The pstack external under `~/.agents` pins its own sha256 (common.yaml.tmpl:54-61). With `--refresh-externals=never`, a missing cache entry is fetched by chezmoi without `make update`'s bounded prefetch (Makefile:123). That is a robustness gap, not an integrity one.
- README.md:199-200 still promises a post-merge deploy without checking the merge.

Resolved since run-10: both notes on the asset step (`update_deepseek_harness`'s undeclared execution, and `pnpm install` in `~/.dsh/profiles/thak` outside srt) no longer apply, because deploy-kit runs no updater step.

Positive patterns:

- Fail-closed producers, each tested (test_deploy_kit.py:185, 199).
- Physical root checks (220).
- Managed-set membership (157).
- Idempotence (273).

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
