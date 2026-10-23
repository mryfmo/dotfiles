/**
 * Request shaping for the SIWC Responses preview. omp's `openai-responses` builder stays the
 * transport; compat keeps most rejected shapes from being built, and the rewrite below is the
 * deterministic guard on every payload omp hands to `before_provider_request`.
 */

/** Provider-level compat passed to `registerProvider`; each key is the switch for one rejected shape. */
export const SIWC_COMPAT = {
	// Full replay with store:false; chaining forces store:true and sends delta-only input.
	statefulResponses: false,
	// System text goes to top-level `instructions` instead of an `input` item with role developer.
	supportsDeveloperRole: false,
	// No `prompt_cache_retention: "24h"`.
	supportsLongPromptCacheRetention: false,
	// No `configuration_update` input items for mid-session effort changes.
	supportsConfigurationUpdate: false,
} as const;

/** Top-level fields the preview rejects (preview-limitations page, facts §4). */
export const REJECTED_FIELDS = [
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
] as const;

type Payload = Record<string, unknown>;

/**
 * Returns the payload the SIWC preview accepts: rejected fields removed, system and developer
 * items folded into `instructions`, `store:false` and `stream:true` forced.
 * Throws on `previous_response_id`: omp then sent delta-only input, so stripping the id would
 * silently drop the conversation history.
 */
export function rewriteResponsesRequest(payload: unknown): Payload {
	if (typeof payload !== "object" || payload === null || Array.isArray(payload)) {
		throw new TypeError("openai-siwc: expected a Responses request object");
	}
	const request = payload as Payload;
	if (request.previous_response_id !== undefined) {
		throw new Error(
			"openai-siwc: refusing a chained request (previous_response_id). SIWC needs full history in `input`; unset PI_OPENAI_STATEFUL for this provider.",
		);
	}
	const out: Payload = { ...request };
	for (const field of REJECTED_FIELDS) delete out[field];

	const instructions = typeof out.instructions === "string" && out.instructions !== "" ? [out.instructions] : [];
	if (Array.isArray(out.input)) {
		const kept: unknown[] = [];
		for (const item of out.input) {
			const text = systemItemText(item);
			if (text === undefined) kept.push(item);
			else if (text !== "") instructions.push(text);
		}
		out.input = kept;
	}
	if (instructions.length > 0) out.instructions = instructions.join("\n\n");
	else delete out.instructions;

	out.store = false;
	out.stream = true;
	return out;
}

/** Text of a `system` or `developer` message item, or undefined for any other item. */
function systemItemText(item: unknown): string | undefined {
	if (typeof item !== "object" || item === null) return undefined;
	const { role, type, content } = item as Payload;
	if (role !== "system" && role !== "developer") return undefined;
	if (type !== undefined && type !== "message") return undefined;
	if (typeof content === "string") return content;
	if (!Array.isArray(content)) return "";
	return content
		.map(part => (typeof part === "object" && part !== null && typeof (part as Payload).text === "string" ? (part as Payload).text : ""))
		.filter(text => text !== "")
		.join("\n");
}

// TODO(unit U3b): measure the wire shape of `subscription_sharing_usage_limit_exceeded` and
// `subscription_sharing_usage_unavailable` (HTTP status and body, or a `response.failed` event)
// before mapping them; omp 18.11.3 retries a 429 five times, which a quota error should not trigger.
