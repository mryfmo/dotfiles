---
reviewed_at: 2026-10-10T22:28:36Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@25b36e1c6e41aed8014af28911dbe9744bacc77a37ad6c1e445b35a03c5030be
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 6
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 6 (six invariants after the Bot review of c1e2582b)

The Bot threads 4239399740-4239399761 on PR 316 were not read: GitHub is unreachable from this sandbox and the task forbids an out-of-sandbox read. Each change is judged on its own mechanics against the fact sheets and the scripts; where the change names a Bot finding, the finding's substance is inferred from the change.

## Changed invariants

INV-1: accepted. The literal first segment plus the tier-by-literal-prefix rule closes allowed_files of ['*'] and friends, and binding the legacy exemption to .orchestration/tasks/ on main closes the branch-copy claim; both are mechanical in V1 and V1c. Note: the schema regex V1 chose admits a wildcard inside the first segment (scripts*); see the task-review receipt.

INV-2: accepted. Byte-for-byte sentence equality against the design read from main is what this seat has been checking by hand each round; now the regime job does it.

INV-3: accepted. previous_head carried in the ACCEPTANCE and revise.yaml, diffed by CI and cross-checked by the host gate against the previous RESULT's head in history, closes the gap round 1 named (CI cannot know the previous head). Note: INV-12 should list "a previous_head that is not the previous RESULT's head" as a gaming path; the generic clause covers its test, so this is wording, not a hole.

INV-5: accepted with one note that V2 must act on. The instruction root and the schema from main, the head as --add-dir data, closes the schema-or-AGENTS.md-on-the-audited-head path for codex. The claude fallback is not fully closed: the headless page states that bare mode "loads skills from its .claude/skills/ folder" of a directory named with --add-dir, so a head that adds or changes .claude/skills/** enters the fallback's context as skill descriptions. The runner should refuse the fallback (exit 2, blocked) when git diff --quiet origin/main <head> -- .claude/skills fails, leaving such a head to the codex path; add the page's sentence as a premise.

INV-7: rejected: the second review's alternative form contradicts the sentence. "or the Codex Bot's review of the boundary PR carrying the design" produces no receipt, no canonical hash and no AGMSG-RESULT from a Codex identity, yet the same sentence requires each receipt to be a schema document naming the hash and both RESULTs to precede the implementing TASK; the only way the Bot form satisfies that is an orchestrator-written receipt for a review it did not perform, which is R5. Right: the Codex review is codex exec --sandbox read-only on the review profile under a codex-review identity (headless, V4's runner, or a seated one until V4), its receipt and RESULT like the Claude one; the Bot's PR review stays what it is, swept feedback. Second gap: the enforcement row (line 153) and V4 (line 172) still describe one -review- identity and one receipt; name the Codex form in both and the gate rule "two RESULTs, one from a Claude -review- identity and one from a Codex -review- identity, both naming the current hash". The round-6 Codex receipt in flight (…-round6-codex.md) is the right shape for this.

INV-12: accepted; the four new gaming paths match INV-1, INV-2 and INV-5 as changed.

INV-4, INV-6, INV-8, INV-9, INV-10, INV-11: unchanged, accepted.

Stage-0 row (line 133) matches INV-7's two reviews; section 10 records rounds 2 to 5 correctly.

Design verdict: revise
