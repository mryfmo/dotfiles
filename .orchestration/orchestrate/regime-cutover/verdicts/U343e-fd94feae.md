## Findings

- P1 (high) [f1 s10] scripts/orchestrator/acp-broker:1146: A worker can write task/.git/objects/info/alternates and HEAD; the unsandboxed push then reads protected Git objects and imports them into the Router repository.
- P2 (high) [f2 s6] scripts/orchestrator/acp-broker:1282: Disabling signal traps before push_back lets broker teardown kill the handler during a push without removing its slot or reporting push=skipped.
- P2 (high) [f1 s6] scripts/orchestrator/acp-broker:1188: Terminating one process group cannot end descendants that create another group or ignore SIGTERM, despite the contract's every-descendant guarantee.
- P2 (high) [f1 s7] scripts/orchestrator/acp-seat:213: If the broker connection ends before its trailer, a worker-emitted trailer-shaped final payload is accepted as a successful broker exit.
- P2 (high) [f1 s5] scripts/orchestrator/acp-broker:1284: An exit-log append failure after a successful push calls refuse, so the client receives no trailer or pushed ref although the ref was written.
- P2 (high) [f10 s2] home/dot_local/bin/common/executable_acp-broker:1: The PR threat table groups the three deployed levers and the two test files into shared rows instead of providing one row per changed path.
- P3 (high) [f1 s2] scripts/orchestrator/acp-seat:235: Python's dollar anchor accepts a terminal newline, so ref or name values ending in newline pass client validation and send an extra line.

## Reproduced

- Scratch Git reproduction of the push sequence: worker-controlled alternates and HEAD resolved a protected commit; pack-objects and index-pack imported its private.txt content into another repository.
- Pure client relay check: a stream ending in a trailer-shaped payload returned status 0 and push=none; the same line followed by payload returned status 2.
- Client regex check: REF.match('HEAD\n') and NAME.match('w1\n') both succeeded.
- git diff --check passed; the checkout remained clean at fd94feaeb19322d9f17ff99f122e7ff900e4987e.
- bash -n and shellcheck -x passed for acp-broker; Python AST parsing passed for acp-seat and acp-relay.py.
- All three deployed lever copies matched their sources byte for byte, and each source hash matched a manifest pin.
- System git failed because the active Command Line Tools path is invalid; system shasum failed because libperl is blocked in this sandbox, so the full broker test suite was not run.

## Notes

The protected-object reproduction used scratch repositories and the same Git operations as push_back; it did not access credential stores or alter the checkout.

Blocking: 1
Filed: 4
Verdict: incorrect
