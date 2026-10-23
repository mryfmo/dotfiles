// Usage: bun run gap-check.ts <bridge src dir> <omp package dir>
// Prints one row per value name the bridge imports from "@earendil-works/*" (multi-line imports included) and
// whether omp's legacy pi shim for that package exports it at runtime, then exits 1 when any is missing, so an
// omp upgrade that drops an export fails the install instead of the first omp session.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const [srcDir, ompDir] = process.argv.slice(2);
if (!srcDir || !ompDir) {
	console.error("usage: bun run gap-check.ts <bridge src dir> <omp package dir>");
	process.exit(2);
}
// omp remaps the pi-ai/compat subpath onto pi-ai (src/extensibility/plugins/legacy-pi-compat.ts, PI_SUBPATH_REMAPS).
const SHIMS: Record<string, string> = {
	"pi-ai": "legacy-pi-ai-shim.ts",
	"pi-ai/compat": "legacy-pi-ai-shim.ts",
	"pi-coding-agent": "legacy-pi-coding-agent-shim.ts",
	"pi-tui": "legacy-pi-tui-shim.ts",
};
const exported = new Map<string, Set<string>>();
for (const [pkg, shim] of Object.entries(SHIMS)) {
	exported.set(pkg, new Set(Object.keys(await import(join(ompDir, "src/extensibility", shim)))));
}

const importPattern = /import\s+(type\s+)?\{([^}]*)\}\s+from\s+"@earendil-works\/([^"]+)"/gs;
let missing = 0;
for (const file of readdirSync(srcDir).filter((name) => name.endsWith(".ts")).sort()) {
	for (const match of readFileSync(join(srcDir, file), "utf8").matchAll(importPattern)) {
		if (match[1]) continue;
		const pkg = match[3];
		for (const spec of match[2].split(",")) {
			const name = spec.trim();
			if (!name || name.startsWith("type ")) continue;
			const imported = name.split(/\s+as\s+/)[0];
			const found = exported.get(pkg)?.has(imported) ?? false;
			if (!found) missing++;
			console.log(`${pkg}\t${imported}\t${file}\t${found ? "FOUND" : "MISSING"}`);
		}
	}
}
process.exit(missing ? 1 : 0);
