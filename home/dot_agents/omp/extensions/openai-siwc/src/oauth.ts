import type { OAuthCredentials, OAuthLoginCallbacks } from "@oh-my-pi/pi-ai";
import { loadRegistration, newRegistration, type Registration, saveRegistration } from "./store";

export const AUTHORIZE_URL = "https://auth.openai.com/api/accounts/authorize";
export const TOKEN_URL = "https://auth.openai.com/api/accounts/oauth/token";
export const RESOURCE = "https://api.openai.com/v1";
export const SCOPES = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct";
export const PLAN_SCOPE = "chatgpt.tokens.use.direct";
/** First-time registration entrypoint only; never saved and never used for token exchange. */
export const REGISTRATION_CLIENT_ID = "dynamic_agent_client";
export const CALLBACK_PATH = "/auth/callback";
export const PREFERRED_PORT = 1455;
const CALLBACK_TIMEOUT_MS = 300_000;
const TOKEN_TIMEOUT_MS = 15_000;
const ACCOUNT_CLAIM = "https://api.openai.com/auth";

type Fetch = (input: string | URL | Request, init?: RequestInit) => Promise<Response>;

export interface CallbackResult {
	code: string;
	/** Issued client_id; the docs return it on the registration callback. */
	clientId?: string;
	scope?: string;
}

/** A bound loopback receiver; `redirectUri` is exactly what the authorize request advertised. */
export interface Loopback {
	redirectUri: string;
	close(): void;
}

export type Listen = (handle: (request: Request) => Response) => Loopback;

export interface SiwcOAuthDeps {
	agentDir: string;
	agentName: string;
	fetch?: Fetch;
	listen?: Listen;
	now?: () => number;
}

/** The `oauth` block for `registerProvider`. */
export function createSiwcOAuth(deps: SiwcOAuthDeps) {
	const listen = deps.listen ?? listenLoopback;
	const now = deps.now ?? Date.now;
	const fetchFor = (callbacks?: OAuthLoginCallbacks): Fetch => (callbacks?.fetch as Fetch | undefined) ?? deps.fetch ?? fetch;

	return {
		name: "ChatGPT plan (Sign in with ChatGPT)",

		async login(callbacks: OAuthLoginCallbacks): Promise<OAuthCredentials> {
			// Saved before the browser opens, so a retried first login reuses the same host id.
			let registration = await loadRegistration(deps.agentDir);
			if (!registration) {
				registration = newRegistration();
				await saveRegistration(deps.agentDir, registration);
			}
			const pkce = await createPkce();
			const state = randomToken();
			const nonce = randomToken();
			const receiver = createCallbackReceiver(state);
			const loopback = listen(receiver.handle);
			try {
				const url = buildAuthorizeUrl({ registration, redirectUri: loopback.redirectUri, state, nonce, challenge: pkce.challenge, agentName: deps.agentName });
				callbacks.onAuth({ url, instructions: registration.clientId ? undefined : `Name and authorize the agent "${deps.agentName}" in the browser.` });
				callbacks.onProgress?.("Waiting for the ChatGPT sign-in callback...");
				const result = await waitFor(receiver.result, callbacks.signal, CALLBACK_TIMEOUT_MS);

				// The server is authoritative: a callback client_id replaces a saved one.
				const clientId = result.clientId ?? registration.clientId;
				if (!clientId) throw new Error("openai-siwc: the registration callback carried no issued client_id");
				if (clientId !== registration.clientId) {
					registration = { ...registration, clientId };
					await saveRegistration(deps.agentDir, registration);
				}

				callbacks.onProgress?.("Exchanging the authorization code...");
				const tokens = await postToken(fetchFor(callbacks), {
					grant_type: "authorization_code",
					client_id: clientId,
					code: result.code,
					code_verifier: pkce.verifier,
					redirect_uri: loopback.redirectUri,
					resource: RESOURCE,
				});
				const credentials = toCredentials(tokens, now(), { requirePlanScope: true, nonce });
				if (credentials.accountId && credentials.accountId !== registration.accountId) {
					await saveRegistration(deps.agentDir, { ...registration, accountId: credentials.accountId });
				}
				return credentials;
			} finally {
				loopback.close();
			}
		},

		async refreshToken(credentials: OAuthCredentials): Promise<OAuthCredentials> {
			const registration = await loadRegistration(deps.agentDir);
			if (!registration?.clientId) throw new Error("openai-siwc: no issued client_id for this profile; run /login openai-siwc");
			const tokens = await postToken(fetchFor(), {
				grant_type: "refresh_token",
				client_id: registration.clientId,
				refresh_token: credentials.refresh,
				resource: RESOURCE,
			});
			const refreshed = toCredentials(tokens, now(), { requirePlanScope: false, fallbackRefresh: credentials.refresh });
			return { ...credentials, ...refreshed, accountId: refreshed.accountId ?? credentials.accountId, email: refreshed.email ?? credentials.email };
		},

		getApiKey(credentials: OAuthCredentials): string {
			return credentials.access;
		},
	};
}

export function buildAuthorizeUrl(args: {
	registration: Registration;
	redirectUri: string;
	state: string;
	nonce: string;
	challenge: string;
	agentName: string;
}): string {
	const registering = args.registration.clientId === undefined;
	const query = new URLSearchParams({
		response_type: "code",
		client_id: args.registration.clientId ?? REGISTRATION_CLIENT_ID,
		redirect_uri: args.redirectUri,
		scope: SCOPES,
		resource: RESOURCE,
		state: args.state,
		nonce: args.nonce,
		code_challenge: args.challenge,
		code_challenge_method: "S256",
		// TODO(unit U3b): the sign-in page marks ext_agent_host_id "Required"; measure whether a
		// later sign-in with the issued client_id accepts it (sent here) or rejects it.
		ext_agent_host_id: args.registration.hostId,
	});
	if (registering) query.set("agent_name_hint", args.agentName);
	return `${AUTHORIZE_URL}?${query}`;
}

/**
 * Loopback request handler. A callback with a foreign state is answered but ignored, because
 * any local process can send one; an error with our state ends the login at once.
 */
export function createCallbackReceiver(expectedState: string): {
	handle: (request: Request) => Response;
	result: Promise<CallbackResult>;
} {
	const settled = Promise.withResolvers<CallbackResult>();
	let done = false;
	const handle = (request: Request): Response => {
		const url = new URL(request.url);
		if (request.method !== "GET" || url.pathname !== CALLBACK_PATH) return new Response("Not Found", { status: 404 });
		const params = url.searchParams;
		if (done || params.get("state") !== expectedState) return page(400, "This sign-in link is not the active one.");
		const error = params.get("error");
		const code = params.get("code");
		done = true;
		if (error) {
			settled.reject(new Error(`openai-siwc: authorization failed: ${error}`));
			return page(400, "Sign-in was not completed. Return to the terminal.");
		}
		if (!code) {
			settled.reject(new Error("openai-siwc: callback carried no authorization code"));
			return page(400, "Sign-in callback was incomplete. Return to the terminal.");
		}
		settled.resolve({ code, clientId: params.get("client_id") ?? undefined, scope: params.get("scope") ?? undefined });
		return page(200, "Signed in. You can close this tab and return to the terminal.");
	};
	return { handle, result: settled.promise };
}

/**
 * Binds 127.0.0.1 only (the docs forbid `localhost`), on 1455 when free, else on a random port;
 * the docs allow a different port on later sign-ins and the registration itself.
 */
export function listenLoopback(handle: (request: Request) => Response, preferredPort = PREFERRED_PORT): Loopback {
	const serve = (port: number) => Bun.serve({ hostname: "127.0.0.1", port, reusePort: false, fetch: handle });
	let server: ReturnType<typeof serve>;
	try {
		server = serve(preferredPort);
	} catch {
		server = serve(0);
	}
	return { redirectUri: `http://127.0.0.1:${server.port}${CALLBACK_PATH}`, close: () => void server.stop(true) };
}

interface TokenResponse {
	access_token?: unknown;
	refresh_token?: unknown;
	id_token?: unknown;
	expires_in?: unknown;
	scope?: unknown;
}

async function postToken(fetchImpl: Fetch, form: Record<string, string>): Promise<TokenResponse> {
	const response = await fetchImpl(TOKEN_URL, {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json" },
		body: new URLSearchParams(form),
		signal: AbortSignal.timeout(TOKEN_TIMEOUT_MS),
	});
	const text = await response.text();
	if (!response.ok) throw new Error(`openai-siwc: ${form.grant_type} failed: ${response.status} ${describeTokenError(text)}`);
	return JSON.parse(text) as TokenResponse;
}

/** Only the OAuth error code and description reach the message; the body is never echoed whole. */
function describeTokenError(text: string): string {
	try {
		const body = JSON.parse(text) as { error?: unknown; error_description?: unknown };
		const code = typeof body.error === "string" ? body.error : (body.error as { code?: unknown } | undefined)?.code;
		const description = typeof body.error_description === "string" ? body.error_description : "";
		return [code, description].filter(part => typeof part === "string" && part !== "").join(": ").slice(0, 200) || "(no error code)";
	} catch {
		return "(non-JSON error body)";
	}
}

function toCredentials(
	tokens: TokenResponse,
	nowMs: number,
	options: { requirePlanScope: boolean; nonce?: string; fallbackRefresh?: string },
): OAuthCredentials {
	const access = tokens.access_token;
	const refresh = typeof tokens.refresh_token === "string" ? tokens.refresh_token : options.fallbackRefresh;
	if (typeof access !== "string" || access === "" || typeof refresh !== "string" || typeof tokens.expires_in !== "number") {
		throw new Error("openai-siwc: token response is missing access_token, refresh_token or expires_in");
	}
	const scopes = typeof tokens.scope === "string" ? tokens.scope.split(" ") : undefined;
	// "A valid ID token alone does not authorize ChatGPT plan usage" (sign-in page).
	// TODO(unit U3b): measure whether a refresh response carries `scope`; absent is accepted on refresh only.
	if ((options.requirePlanScope || scopes) && !scopes?.includes(PLAN_SCOPE)) {
		throw new Error(`openai-siwc: the grant lacks ${PLAN_SCOPE}; this account cannot use ChatGPT plan inference here`);
	}
	const claims = typeof tokens.id_token === "string" ? decodeJwtPayload(tokens.id_token) : undefined;
	if (options.nonce && claims && claims.nonce !== undefined && claims.nonce !== options.nonce) {
		throw new Error("openai-siwc: id_token nonce does not match this sign-in");
	}
	// TODO(unit U3b): confirm the SIWC id_token carries the same account claim as the Codex route.
	const account = claims?.[ACCOUNT_CLAIM] as { chatgpt_account_id?: unknown } | undefined;
	return {
		access,
		refresh,
		expires: nowMs + tokens.expires_in * 1000,
		accountId: typeof account?.chatgpt_account_id === "string" ? account.chatgpt_account_id : undefined,
		email: typeof claims?.email === "string" ? claims.email : undefined,
	};
}

/** Claims only; the token came straight from the token endpoint over TLS, so no signature check. */
function decodeJwtPayload(jwt: string): Record<string, unknown> | undefined {
	const part = jwt.split(".")[1];
	if (!part) return undefined;
	try {
		return JSON.parse(Buffer.from(part, "base64url").toString("utf8")) as Record<string, unknown>;
	} catch {
		return undefined;
	}
}

export async function createPkce(): Promise<{ verifier: string; challenge: string }> {
	const verifier = randomToken(48);
	const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier));
	return { verifier, challenge: Buffer.from(digest).toString("base64url") };
}

function randomToken(bytes = 24): string {
	return Buffer.from(crypto.getRandomValues(new Uint8Array(bytes))).toString("base64url");
}

function waitFor<T>(promise: Promise<T>, signal: AbortSignal | undefined, timeoutMs: number): Promise<T> {
	const bound = signal ? AbortSignal.any([signal, AbortSignal.timeout(timeoutMs)]) : AbortSignal.timeout(timeoutMs);
	return new Promise<T>((resolve, reject) => {
		const onAbort = () => reject(new Error(`openai-siwc: sign-in cancelled or timed out (${bound.reason})`));
		if (bound.aborted) return onAbort();
		bound.addEventListener("abort", onAbort, { once: true });
		promise.then(resolve, reject).finally(() => bound.removeEventListener("abort", onAbort));
	});
}

function page(status: number, message: string): Response {
	return new Response(`<!doctype html><title>openai-siwc</title><p>${message}</p>`, {
		status,
		headers: { "Content-Type": "text/html; charset=utf-8" },
	});
}
