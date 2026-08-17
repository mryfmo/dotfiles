import assert from "node:assert/strict";
import test from "node:test";

import contextdbExtension from "../../home/dot_pi/agent/extensions/contextdb.ts";

const OPTED_CWD = "/workspace/project";
const CLI = `${OPTED_CWD}/.claude/hooks/contextdb_cli.py`;

function harness({ opted = true, execError = null, existsError = null } = {}) {
    const handlers = new Map();
    const calls = [];
    const errors = [];
    let existsChecks = 0;
    const pi = {
        on(event, callback) {
            handlers.set(event, callback);
        },
    };
    const execFile = (file, args, options, callback) => {
        const call = { file, args, options, input: undefined };
        calls.push(call);
        return {
            stdin: {
                end(input) {
                    call.input = input;
                    queueMicrotask(() => callback(execError, "", ""));
                },
            },
        };
    };
    const existsSync = () => {
        existsChecks += 1;
        if (existsError) {
            throw existsError;
        }
        return typeof opted === "function" ? opted() : opted;
    };
    contextdbExtension(pi, execFile, existsSync, (message) => errors.push(message));
    const ctx = {
        cwd: OPTED_CWD,
        sessionManager: { getSessionId: () => "pi-session" },
    };
    return {
        calls,
        errors,
        existsChecks: () => existsChecks,
        invoke: (name, event, context = ctx) => handlers.get(name)(event, context),
    };
}

function payload(call) {
    assert.equal(call.file, "python3");
    assert.deepEqual(call.args, [CLI, "ingest", "--ingested-from", "pi"]);
    assert.deepEqual(call.options, { cwd: OPTED_CWD, encoding: "utf8", timeout: 5000 });
    return JSON.parse(call.input);
}

async function start(harnessInstance) {
    await harnessInstance.invoke("session_start", { type: "session_start", reason: "startup" });
}

test("tool completion captures success and each supported primary argument", async () => {
    const capture = harness();
    await start(capture);
    const fixtures = [
        ["bash", { command: "git status", ignored: "x" }, { command: "git status" }],
        ["read", { path: "README.md", offset: 1 }, { path: "README.md" }],
        ["write", { path: "out.txt", content: "secret" }, { path: "out.txt" }],
        ["edit", { path: "out.txt", oldText: "a" }, { path: "out.txt" }],
        ["grep", { pattern: "needle", path: "." }, { pattern: "needle" }],
        ["find", { pattern: "*.ts", path: "." }, { pattern: "*.ts" }],
    ];

    for (const [index, [toolName, args, toolInput]] of fixtures.entries()) {
        const toolCallId = `call-${index}`;
        await capture.invoke("tool_execution_start", {
            type: "tool_execution_start",
            toolCallId,
            toolName,
            args,
        });
        await capture.invoke("tool_execution_end", {
            type: "tool_execution_end",
            toolCallId,
            toolName,
            result: { omitted: true },
            isError: false,
        });
        assert.deepEqual(payload(capture.calls[index]), {
            hook_event_name: "PostToolUse",
            session_id: "pi-session",
            cwd: OPTED_CWD,
            tool_name: toolName[0].toUpperCase() + toolName.slice(1),
            tool_use_id: toolCallId,
            tool_input: toolInput,
            tool_response: { success: true },
        });
    }
    assert.deepEqual(capture.errors, []);
});

test("tool failure emits the failure hook without raw result output", async () => {
    const capture = harness();
    await start(capture);
    await capture.invoke("tool_execution_start", {
        type: "tool_execution_start",
        toolCallId: "failed-call",
        toolName: "bash",
        args: { command: "false" },
    });
    await capture.invoke("tool_execution_end", {
        type: "tool_execution_end",
        toolCallId: "failed-call",
        toolName: "bash",
        result: { privateOutput: "not captured" },
        isError: true,
    });

    assert.deepEqual(payload(capture.calls[0]), {
        hook_event_name: "PostToolUseFailure",
        session_id: "pi-session",
        cwd: OPTED_CWD,
        tool_name: "Bash",
        tool_use_id: "failed-call",
        tool_input: { command: "false" },
        tool_response: { success: false },
    });
});

test("turn end captures only final assistant text capped at 240 characters", async () => {
    const capture = harness();
    await start(capture);
    await capture.invoke("turn_end", {
        type: "turn_end",
        turnIndex: 1,
        message: {
            role: "assistant",
            content: [
                { type: "thinking", thinking: "private" },
                { type: "text", text: "x".repeat(300) },
            ],
        },
        toolResults: [],
    });

    assert.deepEqual(payload(capture.calls[0]), {
        hook_event_name: "Stop",
        session_id: "pi-session",
        cwd: OPTED_CWD,
        last_assistant_message: "x".repeat(240),
    });
});

test("session compact captures the saved summary", async () => {
    const capture = harness();
    await start(capture);
    await capture.invoke("session_compact", {
        type: "session_compact",
        compactionEntry: { summary: "compact summary" },
        fromExtension: false,
        reason: "threshold",
        willRetry: false,
    });

    assert.deepEqual(payload(capture.calls[0]), {
        hook_event_name: "PostCompact",
        session_id: "pi-session",
        cwd: OPTED_CWD,
        trigger: "threshold",
        compact_summary: "compact summary",
    });
});

test("non-opted cwd remains a completely silent no-op", async () => {
    const capture = harness({ opted: false });
    await start(capture);
    await capture.invoke("turn_end", {
        type: "turn_end",
        turnIndex: 1,
        message: { role: "assistant", content: [{ type: "text", text: "done" }] },
        toolResults: [],
    });
    await capture.invoke("session_compact", {
        type: "session_compact",
        compactionEntry: { summary: "summary" },
        fromExtension: false,
        reason: "manual",
        willRetry: false,
    });

    assert.deepEqual(capture.calls, []);
    assert.deepEqual(capture.errors, []);
});

test("opt-in existence is cached and rechecked at session start", async () => {
    let opted = false;
    const capture = harness({ opted: () => opted });
    const turn = {
        type: "turn_end",
        turnIndex: 1,
        message: { role: "assistant", content: [{ type: "text", text: "done" }] },
        toolResults: [],
    };

    await start(capture);
    await capture.invoke("turn_end", turn);
    opted = true;
    await start(capture);
    await capture.invoke("turn_end", turn);

    assert.equal(capture.existsChecks(), 2);
    assert.equal(capture.calls.length, 1);
});

test("ingest failure and timeout return normally with one stderr line", async (t) => {
    for (const [name, error] of [
        ["failure", Object.assign(new Error("exit 2"), { code: 2 })],
        ["timeout", Object.assign(new Error("timed out"), { killed: true })],
    ]) {
        await t.test(name, async () => {
            const capture = harness({ execError: error });
            await start(capture);
            await assert.doesNotReject(() => capture.invoke("turn_end", {
                type: "turn_end",
                turnIndex: 1,
                message: { role: "assistant", content: [{ type: "text", text: "done" }] },
                toolResults: [],
            }));
            assert.equal(capture.errors.length, 1);
            assert.equal(capture.errors[0], "contextdb: capture failed");
        });
    }
});

test("a synchronous handler error never propagates", async () => {
    const capture = harness({ existsError: new Error("internal") });

    await assert.doesNotReject(() => start(capture));
    assert.deepEqual(capture.calls, []);
    assert.deepEqual(capture.errors, ["contextdb: capture failed"]);
});
