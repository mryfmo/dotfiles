# Needs validation: dotfiles at d4046bdf99a10ac1b627ce4f4c972768e681f92e

No final `needs_validation` record exists in this run: the one candidate has not been through independent validation, so the skill keeps it out of the final records.

The candidate is `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt`, ledger unit `scripts/orchestrator/hcom-seat#seat_write_roots-dsh`. Its claim: U272's srt write root `DSH_HOME` holds `profiles/thak`, where `make update` runs `pnpm install` outside the sandbox. It is listed in `REPORT.md` section 1a, with its blockers and a local plan, for whichever independent verifier takes it.

Its blockers:
- pnpm's default `.pnpmfile.cjs` loading for the version mise provides;
- srt 0.0.81 allowing the contained session to create that file under its write root;
- the absence of an independent verifier on this seat.

The candidate is now on origin/main (U272 merged as #697), so its validation is no longer a merge gate for a branch: it is open on the default branch.
