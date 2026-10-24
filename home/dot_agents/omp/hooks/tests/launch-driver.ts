/**
 * Runs the real stop gate as omp runs it in a seat's pane, for tests/unit/test_hcom_seat.py's launch-boundary
 * regression (regime-cutover U33c): argv is the omp argv hcom-seat launched (JSON), the environment is the one the
 * fake hcom handed to omp. omp parses CLI flags after the extensions load and refuses a flag no loaded extension
 * registered (measured), so `--hcom-team` reaches the gate only once it is registered. Prints
 * `{result, warnings, team}` as JSON, where team is HCOM_TEAM after session start.
 */
import stopGate, { TEAM_FLAG } from "../stop-gate";

const argv: string[] = JSON.parse(process.argv[2] ?? "[]");
const flag = `--${TEAM_FLAG}`;
let value: string | undefined;
argv.forEach((arg, index) => {
	if (arg === flag) value = argv[index + 1];
	else if (arg.startsWith(`${flag}=`)) value = arg.slice(flag.length + 1);
});
type Handler = (...args: unknown[]) => unknown;
const handlers = new Map<string, Handler>();
const registered = new Set<string>();
let parsed = false;
stopGate({
	on: (event: string, handler: Handler) => handlers.set(event, handler),
	registerFlag: (name: string) => registered.add(name),
	getFlag: (name: string) => (parsed && registered.has(name) && name === TEAM_FLAG ? value : undefined),
} as never);
if (value !== undefined && !registered.has(TEAM_FLAG)) throw new Error(`unknown flag: ${flag}`);
parsed = true;
handlers.get("session_start")?.();
const warnings: string[] = [];
const ctx = { cwd: process.cwd(), hasUI: true, ui: { notify: (message: string) => warnings.push(message) } };
const result = handlers.get("session_stop")?.({ type: "session_stop", stop_hook_active: false }, ctx);
process.stdout.write(`${JSON.stringify({ result: result ?? null, warnings, team: process.env.HCOM_TEAM ?? null })}\n`);
