/**
 * `bun src/credentials.ts --profile <profile>`: print how many active `openai-siwc` logins the profile's
 * `agent.db` holds, as one number. `seat-login-preflight` uses it to decide whether a seat can start: a
 * registration record with an issued client proves only that a sign-in began (`oauth.ts` saves the
 * client before the token exchange), and an `agent.db` exists for any profile omp has opened.
 *
 * The count reads the `provider` and `disabled_cause` columns only, never `data`, which holds the tokens.
 * The database is opened read-only. A missing `agent.db` or a database without the credential table holds
 * no login and prints 0. Any other failure exits 2 and names the file, so a failed read is never taken
 * for an absent login.
 */
import { Database } from "bun:sqlite";
import * as fs from "node:fs";
import * as path from "node:path";
import { PROVIDER } from "./index";
import { profileAgentDir } from "./seed";

export function countLogins(agentDir: string): number {
	const file = path.join(agentDir, "agent.db");
	if (!fs.existsSync(file)) return 0;
	const db = new Database(file, { readonly: true });
	try {
		const table = db.query("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'auth_credentials'").get();
		if (table === null) return 0;
		const row = db
			.query("SELECT count(*) AS n FROM auth_credentials WHERE provider = ? AND disabled_cause IS NULL")
			.get(PROVIDER) as { n: number };
		return row.n;
	} finally {
		db.close();
	}
}

if (import.meta.main) {
	const argv = process.argv.slice(2);
	const profile = argv.length === 2 && argv[0] === "--profile" ? argv[1] : undefined;
	try {
		if (profile === undefined) throw new Error("usage: bun src/credentials.ts --profile <profile>");
		process.stdout.write(`${countLogins(profileAgentDir(profile))}\n`);
	} catch (error) {
		process.stderr.write(`openai-siwc credentials: ${(error as Error).message}\n`);
		process.exit(2);
	}
}
