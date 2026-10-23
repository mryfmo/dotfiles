import * as fs from "node:fs/promises";
import * as path from "node:path";

/** One registration per omp profile; tokens live in omp's own `agent.db`, never here. */
export interface Registration {
	hostId: `urn:uuid:${string}`;
	/** Issued by the first authorize callback; absent until registration completes. */
	clientId?: string;
	accountId?: string;
}

// The authorize endpoint refused a bare uuid with `param: ext_agent_host_id` (pilot facts #S0 run 1).
const HOST_ID = /^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

export function registrationPath(agentDir: string): string {
	return path.join(agentDir, "openai-siwc", "registration.json");
}

export function newRegistration(): Registration {
	return { hostId: `urn:uuid:${crypto.randomUUID()}` };
}

export async function loadRegistration(agentDir: string): Promise<Registration | undefined> {
	const file = registrationPath(agentDir);
	let text: string;
	try {
		text = await fs.readFile(file, "utf8");
	} catch (error) {
		if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
		throw error;
	}
	const raw: unknown = JSON.parse(text);
	if (!isRegistration(raw)) throw new Error(`openai-siwc: invalid registration record at ${file}`);
	return { hostId: raw.hostId, clientId: raw.clientId, accountId: raw.accountId };
}

/** Atomic write with 0600 file and 0700 directory, so a crash never leaves a half-written record. */
export async function saveRegistration(agentDir: string, registration: Registration): Promise<void> {
	if (!isRegistration(registration)) throw new Error("openai-siwc: refusing to save an invalid registration record");
	const file = registrationPath(agentDir);
	await fs.mkdir(path.dirname(file), { recursive: true, mode: 0o700 });
	const temp = `${file}.${process.pid}.${Date.now()}.tmp`;
	await fs.writeFile(temp, `${JSON.stringify(registration, null, 2)}\n`, { mode: 0o600 });
	await fs.chmod(temp, 0o600);
	await fs.rename(temp, file);
}

function isRegistration(value: unknown): value is Registration {
	if (typeof value !== "object" || value === null) return false;
	const record = value as Record<string, unknown>;
	const optionalString = (key: string) => record[key] === undefined || (typeof record[key] === "string" && record[key] !== "");
	return typeof record.hostId === "string" && HOST_ID.test(record.hostId) && optionalString("clientId") && optionalString("accountId");
}
