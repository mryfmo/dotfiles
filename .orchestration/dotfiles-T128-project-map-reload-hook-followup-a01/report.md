# RESULT report: dotfiles-T128-project-map-reload-hook-followup-a01

Branch: fix/project-map-reload-target
Base:04590ae9a032372a7eb6e06650ac96bf3eb05c67
Task-copy SHA256:b8b18a8fa0249e18d00346dfed2c87821c22d38f2de22644d0af99c1719f0ad1

## Owned rows implemented

| Owned row | Change | Test |
| --- | --- | --- |
| worker:30cbfb4:1 tab-fallback-reload | Execute reload only while location.pathname ends in /.project-map/index.html; no event string is interpolated into JavaScript. | test_project_map_reload_hook_guards_against_a_tab_navigating_away |
| local:2fb97db:1 advisory-p2 (pin the selected tab) | --pin-tab on both existing agent-browser calls; pin is active before the inter-command close window, and repeated true does not rebind the session. | test_project_map_reload_hook_pins_the_bound_tab_when_it_closes |
| audit:2fb97db:1 target-id-validation | Accept exactly32 ASCII hexadecimal characters, strictly anchored at end, rejecting operation names and trailing newlines. | test_project_map_reload_hook_accepts_only_cdp_target_ids |

The guard test executes the hook's actual JavaScript with Node against map and non-map location objects. The pin test simulates closure before eval's flag processing and persists the earlier tab call's pin state; a pin added only to eval fails this test. The identifier test rejects list/new/close, malformed length, non-hex and newline ids, and accepts uppercase/mixed-case32hex. Existing fixtures now use real-shaped ids and preserve silent success on missing/failed tools. Tests were written first and failed against the unmodified hook; a too-long positive fixture was corrected before final passing validation.

## Validation and scope

The complete generator module passes80 tests, including all six hook tests. ShellCheck, render-check, Ruff format-check and source diff-check pass. Ruff lint has11 diagnostics identical by code/location/message to the untouched base and zero new diagnostics; it is not claimed green. The new ISC004 diagnostic was fixed. Changed source lines:7 (limit200), test additions147 (limit1000;155 test changed lines).

Only home/dot_claude/hooks/executable_project-map-reload.sh and tests/unit/test_generate_agent_configs.py change outside task evidence. The other six allowed source paths need no edits or regenerated outputs. The preceding task's first-open branch is preserved; the older task's ls-only/two-agent-calls wording is read under its nothing-else-changes rule, not as authorization to remove the merged pane-open behavior. No exact event-path selection change is made; that valid advisory belongs to dotfiles-T128-project-map-pane-open-a01-followup-a01.

## User-visible effects and limits

[memory:decision] The fixed project-map-reload session is now pinned, so a closed selected tab stops reload instead of falling back. Pin is sticky in the upstream session and persisted across restarts. On a fresh CDP attach with no saved binding, upstream creates an about:blank tab before the explicit tab command switches to the existing map; this is a real additional inactive tab, not a claim that only the open branch can create one. An existing binding avoids that first-attach blank. The hook itself adds no new CLI subprocess: listing, tab, guarded eval, with the previous first-open branch intact.

This pin placement was checked against agent-browser v0.38.1's actions.rs2532-2585: lifecycle events drain before a changed pin setting; eval-only pin is too late. browser.rs958-1040 binds the current tab when pin is enabled and fails page commands while its bound target is gone. actions.rs3103-3181 restores a saved binding or creates the fresh blank under pin. Repeated true pin is unchanged; tab ref selection recovers the pinned session. References: https://github.com/vercel-labs/agent-browser/blob/v0.38.1/cli/src/native/actions.rs#L2532 and https://github.com/vercel-labs/agent-browser/blob/v0.38.1/cli/src/native/browser.rs#L958 . Installed help confirms the public flag and target-ref contract.

No real browser, tab, hook delivery, close timing or pane placement was exercised. Tests use temporary browser/agent stubs and real jq/Node. Cross-repository suffix selection and accepted duplicate panes remain separate owner work. No installed home state, dependency/lockfile, renderer/settings or permission default changed. No local bats, merge, browser Crit or Plan Mode. CompactionDB consolidation stays with orchestrator; no memory ID is claimed. Knowledge graph is stale; scoped rg used, no update.

cost: n/a

## Worker review

Crit review data was unavailable. Independent read-only review of the two source/test paths found no remaining defects in the three owned rows; resolved JSON and worker receipt are saved here. It verified the pin ordering against upstream source and the passing test logs. The source header was narrowed after review to avoid implying exact event-map identity.
