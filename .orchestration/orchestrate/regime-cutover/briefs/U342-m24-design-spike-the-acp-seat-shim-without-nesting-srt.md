# U342 M-24 design spike: how a DSH control host inside srt starts an omp worker in a sibling sandbox, since srt does not nest

GOAL
The plan's M-24 (the ACP seat shim lever `acp-seat`, tasks T-M-24-01 to 13) assumed `dsh-subagent-acp`, running inside the DSH control host's srt sandbox, spawns `acp-seat`, which runs `srt --settings <worker> -- omp acp`: a second srt inside the first. The M-22 spike measured that srt 0.0.81 does not nest on macOS (six variants: `listen EACCES` on the mux socket, `sandbox_apply: Operation not permitted` with allowAllUnixSockets; decisions rows of phase M-22, 2026-11-06T23:14:30Z), and ADR-002 forbids `allowNestedUserNamespaces` on Linux, so the shim cannot start a sibling sandbox from inside the Router's. R-45 still requires the Router and every Worker in separate srt sandboxes. This spike measures the candidate designs on this host, records what holds, and ends with one recommended shape for M-24, in decisions rows and a short design note; it changes no tracked file.

SCOPE
Scratch only: `SPIKE=$(mktemp -d "${TMPDIR:-/tmp}/m24-spike.XXXXXX")`, outputs under `/tmp/m24/`. Reads: the repository at `/tmp/dotfiles-wt/U313` (a read-only worktree; read the installed lever `~/.local/bin/common/hcom-seat` for the dsh and router rows' settings shape, `seat_sandbox_write`, the canary), the installed srt package (`~/.local/share/mise/installs/npm-anthropic-ai-sandbox-runtime/0.0.81/lib/node_modules/@anthropic-ai/sandbox-runtime/`, its README and `dist/` for `allowLocalBinding`, `allowUnixSockets`, the proxy and mux socket behaviour), the M-22 artefacts (`/tmp/m22/`, `/tmp/dotfiles-wt/U313-report.txt`, the shim `/tmp/dsh-spike-acp.*/bin/acp-shim-spike` if present). May write: `/tmp/m24/design.md` (the note), `/tmp/dotfiles-wt/U342-rows.tsv` (proposed decisions rows, six columns, phase `M-24`), the progress and report files. Not: any file of the repository or the store; no install; no real dsh turn.

CONTEXT
Three candidate shapes. (A) Broker: a seat-launcher process outside every sandbox (started by `hcom-seat` beside the Router, or a per-host daemon of the kit) listens on a loopback port or a Unix socket; inside the Router's sandbox, the ACP agent command `dsh-subagent-acp` spawns is a thin client that connects and relays the ACP stdio stream; the broker starts `srt --settings <worker> -- omp acp` in a sibling sandbox per connection and pipes it. (B) Pre-started workers: `hcom-seat` starts N worker sandboxes ahead of time, each `omp acp` listening on a loopback port the Router may reach; the Router's ACP command is a client to one of them. (C) Same-level worker: `omp acp` runs inside the Router's own sandbox (no second sandbox), bounded by the omp policy denies alone; this breaks R-45 and is recorded as the rejected baseline with its measured exposure, not built. The measurements that decide between A and B: whether a process inside an srt sandbox with the dsh role's settings (allowLocalBinding false) can connect out to a loopback TCP port served outside; whether it can connect to a Unix socket outside its write roots (read-only path) or inside a read root; whether srt's own proxy intercepts loopback; whether the router role's `allowLocalBinding true` changes the answer; whether an outside process can pipe a sandboxed child's stdio with no loss (a 1 MiB JSON-RPC round trip through the relay); and the cost of a pre-started worker (idle omp acp memory, start time) against a per-connection start.

DATA SHAPE
One table in the design note: rows A, B, C; columns `what it needs from srt`, `measured here`, `R-45 holds`, `R-44 holds (one canary before omp)`, `what hcom-seat gains`, `what the Router's profile gains`, `cost`. One recommendation paragraph naming the shape, the new lever or lever change (one sentence each), the srt settings deltas (exact keys), and the tests M-24 writes first. Every measured cell cites its command and output file under `/tmp/m24/`.

CHANGE
1. Build the scratch sandboxes: write two srt settings files by hand in the dsh row's shape (read it from the installed lever's rendering of a dry run, or copy from `/tmp/m22/srt-settings-worker.json`), one with `allowLocalBinding` false (the dsh row) and one true (the router row); write a tiny outside TCP server (`python3 -c` on 127.0.0.1, a random port) and a Unix-socket server under `$SPIKE/sock`. 2. From inside each sandbox, connect to the TCP port and to the Unix socket (`python3 -c` client); record success or the refusal text; repeat with the socket under a read-only grant and under a write grant. 3. Relay round trip: outside the sandbox start `srt --settings <worker> -- python3 -c '<echo server on stdin/stdout>'` with stdio piped through a relay process that also serves the loopback port; from inside the Router's sandbox send a 1 MiB JSON-RPC-shaped line through the client and compare bytes. 4. Cost of B: start `srt --settings <worker> -- omp acp --help` (or `omp --version` under srt) and time it; read its RSS for ten seconds if `omp acp` can idle without stdin closing (else record that it cannot idle). 5. Write the note and the rows; the recommendation names A or B with the measurements that decided it, and names C as rejected with its reason. 6. `git -C /tmp/dotfiles-wt/U313 status --porcelain > /tmp/m24/status.txt` prints nothing; `git -C ~/Workspace/dotfiles status --porcelain --untracked-files=all -- . ':!.orchestration' > /tmp/m24/status-main.txt` equals the baseline taken before step 1.

ACCEPTANCE
1. `/tmp/m24/connect-dsh-tcp.txt`, `connect-dsh-unix.txt`, `connect-router-tcp.txt`, `connect-router-unix.txt` each hold the client's result line (pasted). 2. `/tmp/m24/relay.txt` holds the byte count sent and received and `equal` or the first differing offset (pasted). 3. `/tmp/m24/cost-b.txt` holds the start time and the RSS line or `cannot idle` (pasted). 4. The design note's table has three rows and seven columns with every measured cell citing a file; the recommendation paragraph names one shape. 5. `/tmp/dotfiles-wt/U342-rows.tsv` holds two or more rows of phase `M-24`, six tab-separated columns, no path under `.private`, no kit name. 6. The two status files as CHANGE 6 says (pasted).

VERIFY
ACCEPTANCE pasted into the report; the coordinator reads the note and the rows and writes the M-24 brief from the recommendation.

CLOSURE
remove

TRUST
TRUST: the spike trusts srt 0.0.81 as installed and its documented settings keys as the boundary it measures; it trusts the dsh row's settings shape as rendered by the installed lever; it writes only under `$SPIKE` and `/tmp/m24/`, reads no credential, runs no real dsh or omp turn against a model.

TIMEBOX
60 minutes.

FORBIDDEN
No tracked file change; no install; no `allowNestedUserNamespaces`; no real model turn; no network beyond loopback; no write under `~/.dsh`, `~/.omp`, `~/.local/state`, `~/Workspace`; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/m24/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`; never edit the live store; the deliverables are the files under `/tmp/m24/` and `/tmp/dotfiles-wt/U342-rows.tsv`.
- Progress line at `/tmp/dotfiles-wt/U342-progress.txt`; final report to `/tmp/dotfiles-wt/U342-report.txt`.

REPORT
Status, the recommended shape in one sentence with the two measurements that decided it, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 41, 44, 46); `decisions.tsv` rows of phase M-22 (2026-11-06T23:13:00Z to 23:17:32Z) and the records row 2026-11-07T03:41:31Z; `briefs/U313-m22-spike-dsh-subagent-acp-reaches-omp-acp-inside-srt.md`; handoff/08 §3 rows 3 and 6.
