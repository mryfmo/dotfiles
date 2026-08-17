import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

import type {
    ExtensionAPI,
    ExtensionContext,
    SessionCompactEvent,
    SessionStartEvent,
    ToolExecutionEndEvent,
    ToolExecutionStartEvent,
    TurnEndEvent,
} from "@earendil-works/pi-coding-agent";

type ExecFile = typeof execFile;
type ExistsSync = typeof existsSync;
type ReportError = (message: string) => void;
type Payload = Record<string, unknown>;

const HOOK_TOOL_NAMES: Record<string, string> = {
    bash: "Bash",
    read: "Read",
    write: "Write",
    edit: "Edit",
    grep: "Grep",
    find: "Find",
};

function safe<E>(
    handler: (event: E, ctx: ExtensionContext) => Promise<void> | void,
    reportError: ReportError,
) {
    return async (event: E, ctx: ExtensionContext): Promise<void> => {
        try {
            await handler(event, ctx);
        } catch {
            try {
                reportError("contextdb: capture failed");
            } catch {
                // Reporting must never propagate into Pi's event loop.
            }
        }
    };
}

function primaryToolInput(toolName: string, args: Record<string, unknown>): Payload {
    const tool = toolName.toLowerCase();
    if (tool === "bash" && typeof args.command === "string") {
        return { command: args.command };
    }
    if (["read", "write", "edit"].includes(tool) && typeof args.path === "string") {
        return { path: args.path };
    }
    if (["grep", "find"].includes(tool) && typeof args.pattern === "string") {
        return { pattern: args.pattern };
    }
    return {};
}

function assistantText(event: TurnEndEvent): string {
    if (event.message.role !== "assistant" || !Array.isArray(event.message.content)) {
        return "";
    }
    const text = event.message.content
        .filter((part) => part.type === "text")
        .map((part) => part.text)
        .join("");
    return [...text].slice(0, 240).join("");
}

function ingest(
    cliPath: string,
    cwd: string,
    payload: Payload,
    execFileImpl: ExecFile,
): Promise<void> {
    return new Promise((resolve, reject) => {
        const child = execFileImpl(
            "python3",
            [cliPath, "ingest", "--ingested-from", "pi"],
            { cwd, encoding: "utf8", timeout: 5000 },
            (error) => error ? reject(error) : resolve(),
        );
        if (!child.stdin) {
            reject(new Error("contextdb stdin unavailable"));
            return;
        }
        child.stdin.end(JSON.stringify(payload));
    });
}

export default function contextdbExtension(
    pi: ExtensionAPI,
    execFileImpl: ExecFile = execFile,
    existsSyncImpl: ExistsSync = existsSync,
    reportError: ReportError = (message) => console.error(message),
) {
    let cliPath: string | undefined;
    const toolArgs = new Map<string, Record<string, unknown>>();

    const capture = (ctx: ExtensionContext, payload: Payload): Promise<void> => {
        if (!cliPath) {
            return Promise.resolve();
        }
        return ingest(cliPath, ctx.cwd, {
            ...payload,
            session_id: ctx.sessionManager.getSessionId(),
            cwd: ctx.cwd,
        }, execFileImpl);
    };

    pi.on("session_start", safe<SessionStartEvent>((_event, ctx) => {
        cliPath = undefined;
        toolArgs.clear();
        const candidate = join(ctx.cwd, ".claude", "hooks", "contextdb_cli.py");
        if (existsSyncImpl(candidate)) {
            cliPath = candidate;
        }
    }, reportError));

    pi.on("tool_execution_start", safe<ToolExecutionStartEvent>((event) => {
        const args = event.args;
        toolArgs.set(event.toolCallId, args && typeof args === "object" ? args : {});
    }, reportError));

    pi.on("tool_execution_end", safe<ToolExecutionEndEvent>(async (event, ctx) => {
        const args = toolArgs.get(event.toolCallId) ?? {};
        toolArgs.delete(event.toolCallId);
        await capture(ctx, {
            hook_event_name: event.isError ? "PostToolUseFailure" : "PostToolUse",
            tool_name: HOOK_TOOL_NAMES[event.toolName.toLowerCase()] ?? event.toolName,
            tool_use_id: event.toolCallId,
            tool_input: primaryToolInput(event.toolName, args),
            tool_response: { success: !event.isError },
        });
    }, reportError));

    pi.on("turn_end", safe<TurnEndEvent>(async (event, ctx) => {
        await capture(ctx, {
            hook_event_name: "Stop",
            last_assistant_message: assistantText(event),
        });
    }, reportError));

    pi.on("session_compact", safe<SessionCompactEvent>(async (event, ctx) => {
        await capture(ctx, {
            hook_event_name: "PostCompact",
            trigger: event.reason,
            compact_summary: event.compactionEntry.summary,
        });
    }, reportError));
}
