# T87 Validation

## UA incremental update

- Source baseline: `607e6dc61e20075eb2e560b922d6cdcfae831fb2`.
- Current post-#147 HEAD: `d91b835021981a2fb604c61e2ef324f972cc8795`.
- Changed paths: `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`.
- Decision: partial update; both paths classified structural.
- Replaced nodes: 3; fresh nodes: 3; node IDs unchanged.
- Official UA validation: success. The two auto-corrected fields are pre-existing baseline issues with exact issue parity.
- Independent checks: 1,201 unique nodes, 934 unique edges, 0 dangling edges, 737 unique layer assignments, valid tour references.
- Unchanged nodes, all edges, layers, and tour are JSON-identical to the baseline.
- Fingerprint store: 722 entries in the nested `files` envelope; extensionless shell remains conservative and Python retains structural analysis.
- `git diff --check`: pass.

## Pull-request scope and CI

- PR A #150, `git show --stat`: `.ua/fingerprints.json`, `.ua/knowledge-graph.json`, `.ua/meta.json`, and 13 `.orchestration/**` audit/artifact files only; initial commit `b6407b2` is 16 files, 443 insertions, 16 deletions. The follow-up changes only T87 report/validation/autoskill artifacts.
- PR B #148, `git show --stat a4417ab`: exactly `home/dot_agents/skills/agmsg/templates/cmd.claude-code.md`; 1 file, 185 insertions, 11 deletions.
- PR C #149, `git show --stat origin/main..HEAD`: all three same-class commits touch exactly `home/dot_mise/config.toml` and `home/dot_mise/mise.lock`; no third path.
- Final `gh pr checks 148`: all required checks pass (`nix` skipped by design).
- Final `gh pr checks 149`: all required checks pass (`nix` skipped by design).
- Final `gh pr checks 150`: all required checks pass (`nix` skipped by design).
- No PR was merged or force-pushed. PR C's two CI-pin corrections remain same-class follow-ups and will squash to one class commit under the repository convention.

## Boundary status

- `git status --short .orchestration`: empty.
- `git ls-files --others --exclude-standard .orchestration`: empty.
- The eight canonical-checkout tail files were removed only after commit `b6407b2` was pushed; they remain recoverable from PR #150.
