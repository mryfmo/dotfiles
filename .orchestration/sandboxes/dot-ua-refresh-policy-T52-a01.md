# Sandbox: dot-ua-refresh-policy-T52-a01

- worker-c, branch chore/ua-refresh-policy from origin/main 0790fb74; one commit f700b14, pushed without -u.
- Unsandboxed: git fetch/switch/commit/push, gh, make unit-test/validate-agent-assets, CompactionDB memory add, writes to the main checkout .orchestration.
- The permission gate denied an empirical run of the extracted SessionStart command in a scratch copy (it executed plugin hook text and removed a temp dir); replaced by the read-only gate checks pasted in the validation file.
- No graph analysis, no plugin-cache edits, no subagents.
