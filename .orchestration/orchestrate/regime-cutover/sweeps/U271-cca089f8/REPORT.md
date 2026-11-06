# Security audit: dotfiles at cca089f8e58b976dbbf9aeda51a0f1b8ef17c5b7 (U251d head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U251 commits, rounds 1 to 4, `b49be338..cca089f8`: 7 paths. Round 4 alone is `d49a5349..cca089f8`, 5 paths, +1046 −467. hcom-seat and the updater were read as context. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `cca089f8`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. Every check is `method: source`. |

**Brief corrections.**

- The output directory is **run-8**. The brief's run-7 already holds this seat's U266 sweep of `d49a5349` and is left untouched.
- The brief's prior "run-73" does not exist on this seat; the previous run is run-7, this unit's round 3.
- The base `d1ecd495` predates the branch start `b49be338`.
- The CONTEXT diff line is the U224 sweep's text and was not used.

**Prior run.** All 50 run-7 units are carried with the same IDs:

- The carried candidate `dsh-srt:dsh-home-write-root-run-by-updater` is unchanged.
- The 8 covered units were re-read at `cca089f8` with their lines re-mapped. That includes the srt-interpreter unit resolved in run-7, which stays resolved.
- The 41 out-of-scope units stay out of scope.

**New in this run.** One unit and candidate, `dsh-srt:self-check-helpers-from-caller-path`. It has been present since round 1, and **run-6 and run-7 did not raise it, a coverage gap of those runs disclosed here.**

There are no prior records.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran.
- Neither candidate can get the fresh verifier the skill requires. **Both stay unvalidated in the coverage ledger and are not findings**; findings.json holds no record.
- No critic ran, so this report makes **no clean-coverage claim**.

### Unvalidated candidates (ledger only; not findings, no severity)

| Fingerprint | Ledger unit (surface; boundary; class) | Status |
| --- | --- | --- |
| `dsh-srt:self-check-helpers-from-caller-path` | `scripts/orchestrator/dsh-srt#lever_self_check`; `scripts/orchestrator/hcom-seat#system_path`; Chained vulnerabilities and trust boundaries | New, unvalidated |
| `dsh-srt:dsh-home-write-root-run-by-updater` | `scripts/orchestrator/dsh-srt#write`; `scripts/update-agent-assets.sh#update_deepseek_harness`; Chained vulnerabilities and trust boundaries | Carried from run-6 and run-7, unvalidated |

#### 1. `dsh-srt:self-check-helpers-from-caller-path` (new)

**Claim.** The round-4 header (dsh-srt:23-32) says that before containment the launcher runs only `/usr/bin/stat`, `/usr/bin/readlink`, `/bin/mkdir`, `/bin/rm` and the pinned node and srt pair. That is not true of the self-check.

**Trace.**

- `lever_self_check` (82-128) is called at line 129, before the caller's environment is read and dropped and PATH is set to the system directories (141-153).
- It runs `sed -n -E` (106) with the caller's PATH, environment and cwd.
- Through `command -v sha256sum` it runs the first `sha256sum` on the caller's PATH, else `shasum` from it (114-117). On macOS, which ships no `sha256sum`, any PATH entry holding one is used.
- A PATH entry under DSH_HOME or the scratch root puts a program the contained dsh wrote there into the uncontained launcher. `DSH_HOME/bin` holds the `dsh` wrapper, so it is a natural PATH entry. A relative or empty PATH entry does the same when the caller's cwd is a write root.
- A planted `sha256sum` can print the expected pin, so the self-check also passes.

**What the seat does instead.** hcom-seat sets `PATH=/usr/bin:/bin:/usr/sbin:/sbin` (hcom-seat:101-103) before the identical `lever_self_check` (123-173).

**Tests.** The tests exclude `sed`, `shasum` and `sha256sum` from the planted helpers on purpose: "`lever_self_check` (the shared U31 form, out of this unit's scope) looks them up" (test_dsh_srt.py:96-97).

**Blockers.**

- The caller's PATH and cwd when the operator runs dsh-srt.
- Whether the host has a system `sha256sum`.

**Bounded local check.**

- In a scratch HOME, plant a marker-writing `sha256sum` that prints the real digest, in `DSH_HOME/bin`.
- Run dsh-srt with that directory anywhere on PATH, on a host without a system `sha256sum`, or with it first otherwise.
- A marker written outside srt confirms the claim.

**Owner check.** The PATH of the hosts that run dsh-srt, and whether `DSH_HOME/bin` is on it.

**Smallest fix.** Set `PATH=/usr/bin:/bin:/usr/sbin:/sbin` before `lever_self_check`, as hcom-seat does (move line 133 and the PATH export above line 129, keeping `caller_path` read first). Alternatively, call `/usr/bin/sed` and `/usr/bin/shasum` by absolute path in this lever's copy.

#### 2. `dsh-srt:dsh-home-write-root-run-by-updater` (carried)

**Trace.**

- allowWrite is DSH_HOME whole, the scratch root and `DSH_HOME/.state/claude` (dsh-srt:524, 679, 684).
- The write denies under DSH_HOME are only the settings directory and PROJECT_FILES (189-190, 649-652). So `DSH_HOME/profiles/thak`, `DSH_HOME/dsh` and `DSH_HOME/bin` are writable from inside, including a `.pnpmfile.cjs`, `.npmrc`, `mise.toml` or `.tool-versions` placed in them.
- `make update` runs `update_deepseek_harness` as the operator, outside srt and unchanged on this branch. It runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` (update-agent-assets.sh:2170), and `pnpm install` plus `pnpm run build` in a new tree under `DSH_HOME/dsh` (2161).

**Blockers.** Whether the pinned pnpm executes a `.pnpmfile.cjs` or honours an `.npmrc` there, and whether mise acts on a config planted there without a trust prompt.

**Bounded local check.** Plant those files with marker hooks in a scratch DSH_HOME, and run the profile install offline.

**Smallest fix.** Narrow allowWrite and write-deny `profiles/`, `dsh/`, `bin/` and `plugins/`. Or have the updater refuse unrendered files there before running pnpm or mise.

## 2. Security posture

Round 4 removes almost every helper from the pre-containment path:

- no python3, `env`, `head` or `uname`
- only absolute PATH entries searched
- one trust rule to `/`, including for DSH_HOME and TMPDIR
- a fresh 0700 settings directory, with the file created O_EXCL
- the exported environment enforced to the listed names

srt and its node stay pinned.

Two leads remain:

- the self-check still runs `sed` and a hash tool from the caller's PATH before the reset that hcom-seat does first
- the updater still runs pnpm and mise inside the launcher's `DSH_HOME` write root, outside srt

## 3. Confirmed findings

None. No candidate could be independently validated; see section 1.

## 4. Confirmed finding details

None.

## 5. Needs validation

No `needs_validation` record. The open leads are the two unvalidated candidates in section 1, and they are not records.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes:

- hcom-seat read-denies a configured `REGIME_SEATS_ROOT` (hcom-seat:1751-1754). dsh-srt still denies only `~/.local/state/omp-seats` (181-183).
- hcom-seat's canary probes the operator's `~/.claude/debug` (hcom-seat:1818-1833). dsh-srt's canary is still three probes (694-700).
- The canary's write probe targets the explicitly denied sandbox directory, so a too-broad allowWrite would still pass it.

Positive patterns:

- The environment drop is done by the shell, refuses names it cannot drop, and checks the exported set against ENV_NAMES.
- The bootstrap `stat` holds the four system tools to root ownership with no group or other write.
- Every `stat` and `readlink` answer is shape-checked and fails closed (tests at 1046, 1068, 1099).
- Both lever copies are identical (`dbff15c7…`), and their sha256 `fac6e7e5…` is the manifest pin (agent-config.yaml:896).
- run-7's earlier hardening note about python3's mode rule no longer applies, because python3 no longer runs.

## 7. Coverage summary (coverage-ledger.json, 51 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 8 | In scope. |
| candidate | 2 | The two unvalidated candidates above. |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 41 | Carried. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
