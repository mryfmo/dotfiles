[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:73 The marker format specifies no escaping or rejection of embedded newlines: one worker message can contain a forged acceptance row that the unchanged parsers treat as a separate event; the named history/payload tests need a reader-side framing attack.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:75 Preserving sent-row identification retains selection of the last matching sender/recipient/body rather than the sent message’s ID; two concurrent identical messages can record `read` while this send remains unread, which the prescribed roundtrip fixture does not test.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:84 The required manifest-bound store location has no declaration in `agent-config.yaml`, and neither this task nor T133 authorizes adding it; fixture-only declarations cannot establish the production binding—specify its authoritative location and authorize any required declaration with a threat row.

📝 まとめ: Reviewed all 40 threat rows and cited context; found three design gaps, with parser and receipt-selection behavior confirmed by in-memory probes. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-user isolation and deployment protections remain unverified residuals.
Verdict: incorrect