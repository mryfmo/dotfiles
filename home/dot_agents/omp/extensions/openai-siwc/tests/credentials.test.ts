import { Database } from "bun:sqlite";
import { afterEach, beforeEach, expect, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { countLogins } from "../src/credentials";
import { profileAgentDir } from "../src/seed";

const SCRIPT = path.join(import.meta.dir, "..", "src", "credentials.ts");
const SECRET_DATA = "fake-" + "refresh-value";

let home: string;
beforeEach(() => {
	home = fs.mkdtempSync(path.join(os.tmpdir(), "siwc-credentials-"));
});
afterEach(() => fs.rmSync(home, { recursive: true, force: true }));

function agentDb(profile: string, rows: Array<[string, string | null]>): string {
	const agentDir = profileAgentDir(profile, home);
	fs.mkdirSync(agentDir, { recursive: true });
	const db = new Database(path.join(agentDir, "agent.db"));
	db.run(
		"CREATE TABLE auth_credentials (id INTEGER PRIMARY KEY, provider TEXT NOT NULL, credential_type TEXT NOT NULL, data TEXT NOT NULL, disabled_cause TEXT, identity_key TEXT)",
	);
	for (const [provider, disabled] of rows) {
		db.run("INSERT INTO auth_credentials (provider, credential_type, data, disabled_cause) VALUES (?, 'oauth', ?, ?)", [
			provider,
			SECRET_DATA,
			disabled,
		]);
	}
	db.close();
	return agentDir;
}

function run(profile: string) {
	return Bun.spawnSync([process.execPath, SCRIPT, "--profile", profile], { env: { ...process.env, HOME: home } });
}

test("only active openai-siwc logins count", () => {
	const agentDir = agentDb("audit", [
		["openai-siwc", null],
		["openai-siwc", "revoked"],
		["anthropic", null],
	]);
	expect(countLogins(agentDir)).toBe(1);
});

test("a seeded profile whose agent.db holds no SIWC login counts zero", () => {
	expect(countLogins(agentDb("audit", [["anthropic", null]]))).toBe(0);
});

test("a missing agent.db and a database without the credential table hold no login", () => {
	const agentDir = profileAgentDir("audit", home);
	expect(countLogins(agentDir)).toBe(0);
	fs.mkdirSync(agentDir, { recursive: true });
	new Database(path.join(agentDir, "agent.db")).close();
	expect(countLogins(agentDir)).toBe(0);
});

test("an unreadable agent.db is an error, never zero", () => {
	const agentDir = profileAgentDir("audit", home);
	fs.mkdirSync(agentDir, { recursive: true });
	fs.writeFileSync(path.join(agentDir, "agent.db"), "not a database, but long enough to have a header page\n".repeat(4));
	expect(() => countLogins(agentDir)).toThrow();
	const result = run("audit");
	expect(result.exitCode).toBe(2);
	expect(result.stdout.toString()).toBe("");
	expect(result.stderr.toString()).toContain("openai-siwc credentials:");
});

test("the command prints the count and never the stored data", () => {
	agentDb("security", [["openai-siwc", null]]);
	const result = run("security");
	expect(result.exitCode).toBe(0);
	expect(result.stdout.toString()).toBe("1\n");
	expect(result.stdout.toString() + result.stderr.toString()).not.toContain(SECRET_DATA);
});

test("a bad profile name or usage exits 2", () => {
	expect(run("../x").exitCode).toBe(2);
	expect(Bun.spawnSync([process.execPath, SCRIPT]).exitCode).toBe(2);
});
