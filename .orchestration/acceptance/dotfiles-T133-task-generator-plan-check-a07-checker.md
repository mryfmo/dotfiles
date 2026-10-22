# Acceptance: dotfiles-T133-task-generator-plan-check-a07-checker

Reset of `dotfiles-T133-task-generator-plan-check-a06-checker` (PR #440, round-2 head c439b63c; D-024-57, D-024-58): the audit of c439b63c found an implementation P1 (C15 accepts arbitrary invariants when design_review.design is omitted) and three implementation P2; the mechanism-PR two-round limit forbade a third round. a07 continues PR #440's branch `tools/task-generator-plan-check-a05-checker` from c439b63c and fixes the P1, the audit P2 rows, the local-review decode abort and the two round-2 security symlink P2, with one red-then-green fixture each. The UV_CACHE_DIR refusal of design 5.14 item 9 is not in a07: the a06 R1 fallback stays as a recorded design exception owned by `dotfiles-T133-regime-ci-followup-a02` (restored together with the caller change).

## Authoring (author-loop from `brief-a07-checker.md`, then orchestrator edits)

- Round 1 `…-text-security-922292d.md` and round 2 `…-text-security-0edbd8c.md`: Verdict incorrect; the loop stopped at its two-round limit (exit 7). Recurring P1: the checker's canonical reads trust a PATH-selected gh. Round-2 P2: the measurement base used mutable local origin/main.
- Orchestrator edits (2026-10-21T09:30Z): gh-provenance rows re-owned, fix 7 removed (owner regime-ci-followup-a02), measurement base bound to the canonical main SHA read by the orchestrator's own gh; Checks pasted (observed #435 MERGED 60a6fb2b, canonical main e00de4e0, decoded design digest a027b021…, stage exits).
- Round 3 `…-text-security-fd8c003.md`: Verdict incorrect. P1: moving authority to the orchestrator's bare gh does not authenticate the executable, and the named binding owner binds uv/Python/Node/permgate, not gh. P2: the canonical-main command lacked `--hostname github.com`. P2: shared local git objects are not authenticated for merge-base/numstat.

text-security:922292d:1	executable-provenance
text-security:922292d:2	design-conflict
text-security:0edbd8c:1	executable-provenance
text-security:0edbd8c:2	cap-measurement-base
text-security:fd8c003:1	executable-provenance
text-security:fd8c003:2	canonical-host-binding
text-security:fd8c003:3	measurement-object-trust

re-plan: executable-provenance (rows text-security:922292d:1, text-security:0edbd8c:1, text-security:fd8c003:1 of this text and local:21f52c7:1 of the a06 round-2 head; four rounds in which canonical reads through an unbound gh were taken as authoritative) — specification: no gh read of this regime is authoritative until gh is pinned and bound by absolute path with `--hostname github.com`; the checker's reads are pre-dispatch hygiene, the orchestrator's reads are recorded as non-authoritative evidence, and the record says so; design: the gh binding is owned by `dotfiles-T133-gh-binding-a01` (owner stub written 2026-10-21T09:30Z, after the binding task; pin github-cli in mise, declare the absolute gh path in agent-config.yaml, bind every canonical read), while uv/Python/Node/permgate stay with `dotfiles-T133-trusted-entrypoint-binding-a01`; the cap measurement runs in a fresh private HTTPS bare clone (generalisation owned by `dotfiles-T128-chain-review-scripts-followup-a09`); implementation: the a07 text edit of 2026-10-21T09:30Z (bytes 45b58f323a0eaf62878c2009d6af78351f5c71476386e924082d396574ec4c0d; rows 35-38 and items 2/8 re-owned, `--hostname github.com`, private-clone measurement), no checker code change for this class; verification: C-80 round 4 of these bytes under this line (the first review after it; C-92 allows three), then the anchor review by another context, then dispatch to a Codex seat other than a012.

## Counters (INV-6)

a06 lineage: TASKs=2 (cap amendment resend) revises=1 RESULTs=2 questions=0 blocked-PONGs=6 (snapshot 08:02Z). a07: not dispatched; amendments=0.
- 2026-10-21T09:41Z: Checks re-pasted with the observed values after the pins merge (canonical main 4eafd890454e495fdb1d429734c5835e46c87652, merge-base with c439b63c unchanged, design digest equal, --hostname github.com in the command); bytes c6cebe47312094927a3a607149d8dc8c5d2bcbbfebed3a7d96f63a22da979779; round 4 runs on these bytes.
- 2026-10-21T09:47Z: owner declaration for the records boundary: the residual rows of this lineage named above are owned by dotfiles-T133-gh-binding-a01 (owner stub under .orchestration/tasks/).
- 2026-10-21T21:24Z: C-80 round 4 (`…-text-security-c6cebe4.md`, run by the orchestrator unsandboxed: the classifier approved the call this time): Verdict incorrect. P1: non-authoritative gh output still selected the measurement base and the prerequisites, so a substituted gh could pass the candidate head off as main. P2: `--repo mryfmo/dotfiles` without a fixed host. P2: Checks lacked the exact commands and stage exits of line 119. Edit: the measurement and every prerequisite now come from a fresh private bare clone fetched anonymously over HTTPS with git only (no gh anywhere in the measurement path; #435's merge state is its merge commit's ancestry of refs/heads/main; the design digest is `git show` of that ref); Checks rebuilt with each command and exit; bytes a3125e128a240b1800372977cc3f52bc97cd702e3a5f7f48e46fa1e813b77e65; round 5 is the third and last review under the re-plan line.

text-security:c6cebe4:1	executable-provenance
text-security:c6cebe4:2	canonical-host-binding
text-security:c6cebe4:3	checks-omission
- 2026-10-21T21:28Z: C-80 round 5 (`…-text-security-a3125e1.md`, orchestrator-run): Verdict incorrect, three P1 and two P2. The executable-provenance class moved from gh to bare git (PATH/mise substitution can forge the clone and the measurement), to unsanitised GIT_* (GIT_CONFIG_COUNT rewrites the fixed URL, GIT_DIR redirects reads), and to the checker's forwarded credentials ("non-authoritative" does not stop disclosure); P2: the private clone directory has no worker-write exclusion or consumption-time identity binding; P2: the design-publication assertion is counted, not performed. Five rounds, five incorrect verdicts, one class: no text can close it before a trusted-executable binding exists on the host (design 5.14 items 2-4/9: dotfiles-T133-trusted-entrypoint-binding-a01 and dotfiles-T133-gh-binding-a01), which is the same wall a08 declared at its line 63. STOP (feedback: re-plan, not a patch): the a07 authoring stops here; the decision (hold behind the binding, or an explicit operator waiver of the surviving P1 for dispatch) is escalated with materials.

text-security:a3125e1:1	executable-provenance
text-security:a3125e1:2	environment-sanitisation
text-security:a3125e1:3	executable-provenance
text-security:a3125e1:4	measurement-object-trust
text-security:a3125e1:5	checks-omission
- 2026-10-21T21:30Z: D-024-65 (operator option A): a07 held, undispatched, until the trusted-entrypoint binding is deployed; the C-80 resumes then on these bytes (a3125e1…) or an amended text; #440 open, #411 waits.

