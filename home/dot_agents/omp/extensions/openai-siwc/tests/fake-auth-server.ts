import { expect } from "bun:test";
import { AUTHORIZE_URL, RESOURCE, TOKEN_URL } from "../src/oauth";

const fake = (label: string) => `fake-${label}-${crypto.randomUUID().slice(0, 8)}`;
const jwt = (claims: object) =>
	["e30", Buffer.from(JSON.stringify(claims)).toString("base64url"), "sig"].join(".");

interface PendingCode {
	clientId: string;
	challenge: string;
	redirectUri: string;
	nonce: string;
}

/**
 * Fake auth.openai.com: an authorize step (the "browser") plus a token endpoint with
 * PKCE checking, dynamic registration and single-use rotating refresh tokens.
 */
export class FakeAuthServer {
	registrations: { clientId: string; hostId: string; agentName: string }[] = [];
	authorizeRequests: URLSearchParams[] = [];
	tokenRequests: URLSearchParams[] = [];
	grantedScope = "chatgpt.tokens.use.direct email offline_access openid profile resource.invoke";
	#codes = new Map<string, PendingCode>();
	#liveRefresh = new Map<string, string>();

	/** The browser: validates the authorize URL, registers on first use, then calls the loopback. */
	authorize(url: string, deliver: (request: Request) => Response): Response {
		const parsed = new URL(url);
		expect(`${parsed.origin}${parsed.pathname}`).toBe(AUTHORIZE_URL);
		const q = parsed.searchParams;
		this.authorizeRequests.push(q);
		expect(q.get("response_type")).toBe("code");
		expect(q.get("code_challenge_method")).toBe("S256");
		expect(q.get("resource")).toBe(RESOURCE);
		expect(q.get("scope")?.split(" ")).toContain("chatgpt.tokens.use.direct");
		expect(q.get("redirect_uri")).toMatch(/^http:\/\/127\.0\.0\.1:\d+\/auth\/callback$/);
		expect(q.get("ext_agent_host_id")).toMatch(/^urn:uuid:/);
		let clientId = q.get("client_id") ?? "";
		const callback = new URL(q.get("redirect_uri") ?? "");
		if (clientId === "dynamic_agent_client") {
			clientId = fake("oaiapp");
			this.registrations.push({ clientId, hostId: q.get("ext_agent_host_id") ?? "", agentName: q.get("agent_name_hint") ?? "" });
			callback.searchParams.set("client_id", clientId);
		} else {
			expect(this.registrations.map(r => r.clientId)).toContain(clientId);
		}
		const code = fake("code");
		this.#codes.set(code, {
			clientId,
			challenge: q.get("code_challenge") ?? "",
			redirectUri: q.get("redirect_uri") ?? "",
			nonce: q.get("nonce") ?? "",
		});
		callback.searchParams.set("code", code);
		callback.searchParams.set("scope", this.grantedScope);
		callback.searchParams.set("state", q.get("state") ?? "");
		return deliver(new Request(callback));
	}

	fetch = async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
		expect(String(input)).toBe(TOKEN_URL);
		const form = new URLSearchParams(String(init?.body));
		this.tokenRequests.push(form);
		if (form.get("resource") !== RESOURCE) return oauthError("invalid_target");
		if (form.get("grant_type") === "authorization_code") {
			const pending = this.#codes.get(form.get("code") ?? "");
			this.#codes.delete(form.get("code") ?? "");
			if (!pending) return oauthError("invalid_grant");
			const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(form.get("code_verifier") ?? ""));
			if (Buffer.from(digest).toString("base64url") !== pending.challenge) return oauthError("invalid_grant", "PKCE verification failed");
			if (form.get("client_id") !== pending.clientId || form.get("redirect_uri") !== pending.redirectUri) return oauthError("invalid_client");
			return this.#issue(pending.clientId, pending.nonce);
		}
		if (form.get("grant_type") === "refresh_token") {
			const owner = this.#liveRefresh.get(form.get("refresh_token") ?? "");
			this.#liveRefresh.delete(form.get("refresh_token") ?? "");
			if (!owner || owner !== form.get("client_id")) return oauthError("invalid_grant");
			return this.#issue(owner);
		}
		return oauthError("unsupported_grant_type");
	};

	#issue(clientId: string, nonce?: string): Response {
		const refresh = fake("refresh");
		this.#liveRefresh.set(refresh, clientId);
		const body = {
			access_token: fake("access"),
			refresh_token: refresh,
			id_token: jwt({ nonce, email: "user@example.invalid", "https://api.openai.com/auth": { chatgpt_account_id: "acct-fake" } }),
			expires_in: 3600,
			scope: this.grantedScope,
		};
		return Response.json(body);
	}
}

function oauthError(error: string, description = ""): Response {
	return Response.json({ error, error_description: description }, { status: 400 });
}
