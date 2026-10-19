# Learning triage: dotfiles-T133-regime-ci-a02

These are candidates only; nothing is promoted.

1. [memory:failure] A check that is meant to become a required context must not be judged by code or policy the checked change controls.
   - Under `pull_request`, the workflow, the verifier, the checker, the task copy, `result.txt` and the branch name all belong to the PR.
   - a01 built every rule correctly on top of an untrusted base: the Bot's three P1s.
   - The pattern that holds is `pull_request_target` with `contents: read`. Check out the base sha, fetch `refs/pull/<n>/head` as data and bind it to the event's head sha, read the head only with `git show`, run only base code, and take policy only from base text.
   - Ask "who controls each input of the verdict?" before writing the first rule.
2. [memory:decision] A PR-controlled record (`result.txt`, `precheck.json`) can show consistency among the PR's own records, never authorization.
   - Name such a match "self-attested" in the output, and make the missing trusted record a warning with an operator flag that turns it into a failure.
3. [memory:decision] The first PR that adds a `pull_request_target` workflow cannot run it, because the base has none.
   - The evidence is a local run of the job's exact command line in an isolated base checkout, with the candidate verifier installed for that run only.
   - Never add a head-execution fallback to the workflow.
4. [memory:failure] Fixtures that rewrite a large file count its deletions against the caps. A "compliant" case that replaces a 400-line script with a stub exceeds a small cap; size the fixture policy's cap for the case it tests.
