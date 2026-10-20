---
id: M-20261019-05
date: 2026-10-19
classes: [round-cap-overrun-by-decision-line, class-naming-evades-s1, text-review-unbounded]
severity: P1
---

# The pre-dispatch text review loop ran unbounded (19 rounds on one text)

**What happened.** The C-80 pre-dispatch security review of task texts was repeated as a delta loop: the P1-15 text (`dotfiles-T133-worker-write-boundary-a01`) went through 19 reviews today (6 `correct`), the P1-12 a03 text 8, the ci-efficiency a04 text 7, the verdict a04 text 6, the a07 text 4. Each round fixed only the findings of the previous one (a delta prompt to the review-profile context), and each next review surfaced the next gap of the same family (executable binding: the permgate hook under the sanitized PATH, Python isolation, the deploy check itself; consumer enumeration: validator pins, fixtures, the orchestrator modify script).

**What the rules say.** Plan 006 line 61 (A1): a design review runs 3 rounds and then freezes with a residual list; a task-file review runs one round with the stop condition. INV-6 S1: three findings of one class stop the task for a re-plan of specification, design, implementation and verification. S2: two amendments send the task to design by a context other than its author. Feedback `replan-not-patch`: at the third finding of one class, stop and re-examine the whole, write a `re-plan:` line, ask the operator once per class.

**Why the rules did not fire.**
1. The INV-6 counters count worker rounds, amendments and questions, not pre-dispatch text reviews; the text loop had no counter and no cap.
2. The orchestrator assigned a fresh free-form class slug to each finding (`hook-interpreter-binding`, `interpreter-isolation`, `checker-execution-unbound`, `input-inventory`), so no class reached three rows although the family did; the project-map update of 20:09 JST found it.
3. S2 was satisfied formally (another context wrote each amendment) while the prompt it received was a delta ("fix these findings and nothing else"), so the other context could not re-examine the whole text; the "stop" became a hand-off of the same loop.

**Proper state.**
- A text's pre-dispatch review is capped at 3 rounds per text; at the third `incorrect`, the text is re-planned as a whole (specification, design, implementation, verification, by another context given the whole history of findings, not a delta) or split, and the orchestrator writes the `re-plan:` line and puts the decision with a default in the map's decisions panel.
- Finding classes come from the vocabulary (`.orchestration/learning/classes.yaml`), never free slugs; a new class is added to the vocabulary with its family first, and the S1 count runs per family.
- `regime-counters.sh` counts `text-security` rows per text and reports S1 per family.

**Corrections.** C-92 (text-review cap and whole re-plan), C-93 (vocabulary classes and family counting; counters include text reviews). Applied from this record on: the amendment-8 review of P1-15 is the last delta round; a further binding finding splits the binding into its own task.
