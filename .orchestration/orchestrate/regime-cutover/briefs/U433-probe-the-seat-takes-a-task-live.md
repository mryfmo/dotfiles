# U433 probe: a worker seat takes a TASK live (table row f26)

GOAL
Table row f26 (`tests/autonomous-change-flow.tsv`, seat-takes-task-live) asks whether a live worker seat takes a TASK line from the bus: the dispatch prints a receipt, the seat's `hcom list -v` line moves from `now: listening` to `active` within 75 seconds, and the seat answers on the thread. This brief is that TASK's content: it asks for one line and nothing else.

SCOPE
Nothing of the repository changes. The seat writes one line on the bus.

CONTEXT
The seat is an omp worker seat started by `hcom-seat worker` under srt. The TASK line names this brief.

DATA SHAPE
One RESULT line.

CHANGE
1. Send exactly one line on the team thread `regime`: `RESULT v1 task_id=U433 status=ready_for_review pr=none head=none note=probe answered`. 2. Stop.

ACCEPTANCE
1. The RESULT line above appears on the bus (`hcom events --type message`), sent by the seat.

VERIFY
The coordinator reads the bus.

CLOSURE
remove

TRUST
TRUST: the probe trusts the bus as the record of the seat's answer; it changes nothing.

TIMEBOX
5 minutes.

FORBIDDEN
No file written, no command run beyond `hcom send`, no second line.

REPORT
The one line.

STANDING
`tests/autonomous-change-flow.tsv` row f26.
