---
reviewed_at: 2026-10-11T05:10:10Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-process-rules-redesign-a01
reset_of: dotfiles-T128-process-rules-a01
pr_head_read: origin/docs/regime-pattern@aeb6c5ad
verdict: redesign
---

# Redesign: the threat-table rule of dotfiles-T128-process-rules-a01 (PR 318)

Read on the PR head aeb6c5ad: the SKILL bullet (142 words, with the pattern `^(closed|residual|out-of-scope): \S` and the enumerated controls), the AGENTS.md subsection (with "a placeholder such as `none`" twice), and the two tests that pin them. The three Bot threads were not readable from this seat; their titles in the task are the input. The diagnosis stands: the bullet states a grammar in prose, and each fix (`\S`, then "not `none`" per form) named one more forbidden payload. The replacement names no forbidden payload at all. Shape becomes three rules of `schemas/task.json` in wave V1, each of which the three probes fail mechanically: an empty `closed:` names no test present in the tree; `residual: none` is shorter than the minimum the gate already uses for a reason; `out-of-scope: none` is not a task id in `implementing_tasks`. Until V1 lands, the same three rules are what the task-file review, the Bot and the auditor read against the diff, which `AGENTS.md` already asks of them.

## 1. SKILL.md, "Review and integration invariants": replace the `threat_table` bullet with this one

```markdown
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. Shape is `schemas/task.json`'s (wave V1): a `closed` selector names a test present in the PR tree, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
```

125 words against 142. No regex, no list of forbidden payloads; every sentence carries a token the test below asserts.

## 2. AGENTS.md, "### Orchestration records and trust-boundary code": replace the second bullet with this one

```markdown
- Judge from the diff, whatever the task's metadata says, whether a change touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input). Review such code against the task's `threat_table`: report a missing table or a missing row; report a `closed` row whose test does not close it, a `residual` row whose control does not mitigate the risk, and an `out-of-scope` row whose owner does not own it. Do not re-raise a `residual` row whose control mitigates the risk. Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's.
```

The first and third bullets of the subsection stay as they are.

## 3. tests/unit/test_agmsg_orchestration_docs.py: the two tests become these

```python
    def test_a_trust_boundary_task_carries_a_threat_table(self) -> None:
        text = self.invariants()
        for token in (
            "carries a `threat_table` in its front matter",
            "`closed: tests/<file>::<name>`",
            "`residual: <sentence>`",
            "`out-of-scope: <task id>`",
            "Shape is `schemas/task.json`'s",
            "Substance is the reviewers'",
            "The table is the task's completion condition",
            "a missing row is added once, counted as an amendment",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_threat_table_rule_carries_no_grammar(self) -> None:
        # The reset of PR 318: shape lives in schemas/task.json, never as a pattern in prose.
        text = self.invariants()
        self.assertNotIn("^(closed|residual|out-of-scope)", text)
        self.assertNotIn("`none`", text)
```

`test_threat_table_dispositions_carry_a_payload` is removed; the removal proof for the new negative test is the old pattern pasted back into the bullet.

## 4. What V1 implements (a note for dotfiles-T128-v1-task-schema-a01, not part of PR 318)

`schemas/task.json` gains an optional `threat_table`: an array of objects `{control: string, disposition: string}` whose `disposition` starts with one of the three forms; the validator checks the three shape rules the bullet states (the `closed` selector's file exists in the tree being validated and its name is `tests/<file>::<name>`; the `out-of-scope` id is a key of the design's `implementing_tasks`; the `residual` text after the prefix is at least 20 characters). Those are the V1 task's three sentences; the prose above does not restate them beyond naming them.

## 5. Why this closes the class

The three probes were three instances of one question, "what payload does the prose accept", and prose answers it one payload at a time. A schema answers it once, by what a payload must be rather than what it must not be, and a reviewer answers the part a schema cannot, whether the named test, control or owner is real. Nothing in the replacement invites a fourth probe of the same class; a fourth finding would have to be about substance, which is where the design wants it.
