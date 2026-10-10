# Learning: dotfiles-T124-wave1-task-validator-a01

1. [memory:failure] A shared module that the gate will import must not need a dependency the gate runs without. PyYAML is missing under `make unit-test` and the gate's `python3`, so the task front matter is read by a strict subset parser. It refuses what it cannot read exactly, so it can never silently disagree with PyYAML.
2. [memory:failure] A prose budget test can make a required rule line not fit. Measure the budget first (`test_word_budgets`; the rule had 3 words of room), then fold the line into the closest bullet and make cuts that keep the meaning, avoiding phrases a test pins.
3. [memory:failure] A command string pinned by a parity test (`test_pr_feedback`, step 10's gate command) can keep working while the command gains a variable: GNU make takes `-C <dir>` after the target. Run the whole suite before claiming that a prose-only change is safe.
4. [memory:success] A rule's test should prove it pins the rule: removing each rule in a scratch worktree and watching its test fail found no unpinned rule among twenty.

5. [memory:failure] A push that lands before the Bot has reviewed the previous head hides that review: wait for the Bot on each head, or recheck all Bot threads against the RESULT's list before every push, not only at the end.
6. [memory:failure] Tightening a security parser rule by rule under a reviewer bot never converges: each new rule (receipt binding, scope binding, tiers) opens the next finding. Bot findings on eight consecutive pre-RESULT heads are the T119 pattern the T124 design itself names. Send the RESULT with the open findings named when the rounds stop shrinking.
7. [memory:failure] Read the inbox between questions: Amendment 2 sat unread for 40 minutes while I worked on other findings.

8. [memory:failure] A timing test (an elapsed-time bound) fails under machine load in this sandbox: before reading such a failure as a regression, rerun it alternately at the head and the base. Here the head failed 3 of 3 at a load spike and then passed 2 of 2, as the base did.

Rule candidates written: none (`learning/rule_candidates/` untouched).
