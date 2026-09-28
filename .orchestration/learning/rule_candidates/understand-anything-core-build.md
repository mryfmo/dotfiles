# Rule candidate: the managed asset lifecycle installs Understand-Anything without building its core

Observed 2026-09-28 (T33c blocked PONG): the plugin's incremental update helper
`skills/understand/prepare-incremental.mjs` imports `packages/core/dist/index.js`,
but `dist/` existed neither in the Claude plugin cache
(`~/.claude/plugins/cache/understand-anything/understand-anything/2.9.7`) nor in
the Codex-side clone (`~/.understand-anything-plugin` →
`~/.understand-anything/repo/understand-anything-plugin`). `scripts/update-agent-assets.sh`
installs the plugin and the Codex installer but never runs the documented build
(`pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build`,
SKILL.md:118). `pnpm` is installed via mise but has no global default, so the
build needs `mise exec pnpm@<ver> --` or a mise config entry.

Consequence: every `.ua/` incremental update (the SessionStart/PostToolUse hook
requests) is impossible until someone builds core by hand; the orchestrator did
so once under the machine-state hygiene exemption.

Candidate fix (worker task): make `update-agent-assets.sh` build core after
installing/updating the Codex-side clone (idempotent, skip when `dist/` is newer
than `src/`), pin pnpm in the mise manifest or invoke it through `mise exec`,
and have `make doctor` WARN when `packages/core/dist` is missing.
