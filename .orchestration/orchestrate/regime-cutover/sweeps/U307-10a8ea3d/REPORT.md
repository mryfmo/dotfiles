# Security audit report: dotfiles at 10a8ea3d53f99f56ba0f3c544e5477c624c64f1a

## 1. Run, scope and limits

**Candidate validation is incomplete, so this is a partial pass.** Four carried leads are re-checked at this head, and no independent verifier could run.

| Fingerprint | State at this head |
|---|---|
| `records-sync/redaction/account-identity-residue-in-published-row` | `candidate`, stands, proposed confirmed (section 5a) |
| `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` | `candidate`, narrowed to direct runs, proposed needs_validation (section 5b) |
| `dsh-profile:web-search-routes-to-the-official-api` | `candidate`, refuted on main, proposed rejected (section 5c) |
| `dsh-profile:thak-runs-without-command-sandbox` | `candidate`, proposed rejected (section 5c) |

Per the skill's rule, an unvalidated candidate goes into `findings.json` under no verdict, and the run is `incomplete`.

**Profile and scope.** The profile is `standard`, scoped to records sync 46, commit 10a8ea3d on origin/main 25427b91. It changes 266 paths, all under `.orchestration/orchestrate/regime-cutover/`: 258 added and 6 modified at mode `100644`, and 2 added at `100755`. The scope also includes the four carried leads, re-checked on the new base, which merges U227f (#703) and U272 (#697). Every other path is carried `out_of_scope`.

**Brief discrepancies.** The brief names the unit U274 and the base 8f31cf5c, and asks for run-7 to be carried. The head is records sync 46 on 25427b91, and I carried this seat's latest run, run-16.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and two verifiers per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy. No target code ran. The parent's scripts read git blobs and printed counts, locations and shapes only, never matched text (`agents/parent-hunter/scratch/`).

**Independence gap.** The delegation tool (Task) and eval kernel are denied by policy on this seat. Every phase ran in the parent (`parent-hunter`). The post-wave pass accepted one unit (the host-row executor), which was hunted in the same parent pass. No Phase 3 or Phase 5 verifier ran.

**Deferred.** Nothing.

## 2. Security posture

**Records sync 46.** It publishes no secret and no home path, and its structure holds.

- **Scan.** The parent's scan of the 266 blobs (2,457,930 bytes) finds no token, key, private key, bearer value, JWT, secret assignment or redact word, and 6 masks.
  - Every `/Users/` and `/home/` hit is harmless: `decisions.tsv:525`'s literal placeholder `<name>`, or the repository's own `home/dot_agents`.
  - The only personal email address is the carried identity row's (section 5a).
- **Paths and modes.** All 266 paths are under the store, there are no symlinks or binaries, and `redact-words.txt` is absent.
- **The deliberate credential probe.** `tests/sandbox-write-denies.tsv` row s17 runs `cat ~/.ssh/config` under a worker's srt settings to prove the read is denied. Its published `observed` cell is a 51-character denial (exit 1, "Operation not permitted"), with no config or key content. The deny held, and nothing leaked.
- **The first executable records.**
  - `tests/run-host-rows.py` runs each pending `host` row's command cell with `bash -lc`, the full environment and no sandbox.
  - No published consumer runs it: `.orchestration` is outside chezmoi's source (`.chezmoiroot` = `home`), and no CI step executes records.
  - At this head all 31 host rows are already judged (0 pending), and no notes file is in the tree, so publishing starts nothing.
  - Its store-side use is a hardening note (section 6.1).

**The new base** narrows the file-tool lead (section 5b) and carries the fix for the web-search lead (section 5c).

## 3. Confirmed findings

None. All four leads are unvalidated (section 1).

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None in `findings.json`. The four leads are unvalidated candidates (sections 5a to 5c).

| Title | Trace | Blocker | Local next step | Owner-observed check |
|---|---|---|---|---|
| — | — | — | — | — |

## 5a. Lead: account identity in a published row (not a finding)

**`records-sync/redaction/account-identity-residue-in-published-row`**, carried since run-2. Proposed verdict confirmed, proposed severity low.

Sync 46 appends rows to `decisions.tsv` but keeps the `claude auth status` row at `:509`, byte-identical; it is on origin/main since aabee966. It publishes four account fields:
- the account email's residue, with its employer domain;
- the organisation UUID;
- the organisation name;
- the subscription type.

None is quoted here. The causes are unchanged:
- the literal redact-word scan (`scripts/validate-agent-assets.py:2434-2440`, `:2443-2465`);
- the hand pass (`decisions.tsv:521`);
- no email or account rule (`.github/workflows/agent-assets.yml:69-70`);
- the sync contract's content-review exclusion (`scripts/orchestrator/records-sync.sh:511-515`).

**Fix.**
1. Reduce the store row to "`claude auth status` exit 0, logged in", and publish it with the next sync. The row's history stays in aabee966, so removing it from history needs the owner's decision.
2. Add email and account-key rules to `identifier_reasons`.
3. Treat each component of a multi-part redact word as a word.

## 5b. Lead: the thak file tool can write a checkout's `.git`, now narrowed (not a finding)

**`dsh-profile:thak-fs-tool-writes-workspace-git-unguarded`**, carried from run-14. Proposed verdict needs_validation, narrowed at this head.

- **Closed under the U272 role.** The `hcom-seat dsh` role is now on main.
  - Its working directory is scratch inside the seat's state slot, not a checkout (`scripts/orchestrator/hcom-seat:1236-1240`).
  - Its write roots are `DSH_HOME`, its omp profile and `~/.omp/run` (`:1494`).
  - The checkout, its git directory and common directory, and the store are denied for read and write (`:96-98`, `:1662-1665`, `:1791-1794`).
  - So `workspace-write` can only reach scratch there.
- **Open for a direct run.** The installed wrapper still execs the harness with no srt check (`scripts/update-agent-assets.sh:2174`). A direct `~/.dsh/bin/dsh` run from a checkout keeps the thak file tool active with no kit hook and no permission preset. Its only fence is `workspace-write` under that checkout, `.git` included (upstream `fs/tool-fs/src/write.ts:113-131`; `fs/fs-sandbox/src/index.ts:20-24`, `:113-143`).
- **Blockers.**
  1. The runtime write is upstream behaviour, read but not observed.
  2. Whether the operator runs dsh directly from a checkout, now that the role exists.
- **Smallest fix.** Have the wrapper refuse a run outside srt; the role's shim can export a marker it checks. Or set `DSH_PERMISSION_MODE=read-only` in the wrapper, so that only the role gets workspace writes.

## 5c. Leads refuted at this head (not findings)

- **`dsh-profile:web-search-routes-to-the-official-api`** (from `sweeps/U227-785658d1`). U227f is on main. The patch disables both rows by their base-bundle ids (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-12`), and the web seam fails closed. Proposed verdict rejected.
- **`dsh-profile:thak-runs-without-command-sandbox`** (from `sweeps/U227-785658d1`). `bash-sandbox` is off (`:13-14`), so `tool-bash` cannot activate, as U298 pins on main. Proposed verdict rejected for the shell path.

## 6. Hardening notes and positive patterns

These are not findings.

1. **Records that execute (new).**
   - **What it does.** `tests/run-host-rows.py` runs table command text with `bash -lc`, the full inherited environment and no sandbox, on whichever host the coordinator runs it. The tables come from a worker unit (U274), copied into the store, and any future pending host row runs exactly as written. So do the cells of a notes file, if one is added.
   - **Fix.** Print each pending command and require a confirmation, or run host rows under the worker seat's srt settings where a row does not need the host. Either would keep a worker-authored row from becoming unsandboxed host execution by default.
2. **Executable records are now published** (context). The lever carries file modes by design. Nothing published runs them, but a future consumer that executes files under `.orchestration` would inherit worker-authored code.
3. **Carried.** Hand redaction passes are not a control (`decisions.tsv:521`, `:525`), and run-15's CI-gate context note still applies.
4. **Another seat's open candidate, now on this base** (context, not this run's lead). U272 merged as #697 with a candidate from the sweep-2 seat's run-11 still unvalidated. The dsh role's write roots include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1494`), and `make update` runs `pnpm install` in `${DSH_HOME}/profiles/thak` outside srt, with no `--ignore-pnpmfile` and no `--ignore-scripts` (`scripts/update-agent-assets.sh:2151`). I read both lines at this head and they match. A write the sandboxed harness makes there could run on the host at the next update. It is tracked under that seat's fingerprint (its run-19 `REPORT.md` 1a), so this run does not re-hunt it. Its updater-only fix is `--ignore-pnpmfile --ignore-scripts` on that install.

### Positive patterns

- The sandbox-deny probe's published output proves the deny without leaking what it protects.
- Every host row is already judged before the sync.
- The U272 role confines dsh to a scratch working directory, with no git write path.

## 7. Coverage summary

From `coverage-ledger.json` (52 units):

| Status | Units |
|---|---|
| covered | 5 |
| candidate | 4 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 43 |

- **Covered (5):**
  - the four records-sync units, re-opened: secrets in the copies; copy-set paths and modes; home and host paths; records as CI and agent inputs;
  - the new host-row executor unit.
- **Candidate (4):** the four leads.
- **Out of scope (43):** every other top-level directory, the unchanged records, run-16's two units (on main unchanged), and the earlier carried units.

**Critic results.** The post-wave critic accepted one missing unit (the executor), and the final-clean critic found no work. Both ran in the parent, so this is a single-reviewer coverage statement.
