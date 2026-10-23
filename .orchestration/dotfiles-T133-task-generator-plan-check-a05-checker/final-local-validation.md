# Final local validation observation

The actual process for make validate-agent-assets in /private/tmp/a012-a05-selected-tree completed with exit 0; complete stdout/stderr is clean-candidate-assets.log and ends with agent asset validation ok. This checkout exported selected Git tree dbd3b9d540dfa4802c5963cfab9bc3074526c804, containing the final production/test SHA256 bindings recorded in scanner-fixed-bindings.log. Later changes in this directory update evidence only, including this observation, the command manifest, validation assembly and measurements; no production/test byte changed.

The original dirty worker worktree scan (precommit-assets.log) actually exited 2 on .orchestration/dotfiles-T133-task-generator-plan-check-a03/validation-commands.json, an unrelated untracked predecessor file outside this task's allowed_files. That artifact was preserved, not deleted, edited or retained in this PR. This clean candidate validates the proposed changeset without importing predecessor state. Local Git provides validation provenance only, never canonical design approval.

Base make validate-agent-assets also actually exited 0 in base-assets.log. Earlier premature asset-pass text was withdrawn before publication and the failed outputs remain preserved. Required final-head CI and Bot observations follow in RESULT; no CI pass is claimed before observing it.

The full staged git diff --check exits2 because unmodified captured command outputs contain trailing spaces (notably unittest progress and shfmt diff context); raw evidence is intentionally kept verbatim. The explicit production/test staged diff check exits0 in source-diff-check-final.log. This is separate from required Python/Markdown formatter results, both exit0 after staging all selected paths.
