import { expect, test } from "bun:test";
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import stopGate, { gateMessage, HISTORY_LIMIT, openItems } from "../stop-gate";

// One bus-history.sh row: id, at, from, to, kind (first word), body.
const row = (id: number, from: string, text: string): string =>
	[id, "2026-10-23T05:00:00+00:00", from, "-", text.split(" ")[0], text].join("\t");

const ROWS = [
	row(3, "orch", "AGMSG-TASK v1 task_id=t1 brief=briefs/U9.md"),
	row(4, "orch", "TASK v1 task_id=t2 brief=briefs/U14.md"),
	row(5, "orch", "AGMSG-PING v1 task_id=t1"),
	row(6, "worker", "AGMSG-RESULT v1 task_id=t1 status=ready_for_review pr=https://example/pull/1 head=abc"),
	row(7, "worker", "RESULT v1 task_id=t2 status=ready_for_review pr=https://example/pull/2 head=def"),
	row(8, "orch", "TASK v1 task_id=t2-audit head=def brief=briefs/U14.md"),
	row(9, "audit", "AGMSG-VERDICT v1 task_id=t2-audit verdict=correct head=def findings=0"),
	row(10, "orch", "MERGED v1 task_id=t2 sha=0123456"),
	row(11, "orch", "TASK v1 task_id=t3 brief=briefs/U11.md"),
	row(12, "orch", "PONG v1 status=idle"),
];
const tsv = (rows: string[]): string => `${rows.join("\n")}\n`;

test("an unanswered TASK and an unjudged RESULT are open; MERGED closes, PING and PONG move nothing", () => {
	expect(openItems(tsv(ROWS), "orch")).toEqual([
		{ taskId: "t1", owes: "owes a VERDICT, MERGED or HOLD line", id: 6 },
		{ taskId: "t3", owes: "awaiting RESULT", id: 11 },
	]);
});

test("the audit seat's VERDICT closes the TASK sent to it under the same task_id and nothing else; the seat's own HOLD or VERDICT closes its debt", () => {
	expect(openItems(tsv(ROWS.slice(0, 6)), "orch").map(item => item.taskId)).toEqual(["t1", "t2", "t2-audit"]);
	expect(openItems(tsv(ROWS.slice(0, 7)), "orch").map(item => item.taskId)).toEqual(["t1", "t2"]);
	const held = [...ROWS, row(13, "orch", "HOLD v1 task_id=t3 note=waiting"), row(14, "orch", "VERDICT v1 task_id=t1 verdict=correct")];
	expect(openItems(tsv(held), "orch")).toEqual([]);
	expect(openItems("", "orch")).toEqual([]);
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

/** A scratch repository whose bus-history.sh records its argv and prints `rows`, or a window full of open TASKs. */
function seat(rows: string[], env: Record<string, string | undefined>, full = false) {
	const cwd = mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), "stop-gate-"));
	mkdirSync(join(cwd, "scripts/orchestrator"), { recursive: true });
	writeFileSync(join(cwd, "rows.tsv"), tsv(rows));
	const fake = join(cwd, "scripts/orchestrator/bus-history.sh");
	const body = full
		? `seq 1 "$3" | awk '{ print $1 "\\t2026-10-23T05:00:00+00:00\\torch\\t-\\tTASK\\tTASK v1 task_id=t" $1 }'`
		: `cat "${cwd}/rows.tsv"`;
	writeFileSync(fake, `#!/bin/sh\nprintf '%s\\n' "$*" > "${cwd}/argv"\n${body}\n`);
	chmodSync(fake, 0o755);
	const saved: Record<string, string | undefined> = {};
	for (const [key, value] of Object.entries({ HCOM_TEAM: "u9team", HCOM_NAME: "orch", OMP_STOP_GATE_ALLOW_OPEN: undefined, ...env })) {
		saved[key] = process.env[key];
		if (value === undefined) delete process.env[key];
		else process.env[key] = value;
	}
	const handlers = new Map<string, Handler>();
	stopGate({ on: (event: string, handler: Handler) => handlers.set(event, handler) } as never);
	for (const [key, value] of Object.entries(saved)) {
		if (value === undefined) delete process.env[key];
		else process.env[key] = value;
	}
	const warnings: string[] = [];
	const ctx = { cwd, hasUI: true, ui: { notify: (message: string, type?: string) => warnings.push(`${type}: ${message}`) } };
	const stop = (stop_hook_active = false) => handlers.get("session_stop")!({ type: "session_stop", stop_hook_active }, ctx);
	return { cwd, warnings, stop };
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
	expect(inert.warnings).toEqual(["warning: stop-gate: inert, HCOM_TEAM is unset; the turn ends unchecked."]);
});
