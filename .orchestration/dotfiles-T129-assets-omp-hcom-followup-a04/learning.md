# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a04

These are candidates only; nothing is promoted.

1. [memory:decision] A fix for the sandbox's temporary-directory refusal can be pinned without a hook in the script. Set `TMPDIR` to a directory inside the test's home, and assert on a path the script already exposes: here, the `-o` argument the fixture `curl` logs. The download directory is its parent.
   - The assertion lists the paths. When `mktemp` fails and `curl` never runs, the test fails by assertion (`[] != [tmp]`), never by an index error.
2. [memory:failure] macOS `mktemp -d` without a template ignores `TMPDIR`: at `725b25bf`, with `TMPDIR` set, it still chose the per-user default. GNU `mktemp` honours `TMPDIR`, but names the directory `tmp.*`.
   - Asserting on the template's own prefix (`update-agent-assets.`) as well as the parent makes the test red on both platforms. The pre-push review showed this with a GNU-style shim.
   - The worker's draft had claimed Linux would pass the old code. Prove a platform claim, do not infer it.
3. [memory:decision] When a revise line's `check=` carries prose, the owner task's `revise.yaml` names the test it adds as the round's selector, and says so in a comment. Otherwise the record would point at no test.
