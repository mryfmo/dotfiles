[P2] high .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:38 `-I` leaves system-site initialization enabled (`no_site=0` here), so `.pth` files and `sitecustomize` can load nonstdlib code; add `-S` or explicitly declare and control those startup inputs.

[P2] high .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:38 The input inventory omits inherited `HOME`, physical cwd and filesystem symlink state needed by the re-plan’s normalisation, leaving their sources and trust seam unspecified under C-57.

[P3] high .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-review-a01.md:17 The stop condition still expects premise 2 to replay `absent`, whereas the amended task records—and this checkout returns—`present`.

Hashes match; changes are limited to the workflow row and Amendment section; checker and mask checks pass; premises replay `present`/`present`.

Not checked: implementation, CI or live browser behavior; the runtime guarantees above remain unresolved.
Task-file verdict: dotfiles-T128-project-map-pane-open-a01-followup-a01: revise