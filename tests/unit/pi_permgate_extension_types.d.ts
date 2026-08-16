declare module "@earendil-works/pi-coding-agent" {
    export interface ToolCallEvent {
        toolName: string;
        input: Record<string, unknown>;
    }

    export interface ExtensionContext {
        mode: "tui" | "rpc" | "json" | "print";
        hasUI: boolean;
        ui: {
            confirm(title: string, message: string): Promise<boolean>;
        };
    }

    export interface ExtensionAPI {
        on(
            event: "tool_call",
            handler: (
                event: ToolCallEvent,
                ctx: ExtensionContext,
            ) => Promise<{ block: true; reason: string } | undefined>,
        ): void;
    }
}

declare module "node:child_process" {
    export interface ChildProcess {
        stdin: { end(input: string): void } | null;
    }

    export function execFile(
        file: string,
        args: string[],
        options: { encoding: "utf8"; timeout: number },
        callback: (error: Error | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
}
