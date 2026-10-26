[P2] high implementation `install/ubuntu/client/ghostty.sh:55` — Filtering only `Failed to fetch` lines hides other fatal errors: a PPA warning plus a failing apt post-update hook becomes status 75, then installer success, violating Item 1’s requirement to preserve non-PPA failures. [APT source](https://github.com/Debian/apt/blob/main/apt-pkg/update.cc).

[P2] high specification `.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md:61` — Amendment 3 prescribes skipping on `dpkg -s` success, which proves a status record exists, not that installation completed; the implementation at `install/ubuntu/client/ghostty.sh:67` reproduced exit 0 without repair for a half-configured package. [dpkg documentation](https://manpages.debian.org/trixie/dpkg/dpkg-query.1.en.html).

[P2] high evidence `.orchestration/dotfiles-T133-install-ppa-resilience-a01/validation.md:14` — The claimed verbatim command contains a placeholder grep expression that cannot produce the pasted output; lines 146 and 153 also substitute prose for executable commands, leaving amendment 3’s evidence correction incomplete.

[P2] high orchestration `.orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md:65` — The non-fetch-error defect is deferred to an owner stub despite being a small fix within `allowed_files`; only one revise is recorded and no exhausted limit is established, contrary to Playbook step 10’s required in-scope revise path.

No `INV-n` declarations or design-invariant reference appear in the task; there are no declared invariant rows to enumerate.

Orchestration findings: 2 (task specification and acceptance disposition).

[PR 454](https://github.com/mryfmo/dotfiles/pull/454): all 12 final-head checks passed; task-copy hash matches; changes remain within both caps.

Not checked: local Bats, live Ubuntu installation, or unavailable CI log/annotation bodies. Nothing modified; false-success installation paths remain.
Verdict: incorrect