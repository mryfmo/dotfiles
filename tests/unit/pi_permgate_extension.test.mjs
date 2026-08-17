import assert from "node:assert/strict";
import test from "node:test";

import permgateExtension from "../../home/dot_pi/agent/extensions/permgate.ts";

const BLOCKED = { block: true, reason: "blocked by policy" };

function harness({ stdout = '{"decision":"allow"}\n', error = null } = {}) {
    let handler;
    const calls = [];
    const pi = {
        on(event, callback) {
            assert.equal(event, "tool_call");
            handler = callback;
        },
    };
    const execFile = (file, args, options, callback) => ({
        stdin: {
            end(input) {
                calls.push({ file, args, options, input });
                queueMicrotask(() => callback(error, stdout, ""));
            },
        },
    });
    permgateExtension(pi, execFile);
    return { calls, invoke: (event, ctx) => handler(event, ctx) };
}

function event(toolName, input) {
    return { type: "tool_call", toolCallId: "call-1", toolName, input };
}

function context({ interactive = false, confirmed = false, mode } = {}) {
    let confirmations = 0;
    return {
        ctx: {
            cwd: "/workspace/project",
            mode: mode ?? (interactive ? "tui" : "print"),
            hasUI: interactive,
            ui: {
                async confirm() {
                    confirmations += 1;
                    return confirmed;
                },
            },
        },
        confirmations: () => confirmations,
    };
}

test("allow proceeds and sends normalized stdin with the seven-second timeout", async () => {
    const gate = harness();
    const ui = context();

    assert.equal(await gate.invoke(event("bash", { command: "git status" }), ui.ctx), undefined);
    assert.deepEqual(gate.calls, [
        {
            file: "permgate",
            args: ["pi"],
            options: { encoding: "utf8", timeout: 7000 },
            input: '{"tool":"bash","command":"git status","cwd":"/workspace/project"}',
        },
    ]);
});

test("read sends cwd while preserving the path bytes for permgate", async () => {
    const gate = harness();

    assert.equal(
        await gate.invoke(event("read", { path: "../raw/../input.txt" }), context().ctx),
        undefined,
    );
    assert.equal(
        gate.calls[0].input,
        '{"tool":"read","path":"../raw/../input.txt","cwd":"/workspace/project"}',
    );
});

test("deny blocks with the fixed one-line reason", async () => {
    const gate = harness({ stdout: '{"decision":"deny"}\n' });

    assert.deepEqual(await gate.invoke(event("write", { path: "output.txt" }), context().ctx), BLOCKED);
});

test("ask uses interactive confirmation", async () => {
    for (const confirmed of [true, false]) {
        const gate = harness({ stdout: '{"decision":"ask"}\n' });
        const ui = context({ interactive: true, confirmed });

        assert.deepEqual(
            await gate.invoke(event("edit", { path: "output.txt" }), ui.ctx),
            confirmed ? undefined : BLOCKED,
        );
        assert.equal(ui.confirmations(), 1);
    }
});

test("ask blocks without interactive UI", async () => {
    const gate = harness({ stdout: '{"decision":"ask"}\n' });
    const ui = context();

    assert.deepEqual(await gate.invoke(event("bash", { command: "echo hi" }), ui.ctx), BLOCKED);
    assert.equal(ui.confirmations(), 0);
});

test("ask blocks in RPC mode even when dialog UI is available", async () => {
    const gate = harness({ stdout: '{"decision":"ask"}\n' });
    const ui = context({ interactive: true, confirmed: true, mode: "rpc" });

    assert.deepEqual(await gate.invoke(event("bash", { command: "echo hi" }), ui.ctx), BLOCKED);
    assert.equal(ui.confirmations(), 0);
});

test("nonzero, timeout, malformed output, and malformed gated input fail closed", async (t) => {
    const fixtures = [
        ["nonzero", { error: Object.assign(new Error("exit 2"), { code: 2 }) }],
        ["timeout", { error: Object.assign(new Error("timed out"), { killed: true }) }],
        ["malformed", { stdout: "not-json\n" }],
    ];
    for (const [name, fixture] of fixtures) {
        await t.test(name, async () => {
            const gate = harness(fixture);
            assert.deepEqual(await gate.invoke(event("bash", { command: "echo hi" }), context().ctx), BLOCKED);
        });
    }

    const gate = harness();
    assert.deepEqual(await gate.invoke(event("write", {}), context().ctx), BLOCKED);
    assert.deepEqual(
        await gate.invoke(event("write", { path: "output.txt" }), { ...context().ctx, cwd: undefined }),
        BLOCKED,
    );
    assert.equal(gate.calls.length, 0);
});

test("ungated passthrough tools never invoke permgate", async () => {
    const gate = harness();
    for (const toolName of ["grep", "find", "ls", "agmsg_send"]) {
        assert.equal(await gate.invoke(event(toolName, { path: "." }), context().ctx), undefined);
    }
    assert.equal(gate.calls.length, 0);
});
