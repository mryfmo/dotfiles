declare module "@earendil-works/pi-coding-agent" {
    export interface SessionStartEvent {
        type: "session_start";
        reason: "startup" | "reload" | "new" | "resume" | "fork";
    }

    export interface ToolExecutionStartEvent {
        type: "tool_execution_start";
        toolCallId: string;
        toolName: string;
        args: any;
    }

    export interface ToolExecutionEndEvent {
        type: "tool_execution_end";
        toolCallId: string;
        toolName: string;
        result: any;
        isError: boolean;
    }

    export interface TurnEndEvent {
        type: "turn_end";
        turnIndex: number;
        message:
            | { role: "assistant"; content: ({ type: "text"; text: string } | { type: string })[] }
            | { role: string; content?: unknown };
        toolResults: unknown[];
    }

    export interface SessionCompactEvent {
        type: "session_compact";
        compactionEntry: { summary: string };
        fromExtension: boolean;
        reason: "manual" | "threshold" | "overflow";
        willRetry: boolean;
    }

    export interface ExtensionContext {
        cwd: string;
        sessionManager: { getSessionId(): string };
    }

    export interface ExtensionAPI {
        on(event: string, handler: (event: any, ctx: ExtensionContext) => Promise<void>): void;
    }
}

declare module "node:child_process" {
    export interface ChildProcess {
        stdin: { end(input: string): void } | null;
    }

    export function execFile(
        file: string,
        args: string[],
        options: { cwd: string; encoding: "utf8"; timeout: number },
        callback: (error: Error | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
}

declare module "node:fs" {
    export function existsSync(path: string): boolean;
}

declare module "node:path" {
    export function join(...paths: string[]): string;
}

declare module "node:os" {
    export function homedir(): string;
}
