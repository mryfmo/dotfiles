declare module "typebox" {
    interface StringSchema {
        readonly __type: string;
    }
    interface ObjectSchema<P> {
        readonly __type: { [K in keyof P]: P[K] extends StringSchema ? string : never };
    }
    export const Type: {
        String(options?: { description?: string }): StringSchema;
        Object<P>(properties: P, options?: { additionalProperties?: boolean }): ObjectSchema<P>;
    };
}

declare module "@earendil-works/pi-coding-agent" {
    interface ToolResult {
        content: { type: "text"; text: string }[];
        details: { success: boolean };
        isError?: boolean;
    }
    interface ToolDefinition<P> {
        name: string;
        label: string;
        description: string;
        promptSnippet: string;
        promptGuidelines: string[];
        parameters: P;
        execute(
            toolCallId: string,
            params: P extends { readonly __type: infer T } ? T : never,
        ): Promise<ToolResult>;
    }
    export interface ExtensionAPI {
        registerTool<P>(tool: ToolDefinition<P>): void;
    }
}

declare module "node:child_process" {
    export function execFile(
        file: string,
        args: string[],
        options: { encoding: "utf8"; timeout: number },
        callback: (error: Error | null, stdout: string, stderr: string) => void,
    ): unknown;
}

declare module "node:os" {
    export function homedir(): string;
}

declare const process: { env: { AGMSG_PI_IDENTITY?: string } };
