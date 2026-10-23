import { afterEach, beforeEach, expect, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type { OAuthLoginCallbacks } from "@oh-my-pi/pi-ai";
import { createCallbackReceiver, createSiwcOAuth, listenLoopback, type Listen } from "../src/oauth";
import { loadRegistration, registrationPath } from "../src/store";
import { FakeAuthServer } from "./fake-auth-server";

let agentDir: string;
let server: FakeAuthServer;
let closed: number;
let handle: ((request: Request) => Response) | undefined;
let callbackPages: number[];

// Stands in for the 127.0.0.1 listener: the fake browser calls the handler directly.
const listen: Listen = h => {
	handle = h;
	return { redirectUri: "http://127.0.0.1:1455/auth/callback", close: () => void closed++ };
};

const browser = (): OAuthLoginCallbacks => ({
	onAuth: ({ url }) => {
		const response = server.authorize(url, request => (handle as (r: Request) => Response)(request));
		callbackPages.push(response.status);
	},
	onPrompt: async () => {
		throw new Error("the SIWC login never prompts");
	},
});

beforeEach(() => {
	agentDir = fs.mkdtempSync(path.join(os.tmpdir(), "siwc-oauth-"));
	server = new FakeAuthServer();
	closed = 0;
	callbackPages = [];
});
afterEach(() => fs.rmSync(agentDir, { recursive: true, force: true }));

const oauth = (now = () => 1_000_000) => createSiwcOAuth({ agentDir, agentName: "omp-test", fetch: server.fetch, listen, now });

test("first login registers through dynamic_agent_client and exchanges the code with PKCE", async () => {
	const credentials = await oauth().login(browser());

	expect(server.registrations).toHaveLength(1);
	const [authorize] = server.authorizeRequests;
	expect(authorize.get("client_id")).toBe("dynamic_agent_client");
	expect(authorize.get("agent_name_hint")).toBe("omp-test");
	const saved = await loadRegistration(agentDir);
	expect(saved?.hostId).toBe(server.registrations[0].hostId);
	expect(saved?.clientId).toBe(server.registrations[0].clientId);
	expect(saved?.accountId).toBe("acct-fake");

	const [exchange] = server.tokenRequests;
	expect(exchange.get("grant_type")).toBe("authorization_code");
	expect(exchange.get("client_id")).toBe(saved?.clientId);
	expect(exchange.has("client_secret")).toBe(false);
	expect(credentials.expires).toBe(1_000_000 + 3600 * 1000);
	expect(credentials.access.startsWith("fake-access-")).toBe(true);
	expect(credentials.email).toBe("user@example.invalid");
	expect(callbackPages).toEqual([200]);
	expect(closed).toBe(1);
	const written = fs.readFileSync(registrationPath(agentDir), "utf8");
	expect(written).not.toContain(credentials.access);
	expect(written).not.toContain(credentials.refresh);
	expect(fs.readdirSync(path.dirname(registrationPath(agentDir)))).toEqual(["registration.json"]);
});

test("a later login reuses the issued client_id and host id and registers nothing new", async () => {
	await oauth().login(browser());
	const first = await loadRegistration(agentDir);
	await oauth().login(browser());

	expect(server.registrations).toHaveLength(1);
	const second = server.authorizeRequests[1];
	expect(second.get("client_id")).toBe(first?.clientId);
	expect(second.get("ext_agent_host_id")).toBe(first?.hostId);
	expect(second.has("agent_name_hint")).toBe(false);
	expect(await loadRegistration(agentDir)).toEqual(first);
});

test("refresh rotates the refresh token with the saved client_id and resource", async () => {
	const login = await oauth().login(browser());
	const first = await oauth(() => 2_000_000).refreshToken(login);
	const second = await oauth(() => 3_000_000).refreshToken(first);

	const refreshes = server.tokenRequests.filter(form => form.get("grant_type") === "refresh_token");
	const clientId = (await loadRegistration(agentDir))?.clientId;
	expect(refreshes.map(form => form.get("client_id"))).toEqual([clientId, clientId]);
	expect(refreshes[0].get("refresh_token")).toBe(login.refresh);
	expect(refreshes[1].get("refresh_token")).toBe(first.refresh);
	expect(first.refresh).not.toBe(login.refresh);
	expect(second.expires).toBe(3_000_000 + 3600 * 1000);
	// The fake server, like the real one, accepts each refresh token once.
	await expect(oauth().refreshToken(login)).rejects.toThrow("refresh_token failed: 400 invalid_grant");
});

test("refresh without a registration record tells the operator to log in", async () => {
	await expect(oauth().refreshToken({ access: "a", refresh: "r", expires: 0 })).rejects.toThrow("run /login openai-siwc");
});

test("a grant without chatgpt.tokens.use.direct is refused", async () => {
	server.grantedScope = "openid profile email offline_access";
	await expect(oauth().login(browser())).rejects.toThrow("lacks chatgpt.tokens.use.direct");
});

test("the callback receiver ignores foreign state and ends on our state", async () => {
	const receiver = createCallbackReceiver("our-state");
	const at = (query: string) => receiver.handle(new Request(`http://127.0.0.1:1455/auth/callback?${query}`));
	expect(receiver.handle(new Request("http://127.0.0.1:1455/other")).status).toBe(404);
	expect(at("state=forged&code=x").status).toBe(400);
	expect(at("state=our-state&code=c1&client_id=oaiapp-fake").status).toBe(200);
	expect(at("state=our-state&code=c2").status).toBe(400);
	expect(await receiver.result).toEqual({ code: "c1", clientId: "oaiapp-fake", scope: undefined });

	const denied = createCallbackReceiver("s");
	denied.handle(new Request("http://127.0.0.1:1455/auth/callback?state=s&error=access_denied"));
	await expect(denied.result).rejects.toThrow("authorization failed: access_denied");
});

test("login honours cancellation while waiting for the browser", async () => {
	const controller = new AbortController();
	const pending = oauth().login({ ...browser(), onAuth: () => controller.abort("user pressed escape"), signal: controller.signal });
	await expect(pending).rejects.toThrow("cancelled or timed out");
	expect(closed).toBe(1);
});

const canBindLoopback = (() => {
	try {
		Bun.serve({ hostname: "127.0.0.1", port: 0, fetch: () => new Response() }).stop(true);
		return true;
	} catch {
		return false;
	}
})();
if (!canBindLoopback) console.warn("SKIP loopback bind test: this sandbox refuses binding 127.0.0.1");

test.skipIf(!canBindLoopback)("the loopback listener binds 127.0.0.1 and serves the callback path", async () => {
	const receiver = createCallbackReceiver("s");
	const loopback = listenLoopback(receiver.handle, 0);
	try {
		expect(loopback.redirectUri).toMatch(/^http:\/\/127\.0\.0\.1:\d+\/auth\/callback$/);
		const response = await fetch(`${loopback.redirectUri}?state=s&code=c`);
		expect(response.status).toBe(200);
		expect((await receiver.result).code).toBe("c");
	} finally {
		loopback.close();
	}
});
