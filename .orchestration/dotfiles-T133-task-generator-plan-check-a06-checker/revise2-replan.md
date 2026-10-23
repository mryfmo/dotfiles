# S1 final round2 re-plan

Owner2784 revises reviewed06ffefbc, final fix round2of2. Two high-confidence P2 findings: raw Unicode directory pruning skips C12 descendants (source246), and lexical-only C16 misses a literal file alias into scripts/orchestrator (source465). This is the fourth input-validation recurrence in the lineage.

## Goal
Make every task-controlled local filesystem check preserve original spelling until resolution and identity confinement; use NFC only for lexical matching and API naming.

## Scope
Only the checker, its two named test modules and this own artifact directory. No parent-execution, permission, resolver, workflow, graph, deployment or fixture-owner changes. No new runtime helper/dependency/config.

## Assumptions
Task SHA d0ad49f43aae4be0360cb88339b5d9f23e92e5588d38e3a93a3fbc58a6fe5faa and caps unchanged: production additions+deletions<=400, test additions<=700 with deletions disclosed. Baseline396 production,613 test additions22 deletions. Worker network unavailable; orchestrator transports exact local commit and owns CI/integration. Questions/amendments exhausted; cap changes require owner decision.

## Design
One record keeps original Path, confined real target, NFC lexical key and NFC real-target key. Metadata strings retain original spelling; internal enumerated Path values never grant external absolute-path syntax. Resolve using original Path, identify the containing root ancestor with samefile, then derive real-target key relative to that ancestor. Never deduplicate filesystem entries by normalized key. Directory pruning and leaf matching both normalize comparison keys, preserving enumeration identity. Literal and glob scopes use the same classification loop; directory links are yielded as unsafe and never traversed. Fixture/evidence exemptions require lexical and real containment. C16 consumes resolved target keys and keeps lexical scope applicability for nonexistent files.
Callers: C6 uses original design path for boundary and lexical key for pinned canonical API bytes; C10 script paths; C11 closed selector and owner task; C12 scopes and files; C14 authorized fixed probes. C7 lexical token existence uses the same boundary record. Host executable identity remains lower-level confined(), without task grammar. No shell startup, PATH, auth forwarding or permission defaults change.

## Tests
Before production edits add three methods: Unicode directory pruning with unnamed file and escaping link; literal fixture file alias into orchestrator; cross-consumer raw/NFC identity with valid canonical bytes and authorized premises. Each must fail old source by assertion, never error/skip. Repeat full modules315/312, required16 historical selectors, behavior mutants, source format/R4 lint, clean selected-tree assets and worker review gate. Independent read-only design support and final review evidence; no Crit browser.

## Open Questions
None. Implement once, measure. If complete pipeline exceeds400, stop and PONG exact numbers rather than remove a defense or move runtime code into artifacts.
