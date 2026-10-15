---
task: dotfiles-T128-chain-github-scripts-a01
head: d15fa8779c298a841fe2791316f022228232a402
pr: 356
base: 5ec860520075a2f0bbb551232de0f868e481a59c
started: 2026-10-14T12:34:32Z
finished: 2026-10-14T12:35:56Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Make disposition replies parseable by fill_sweep — scripts/orchestrator/resolve-threads.sh:48-52

```text
The scripts largely implement the requested workflow, but generated resolution replies are incompatible with the existing sweep parser. This can leave previously dispositioned review comments undispositioned when integration evidence is refreshed.

Review comment:

- [P2] Make disposition replies parseable by fill_sweep — scripts/orchestrator/resolve-threads.sh:48-52
  When a thread's disposition comes only from the sweep JSON rather than the TSV, regenerating the sweep after resolution loses that disposition: `fill_sweep.py` recognizes reply dispositions only when `fixed:…` or `not-applicable:…` is enclosed in backticks, but these reply bodies emit it as plain text. The original review comment then remains a gap and blocks the required integration sweep unless its row is manually recreated. Emit the disposition in the format consumed by `REPLY`, and add a round-trip test through `fill_sweep.py`; this supports the integration requirement in [AGENTS.md:75-78](AGENTS.md#L75-L78).
The scripts largely implement the requested workflow, but generated resolution replies are incompatible with the existing sweep parser. This can leave previously dispositioned review comments undispositioned when integration evidence is refreshed.

Review comment:

- [P2] Make disposition replies parseable by fill_sweep — scripts/orchestrator/resolve-threads.sh:48-52
  When a thread's disposition comes only from the sweep JSON rather than the TSV, regenerating the sweep after resolution loses that disposition: `fill_sweep.py` recognizes reply dispositions only when `fixed:…` or `not-applicable:…` is enclosed in backticks, but these reply bodies emit it as plain text. The original review comment then remains a gap and blocks the required integration sweep unless its row is manually recreated. Emit the disposition in the format consumed by `REPLY`, and add a round-trip test through `fill_sweep.py`; this supports the integration requirement in [AGENTS.md:75-78](AGENTS.md#L75-L78).
```
