# Codex audit — dot-codex-apparmor-userns-T30-a01 (commit ad5f95d)

Invocation: `codex --profile audit review --commit ad5f95d` (orchestrator, 2026-09-27, first audit-lane runs after T30 deploy).

Session header:

```
OpenAI Codex v0.157.1
--------
workdir: /home/moriya/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a0e14c-08b9-7030-88c1-18b76a70584d
--------
user
```

Findings (verbatim, deduplicated tail of the review output):

```
Skipped installations can remain permanently skipped after prerequisites become available, and the health check treats a missing sandbox dependency as optional. Both issues undermine reliable sandbox setup and diagnosis.

Full review comments:

- [P2] Retry profile installation after a skipped apply — /home/moriya/Workspace/dotfiles/home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl:3-4
  If the first `chezmoi apply` runs before bwrap is installed, the installer exits successfully without installing the profile. Because this is a `run_onchange` script whose rendered contents only depend on repository files, installing bwrap afterward does not trigger another attempt. Subsequent applies therefore leave sandboxed Codex broken, including when following doctor's suggested repair. Make skipped installations retryable or include prerequisite state in the execution trigger.

- [P2] Report missing bwrap as a required failure when Codex exists — /home/moriya/Workspace/dotfiles/scripts/check-tools.sh:188-190
  With the AppArmor restriction enabled and Codex installed, removing or never installing `/usr/bin/bwrap` only increments `optional_warnings`, allowing the tool health check to succeed despite the missing sandbox dependency. This contradicts the required failure reported when bwrap exists but cannot create namespaces. Increment `required_failures` in this branch as well so `make doctor` does not report success for an unusable sandbox.



```
