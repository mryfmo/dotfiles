[P1] high .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md:71 origin/main supports neither `uv-tool` nor the proposed hcom installer, and its validator rejects `uv-tool`; specify plan 023’s exact-version UV installation and include the necessary schema changes in allowed_files.

[P2] high .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md:71 Require a manifest-pinned SHA-256 of the omp installer before execution, because its own payload checksum does not satisfy the existing installer-script flow’s verification of the downloaded script.

[P2] high .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md:23 The claimed Bats coverage of check-tools is absent from item 4, whose binary-version assertions would still pass if both reporting probes were omitted.

[P2] high .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md:82 Stop condition 4 requires pasted checker and mask results, but neither is recorded in this file, although replay returned `OK`, `masked 0 match(es)`, and both recorded premise outputs.

Not run: Bats or installers; remote freshness remains unverified because GitHub DNS resolution failed.
Task-file verdict: dotfiles-T129-assets-omp-hcom-a01: revise