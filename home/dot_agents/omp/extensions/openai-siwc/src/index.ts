import type { ExtensionAPI, ProviderModelConfig } from "@oh-my-pi/pi-coding-agent";
import { createSiwcOAuth, RESOURCE } from "./oauth";
import { rewriteResponsesRequest, SIWC_COMPAT } from "./requests";

export const PROVIDER = "openai-siwc";
/** Shown on the ChatGPT consent screen and in the account's agent list. */
export const AGENT_NAME = "omp-dotfiles";

/**
 * `GET /v1/models` returned no entries on this route (pilot facts #S0), so the ids are static.
 * Limits are omp 18.11.3's catalog row for `openai/gpt-6.1-sol` (pi-catalog src/models.json).
 * TODO(unit U3b): add `gpt-6-astra` after one measured completion on this route; measure image input.
 */
export const MODELS: ProviderModelConfig[] = [
	{
		id: "gpt-6.1-sol",
		name: "GPT-6.1 Sol (ChatGPT plan)",
		reasoning: true,
		thinking: { mode: "effort", efforts: ["low", "medium", "high", "xhigh", "max"] },
		input: ["text"],
		cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
		contextWindow: 1_050_000,
		maxTokens: 128_000,
	},
];

export default function openaiSiwc(pi: ExtensionAPI): void {
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
