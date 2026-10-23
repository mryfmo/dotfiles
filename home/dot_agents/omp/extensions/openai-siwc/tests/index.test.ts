import { expect, test } from "bun:test";
import openaiSiwc, { PROVIDER } from "../src/index";

function load() {
	const providers: [string, Record<string, unknown>][] = [];
	const hooks: [string, (event: { payload: unknown }, ctx: { model?: { provider: string } }) => unknown][] = [];
	const pi = {
		pi: { getAgentDir: () => "/nonexistent/agent" },
		registerProvider: (name: string, config: Record<string, unknown>) => providers.push([name, config]),
		on: (event: string, handler: never) => hooks.push([event, handler]),
	};
	openaiSiwc(pi as never);
	return { providers, hooks };
}

test("the extension refuses to load when PI_OPENAI_STATEFUL would turn chaining on", () => {
	const saved = process.env.PI_OPENAI_STATEFUL;
	try {
		for (const value of ["1", "true", "yes", "on"]) {
			process.env.PI_OPENAI_STATEFUL = value;
			expect(load).toThrow("Unset it and restart omp");
		}
		process.env.PI_OPENAI_STATEFUL = "0";
		expect(load().providers).toHaveLength(1);
	} finally {
		if (saved === undefined) delete process.env.PI_OPENAI_STATEFUL;
		else process.env.PI_OPENAI_STATEFUL = saved;
	}
});

test("the extension registers one oauth provider on the Responses API and hooks only its own requests", () => {
	const { providers, hooks } = load();

	expect(providers.map(([name]) => name)).toEqual([PROVIDER]);
	const config = providers[0][1] as { api: string; baseUrl: string; compat: object; oauth: { name: string }; models: { id: string }[] };
	expect(config.api).toBe("openai-responses");
	expect(config.baseUrl).toBe("https://api.openai.com/v1");
	expect(config.compat).toMatchObject({ statefulResponses: false, supportsDeveloperRole: false });
	expect(typeof config.oauth.name).toBe("string");
	expect(config.models.map(model => model.id)).toEqual(["gpt-6.1-sol", "gpt-6-astra"]);
	expect(config).not.toHaveProperty("fetchDynamicModels");

	expect(hooks.map(([event]) => event)).toEqual(["before_provider_request"]);
	const hook = hooks[0][1];
	const payload = { input: [{ role: "developer", content: "d" }], max_output_tokens: 5 };
	expect(hook({ payload }, { model: { provider: PROVIDER } })).toEqual({ input: [], instructions: "d", store: false, stream: true });
	expect(hook({ payload }, { model: { provider: "openai" } })).toBeUndefined();
});
