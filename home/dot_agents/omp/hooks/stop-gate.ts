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
 * Team: the `--hcom-team <team>` flag this extension registers, which `hcom-seat` passes with exactly the team
 * it launched the seat on, then HCOM_TEAM. hcom passes HCOM_DIR into the pane it launches but not HCOM_TEAM
 * (measured in the U33 pilot), and a team guessed from the seat's checkout would read another thread when the
 * launcher was given an explicit team, so the gate never derives one. At session start the chosen team is
 * exported as HCOM_TEAM, so the seat's own commands inherit it. Environment: HCOM_DIR (the bus store, read by
 * bus-history.sh), HCOM_NAME or `hcom list self name` (the seat's own hcom name), OMP_STOP_GATE_ALLOW_OPEN=1
 * (end the turn anyway, with the warning). Without a team or a name the gate is inert and says so once per
 * stop. bus-history.sh is the copy chezmoi installs read-only at `$HOME/.local/bin/common/bus-history.sh`
 * (regime-cutover U31, U33), never a script from the seat's cwd, so a worktree of a pull request cannot answer
 * the gate with its own rows.
 */
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

export type OpenItem = { taskId: string; owes: string; id: number };

type Ctx = { cwd: string; hasUI: boolean; ui: { notify(message: string, type?: "info" | "warning" | "error"): void } };

// omp's parseFlag truthy set (pi-utils src/env.ts:472-482).
const TRUTHY = new Set(["1", "y", "Y", "true", "TRUE", "yes", "YES", "on", "ON"]);

// bus-history.sh keeps the newest --limit rows (default 200), so an old debt would fall out of a busy
// thread's window. Ask for far more than a program writes, and never trust a window that is full.
export const HISTORY_LIMIT = 100_000;

/** The installed bus-history.sh, resolved from HOME when the gate is registered (never from the cwd). */
export function busHistoryPath(home = process.env.HOME ?? homedir()): string {
	return join(home, ".local/bin/common/bus-history.sh");
}

/** The CLI flag `hcom-seat` passes after `--` (omp hands it to this extension; U33c). */
export const TEAM_FLAG = "hcom-team";

// hcom's team grammar.
const TEAM = /^[a-z0-9][a-z0-9_-]{0,63}$/;

/** The team the launcher selected: the flag, else HCOM_TEAM; never one guessed from the cwd. */
export function chooseTeam(flag: unknown, env: string | undefined): { team: string; error?: string } {
	const [team, source] = typeof flag === "string" && flag !== "" ? [flag, `--${TEAM_FLAG}`] : [env ?? "", "HCOM_TEAM"];
	if (team === "") return { team: "", error: `launched without --${TEAM_FLAG} and HCOM_TEAM is unset` };
	if (!TEAM.test(team)) return { team: "", error: `${source} ${JSON.stringify(team)} is not an hcom team name` };
	return { team };
}

// Per kind (an older sender's `AGMSG-` prefix is ignored), what a row from the seat / from another seat does to its
// task: a string opens it with that debt, null closes it, undefined leaves it alone. The newest
// moving row per task_id decides, so a HOLD or MERGED after a RESULT closes it and a new TASK reopens it.
export const MOVES: Record<string, [seat: string | null | undefined, other: string | null | undefined]> = {
	TASK: ["awaiting RESULT", undefined],
	RESULT: [undefined, "owes a VERDICT, MERGED or HOLD line"],
	VERDICT: [null, undefined],
	MERGED: [null, undefined],
	HOLD: [null, undefined],
};

/** Open items in bus-history.sh rows (`id<TAB>at<TAB>from<TAB>to<TAB>kind<TAB>body`, ascending by id). */
export function openItems(tsv: string, seat: string): OpenItem[] {
	const latest = new Map<string, OpenItem | null>();
	const tasked = new Map<string, string>();
	// The seats this seat's TASK for an id went to: one name, or a comma list for a thread send.
	const sentTo = (taskId: string, name: string) => (tasked.get(taskId) ?? "").split(",").includes(name);
	for (const line of tsv.split("\n")) {
		const [id, , from, to, kind = "", body = ""] = line.split("\t");
		const taskId = /(?:^|\s)task_id=(\S+)/.exec(body)?.[1];
		if (!taskId) continue;
		// An older sender's `AGMSG-` prefix is ignored, so a seat still sending it keeps closing items (U35).
		const name = kind.replace(/^AGMSG-/, "");
		let move = MOVES[name]?.[from === seat ? 0 : 1];
		if (from === seat && name === "TASK") tasked.set(taskId, to);
		// Another seat's row opens a debt only on a task this seat sent to that very seat, so a peer's RESULT on its
		// own unit never holds a worker seat, which shares the thread (U33c: every seat loads the gate). Another
		// seat's VERDICT is text: a worker must not settle the seat's debt on its own unit.
		if (from !== seat && typeof move === "string" && !sentTo(taskId, from)) move = undefined;
		if (move === undefined) continue;
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
	pi.registerFlag(TEAM_FLAG, { description: "The hcom team this seat was launched on (hcom-seat passes it)", type: "string" });
	const envTeam = process.env.HCOM_TEAM;
	let chosen: { team: string; error?: string } | undefined;
	// omp parses extension flags after the extensions load, so the flag is read at session start (measured: getFlag
	// is undefined while the extension loads and holds the value at session_start), or at the first stop.
	const resolveTeam = () => {
		if (chosen) return chosen;
		chosen = chooseTeam(pi.getFlag(TEAM_FLAG), envTeam);
		if (chosen.team) process.env.HCOM_TEAM = chosen.team;
		return chosen;
	};
	const allowOpen = TRUTHY.has(process.env.OMP_STOP_GATE_ALLOW_OPEN ?? "");
	const since = new Date().toISOString().replace(/\.\d+Z$/, "Z");
	let seat = process.env.HCOM_NAME ?? "";
	const busHistory = busHistoryPath();
	pi.on("session_start", () => {
		resolveTeam();
	});
	pi.on("session_stop", (event, ctx) => {
		seat ||= run("hcom", ["list", "self", "name"]).out.trim();
		const { team, error } = resolveTeam();
		if (!team || !seat) {
			const why = team ? "the seat has no hcom name" : `no team (${error})`;
			warn(ctx, `stop-gate: inert, ${why}; the turn ends unchecked.`);
			return;
		}
		const args = [team, "--limit", String(HISTORY_LIMIT), "--since", since];
		const history = run(busHistory, args, ctx.cwd);
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
