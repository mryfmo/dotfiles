# T32 learning triage

## Candidates

1. `herdr pane wait-output` also searches output already in the pane, per its
   help text: "including existing output". Any marker waited for in a
   *reused* pane needs a per-run nonce, or it matches the previous run at
   once. The wait regex should also require content the echoed command line
   cannot contain, such as `:[0-9]+` versus the literal `:%s`.
2. `cmd | tee file; echo $?` reports tee's status. Wrap the pipeline in
   `bash -c 'set -o pipefail; …'` when the exit status matters and the target
   shell is an interactive pane of unknown flavor.
3. `herdr-agents` tab scoping (`panes_on_pane_tab`) applies only after
   worker/claude pane selection in full-mode heal. `empty_pane_id` sees every
   pane in the workspace. Any new helper-owned pane in a pair workspace must
   carry a label that `empty_pane_id` excludes, as `files` and `audit` now do.
   The mutation baseline showed the worker being started inside such a pane.
4. herdr 0.9.1 `tab create` accepts `--label`, so no follow-up `tab rename`
   is needed.

5. The agmsg delivery miss happened again: the T32 `AGMSG-PING`
   (2026-09-27T23:30:34Z) produced no Monitor event and no turn notice for
   `claude-standard-dot-a005`, the same shape as T31 learning 7. Until the
   cause is understood, a worker acting under a non-session identity should
   run `inbox.sh <team> <identity>` at each milestone (push, CI green, before
   RESULT). The root cause is not established.

## Promotion

None. These are candidates only; the task does not allow promotion.
