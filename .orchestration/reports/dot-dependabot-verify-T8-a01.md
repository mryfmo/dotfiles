# T8 Dependabot verification
status: ready_for_review
cost: n/a

## Verdicts

- [PR #155](https://github.com/mryfmo/dotfiles/pull/155), head 01c8bdd3ba593b83d2a960ebde3bcaf0c044c4c0: **safe to merge as-is**. No workflow adjustment required. Latest run [36092281398](https://github.com/mryfmo/dotfiles/actions/runs/36092281398) passes all three test jobs; their Setup uv steps each conclude success.
- [PR #125](https://github.com/mryfmo/dotfiles/pull/125), head 60c1be401180e96684903424bc4f8fc9567acd98: **safe to merge as-is on the requested static-evidence fallback**, not a claim of executed Nix compatibility. No workflow adjustment identified. Local Nix is absent; current CI explicitly skips nix. The runtime upgrade retains a residual untested risk.

## #155: actual historical failure

[memory:decision] The task premise is contradicted by the job API and logs. Run [34730808923](https://github.com/mryfmo/dotfiles/actions/runs/34730808923), head 1b1b976459e80e7025ba0f7ac535b36c356d1a33, has one failed macOS test and two cancelled Ubuntu jobs, not three PermissionError failures.

The traceback at 2026-09-13T01:33:35.068 belongs to **Smoke-test statusline tools without network**. Its source is the inline Python command in .github/workflows/test.yaml:
`python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0))'`.
Python reports **File "<string>", line 1, in <module>**, at socket.bind, with PermissionError Errno 1. It is not a frame in scripts/check-statusline-tools.py. The command runs inside an if under sandbox-exec with deny network*. Success would explicitly fail the step; denied bind is expected. The step concludes success. Shell errexit does not abort on that if condition.

The subsequent **Run shfmt** step fails on scripts/upgrade-tools.sh lines 398/417: shfmt moves `; then` from the heredoc opener to a standalone `then` after EOF. Setup uv is later and skipped on that macOS job. Ubuntu client successfully ran Setup uv before cancellation. Thus uv cache, Python directories, working directory and Python pinning cannot explain the macOS failure.

[memory:decision] Main commit [bf2110fd85debadd0a906361ed510c7fe2db6b0b](https://github.com/mryfmo/dotfiles/commit/bf2110fd85debadd0a906361ed510c7fe2db6b0b) (#158) reformats that exact heredoc and pins shfmt 3.14.1 via mise across brew/apt runners. Old run source invokes unpinned shfmt; current main uses mise x shfmt@3.14.1. The network oracle remains unchanged. The task's approximate base 5ac784a already contains bf2110f (ancestry exit 0), so it is not the failing snapshot; the actual run head was used for the comparison. That historical head used setup-uv v10.1.0, whereas the current PR proposes v10.2.0.

## setup-uv release/usage mapping

All three uses in agent-assets.yml, docs.yml and test.yaml specify only enable-cache: false and pin a full commit SHA. No manifest-file, version-file, python-version, activate-environment, cache-local-path or working-directory override. No tracked root uv.toml, pyproject.toml, uv.lock, .python-version or .tool-versions.

| Change | Effect on this repository |
|---|---|
| [v8.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v8.0.0): removes legacy custom manifest format | None: no custom manifest. |
| v8.0.0: stops major/minor tags; immutable full releases | None: PR pins c18668ad3cf93ea998bef934396af7bb5c839dc7, not a floating v10 tag. |
| [v9.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v9.0.0): prune-cache defaults false | None for Actions cache: explicitly disabled everywhere. |
| [v10.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v10.0.0): auto cache disabled for sensitive events | None: explicit false bypasses auto; current source also excludes tag pushes. |
| v10: selected .tool-versions can supply Python; paths rejected; latest-known selector | No selected version file/Python input; root files absent. Existing latest uv resolution remains. |
| v8.3 uv.lock version source; v8.1 no-project for activated venv | Neither mechanism used. |
| [v10.2.0](https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0): save-cache auto excludes merge queues | No cache saves with enable-cache false. |
| v8.2 mirror/token fixes; v10.1 NO_PROXY/checksum improvements | No new required workflow input. Network-denied smoke is an earlier separate step, not the action environment. |

Source comparison of v7.6.0 and v10.2.0 action.yml and src/utils/inputs.ts additionally shows: working-directory remains github.workspace; activate-environment remains false; both actions already use node24. getUvPythonDir preserves an existing UV_PYTHON_INSTALL_DIR, otherwise uses RUNNER_TEMP/uv-python-dir on GitHub-hosted runners in both versions. Cache directory precedence (input/config/env, then default only when enabled) remains equivalent. No directory migration or Python pinning fix is warranted. Docs and agent-assets workflows are mapped statically; the test workflow has direct latest-run execution evidence.

## #125: installer release comparison and validation limit

[Upstream comparison](https://github.com/cachix/install-nix-action/compare/v31.10.7...v31.11.1) changes the consumer install-nix.sh default from Nix **2.34.8 to 2.35.2**, plus an upstream-only CI skip for the latest installer on x86_64-darwin. Action interface and downstream flake evaluation commands are unchanged.

[v31.11.0](https://github.com/cachix/install-nix-action/releases/tag/v31.11.0) updates Nix to 2.35.1; [v31.11.1](https://github.com/cachix/install-nix-action/releases/tag/v31.11.1) updates to 2.35.2 and cites the build-crash fix for Assertion !awake.empty(). This is an installed Nix minor-version upgrade, not just an inert action metadata change.

`command -v nix` returned exit 1 with no output. Therefore no checkout worktree, local flake check or eval was performed; no Nix installation was attempted. Workflow actually has **three** nix eval commands, plus flake check, across ubuntu-latest/macOS-14, not two evals. Their unchanged definitions are pasted in validation.

Latest PR checks pass but nix is skipped in [run 36092266976](https://github.com/mryfmo/dotfiles/actions/runs/36092266976), as its path predicate requires flake.nix, flake.lock or nix/. Rerunning this run alone would not exercise the action. Cheapest permitted evidence is the inspected upstream installer/release diff plus unchanged evaluations; this is static evidence, not CI-side runtime proof. No fake lockfile change, dispatch input, or workflow trigger hack is proposed. A future genuine Nix-input change will naturally exercise the existing matrix. If runtime proof is an absolute merge gate, hold #125 until an already available Nix environment can execute the unchanged checks.

## Process and durable record

gh-first-workflow kept investigation on gh APIs/logs, agmsg-orchestration defines this evidence handoff, and Ponytail avoided unnecessary workflow edits or installing Nix. No tracked files changed, no local Bats, commits, pushes, PR writes, GitHub comments or merges.

CompactionDB command (output c14a8e35-136b-4807-b3c2-bc4f89aa1d47 appears verbatim in validation):
```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T8: setup-uv PR155 old run34730808923 failed macOS shfmt before setup-uv; PermissionError is the expected network-denial oracle. Main bf2110f fixed heredoc formatting and pinned shfmt3.14.1. Current PR155 tests pass; cache-disabled SHA-pinned usage needs no v8-v10 adjustment. PR125 only updates installed Nix2.34.8 to2.35.2; no local nix and filtered CI skipped its job, so static compatibility verdict is not runtime proof.'
```

See validation/dot-dependabot-verify-T8-a01.md for every captured investigation command/output, including the two raw-content API parse errors and successful base64-content fallback.

