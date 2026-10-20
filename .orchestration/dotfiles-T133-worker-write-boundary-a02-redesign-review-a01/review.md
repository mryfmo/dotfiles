---
task_id: dotfiles-T133-worker-write-boundary-a02-redesign-review-a01
seat: claude-standard-dot-a011
task_sha256: 6c636456e4baab6c4e29961c6c5693585e2a7f8b681f1ea2005cc76c234f71f6
design: .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
design_sha256: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b
verdict: accept
---

# Review: the a03 redesign as the INV-6 reset of dotfiles-T133-worker-write-boundary-a02

Read only. The files were read in the main checkout on 2026-10-20 (`origin/main` `f7f38067`). A is the a02 text (`ae1088a7…`), B the a03 text, and R the a02 acceptance record (working copy, chronology lines 73 to 81). A read-only helper extracted the line citations, and this seat checked the decisive ones itself.

## Hash

`shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md` gives `49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b`, which equals the task's value.

## Item 1: the hash

ok.

## Item 2: reset_of, the findings and no widening

ok. B:30 reads `reset_of: [dotfiles-T133-worker-write-boundary-a02]`.

The findings that forced the reset (R:73 to R:81; no audit of `c0f50fa1` exists, see R:77 and B:220) are each answered by a stated control:

| Row | Finding | Where B answers it |
| --- | --- | --- |
| `security:c0f50fa:1` | AWS credential-chain selectors | B:413 refuses `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` before any credential lookup; B:389 admits only `AWS_EC2_METADATA_DISABLED="true"` |
| `security:c0f50fa:2` | screening only the dotfiles anchor | B:425: every launch route refuses another repository before worktree creation, registration, hook writes, trust or spawn (R's second remedy) |
| `security:c0f50fa:3` | object-form plugin mappings | B:448 and B:437 refuse `{"source": …}`, inline content, arrays and objects |
| `local:c0f50fa:1` | the actual managed skill directory | B:429 inventories the enterprise `<managed-root>/.claude/skills` on both platforms |
| `local:c0f50fa:2` | project settings widening the sandbox | B:373 and B:466: worker exclusions are empty, and extra write roots or sockets are refused before array merging |
| `local:c0f50fa:3` | the parent directory for the install | B:476, item 13 |
| `local:c0f50fa:4` | reconciling after Herdr's installer | B:474, item 12 |
| the re-plan (R:73) | from screening listed keys to allowlisting accepted inputs | B:304 and B:324 |

**No widening.** `allowed_files` differs only by the a03 evidence directory replacing a02's (B:28 and A:28); the other 21 entries are identical. Neither text has a closed row that the other makes residual, since A had no closed rows and B adds eight (B:99 to B:137). The write grants, the three administrative exclusions, the Herdr-only socket, the PermissionRequest exception and the unchanged Codex arguments and network policy match between the texts (A:604/B:371, A:685-693/B:466, A:462/B:468, A:814/B:417).

The new launch-environment allowlist (B:391-405) narrows A, which only screened selectors. Its names grant no sandbox exception (B:401). `CHEZMOI_SOURCE_DIR` and `CHEZMOI_HOME_DIR` (B:405) are preparation-only trusted bindings, "not caller-selected worker configuration or executable roots", consistent with A:795.

Advisory notes, P3, none blocking:

- **B:405.** The value authority for `CHEZMOI_SOURCE_DIR` and `CHEZMOI_HOME_DIR` names no concrete check, such as equality with the validated home's chezmoi source. Every other row in the table names its value.
- **A:966.** A's "Add no new store-derived sourcing" has no equivalent in B; B:581 only assigns the ownership. B:304's general refusal arguably covers it, but the explicit prohibition is gone.
- **A:1056.** The Completion clauses and the advisory-P2 owner `dotfiles-T133-worker-write-boundary-followup-a01` are not restated. B:353 brings both `c0f50fa1` P2 fixes into scope instead, and the orchestrator reconciles the owner rows.
- **Residual rows.** B's residual rows cite no test selector, while A's did (A:32, A:76).
- **B:369 and B:427-429.** B both admits additional-directory `.claude` and skills roots and fixes `additionalDirectories` to `[]` while refusing caller-added ones. That is an internal tension worth one sentence.
- **B:306 and B:615.** B grants two correction rounds while continuing PR #431. R:73 cites the operator's order of no third round on a mechanism PR, while R:77 itself directs the continuation. The reset anchor is the orchestrator's call, so this is noted, not judged.

## Item 3: dispatched already, nothing changed

ok. This review changed no repository file other than this record in the seat's worktree. It made no commit, push or PR, and dispatched nothing.

## Verdict

accept
