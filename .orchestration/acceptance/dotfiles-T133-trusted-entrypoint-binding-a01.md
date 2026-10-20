---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-trusted-entrypoint-binding-a01"
}
---

# Acceptance record: dotfiles-T133-trusted-entrypoint-binding-a01

The executable-binding family split out of plan 024 P1-15 by D-024-26: exact probed declarations for uv, Python and node, the bound PermissionRequest hook through the rendered absolute uv and isolated Python, the deploy-time effective-settings check, the formatter PATH; after: P1-15 and ci-efficiency-followup-a04 (the trusted interpreter resolver). Text designed by the review-profile context with probed premises (`.agents/worklog/orchestrator-glue/redesign/binding-a01.md`, prompt `binding-a01-design-prompt.md`); security: true; a Codex seat (D-024-25).

- 2026-10-19T12:02Z: design installed (`binding-a01.md`, 247 lines; premises probed; after: P1-15 and ci-efficiency-followup-a04); checker OK; C-80 first review started.
- 2026-10-19T12:06:42Z: C-80 first review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 uv's identity and containment are checked inside the checker uv launches (the parent must verify the uv binary before any exec); P2 shlex token equality loses quoting (compare the raw command against the rendered canonical form); P2 the generator probe under the base Python has no PyYAML (run it through the bound uv with the seeded private cache). Round 2 by the review-profile context (prompt `binding-a01r2-redesign-prompt.md`).
text-security:binding-r1:1	executable-binding
text-security:binding-r1:2	quoting-preservation
text-security:binding-r1:3	dependency-environment
- 2026-10-19T12:17Z: round-2 text (`binding-a01r2.md`) installed: the parent verifies the uv binary before any exec, quote-preserving command comparison, the generator probe through the bound uv with the seeded cache; checker OK; C-80 round 2 started.
- 2026-10-19T12:35:39Z: C-80 second review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the shell-form hook starts an outer shell before `env -i`, so inherited loader inputs run before the privileged parent validates anything (the hook form itself must be the trusted parent: exec form, or the managed hook command is the launcher program with no outer shell); P1 the mandatory online cache seed bypasses the bound parent (no env clearing, no `--isolated`, no verified `--python`, no `-I`). Round 3 to be written with both; the task is after P1-15 and the resolver, so it is not on the critical path.
text-security:binding-r2:1	executable-binding
text-security:binding-r2:2	executable-binding
- 2026-10-19T19:57Z: host pause 13:03Z to 19:55Z (the sandboxed send queued at 13:02 executed at 19:55); the binding text's third review (12:59Z, `…-text-security-*.md`): `Verdict: incorrect` on one P2: the positive fixture admits `sys.executable` and fallback uv installations that the pinned launcher rejects, so CI with setup-uv and no pinned mise Python cannot pass while skipping is forbidden. Three reviews consumed: C-92 re-plan.
re-plan: fixture-vs-binding (rows text-security:binding-r1:1, text-security:binding-r2:1, text-security:binding-r2:2, text-security:binding-r3:1) — specification: the text demanded one hook execution test that is both pinned-binding-faithful and runnable on runners without the pinned installation; design: the launcher trusts the manifest its parent names (a `--manifest <path>` argument under the trusted prefix), so a test passes a fixture manifest bound to the runner's real uv and python and the launcher applies every check (shape, regular file, no shims, no worker-writable roots) to those paths — not a bypass, the same code path with a different trusted input; the production manifest is the rendered one; implementation: the round-4 text states the manifest argument, the fixture manifest test on runners, and the pinned-installation test on the host only (named skip elsewhere, recorded); verification: both tests plus the launcher refusing a manifest outside the repository or the test fixture root.
text-security:binding-r3:1	fixture-vs-binding
- 2026-10-19T20:10Z: re-planned text (`binding-a01r4.md`, 417 lines: the launcher trusts the manifest its parent names with `--manifest`/`--fixture-root`, fixture manifests on runners, the pinned case on the host) installed; checker OK; C-80 (first after the re-plan) started.
- 2026-10-19T20:13:07Z: C-80 (first after the re-plan; the manifest-trusting launcher): `Verdict: correct`. The text waits for its prerequisites (P1-15 and ci-efficiency-followup-a04); a Codex seat takes it then (D-024-25).
- 2026-10-19T21:33:05Z: `after:` retargeted from the withdrawn dotfiles-T133-worker-write-boundary-a01 (PR #431 reset) to its reset successor dotfiles-T133-worker-write-boundary-a02; one line, same length, body unchanged (sha256 1cc2a02b0876… -> 2ed7e01d8239…; the C-80 verdict on the body stands); checker OK. Found by the project-map pass at 06:30 JST.
