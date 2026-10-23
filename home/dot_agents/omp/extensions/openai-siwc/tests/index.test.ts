import { expect, test } from "bun:test";
import openaiSiwc, { PROVIDER } from "../src/index";

test("the extension registers one oauth provider on the Responses API and hooks only its own requests", () => {
	const providers: [string, Record<string, unknown>][] = [];
	const hooks: [string, (event: { payload: unknown }, ctx: { model?: { provider: string } }) => unknown][] = [];
	const pi = {
		pi: { getAgentDir: () => "/nonexistent/agent" },
		registerProvider: (name: string, config: Record<string, unknown>) => providers.push([name, config]),
		on: (event: string, handler: never) => hooks.push([event, handler]),
	};
	openaiSiwc(pi as never);

	expect(providers.map(([name]) => name)).toEqual([PROVIDER]);
	const config = providers[0][1] as { api: string; baseUrl: string; compat: object; oauth: { name: string }; models: { id: string }[] };
	expect(config.api).toBe("openai-responses");
	expect(config.baseUrl).toBe("https://api.openai.com/v1");
	expect(config.compat).toMatchObject({ statefulResponses: false, supportsDeveloperRole: false });
	expect(typeof config.oauth.name).toBe("string");
	expect(config.models.map(model => model.id)).toEqual(["gpt-6.1-sol"]);

	expect(hooks.map(([event]) => event)).toEqual(["before_provider_request"]);
	const hook = hooks[0][1];
	const payload = { input: [{ role: "developer", content: "d" }], max_output_tokens: 5 };
	expect(hook({ payload }, { model: { provider: PROVIDER } })).toEqual({ input: [], instructions: "d", store: false, stream: true });
	expect(hook({ payload }, { model: { provider: "openai" } })).toBeUndefined();
});
