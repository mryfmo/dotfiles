import { afterEach, beforeEach, expect, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { loadRegistration, newRegistration, registrationPath, saveRegistration } from "../src/store";

let agentDir: string;
beforeEach(() => {
	agentDir = fs.mkdtempSync(path.join(os.tmpdir(), "siwc-store-"));
});
afterEach(() => fs.rmSync(agentDir, { recursive: true, force: true }));

test("a profile without a record loads as undefined", async () => {
	expect(await loadRegistration(agentDir)).toBeUndefined();
});

test("a saved record round-trips and is private to the user", async () => {
	const record = { ...newRegistration(), clientId: "oaiapp-fake-client" };
	await saveRegistration(agentDir, record);
	expect(await loadRegistration(agentDir)).toEqual({ ...record, accountId: undefined });
	const file = registrationPath(agentDir);
	expect(fs.statSync(file).mode & 0o777).toBe(0o600);
	expect(fs.statSync(path.dirname(file)).mode & 0o777).toBe(0o700);
	expect(fs.readdirSync(path.dirname(file))).toEqual(["registration.json"]);
});

test("new host ids use the urn:uuid form the authorize endpoint requires", () => {
	expect(newRegistration().hostId).toMatch(/^urn:uuid:[0-9a-f-]{36}$/);
});

test("a record with a bare uuid host id is refused on load and on save", async () => {
	const bare = { hostId: crypto.randomUUID() };
	fs.mkdirSync(path.dirname(registrationPath(agentDir)), { recursive: true });
	fs.writeFileSync(registrationPath(agentDir), JSON.stringify(bare));
	await expect(loadRegistration(agentDir)).rejects.toThrow("invalid registration record");
	await expect(saveRegistration(agentDir, bare as never)).rejects.toThrow("invalid registration record");
});
