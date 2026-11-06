# Security audit: dotfiles at 837d599641eed7066a0eea3d46d994830a463311 (U276b head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U276 and U276b commits, `4525d339..837d5996`: 5 paths (`scripts/deploy-kit.sh`, the Makefile target, the README paragraph, the tests, and the updater's single-step dispatch row). Round 2 alone is `49108595..837d5996`, 4 paths, +284 −99. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `837d5996` on `feat/make-deploy-kit`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- **The brief's GOAL and hunt focus describe U251** (`dsh-srt`), which is not in this head. The head the brief and the TASK name, `837d5996`, is U276b, round 2 of `make deploy-kit`, so this run sweeps U276 and U276b.
- The output directory is **run-10**. The brief's run-9 already holds this seat's U278 sweep and is left untouched.
- The brief's prior "run-93" does not exist; the previous run is run-9, this unit's round 1.

**Prior run.**

- All 58 run-9 units are carried with the same IDs.
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
| `deploy-kit:named-apply-skips-dirty-source-guard` | `scripts/deploy-kit.sh#apply`; `home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl`; Chained vulnerabilities and trust boundaries | Carried from run-9, unvalidated |

**Claim.** The narrow deploy installs the levers and their pins from a chezmoi source that nothing checks against the merged main.

**Trace.**

- `make update`'s whole apply (Makefile:124) runs the source's `run_before_00-refuse-dirty-source`. It refuses a source whose `home/`, `install/` or `scripts/` differ from origin/main as last fetched (run_before_00-refuse-dirty-source.sh.tmpl:4-14), "so changes reach the host only through a merged pull request" (README.md:351-354).
- `deploy-kit` applies the pending kit targets by name (deploy-kit.sh:73, 215-225). By its own statement, a named apply runs no `run_` script (35-37). It pulls nothing (README.md:206), and round 2 adds no comparison with a merged ref.
- Its targets include `~/.local/bin/common/pr-merge.sh`, which the orchestrator policy allows (orchestrator.yml:36-37), and `~/.agents/agent-config.yaml`, which holds the pin that lever's self-check reads.
- The contained orchestrator seat can write that source: its write roots begin with the checkout (hcom-seat:1367, 1373).
- The tests have no case for a dirty source (test_deploy_kit.py:155 is the only guard reference, a fixture row).

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

Round 2 tightens the deploy:

- The roots must be the real directories they name.
- Every chezmoi read is limited to those roots, with `--refresh-externals=never`.
- Listings are split without a here-string, so a failed temporary file never reads as an empty listing.
- The updater runs one named kit function at a time and never its `main`; a structural test refuses a bare call.

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

- The asset table (deploy-kit.sh:21-29) describes `update_deepseek_harness` by its writes under the kit roots. The step also downloads the harness archive and runs `mise exec -- pnpm install` and `pnpm run build` (update-agent-assets.sh:2061, 2093, 2102), which write pnpm's store and run mise outside those roots. The table describes writes, not execution.
- `deploy-kit` now runs `update_deepseek_harness`, and so runs `pnpm install` in `~/.dsh/profiles/thak` outside srt. Where a DSH launcher or seat makes `DSH_HOME` a write root, `deploy-kit` is one more uncontained runner of that directory. That covers this seat's `dsh-srt:dsh-home-write-root-run-by-updater` from run-6 to run-8, and the U272 seat lead reported on this thread.
- The pstack external under `~/.agents` pins its own sha256 (common.yaml.tmpl:54-61). With `--refresh-externals=never`, a missing cache entry is fetched by chezmoi without `make update`'s bounded prefetch. That is a robustness gap, not an integrity one.
- README.md:199-200 still promises a post-merge deploy without checking the merge.

Positive patterns:

- Fail-closed producers, each tested (test_deploy_kit.py:218).
- Physical root checks (233).
- One named updater function at a time (175, 185, 193, 292).
- Idempotence (284).

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
