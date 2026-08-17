import { execFile } from "node:child_process";

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

type ExecFile = typeof execFile;
type Decision = "allow" | "deny" | "ask";
type Action =
    | { tool: "bash"; command: string; cwd: string }
    | { tool: "read" | "write" | "edit"; path: string; cwd: string };

const BLOCKED = { block: true, reason: "blocked by policy" } as const;

function normalizedAction(
    toolName: string,
    input: Record<string, unknown>,
    cwd: unknown,
): Action | undefined {
    if (typeof cwd !== "string") {
        return undefined;
    }
    if (toolName === "bash" && typeof input.command === "string") {
        return { tool: toolName, command: input.command, cwd };
    }
    if (
        (toolName === "read" || toolName === "write" || toolName === "edit") &&
        typeof input.path === "string"
    ) {
        return { tool: toolName, path: input.path, cwd };
    }
    return undefined;
}

function askPermgate(action: Action, execFileImpl: ExecFile): Promise<Decision> {
    return new Promise((resolve, reject) => {
        const child = execFileImpl(
            "permgate",
            ["pi"],
            { encoding: "utf8", timeout: 7000 },
            (error, stdout) => {
                if (error) {
                    reject(error);
                    return;
                }
                const match = /^\{"decision":"(allow|deny|ask)"\}\n$/.exec(stdout);
                if (!match) {
                    reject(new Error("malformed permgate decision"));
                    return;
                }
                resolve(match[1] as Decision);
            },
        );
        if (!child.stdin) {
            reject(new Error("permgate stdin unavailable"));
            return;
        }
        child.stdin.end(JSON.stringify(action));
    });
}

export default function permgateExtension(pi: ExtensionAPI, execFileImpl: ExecFile = execFile) {
    pi.on("tool_call", async (event, ctx) => {
        if (!["bash", "read", "write", "edit"].includes(event.toolName)) {
            return undefined;
        }
        const action = normalizedAction(event.toolName, event.input, ctx.cwd);
        if (!action) {
            return BLOCKED;
        }
        try {
            const decision = await askPermgate(action, execFileImpl);
            if (decision === "allow") {
                return undefined;
            }
            if (decision === "ask" && ctx.mode === "tui" && ctx.hasUI) {
                const confirmed = await ctx.ui.confirm(
                    "Permission required",
                    `Allow ${event.toolName} tool call?`,
                );
                return confirmed ? undefined : BLOCKED;
            }
        } catch {
            return BLOCKED;
        }
        return BLOCKED;
    });
}
