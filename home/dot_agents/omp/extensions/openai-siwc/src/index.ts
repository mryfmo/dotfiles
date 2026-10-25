import type { ExtensionAPI, ProviderModelConfig } from "@oh-my-pi/pi-coding-agent";
import { createSiwcOAuth, RESOURCE } from "./oauth";
import { rewriteResponsesRequest, SIWC_COMPAT } from "./requests";

export const PROVIDER = "openai-siwc";
/** Shown on the ChatGPT consent screen and in the account's agent list. */
export const AGENT_NAME = "omp-dotfiles";

// omp's parseFlag truthy set (pi-utils src/env.ts:472-482), so this reads the flag as `$flag` does.
const TRUTHY = new Set(["1", "y", "Y", "true", "TRUE", "yes", "YES", "on", "ON"]);

const row = (id: string, name: string): ProviderModelConfig => ({
	id,
	name,
	reasoning: true,
	thinking: { mode: "effort", efforts: ["low", "medium", "high", "xhigh", "max"] },
	// Image input on this route is unmeasured.
	input: ["text"],
	cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
	contextWindow: 1_050_000,
	maxTokens: 128_000,
});

/**
 * Static ids (`openai-siwc/<id>`): #S0 read `GET /v1/models` as `data[].id` and listed nothing, but the SIWC
 * docs return a `models` array of `{slug, visibility}`, so discovery is unmeasured and `fetchDynamicModels`
 * waits for a re-probe (docs/openai-siwc.md, open questions). Limits are omp 18.11.3's catalog rows for
 * `openai/<id>` (pi-catalog src/models.json). Both completed on this route: `gpt-6.1-sol` in #S0 and G2,
 * `gpt-6-astra` in the audit verdicts from 2026-10-23 on (pilot facts, done predicate (3)).
 */
export const MODELS: ProviderModelConfig[] = [
	row("gpt-6.1-sol", "GPT-6.1 Sol (ChatGPT plan)"),
	row("gpt-6-astra", "GPT-6 Astra (ChatGPT plan)"),
];

export default function openaiSiwc(pi: ExtensionAPI): void {
	// PI_OPENAI_STATEFUL outranks compat and turns on previous_response_id chaining with delta-only
	// input, which SIWC refuses. A hook throw cannot stop that: omp's runner reports the throw and
	// sends the unrewritten payload, so the guard is refusing to load.
	if (TRUTHY.has(process.env.PI_OPENAI_STATEFUL ?? "")) {
		throw new Error("openai-siwc: PI_OPENAI_STATEFUL is set; SIWC needs full history in `input`. Unset it and restart omp.");
	}
	pi.registerProvider(PROVIDER, {
		baseUrl: RESOURCE,
		api: "openai-responses",
		compat: SIWC_COMPAT,
		oauth: createSiwcOAuth({ agentDir: pi.pi.getAgentDir(), agentName: AGENT_NAME }),
		models: MODELS,
	});
	// omp passes this hook to every openai-responses request and retry as `onPayload`.
	pi.on("before_provider_request", (event, ctx) =>
		ctx.model?.provider === PROVIDER ? rewriteResponsesRequest(event.payload) : undefined,
	);
}
