---
task: dotfiles-T133-ci-efficiency-a02
head: 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719
pr: 409
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
started: 2026-10-18T13:17:33Z
finished: 2026-10-18T13:23:57Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Decode Git-quoted filenames before filtering bootstrap paths — .github/workflows/remote.yaml:77-78
- [P2] Run registry validation for flakes.yaml-only changes — .github/workflows/test.yaml:113-115

```text
The path gates can report success without validating registry-only changes or Git-quoted bootstrap inputs. Seventeen read-only checks passed; fixture-based tests were blocked by the sandbox.

Full review comments:

- [P2] Run registry validation for flakes.yaml-only changes — .github/workflows/test.yaml:113-115
  When a PR changes only `.github/flakes.yaml`, this expression matches nothing, so every unit-test job skips execution. The agent-assets workflow does not validate this registry either. Invalid or overly broad edits to an existing signature can therefore bypass the new production-registry test and merge with green checks. Include the registry in the relevant paths and test a registry-only diff so its declared `closed` control is enforced ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Decode Git-quoted filenames before filtering bootstrap paths — .github/workflows/remote.yaml:77-78
  For a PR changing only a bootstrap input containing a double quote, backslash, tab, or newline, Git still C-quotes the filename despite `core.quotePath=false`. For example, a script named `home/.chezmoiscripts/run_after_check".sh` is reported with a leading double quote and matches none of these prefixes. All public-bootstrap checks consequently succeed without executing it; the previous exclusion-only gate did run such changes. Parse NUL-delimited paths or decode Git's quoting, and cover this case in the bootstrap control ([AGENTS.md:78](AGENTS.md#L78)).
The path gates can report success without validating registry-only changes or Git-quoted bootstrap inputs. Seventeen read-only checks passed; fixture-based tests were blocked by the sandbox.

Full review comments:

- [P2] Run registry validation for flakes.yaml-only changes — .github/workflows/test.yaml:113-115
  When a PR changes only `.github/flakes.yaml`, this expression matches nothing, so every unit-test job skips execution. The agent-assets workflow does not validate this registry either. Invalid or overly broad edits to an existing signature can therefore bypass the new production-registry test and merge with green checks. Include the registry in the relevant paths and test a registry-only diff so its declared `closed` control is enforced ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Decode Git-quoted filenames before filtering bootstrap paths — .github/workflows/remote.yaml:77-78
  For a PR changing only a bootstrap input containing a double quote, backslash, tab, or newline, Git still C-quotes the filename despite `core.quotePath=false`. For example, a script named `home/.chezmoiscripts/run_after_check".sh` is reported with a leading double quote and matches none of these prefixes. All public-bootstrap checks consequently succeed without executing it; the previous exclusion-only gate did run such changes. Parse NUL-delimited paths or decode Git's quoting, and cover this case in the bootstrap control ([AGENTS.md:78](AGENTS.md#L78)).
```
