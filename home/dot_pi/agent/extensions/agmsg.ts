import { execFile } from "node:child_process";
import { homedir } from "node:os";

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

type ExecFile = typeof execFile;
type SendResult = {
    content: { type: "text"; text: string }[];
    details: { success: boolean };
    isError?: boolean;
};

const success = (): SendResult => ({
    content: [{ type: "text", text: "agmsg_send: sent" }],
    details: { success: true },
});

const failure = (message = "agmsg_send: failed"): SendResult => ({
    content: [{ type: "text", text: message }],
    details: { success: false },
    isError: true,
});

function sendMessage(
    script: string,
    args: string[],
    execFileImpl: ExecFile,
): Promise<void> {
    return new Promise((resolve, reject) => {
        execFileImpl(
            script,
            args,
            { encoding: "utf8", timeout: 10000 },
            (error) => error ? reject(error) : resolve(),
        );
    });
}

export default function agmsgExtension(
    pi: ExtensionAPI,
    execFileImpl: ExecFile = execFile,
    identity: string | undefined = process.env.AGMSG_PI_IDENTITY,
    home: string = homedir(),
) {
    // Pi v0.84.1 docs/extensions.md:1338-1365 defines this prompt/schema shape.
    // Permgate gates bash/read/write/edit only; this tool is safe through fixed-path argv construction.
    pi.registerTool({
        name: "agmsg_send",
        label: "Send agmsg message",
        description: "Send one message through agmsg with the worker identity pinned by the bridge.",
        promptSnippet: "Send AGMSG-RESULT messages through the agmsg bus",
        promptGuidelines: [
            "Use agmsg_send to send every AGMSG-RESULT message; final assistant text is not the RESULT.",
        ],
        parameters: Type.Object({
            team: Type.String({ description: "agmsg team name" }),
            to: Type.String({ description: "recipient agent identity" }),
            body: Type.String({ description: "complete one-line agmsg message" }),
        }, { additionalProperties: false }),
        async execute(_toolCallId, params) {
            if (!identity) {
                return failure("agmsg_send: missing AGMSG_PI_IDENTITY");
            }
            const script = `${home}/.agents/skills/agmsg/scripts/send.sh`;
            try {
                await sendMessage(
                    script,
                    [params.team, identity, params.to, params.body],
                    execFileImpl,
                );
                return success();
            } catch {
                return failure();
            }
        },
    });
}
