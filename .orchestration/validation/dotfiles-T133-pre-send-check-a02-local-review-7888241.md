---
task: dotfiles-T133-pre-send-check-a02
head: 78882410718dff320194339e02d37fb54c2e856a
pr: 442
base: e042663b2d6efd9205f7d388bf881c01d3880642
started: 2026-10-21T04:11:42Z
finished: 2026-10-21T04:19:10Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Emit a refusal when the helper fails without producing output — scripts/orchestrator/pre-send.sh:85-87
- [P2] Recognize level-two headings beyond the literal space prefix — scripts/orchestrator/pre-send.sh:77-78
- [P2] Restrict line extraction to actual checker location records — scripts/orchestrator/pre-send.sh:33-33

```text
The preflight can leak secret fragments, incorrectly accept empty owner sections, and omit refusal diagnostics after helper failures. Read-only probes reproduced these behaviors; the full test suite was not run.

Full review comments:

- [P2] Restrict line extraction to actual checker location records — scripts/orchestrator/pre-send.sh:33-33
  With malformed YAML such as `x: [<redacted:secret-pattern>`, PyYAML quotes the source line in its diagnostic. This unanchored regex also matches the quoted token, causing output to include `123456782` as a supposed line number and exposing the secret fragment `12345678`. Extract only actual location records and reject numbers outside the task's line range. Add this case to the secret-fragment closure test required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Recognize level-two headings beyond the literal space prefix — scripts/orchestrator/pre-send.sh:77-78
  If the next acceptance-record heading is valid Markdown such as `  ## Next` or `##\tNext`, this condition leaves `inside` true. Bullets in that unrelated section then count as owner work, allowing a one-item task with an empty owner section to pass. Recognize indented, tab-separated, and empty level-two headings when ending the section, and test that subsequent rows cannot satisfy it.

- [P2] Emit a refusal when the helper fails without producing output — scripts/orchestrator/pre-send.sh:85-87
  An uncaught helper error—for example, reading an existing acceptance record without read permission—returns status 1 before the accumulated refusals are printed. This guard preserves that status without supplying a diagnostic, while stderr is discarded, leaving only the digest and no required named refusal. Treat a nonzero status with empty output as a fixed refusal and add a failure-path regression.
The preflight can leak secret fragments, incorrectly accept empty owner sections, and omit refusal diagnostics after helper failures. Read-only probes reproduced these behaviors; the full test suite was not run.

Full review comments:

- [P2] Restrict line extraction to actual checker location records — scripts/orchestrator/pre-send.sh:33-33
  With malformed YAML such as `x: [<redacted:secret-pattern>`, PyYAML quotes the source line in its diagnostic. This unanchored regex also matches the quoted token, causing output to include `123456782` as a supposed line number and exposing the secret fragment `12345678`. Extract only actual location records and reject numbers outside the task's line range. Add this case to the secret-fragment closure test required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Recognize level-two headings beyond the literal space prefix — scripts/orchestrator/pre-send.sh:77-78
  If the next acceptance-record heading is valid Markdown such as `  ## Next` or `##\tNext`, this condition leaves `inside` true. Bullets in that unrelated section then count as owner work, allowing a one-item task with an empty owner section to pass. Recognize indented, tab-separated, and empty level-two headings when ending the section, and test that subsequent rows cannot satisfy it.

- [P2] Emit a refusal when the helper fails without producing output — scripts/orchestrator/pre-send.sh:85-87
  An uncaught helper error—for example, reading an existing acceptance record without read permission—returns status 1 before the accumulated refusals are printed. This guard preserves that status without supplying a diagnostic, while stderr is discarded, leaving only the digest and no required named refusal. Treat a nonzero status with empty output as a fixed refusal and add a failure-path regression.
```
