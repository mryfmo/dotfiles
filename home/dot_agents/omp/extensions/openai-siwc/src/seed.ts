/**
 * `bun src/seed.ts --profile <profile> --client-id <id>`: write a registration record that reuses an
 * already issued `client_id` with a fresh host id, so a second host (the Ubuntu seat host) signs in as
 * its own agent host under the same client, and the returning sign-in skips the naming step. SIWC
 * allows one issued client for several hosts, each with its own host id; a refresh token is never
 * shared, so this record carries no token and the host still signs in once (docs/remote-host-logins.md).
 *
 * The record lives where omp's agent dir for the profile is (`~/.omp/profiles/<profile>/agent`, or
 * `~/.omp/agent` for `--profile default`). An existing record is never replaced: it may belong to a
 * live session, so seeding refuses and names the file.
 */
import * as os from "node:os";
import * as path from "node:path";
import { loadRegistration, newRegistration, registrationPath, saveRegistration } from "./store";

// The client ids the authorize callback issued so far are plain tokens; anything else is a typo.
const CLIENT_ID = /^[A-Za-z0-9_.:-]{1,200}$/;
const PROFILE = /^[a-z0-9][a-z0-9_-]{0,63}$/;

export function profileAgentDir(profile: string, home: string = os.homedir()): string {
	if (!PROFILE.test(profile)) throw new Error(`openai-siwc seed: invalid profile name ${JSON.stringify(profile)}`);
	return profile === "default" ? path.join(home, ".omp", "agent") : path.join(home, ".omp", "profiles", profile, "agent");
}

/** Writes the seeded record and returns its path; refuses an existing record. */
export async function seedRegistration(agentDir: string, clientId: string): Promise<string> {
	if (!CLIENT_ID.test(clientId)) throw new Error(`openai-siwc seed: invalid client id ${JSON.stringify(clientId)}`);
	const file = registrationPath(agentDir);
	// loadRegistration throws on an unreadable or invalid record, which must stop the seed too.
	if (await loadRegistration(agentDir)) {
		throw new Error(`openai-siwc seed: ${file} already exists; it is never replaced (move it aside first if it is stale)`);
	}
	await saveRegistration(agentDir, { ...newRegistration(), clientId });
	return file;
}

function parseArgs(argv: string[]): { profile: string; clientId: string } {
	let profile: string | undefined;
	let clientId: string | undefined;
	for (let i = 0; i < argv.length; i += 1) {
		const flag = argv[i];
		const value = argv[i + 1];
		if ((flag === "--profile" || flag === "--client-id") && value !== undefined) {
			if (flag === "--profile") profile = value;
			else clientId = value;
			i += 1;
		} else {
			throw new Error(`openai-siwc seed: unexpected argument ${JSON.stringify(flag)}`);
		}
	}
	if (!profile || !clientId) throw new Error("usage: bun src/seed.ts --profile <profile> --client-id <issued client id>");
	return { profile, clientId };
}

if (import.meta.main) {
	try {
		const { profile, clientId } = parseArgs(process.argv.slice(2));
		const file = await seedRegistration(profileAgentDir(profile), clientId);
		const record = await loadRegistration(path.dirname(path.dirname(file)));
		process.stdout.write(`seeded ${file} (host ${record?.hostId}, client ${record?.clientId})\n`);
	} catch (error) {
		process.stderr.write(`${(error as Error).message}\n`);
		process.exit(2);
	}
}
