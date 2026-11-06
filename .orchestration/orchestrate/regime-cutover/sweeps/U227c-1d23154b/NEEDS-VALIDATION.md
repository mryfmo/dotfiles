# Needs validation: dotfiles at 1d23154b71932e74902cf9ac95b2eeaf7b055215

No unresolved record exists in this run, and run-6 carried none.

The brief's three questions were each settled from source:
- **The rendered rows as configuration.** They are constants and regex-checked models, and the profile is the operator's own file.
- **The symlink step.** Every input is a physical path under `DSH_HOME`; a non-symlink at the link name is refused; relinks are atomic.
- **No key or Ollama row survives.** Only the `omp-gateway` route exists, and the search found no DSH key row.

The merge-ordering note (the profile names a plugin U240 deploys) fails closed and is recorded as hardening in `REPORT.md` section 6, not as a lead. Whether U240 merges first is the coordinator's sequencing decision, not a fact outside the source.
