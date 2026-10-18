---
task_id: dotfiles-T133-dispositions-a01
round: 1
---

# Learning

Task-local triage; nothing promoted.

- On PR #409, "the newest commit touching the thread's hunk" and "the commit that fixed the finding" differ for one of two threads: a later commit (492e7e28) inserted lines inside the hunk the fix (99b07d2b) had changed. A machine proposal is therefore a candidate, never a disposition. Applies to item (16), the second opinion that confirms proposals: it should compare the proposal with the commit message and the finding, not only the hunk.
- When a gate wrapper keeps a private PATH, any tool that step runs inherits its limits. Here `uv` is absent, so a `test:` refutation run from the gate falls back to the wrapper's own interpreter, and an https fetch loses the proxy variables `env -i` drops. Applies to every step added to `orch-gate.sh`: state what the step can reach under `env -i` before relying on it.
- A new refutation form had to fit an existing grammar the gate enforces (`; evidence=` exactly once) without editing the gate. Putting the form in the evidence payload kept every record valid for the unchanged gate and made "legacy" a classification instead of a parse failure.
- Before pushing a change to a script, run every test module that drives it (`git grep -l <script> -- tests`), not only the ones in `allowed_files`. Here `test_orchestrator_tools.py` used "the interpreter never ran" as its proof that "the gate never ran", and a new step that reused the interpreter broke that proxy on CI. A step added to a wrapper belongs where the task's premise puts it (here right before the gate), which kept that proxy true.
- Revise 1: a refutation must be verified where the claim lives. A test run on the trusted checkout tests the code before the regression, and a run of the head's code on the orchestrator's host crosses the trust boundary. The head's own CI log is the only place a test: claim about the head can be checked, and only an executed `... ok` line counts. Applies to item (16) and to any gate step that weighs a worker's evidence.
- Revise 1: a form whose input the caller chooses proves what the caller wants (`diff:<head>..<head>`). Fix the input in the tool, compare the caller's against it, and record a form that cannot prove reachability as a claim. Applies to every evidence form.
