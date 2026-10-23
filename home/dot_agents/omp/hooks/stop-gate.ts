/**
 * stop-gate: refuse to end an orchestrator seat's turn while it owes a reply on the hcom bus.
 *
 * Loaded with `omp -e ~/.agents/omp/hooks` (omp 18.11.3 scans a directory one level deep for
 * `.ts` files, src/extensibility/extensions/directory-resolution.ts:101-140, loader.ts:652-656).
 * It hooks `session_stop`, fired when a main-agent turn is about to settle
 * (src/extensibility/shared-events.ts:109-119; registration extensions/types.ts:1661). A result
 * `{decision: "block", reason}` schedules one hidden continuation turn with `reason` as the model's
 * context (extensions/runner.ts:1689-1692, session/agent-session.ts:5196-5198 and :5291-5301).
 * `block` is exempt from the continuation cap (agent-session.ts:5276), so once `stop_hook_active`
 * says the gate already blocked this settle (agent-session.ts:5264) it answers `{continue: true,
 * reason}` instead, which the cap of 8 bounds (agent-session.ts:470).
 *
 * Environment: HCOM_DIR (the bus store, read by bus-history.sh), HCOM_TEAM (the thread the seat's
 * TASK lines name), HCOM_NAME or `hcom list self name` (the seat's own hcom name),
 * OMP_STOP_GATE_ALLOW_OPEN=1 (end the turn anyway, with the warning). Without a team or a name the
 * gate is inert and says so once per stop.
 */
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

export type OpenItem = { taskId: string; owes: string; id: number };

type Ctx = { cwd: string; hasUI: boolean; ui: { notify(message: string, type?: "info" | "warning" | "error"): void } };

// omp's parseFlag truthy set (pi-utils src/env.ts:472-482).
const TRUTHY = new Set(["1", "y", "Y", "true", "TRUE", "yes", "YES", "on", "ON"]);

// bus-history.sh keeps the newest --limit rows (default 200), so an old debt would fall out of a busy
// thread's window. Ask for far more than a program writes, and never trust a window that is full.
export const HISTORY_LIMIT = 100_000;

// Per kind (its AGMSG- prefix dropped), what a row from the seat / from another seat does to its
// task: a string opens it with that debt, null closes it, undefined leaves it alone. The newest
// moving row per task_id decides, so a HOLD or MERGED after a RESULT closes it and a new TASK reopens it.
// A VERDICT closes from any seat: the audit seat answers the seat's `U<n>-audit` TASK under that same
// task_id (hcom-audit SKILL), while the seat's debt on `U<n>` itself waits for its own VERDICT, MERGED or HOLD.
const MOVES: Record<string, [seat: string | null | undefined, other: string | null | undefined]> = {
	TASK: ["awaiting RESULT", undefined],
	RESULT: [undefined, "owes a VERDICT, MERGED or HOLD line"],
	VERDICT: [null, null],
	MERGED: [null, undefined],
	HOLD: [null, undefined],
};

/** Open items in bus-history.sh rows (`id<TAB>at<TAB>from<TAB>to<TAB>kind<TAB>body`, ascending by id). */
export function openItems(tsv: string, seat: string): OpenItem[] {
	const latest = new Map<string, OpenItem | null>();
	for (const line of tsv.split("\n")) {
		const [id, , from, , kind = "", body = ""] = line.split("\t");
		const taskId = /(?:^|\s)task_id=(\S+)/.exec(body)?.[1];
		const move = MOVES[kind.replace(/^AGMSG-/, "")]?.[from === seat ? 0 : 1];
		if (!taskId || move === undefined) continue;
		latest.set(taskId, move === null ? null : { taskId, owes: move, id: Number(id) });
	}
	return [...latest.values()].filter((item): item is OpenItem => item !== null).sort((a, b) => a.id - b.id);
}

export function gateMessage(open: OpenItem[], team: string): string {
	const items = open.map(item => `${item.taskId} ${item.owes} (row ${item.id})`).join("; ");
	return `stop-gate: ${open.length} open item(s) on hcom thread ${team}: ${items}. Answer them, wait with \`hcom listen\`, or send \`HOLD v1 task_id=<id> note=<why>\` on the thread; OMP_STOP_GATE_ALLOW_OPEN=1 ends the turn with this warning.`;
}

function run(command: string, args: string[], cwd?: string): { out: string; error?: string } {
	// 64 MiB holds a full HISTORY_LIMIT window of long rows; the default 1 MiB would report ENOBUFS first.
	const result = spawnSync(command, args, {
		cwd,
		encoding: "utf8",
		timeout: 20_000,
		maxBuffer: 64 * 1024 * 1024,
		stdio: ["ignore", "pipe", "pipe"],
	});
	if (result.status === 0) return { out: result.stdout };
	return { out: "", error: (result.stderr || result.error?.message || `exit ${result.status}`).trim() };
}

function warn(ctx: Ctx, message: string): void {
	if (ctx.hasUI) ctx.ui.notify(message, "warning");
	else process.stderr.write(`${message}\n`);
}

export default function stopGate(pi: ExtensionAPI): void {
	const team = process.env.HCOM_TEAM ?? "";
	const allowOpen = TRUTHY.has(process.env.OMP_STOP_GATE_ALLOW_OPEN ?? "");
	const since = new Date().toISOString().replace(/\.\d+Z$/, "Z");
	let seat = process.env.HCOM_NAME ?? "";
	pi.on("session_stop", (event, ctx) => {
		seat ||= run("hcom", ["list", "self", "name"]).out.trim();
		if (!team || !seat) {
			warn(ctx, `stop-gate: inert, ${team ? "the seat has no hcom name" : "HCOM_TEAM is unset"}; the turn ends unchecked.`);
			return;
		}
		const args = [team, "--limit", String(HISTORY_LIMIT), "--since", since];
		const history = run(join(ctx.cwd, "scripts/orchestrator/bus-history.sh"), args, ctx.cwd);
		if (history.error !== undefined) {
			warn(ctx, `stop-gate: bus unread (${history.error}); the turn ends unchecked.`);
			return;
		}
		if (history.out.split("\n").filter(line => line !== "").length >= HISTORY_LIMIT) {
			warn(ctx, `stop-gate: bus history is full at ${HISTORY_LIMIT} rows since ${since}, so older debts may be hidden; the turn ends unchecked.`);
			return;
		}
		const open = openItems(history.out, seat);
		if (open.length === 0) return;
		const message = gateMessage(open, team);
		warn(ctx, message);
		if (allowOpen) return;
		return { decision: event.stop_hook_active ? undefined : "block", continue: true, reason: message };
	});
}
