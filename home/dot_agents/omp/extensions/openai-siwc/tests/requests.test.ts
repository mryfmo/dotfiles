import { expect, test } from "bun:test";
import * as os from "node:os";
import * as path from "node:path";
import { rewriteResponsesRequest, SIWC_COMPAT } from "../src/requests";

// Copied from the SIWC preview-limitations page (facts §4), not from src, so a field dropped there fails here.
const DOCUMENTED_REJECTED = [
	"background",
	"conversation",
	"max_output_tokens",
	"max_tool_calls",
	"metadata",
	"moderation",
	"multi_agent",
	"prompt",
	"prompt_cache_retention",
	"safety_identifier",
	"temperature",
	"top_logprobs",
	"top_p",
	"truncation",
	"user",
];

test("every rejected field is removed and store/stream are forced", () => {
	const payload: Record<string, unknown> = { model: "m", input: [], store: true, stream: false, prompt_cache_key: "k" };
	for (const field of DOCUMENTED_REJECTED) payload[field] = 1;
	const out = rewriteResponsesRequest(payload);
	for (const field of DOCUMENTED_REJECTED) expect(out).not.toHaveProperty(field);
	expect(out).toMatchObject({ model: "m", store: false, stream: true, prompt_cache_key: "k" });
	expect(payload.store).toBe(true);
});

test("system and developer items fold into instructions in order", () => {
	const out = rewriteResponsesRequest({
		instructions: "base",
		input: [
			{ role: "developer", content: "dev string" },
			{ role: "user", content: [{ type: "input_text", text: "hi" }] },
			{ type: "message", role: "system", content: [{ type: "input_text", text: "sys part" }] },
			{ type: "function_call_output", call_id: "c", output: "x" },
		],
	});
	expect(out.instructions).toBe("base\n\ndev string\n\nsys part");
	expect(out.input).toEqual([
		{ role: "user", content: [{ type: "input_text", text: "hi" }] },
		{ type: "function_call_output", call_id: "c", output: "x" },
	]);
});

test("a chained request is refused instead of losing its history", () => {
	expect(() => rewriteResponsesRequest({ previous_response_id: "resp_1", input: [] })).toThrow("PI_OPENAI_STATEFUL");
});

// Drives omp's own openai-responses builder and SSE parser (the installed 18.11.3), the path
// a real turn takes, with the HTTP call answered by a fake Responses stream.
const OMP = process.env.OMP_PACKAGE_DIR ?? path.join(os.homedir(), ".local/lib/node_modules/@oh-my-pi/pi-coding-agent");
const PI = path.join(OMP, "node_modules/@oh-my-pi");
const { streamSimple } = await import(path.join(PI, "pi-ai/src/index.ts"));
const { buildModel } = await import(path.join(PI, "pi-catalog/src/build.ts"));

const FAKE_BEARER = "fake-bearer";
const sse = (type: string, data: object) => `event: ${type}\ndata: ${JSON.stringify({ type, ...data })}\n\n`;

type Respond = (body: { model: string }) => Response;

function fakeResponses(captured: unknown[], respond: Respond) {
	return async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
		expect(String(input)).toBe("https://api.openai.com/v1/responses");
		const body = JSON.parse(String(init?.body));
		captured.push(body);
		return respond(body);
	};
}

const completed: Respond = body => {
	const message = { type: "message", id: "msg_1", role: "assistant", status: "completed", content: [{ type: "output_text", text: "PONG", annotations: [] }] };
	const response = { id: "resp_1", object: "response", status: "completed", model: body.model, output: [message], usage: { input_tokens: 3, output_tokens: 1, total_tokens: 4 } };
	const stream =
		sse("response.created", { response: { ...response, status: "in_progress", output: [] } }) +
		sse("response.output_item.added", { output_index: 0, item: { ...message, status: "in_progress", content: [] } }) +
		sse("response.output_text.delta", { item_id: "msg_1", output_index: 0, content_index: 0, delta: "PONG" }) +
		sse("response.output_item.done", { output_index: 0, item: message }) +
		sse("response.completed", { response });
	return new Response(stream, { headers: { "Content-Type": "text/event-stream" } });
};

// `retry-after: 0` keeps omp's transport backoff at zero so the attempt count is observable fast.
const planError =
	(status: number, code: string): Respond =>
	() =>
		Response.json(
			{ error: { message: `fake ${code}`, type: "invalid_request_error", code } },
			{ status, headers: { "retry-after": "0" } },
		);

async function runTurn(compat: object | undefined, respond: Respond = completed) {
	const model = buildModel({
		id: "gpt-6.1-sol",
		name: "GPT-6.1 Sol",
		provider: "openai-siwc",
		api: "openai-responses",
		baseUrl: "https://api.openai.com/v1",
		reasoning: true,
		input: ["text"],
		cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
		contextWindow: 1_050_000,
		maxTokens: 128_000,
		compat,
	});
	const captured: Record<string, unknown>[] = [];
	const events: {
		type: string;
		reason?: string;
		message?: { content: { type: string; text?: string }[] };
		error?: { stopReason: string; errorMessage?: string; errorStatus?: number; api?: string };
	}[] = [];
	const stream = streamSimple(
		model,
		{ systemPrompt: "You are the auditor.", messages: [{ role: "user", content: "Reply PONG", timestamp: 0 }] },
		{
			apiKey: FAKE_BEARER,
			sessionId: "session-1",
			maxTokens: 1000,
			cacheRetention: "long",
			reasoning: "high",
			fetch: fakeResponses(captured, respond),
			// What sdk.ts wires to before_provider_request, where this extension's hook runs.
			onPayload: (payload: unknown) => rewriteResponsesRequest(payload),
		},
	);
	for await (const event of stream) events.push(event);
	return { body: captured[0], last: events.at(-1), calls: captured.length };
}

function expectSiwcShape(body: Record<string, unknown>) {
	expect(body.store).toBe(false);
	expect(body.stream).toBe(true);
	expect(body).not.toHaveProperty("previous_response_id");
	for (const field of DOCUMENTED_REJECTED) expect(body).not.toHaveProperty(field);
	expect(body.instructions).toBe("You are the auditor.");
	const roles = (body.input as { role?: string }[]).map(item => item.role);
	expect(roles).not.toContain("developer");
	expect(roles).not.toContain("system");
}

test("an omp turn with the provider compat reaches SIWC in the accepted shape and completes", async () => {
	const { body, last, calls } = await runTurn(SIWC_COMPAT);
	expect(calls).toBe(1);
	expectSiwcShape(body);
	expect(last?.type).toBe("done");
	expect(last?.reason).toBe("stop");
	expect(last?.message?.content.find(part => part.type === "text")?.text).toBe("PONG");
});

test("the rewrite alone still cleans omp's default request (developer item, cache retention, max_output_tokens)", async () => {
	const { body, last } = await runTurn(undefined);
	expectSiwcShape(body);
	expect(last?.type).toBe("done");
});

// omp's own error classifier; TurnRecovery retries a failed turn only when `retriable` holds.
const AIError = await import(path.join(PI, "pi-ai/src/error/index.ts"));

test("subscription_sharing_usage_unavailable on a 403 ends the turn after one request and is not retried", async () => {
	const { last, calls } = await runTurn(SIWC_COMPAT, planError(403, "subscription_sharing_usage_unavailable"));
	expect(calls).toBe(1);
	expect(last?.type).toBe("error");
	expect(last?.error?.errorMessage).toContain("subscription_sharing_usage_unavailable");
	expect(AIError.retriable(AIError.classifyMessage(last?.error ?? {}))).toBe(false);
});

test("subscription_sharing_usage_limit_exceeded on a 429 is a usage limit, not a provider retry", async () => {
	const { last, calls } = await runTurn(SIWC_COMPAT, planError(429, "subscription_sharing_usage_limit_exceeded"));
	expect(last?.type).toBe("error");
	expect(last?.error?.errorMessage).toContain("subscription_sharing_usage_limit_exceeded");
	const id = AIError.classifyMessage(last?.error ?? {});
	expect(AIError.is(id, AIError.Flag.UsageLimit)).toBe(true);
	expect(AIError.isProviderRetryableError(new Error(last?.error?.errorMessage))).toBe(false);
	// shortcut: omp 18.11.3's transport (fetchWithRetry) still resends a 429 up to 6 times and no
	// extension hook reaches it on the built-in transport; this pins the count until one does.
	expect(calls).toBe(6);
});
