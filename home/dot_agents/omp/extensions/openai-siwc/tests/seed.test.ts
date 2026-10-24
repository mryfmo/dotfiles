import { afterEach, beforeEach, expect, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { profileAgentDir, seedRegistration } from "../src/seed";
import { loadRegistration, registrationPath, saveRegistration } from "../src/store";

let home: string;
beforeEach(() => {
	home = fs.mkdtempSync(path.join(os.tmpdir(), "siwc-seed-"));
});
afterEach(() => fs.rmSync(home, { recursive: true, force: true }));

const HOST_ID = /^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

test("a seeded record carries the given client id and a fresh urn:uuid host id", async () => {
	const first = profileAgentDir("audit", home);
	const second = profileAgentDir("security", home);
	await seedRegistration(first, "oaiapp_fake_client");
	await seedRegistration(second, "oaiapp_fake_client");
	const a = await loadRegistration(first);
	const b = await loadRegistration(second);
	expect(a?.clientId).toBe("oaiapp_fake_client");
	expect(a?.hostId).toMatch(HOST_ID);
	expect(b?.hostId).toMatch(HOST_ID);
	expect(a?.hostId).not.toBe(b?.hostId);
	expect(fs.statSync(registrationPath(first)).mode & 0o777).toBe(0o600);
	expect(path.relative(home, first)).toBe(path.join(".omp", "profiles", "audit", "agent"));
	expect(path.relative(home, profileAgentDir("default", home))).toBe(path.join(".omp", "agent"));
});

test("an existing record is never replaced", async () => {
	const agentDir = profileAgentDir("audit", home);
	const live = { hostId: "urn:uuid:11111111-1111-4111-8111-111111111111" as const, clientId: "oaiapp_live" };
	await saveRegistration(agentDir, live);
	const before = fs.readFileSync(registrationPath(agentDir), "utf8");
	await expect(seedRegistration(agentDir, "oaiapp_other")).rejects.toThrow("already exists; it is never replaced");
	expect(fs.readFileSync(registrationPath(agentDir), "utf8")).toBe(before);
});

test("an unreadable record stops the seed instead of being overwritten", async () => {
	const agentDir = profileAgentDir("audit", home);
	fs.mkdirSync(path.dirname(registrationPath(agentDir)), { recursive: true });
	fs.writeFileSync(registrationPath(agentDir), "{ not json");
	await expect(seedRegistration(agentDir, "oaiapp_fake_client")).rejects.toThrow();
	expect(fs.readFileSync(registrationPath(agentDir), "utf8")).toBe("{ not json");
});

test("a malformed client id or profile name is refused", async () => {
	for (const clientId of ["", "has space", "x".repeat(201), "semi;colon"]) {
		await expect(seedRegistration(profileAgentDir("audit", home), clientId)).rejects.toThrow("invalid client id");
	}
	for (const profile of ["../audit", "Audit", ""]) {
		expect(() => profileAgentDir(profile, home)).toThrow("invalid profile name");
	}
});

test("the CLI seeds the profile's record under HOME and exits 2 on a refusal", async () => {
	const run = (...args: string[]) =>
		Bun.spawnSync([process.execPath, path.join(import.meta.dir, "../src/seed.ts"), ...args], { env: { ...process.env, HOME: home } });
	const ok = run("--profile", "audit", "--client-id", "oaiapp_fake_client");
	expect(ok.exitCode).toBe(0);
	const file = registrationPath(profileAgentDir("audit", home));
	expect(ok.stdout.toString()).toBe(`seeded ${file} (host ${(await loadRegistration(path.dirname(path.dirname(file))))?.hostId}, client oaiapp_fake_client)\n`);
	const again = run("--profile", "audit", "--client-id", "oaiapp_fake_client");
	expect(again.exitCode).toBe(2);
	expect(again.stderr.toString()).toContain("already exists");
	expect(run("--profile", "audit").exitCode).toBe(2);
});
