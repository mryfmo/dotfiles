# Security audit: dotfiles at 0f17e8ab86b3336d558940f09522194eff3cec08 (U283c head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | The U283, U283b and U283c commits, `a23e4541..0f17e8ab`: 4 paths (`scripts/update-agent-assets.sh`, `scripts/lib/asset-manifest.sh` and their two test modules), +749 −28. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `0f17e8ab` on `fix/updater-single-function-fails-closed`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- The output directory is **run-13**. The brief's run-12 already holds this seat's U289 sweep and is left untouched.
- The brief's prior "run-10 (the U283c head)" is not this seat's: this seat's run-10 is the U282 deploy-kit sweep. The U283 sweeps were made on another seat, whose state root this seat cannot read, so **no U283 record is carried** and the unit was hunted fresh.
- The branch's base is `a23e4541` (`git merge-base HEAD origin/main`), not `8f31cf5c`; the brief's CONTEXT diff line (`c4195463..HEAD`, one file) was not used.

**Prior run.** run-12's 58 units are carried for their identities, and 5 units are added for the U283 surfaces. The 7 deploy-kit units, run-12's unvalidated candidate `deploy-kit:named-apply-skips-dirty-source-guard` among them, are out of scope here: `scripts/deploy-kit.sh` is not in this head (the branch predates the U276 merge). That candidate stays open for the deploy-kit unit.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran.
- The hunt raised no candidate, so no validation was skipped; findings.json holds no record.
- No critic ran, so this report makes **no clean-coverage claim**.

## 2. Security posture

The unit makes the updater fail closed where it did not:

- **Single-step runs** end with `fail_on_pin_failures` (update-agent-assets.sh:2876-2877). A step that returns non-zero already exits under `set -Eeuo pipefail` (11), because `main` runs at top level (2919-2921). So a single step exits 0 only when it neither failed nor counted a failure. The whitelist names thirteen steps, each a function at this head, and any other argument list exits 2 (2873-2882; tests 508, 521).
- **Destinations are proven before a delete or sync** (127-157). The parent must be a real directory whose physical path is its spelling under the physical HOME, and the destination must not be a link. This holds at all four sites: 1511, 1648, 1728 and 2836.
- **A failed or empty CompactionDB sync is never recorded as installed.** It is counted, marked in the manifest and reported by the doctor until a sync completes (2811-2851; tests 165-269).
- **The manifest pruner** refuses a linked or non-regular manifest, and decides the retired set in one status-checked jq program; its failure now fails the run (asset-manifest.sh:158-194; update-agent-assets.sh:2860-2862).
- **The harness build** runs mise with `MISE_EXEC_AUTO_INSTALL=false` (2142, 2151). This is mise's `exec_auto_install` setting, present on this host.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

### 6.1 The destination proof admits all of `~/.local`

`assert_asset_destination` accepts any destination under `~/.local/` (update-agent-assets.sh:129-135). That tree holds `~/.local/state/omp-seats`, where the seat checkouts and state roots live; seats may write those (hcom-seat:1373). No current caller writes there; the four destinations are:

- `~/.agents/compactiondb`
- `~/.agents/skills/security-audit`
- `~/.local/lib/omp-extensions/pi-claude-bridge`
- `~/.local/share/agent-assets/omp/omp.previous`

So this is not reachable today. Naming the callers' parents in the case would keep a later caller from passing a seat-writable destination.

### 6.2 Check-to-use windows

The proof runs one command before the write for CompactionDB (2836-2837) and for the omp aside (1511). The window is longer at two sites:

- **The pi bridge.** The proof runs before the unpack, the patches, `bun install` and the gap check, which all precede the `rm -rf` and `mv` of 1669-1678.
- **The security-audit skill.** The proof runs before the unpack, which precedes 1736-1745.

A parent replaced by a link inside that window is written through. `~/.agents` and `~/.local/lib` are no seat write root, so only an uncontained process could race it. Repeating the proof just before the rename would shorten every window to one command.

### 6.3 Other notes

- `mkdir -p` of the parent runs before the proof (1511, 1647, 1727, 2835). Through a linked component, it creates empty directories outside the asset tree before the refusal.
- A refusal in `update_compactiondb` returns 1 and ends the full run under `set -e`, before `ensure_herdr_integrations`, the prune and `refresh_codex_hook_trust` (2911-2914). The run fails closed, but those steps are skipped for that run.
- The manifest writer `_manifest_record` still tests the path with `[ -f ]` (asset-manifest.sh:108). That follows a link, reads its target and renames over the path (119), and with a directory at the path the rename moves the temporary file into it. The pruner now refuses both shapes (163-166). `~/.agents` is no seat write root, so this is consistency, not reachability.

### Positive patterns

- Every new refusal and failure path has a failure-injection test:
  - physical-path read failures (test_update_agent_assets.py:404)
  - a linked destination at each call site (53, 331, 571, 600)
  - a corrupt or non-file manifest (280, 305; test_asset_manifest.py:6)
  - a failed, partial or empty sync (204, 223, 255)
  - a failed record (269)
  - a failing single step (462)
- The prune decision moved from a here-string loop to one status-checked jq program, so a failed temporary file can no longer read as "nothing retired".

## 7. Coverage summary (coverage-ledger.json, 63 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 6 | The destination proof, the single-step dispatch, the manifest pruner, the CompactionDB failure mark, the unit's diff scan, and the updater's main for the mise setting. |
| candidate | 0 | — |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 57 | Carried from run-12; the 7 deploy-kit units among them are not in this head. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
