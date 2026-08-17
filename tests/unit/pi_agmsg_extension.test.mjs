import assert from "node:assert/strict";
import { registerHooks } from "node:module";
import { test } from "node:test";

const typeboxSource = `
    export const Type = {
            String: (options = {}) => ({ type: "string", ...options }),
            Object: (properties, options = {}) => ({
                type: "object",
                properties,
                ...options,
            }),
    };
`;
registerHooks({
    resolve(specifier, context, nextResolve) {
        if (specifier === "typebox") {
            return {
                url: `data:text/javascript,${encodeURIComponent(typeboxSource)}`,
                shortCircuit: true,
            };
        }
        return nextResolve(specifier, context);
    },
});

const { default: agmsgExtension } = await import(
    "../../home/dot_pi/agent/extensions/agmsg.ts"
);

const IDENTITY = "pi-standard-project";
const HOME = "/home/pi-worker";
const SEND = `${HOME}/.agents/skills/agmsg/scripts/send.sh`;

function harness(options = {}) {
    const identity = Object.hasOwn(options, "identity") ? options.identity : IDENTITY;
    const error = options.error ?? null;
    let tool;
    const calls = [];
    const pi = {
        registerTool(definition) {
            tool = definition;
        },
    };
    const execFile = (file, args, options, callback) => {
        calls.push({ file, args, options });
        queueMicrotask(() => callback(error, "ignored stdout", "ignored stderr"));
        return {};
    };
    agmsgExtension(pi, execFile, identity, HOME);
    return {
        calls,
        tool: () => tool,
        execute: (params) => tool.execute("call-1", params),
    };
}

test("registers the pinned typed schema and explicit RESULT prompt guidance", () => {
    const tool = harness().tool();

    assert.equal(tool.name, "agmsg_send");
    assert.equal(tool.label, "Send agmsg message");
    assert.deepEqual(tool.parameters, {
        type: "object",
        properties: {
            team: { type: "string", description: "agmsg team name" },
            to: { type: "string", description: "recipient agent identity" },
            body: { type: "string", description: "complete one-line agmsg message" },
        },
        additionalProperties: false,
    });
    assert.match(tool.promptSnippet, /AGMSG-RESULT/);
    assert.deepEqual(tool.promptGuidelines, [
        "Use agmsg_send to send every AGMSG-RESULT message; final assistant text is not the RESULT.",
    ]);
    assert.equal("from" in tool.parameters.properties, false);
});

test("spawns send.sh with one argv array and no shell", async () => {
    const send = harness();
    const body = 'AGMSG-RESULT v1 task_id=T68b note="; touch never-runs"';

    const result = await send.execute({ team: "workers", to: "orchestrator", body });

    assert.deepEqual(send.calls, [{
        file: SEND,
        args: ["workers", IDENTITY, "orchestrator", body],
        options: { encoding: "utf8", timeout: 10000 },
    }]);
    assert.deepEqual(result, {
        content: [{ type: "text", text: "agmsg_send: sent" }],
        details: { success: true },
    });
});

test("missing identity returns a fixed error without spawning", async () => {
    for (const identity of [undefined, ""]) {
        const send = harness({ identity });
        const result = await send.execute({ team: "workers", to: "orchestrator", body: "body" });
        assert.deepEqual(result, {
            content: [{ type: "text", text: "agmsg_send: missing AGMSG_PI_IDENTITY" }],
            details: { success: false },
            isError: true,
        });
        assert.deepEqual(send.calls, []);
    }
});

test("send failure returns one fixed error line", async () => {
    const send = harness({ error: Object.assign(new Error("secret stderr"), { code: 7 }) });

    const result = await send.execute({ team: "workers", to: "orchestrator", body: "body" });

    assert.deepEqual(result, {
        content: [{ type: "text", text: "agmsg_send: failed" }],
        details: { success: false },
        isError: true,
    });
});
