# Learning: dotfiles-T104-pins-2026-10-06-a01

- **Classify each test hit before syncing a pin.** A grep for old versions turns up both live assertions and fixtures. Here every hit was a fixture: a synthetic manifest, a fake release listing, or a fake `setup.sh`, kept independent of the live manifest on purpose. `make unit-test` passing unchanged confirms it. Syncing them would have broken that independence.
