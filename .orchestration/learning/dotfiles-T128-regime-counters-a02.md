# Learning triage: dotfiles-T128-regime-counters-a02

Candidates only; nothing promoted.

1. [memory:decision] A token-based reader of agmsg bodies reads the first `key=` token for every field it decides on (task_id, status, verdict, head, pr, design_sha256), never "any token equals". Notes routinely quote other messages' fields. Applies to V3a's stop-gate and gate counters.
2. [memory:failure] `uv run --with <pkg>` is not offline-safe: uv revalidates pypi's simple index after its cache window, and a sandbox blocks the fetch. Use `uv run --offline …` first, falling back online only when uv itself fails. The child must signal its answer on stdout, not via its exit code, or every "no" also triggers the fallback. Applies to any script or test that pulls PyYAML through uv, including the masker step in Worker Playbook step 5.
3. [memory:failure] jq has a builtin `has(key)` for objects: after deleting a local `def has($v)`, a leftover `has("status=blocked")` still compiles and silently tests object keys. Grep a deleted jq helper's name, including in mutation scripts.
4. Fixtures count toward INV-2's `tests/` cap. Export them projected to the fields the tests read, one object per line (`jq -c`), never pretty-printed API dumps: PR 313's comments went from 678 lines to 46.
5. A new guard can shadow an older one, so the older one's mutation survives (here the `reset_of` check shadowed the hash check). Each guard needs a case where only it holds the line.
