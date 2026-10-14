#!/usr/bin/env bash
# @file orch-gate.sh
# @brief Run the integration gate on a PR checkout's head from the review worktree, with the task's evidence copied in.
# @description
#   Plan 007 T718, the parameterised form of the orchestrator's gate wrapper. The head is always `git -C
#   <pr-worktree> rev-parse HEAD`. From the checkout this script lives in, it requires the task's sweep JSON (whose
#   `pr` must be <pr>), the audit of this head and its `.last.md`, the review receipt, the crit JSON and the
#   acceptance record, all under `.orchestration/`, before it checks the clean review worktree
#   `.claude/worktrees/orchestrator-review` out at the head; a head that tracks a symlink under `.orchestration`
#   is refused, so no copy follows a link out of the worktree. It copies them in and runs, with the review worktree
#   as its working tree, the gate `make require-crit-review` runs, but this checkout's copy: the head's Makefile
#   and gate are PR-controlled (PR #350 thread 4265190252), so `scripts/require-crit-review.py` and the validator
#   it loads must equal origin/main's here. The interpreter is `uv python find` in this checkout, resolved before
#   the review worktree is entered and run directly, so no uv reads the head's `.python-version` or `uv.toml`
#   (uv runs an executable a `.python-version` names; the audit of f48593d6). The gate runs under `env -i` with
#   exactly PATH and HOME as this shell has them, its inputs AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE,
#   PR_FEEDBACK_EVIDENCE, REVIEW_EVIDENCE and AGENT_REVIEWED=1, and PYTHONSAFEPATH=1, as `-I -P <gate> --base
#   origin/main`: nothing else of this shell or of the head reaches the gate or the collector and gh it starts
#   (the audit of a06c874e). A trap set before the head checkout restores the review worktree to origin/main
#   whatever fails or the gate says.
# @arg $1 string Task id.
# @arg $2 path The PR's checkout (its HEAD is the gated head).
# @arg $3 int PR number.
# @exitcode 0 The gate passed.
# @exitcode 2 Usage error, or a refused precondition.
# @exitcode * Otherwise the gate's own status.
# @example
#   scripts/orchestrator/orch-gate.sh dotfiles-T128-orchestrator-tools-a05 .claude/worktrees/worker-c 350
set -euo pipefail

usage() {
    echo "usage: orch-gate.sh <task> <pr-worktree> <pr>" >&2
    exit 2
}
refuse() {
    echo "orch-gate: $1; refused" >&2
    exit 2
}
(($# == 3)) || usage
task=$1 pr=$3
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && ${pr} =~ ^[0-9]+$ ]] || usage
head="$(git -C "$2" rev-parse HEAD)"
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
review="${root}/.claude/worktrees/orchestrator-review"
v=.orchestration/validation
sweep="${v}/${task}-pr-feedback.json" audit="${v}/${task}-audit-${head:0:7}.md"
record=".orchestration/acceptance/${task}.md" receipt="${v}/${task}-review-receipt.md"
evidence=("${sweep}" "${audit}" "${audit}.last.md" "${receipt}" "${v}/${task}-crit.json" "${record}")
cd -- "${root}"
git diff --quiet origin/main -- scripts/require-crit-review.py scripts/validate-agent-assets.py ||
    refuse "the gate here differs from origin/main's"
for f in "${evidence[@]}"; do
    [[ -f ${f} ]] || refuse "${f} is missing"
done
[[ $(jq -r .pr "${sweep}") == "${pr}" ]] || refuse "${sweep} is not the sweep of PR ${pr}"
[[ -z $(git ls-tree -r "${head}" -- .orchestration | awk '$1 == "120000"') ]] ||
    refuse "${head:0:7} tracks a symlink under .orchestration (PR #350 thread 4265190259)"
python="$(uv python find)" || refuse "uv found no interpreter in ${root}"
[[ -z $(git -C "${review}" status --porcelain --untracked-files=all) ]] || refuse "the review worktree is not clean"
trap 'git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main' EXIT
git -C "${review}" checkout -q --detach "${head}"
for f in "${evidence[@]}"; do
    mkdir -p "${review}/$(dirname -- "${f}")"
    cp -- "${f}" "${review}/${f}"
done
rc=0
(
    # errexit is off left of ||, so a failed cd exits here instead of gating another tree.
    cd -- "${review}" || exit 2
    # Built, not filtered: CRIT_REVIEW=off, CRIT_REVIEWED=1 (thread 4265190267) or a PYTHONPATH that loads the head's
    # sitecustomize.py into the collector (the audit of a06c874e) cannot come along.
    env -i PATH="${PATH}" HOME="${HOME}" AUDIT_EVIDENCE="${audit}" ACCEPTANCE_EVIDENCE="${record}" \
        PR_FEEDBACK_EVIDENCE="${sweep}" REVIEW_EVIDENCE="${receipt}" AGENT_REVIEWED=1 PYTHONSAFEPATH=1 \
        "${python}" -I -P "${root}/scripts/require-crit-review.py" --base origin/main
) || rc=$?
echo "orch-gate: ${task} at ${head:0:7} for PR ${pr}: gate rc=${rc}"
exit "${rc}"
