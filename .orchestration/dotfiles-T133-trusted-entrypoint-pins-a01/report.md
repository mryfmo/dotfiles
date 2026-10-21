# Exact trusted-entrypoint pins

Producer: worker (Codex seat), codex-standard-dot-a012, standard profile.
Base: e042663b2d6efd9205f7d388bf881c01d3880642 (PR448; orchestrator resume2952).
Branch: tools/trusted-entrypoint-pins-a01. Local delivery head is supplied by the post-commit PONG; PR/CI/Bot are pending orchestrator transport.
Current task-copy SHA256: 70feed416161304c90552bc8f7c169868a5b00e35857947a4855c9710ba92dbc. Prior0908b8f4 bytes retained in task-before-amendment-1.md.

uv now holds0.13.1 and Node26.12.0; Python remains3.15.0. Adjacent English reasons explain both new held tools and all three trusted-entrypoint pins. Every other mise setting/tool remains unchanged. Existing supply-chain policy adds exactly node/uv to held, preserving non-held latest, exact held-set and immediate-comment requirements. Installed state is not changed; every mise consumer now keeps these uv/Node versions until the declaration is changed.

The exact-pin regression reads real TOML. The installed PermissionRequest test compares the complete rendered real-manifest command, requires exactly one group/hook, and retains permgate executable-leaf, claude argument and Codex assertions. Synthetic legacy/custom/idempotence fixtures and other generator-module AST are unchanged. The supply-chain module AST changes only its two held assignments. No new helper/dependency, generator/agent manifest/template/launcher/workflow/resolver changes.

## Validation and review

Historical pin assertion-red: one failure/zero errors before config change on ac816ebd; the new base's config is byte-identical and both prepared methods survived rebase. The independently found supply-chain P1 was reproduced before its held-map fix (one assertion failure/zero errors). Amendment1/TASK2955 then authorized the missing test and adjacent reasons. Both regressions are green afterward.

Amendment1: complete generator92/92 and supply-chain20/20 pass; render-check and Ruff format pass. Ruff check remains exit1 with the same14 baseline findings (11generator+3supply-chain), exact path/code/message/source-line multiset deltas empty. No suppressions or lint-baseline edits. Independent review context1/correction round1 verified P1 fixed and found no remaining source issue. Selected-tree assets passed (exit0, inherited regime warnings), comparison lint passed over all56 measured paths (exit0, five unchanged-file warnings), and the reviewed selected-tree gate passed (exit0). Full outputs and actual command statuses are in validation.md. Canonical privacy checks cover the final submitted records; final-head GitHub CI/Bot remain pending.

Source6/16, tests22/48; per-file numstat and complete measured record paths are in amend1-budget.json. Records are data only; timestamp plan/todo/learn worklogs and foreign untracked evidence are excluded. Selected-tree validation uses authenticated base plus exact scoped candidate bytes; canonical privacy checks cover submitted record contents. This makes no approval claim about foreign untracked evidence in the live checkout.

## Remaining authority and limits

Orchestrator (Claude seat, sandboxed Bash) owns transport/PR, final-head CI/Bot observations, feedback dispositions, task audit/security evidence and integration under D-024-36. No RESULT before final-head green CI and the bounded automatic Bot window. No @codex review, Bats locally, network, install/apply, deployment or live hook/socket execution.

Pins and tests establish declaration consistency, not installed executable identity, startup isolation or same-UID credential protection; resolver/binding follow-ups retain those responsibilities. cost: n/a.

Full staged git diff --check exits2 only for the immutable current/prior task copies' canonical EOF blank lines; their exact hashes are required. Code-only diff --check exits0. No suppression or task-byte rewrite was made. Verbatim diagnostics are in validation.md.
