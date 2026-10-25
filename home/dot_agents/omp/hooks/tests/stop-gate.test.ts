import { expect, test } from "bun:test";
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import stopGate, { busHistoryPath, chooseTeam, gateMessage, HISTORY_LIMIT, MOVES, openItems, TEAM_FLAG } from "../stop-gate";

// One bus-history.sh row: id, at, from, to (the delivered seat; `-` for a thread reply), kind (first word), body.
const row = (id: number, from: string, text: string, to = "-"): string =>
	[id, "2026-10-23T05:00:00+00:00", from, to, text.split(" ")[0], text].join("\t");

const ROWS = [
	row(3, "orch", "TASK v1 task_id=t1 brief=briefs/U9.md", "worker"),
	row(4, "orch", "TASK v1 task_id=t2 brief=briefs/U14.md", "worker"),
	row(5, "orch", "PING v1 task_id=t1"),
	row(6, "worker", "RESULT v1 task_id=t1 status=ready_for_review pr=https://example/pull/1 head=abc"),
	row(7, "worker", "RESULT v1 task_id=t2 status=ready_for_review pr=https://example/pull/2 head=def"),
	row(10, "orch", "MERGED v1 task_id=t2 sha=0123456"),
	row(11, "orch", "TASK v1 task_id=t3 brief=briefs/U11.md", "worker"),
	row(12, "orch", "PONG v1 status=idle"),
];
const tsv = (rows: string[]): string => `${rows.join("\n")}\n`;

test("an unanswered TASK and an unjudged RESULT are open; MERGED closes, PING and PONG move nothing", () => {
	expect(openItems(tsv(ROWS), "orch")).toEqual([
		{ taskId: "t1", owes: "owes a VERDICT, MERGED or HOLD line", id: 6 },
		{ taskId: "t3", owes: "awaiting RESULT", id: 11 },
	]);
});

test("the seat's own HOLD or VERDICT closes its debt", () => {
	expect(openItems(tsv(ROWS.slice(0, 5)), "orch").map(item => item.taskId)).toEqual(["t1", "t2"]);
	const held = [...ROWS, row(13, "orch", "HOLD v1 task_id=t3 note=waiting"), row(14, "orch", "VERDICT v1 task_id=t1 verdict=correct")];
	expect(openItems(tsv(held), "orch")).toEqual([]);
	expect(openItems("", "orch")).toEqual([]);
});

test("another seat's VERDICT settles nothing: not a worker's on its own unit, not one on a TASK sent to it, not one on an id never tasked", () => {
	const open = ROWS.slice(0, 5);
	const still = [
		{ taskId: "t1", owes: "owes a VERDICT, MERGED or HOLD line", id: 6 },
		{ taskId: "t2", owes: "owes a VERDICT, MERGED or HOLD line", id: 7 },
	];
	expect(openItems(tsv([...open, row(13, "worker", "VERDICT v1 task_id=t2 verdict=correct head=def")]), "orch")).toEqual(still);
	expect(openItems(tsv([...open, row(13, "audit", "VERDICT v1 task_id=t9-audit verdict=correct head=def")]), "orch")).toEqual(still);
	// U58: the audit is no seat, so a VERDICT from the seat an `-audit` TASK went to no longer closes that TASK.
	const tasked = [...open, row(13, "orch", "TASK v1 task_id=t2-audit head=def", "audit")];
	const awaiting = [...still, { taskId: "t2-audit", owes: "awaiting RESULT", id: 13 }];
	expect(openItems(tsv([...tasked, row(14, "audit", "VERDICT v1 task_id=t2-audit verdict=correct head=def")]), "orch")).toEqual(awaiting);
});

test("a peer's RESULT on its own unit opens nothing for a seat that did not task it (U33c: every seat loads the gate)", () => {
	// The worker's view of the shared thread: its own TASK from orch, a peer's TASK and RESULT.
	const thread = [
		row(3, "orch", "TASK v1 task_id=t1 brief=briefs/U9.md", "worker"),
		row(4, "orch", "TASK v1 task_id=t5 brief=briefs/U5.md", "peer"),
		row(5, "peer", "RESULT v1 task_id=t5 status=ready_for_review pr=https://example/pull/5 head=aaa"),
	];
	expect(openItems(tsv(thread), "worker")).toEqual([]);
	// The orchestrator still owes a VERDICT on the RESULT of a TASK it sent, also to a comma list of seats.
	expect(openItems(tsv(thread), "orch").map(item => [item.taskId, item.owes])).toEqual([
		["t1", "awaiting RESULT"],
		["t5", "owes a VERDICT, MERGED or HOLD line"],
	]);
	const listed = [row(3, "orch", "TASK v1 task_id=t7", "peer,worker"), row(4, "worker", "RESULT v1 task_id=t7 status=done")];
	expect(openItems(tsv(listed), "orch")).toEqual([{ taskId: "t7", owes: "owes a VERDICT, MERGED or HOLD line", id: 4 }]);
});

test("a retired AGMSG- prefixed kind is not a kind: it neither opens nor closes a task", () => {
	const thread = [
		row(3, "orch", "AGMSG-TASK v1 task_id=t1", "worker"),
		row(4, "orch", "TASK v1 task_id=t2", "worker"),
		row(5, "worker", "RESULT v1 task_id=t2 status=ready_for_review head=abc"),
		row(6, "orch", "AGMSG-VERDICT v1 task_id=t2 verdict=correct"),
		row(7, "orch", "TASK v1 task_id=t3", "worker"),
		row(8, "orch", "AGMSG-MERGED v1 task_id=t3 sha=0123456"),
		row(9, "orch", "TASK v1 task_id=t4", "worker"),
		row(10, "orch", "AGMSG-HOLD v1 task_id=t4 note=waiting"),
		row(11, "orch", "TASK v1 task_id=t5", "worker"),
		row(12, "worker", "AGMSG-RESULT v1 task_id=t5 status=ready_for_review head=fed"),
	];
	expect(openItems(tsv(thread), "orch")).toEqual([
		{ taskId: "t2", owes: "owes a VERDICT, MERGED or HOLD line", id: 5 },
		{ taskId: "t3", owes: "awaiting RESULT", id: 7 },
		{ taskId: "t4", owes: "awaiting RESULT", id: 9 },
		{ taskId: "t5", owes: "awaiting RESULT", id: 11 },
	]);
});

test("a status=question PONG moves nothing, from any seat (U35)", () => {
	const thread = [
		row(3, "orch", "TASK v1 task_id=t7 brief=b.md", "worker"),
		row(4, "worker", "PONG v1 task_id=t7 status=question note=scope"),
		row(5, "peer", "PONG v1 task_id=t7 status=question note=x"),
	];
	expect(openItems(tsv(thread), "orch")).toEqual([{ taskId: "t7", owes: "awaiting RESULT", id: 3 }]);
	expect(openItems(tsv(thread), "worker")).toEqual([]);
});

test("the message lists every item with its row and both ways out", () => {
	const message = gateMessage(openItems(tsv(ROWS), "orch"), "u9team");
	expect(message).toBe(
		"stop-gate: 2 open item(s) on hcom thread u9team: t1 owes a VERDICT, MERGED or HOLD line (row 6); t3 awaiting RESULT (row 11). " +
			"Answer them, wait with `hcom listen`, or send `HOLD v1 task_id=<id> note=<why>` on the thread; OMP_STOP_GATE_ALLOW_OPEN=1 ends the turn with this warning.",
	);
});

type StopResult = { decision?: "block"; continue?: boolean; reason?: string } | undefined;
type Handler = (event: { type: "session_stop"; stop_hook_active: boolean }, ctx: unknown) => StopResult;

/**
 * A scratch seat: HOME holds the installed bus-history.sh fake, which records its argv and prints `rows` (or a window
 * full of open TASKs); the cwd holds a decoy `scripts/orchestrator/bus-history.sh` that marks itself if anything runs it.
 */
function seat(rows: string[], env: Record<string, string | undefined>, full = false, flags: Record<string, string> = {}) {
	const cwd = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), "stop-gate-"));
	const home = join(cwd, "home");
	mkdirSync(join(home, ".local/bin/common"), { recursive: true });
	mkdirSync(join(cwd, "scripts/orchestrator"), { recursive: true });
	writeFileSync(join(cwd, "rows.tsv"), tsv(rows));
	const fake = busHistoryPath(home);
	const body = full
		? `seq 1 "$3" | awk '{ print $1 "\\t2026-10-23T05:00:00+00:00\\torch\\t-\\tTASK\\tTASK v1 task_id=t" $1 }'`
		: `cat "${cwd}/rows.tsv"`;
	writeFileSync(fake, `#!/bin/sh\nprintf '%s\\n' "$*" > "${cwd}/argv"\n${body}\n`);
	chmodSync(fake, 0o755);
	const decoy = join(cwd, "scripts/orchestrator/bus-history.sh");
	writeFileSync(decoy, `#!/bin/sh\ntouch "${cwd}/decoy-ran"\nprintf '1\\t2026-10-23T05:00:00+00:00\\tx\\t-\\tTASK\\tTASK v1 task_id=decoy\\n'\n`);
	chmodSync(decoy, 0o755);
	const saved: Record<string, string | undefined> = {};
	for (const [key, value] of Object.entries({ HOME: home, HCOM_TEAM: "u9team", HCOM_NAME: "orch", OMP_STOP_GATE_ALLOW_OPEN: undefined, ...env })) {
		saved[key] = process.env[key];
		if (value === undefined) delete process.env[key];
		else process.env[key] = value;
	}
	const handlers = new Map<string, Handler>();
	const registered = new Set<string>();
	// omp's order (measured, U33c): the extension loads, the CLI flags are parsed, then session_start fires.
	let parsed = false;
	stopGate({
		on: (event: string, handler: Handler) => handlers.set(event, handler),
		registerFlag: (name: string) => registered.add(name),
		getFlag: (name: string) => (parsed && registered.has(name) ? flags[name] : undefined),
	} as never);
	parsed = true;
	(handlers.get("session_start") as unknown as (() => void) | undefined)?.();
	const exported = process.env.HCOM_TEAM;
	for (const [key, value] of Object.entries(saved)) {
		if (value === undefined) delete process.env[key];
		else process.env[key] = value;
	}
	const warnings: string[] = [];
	const ctx = { cwd, hasUI: true, ui: { notify: (message: string, type?: string) => warnings.push(`${type}: ${message}`) } };
	const stop = (stop_hook_active = false) => handlers.get("session_stop")!({ type: "session_stop", stop_hook_active }, ctx);
	return { cwd, home, warnings, stop, registered, exported };
}

test("open items block the first settle and ride the capped continuation afterwards", () => {
	const { cwd, warnings, stop } = seat(ROWS, {});
	const first = stop();
	expect(first?.decision).toBe("block");
	expect(first?.continue).toBe(true);
	expect(first?.reason).toContain("t1 owes a VERDICT, MERGED or HOLD line (row 6); t3 awaiting RESULT (row 11)");
	expect(stop(true)).toEqual({ decision: undefined, continue: true, reason: first?.reason });
	expect(warnings).toEqual([`warning: ${first?.reason}`, `warning: ${first?.reason}`]);
	expect(readFileSync(join(cwd, "argv"), "utf8")).toMatch(/^u9team --limit 100000 --since \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\n$/);
});

test("a full history window is not trusted: the turn ends with a warning instead of a verdict", () => {
	const { warnings, stop } = seat([], {}, true);
	expect(stop()).toBeUndefined();
	expect(warnings).toHaveLength(1);
	expect(warnings[0]).toStartWith(`warning: stop-gate: bus history is full at ${HISTORY_LIMIT} rows since `);
});

test("all answered allows silently; OMP_STOP_GATE_ALLOW_OPEN allows with the warning; no team is inert", () => {
	const answered = seat([...ROWS, row(13, "orch", "HOLD v1 task_id=t3"), row(14, "orch", "MERGED v1 task_id=t1")], {});
	expect(answered.stop()).toBeUndefined();
	expect(answered.warnings).toEqual([]);

	const allowed = seat(ROWS, { OMP_STOP_GATE_ALLOW_OPEN: "1" });
	expect(allowed.stop()).toBeUndefined();
	expect(allowed.warnings).toHaveLength(1);
	expect(allowed.warnings[0]).toStartWith("warning: stop-gate: 2 open item(s)");

	const inert = seat(ROWS, { HCOM_TEAM: undefined });
	expect(inert.stop()).toBeUndefined();
	expect(inert.warnings).toHaveLength(1);
	expect(inert.warnings).toEqual([
		"warning: stop-gate: inert, no team (launched without --hcom-team and HCOM_TEAM is unset); the turn ends unchecked.",
	]);
});

test("bus-history.sh is the installed copy under HOME, never the one in the seat's cwd (U33)", () => {
	expect(busHistoryPath("/h")).toBe("/h/.local/bin/common/bus-history.sh");
	const { cwd, warnings, stop } = seat(ROWS, {});
	expect(stop()?.decision).toBe("block");
	expect(existsSync(join(cwd, "argv"))).toBe(true);
	expect(existsSync(join(cwd, "decoy-ran"))).toBe(false);
	expect(warnings[0]).not.toContain("decoy");
	// The rule table U33 leaves unchanged.
	expect(MOVES).toEqual({
		TASK: ["awaiting RESULT", undefined],
		RESULT: [undefined, "owes a VERDICT, MERGED or HOLD line"],
		VERDICT: [null, undefined],
		MERGED: [null, undefined],
		HOLD: [null, undefined],
	});
});

test("the launcher's --hcom-team wins over HCOM_TEAM and is exported; the cwd's slug is never read (U33c)", () => {
	const flagged = seat(ROWS, { HCOM_TEAM: undefined }, false, { [TEAM_FLAG]: "custom" });
	expect([...flagged.registered]).toEqual(["hcom-team"]);
	expect(flagged.exported).toBe("custom");
	expect(flagged.stop()?.decision).toBe("block");
	expect(readFileSync(join(flagged.cwd, "argv"), "utf8")).toStartWith("custom --limit 100000 --since ");
	const both = seat(ROWS, { HCOM_TEAM: "regime" }, false, { [TEAM_FLAG]: "custom" });
	both.stop();
	expect(readFileSync(join(both.cwd, "argv"), "utf8")).toStartWith("custom --limit ");
	const envOnly = seat(ROWS, { HCOM_TEAM: "regime" });
	envOnly.stop();
	expect(readFileSync(join(envOnly.cwd, "argv"), "utf8")).toStartWith("regime --limit ");
	// A regime-env beside the installed bus-history.sh is never consulted.
	const ignored = seat(ROWS, { HCOM_TEAM: undefined });
	writeFileSync(join(ignored.home, ".local/bin/common/regime-env"), "regime_env() { HCOM_TEAM=kitteam; }\n");
	expect(ignored.stop()).toBeUndefined();
	expect(existsSync(join(ignored.cwd, "argv"))).toBe(false);
});

test("a team that breaks hcom's grammar is refused, whichever source carried it", () => {
	expect(chooseTeam("Custom Team", "regime")).toEqual({ team: "", error: '--hcom-team "Custom Team" is not an hcom team name' });
	expect(chooseTeam(undefined, "-x")).toEqual({ team: "", error: 'HCOM_TEAM "-x" is not an hcom team name' });
	expect(chooseTeam("", "regime")).toEqual({ team: "regime" });
	const bad = seat(ROWS, { HCOM_TEAM: undefined }, false, { [TEAM_FLAG]: "x;y" });
	expect(bad.exported).toBeUndefined();
	expect(bad.stop()).toBeUndefined();
	expect(bad.warnings[0]).toBe('warning: stop-gate: inert, no team (--hcom-team "x;y" is not an hcom team name); the turn ends unchecked.');
});
