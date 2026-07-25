# T30 validation

Worktree: `/Users/mryfmo/Workspace/dotfiles-t30`

```text
$ git -C /Users/mryfmo/Workspace/dotfiles-t30 status --short
(no output; clean after commit)

$ git -C /Users/mryfmo/Workspace/dotfiles-t30 show --stat HEAD
commit c67a662894f92f61164c843836debf49c7c45e87
Author: mryfmo <mryfmo@gmail.com>
Date:   Sat Jul 25 10:23:05 2026 +0900

    chore(orchestration): sync T29 regime default-on evidence

 .../autoskill/runs/T29-agmsg-regime-default-on.md  |  3 +
 .../learning/T29-agmsg-regime-default-on.md        |  3 +
 .../reports/T29-agmsg-regime-default-on.md         | 14 ++++
 .../sandboxes/T29-agmsg-regime-default-on.md       |  7 ++
 .../tasks/T29-agmsg-regime-default-on.md           | 77 ++++++++++++++++++++++
 .../tasks/T30-orchestration-evidence-sync.md       | 54 +++++++++++++++
 .../validation/T29-agmsg-regime-default-on.md      | 24 +++++++
 7 files changed, 182 insertions(+)

$ diff <main-copy> <t30-copy>  # repeated for all seven authorized paths after the two authorized corrections
(no output; all seven files are byte-identical)
```
