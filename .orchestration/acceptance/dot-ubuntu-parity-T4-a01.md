# dot-ubuntu-parity-T4-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - commits 0d53cc5 4d6f348 c09a062 a8a1a8b 481fb0f (+b14239e artifacts); diff scope within allowed_files
  - independent re-run: make format clean / validate-agent-assets ok / unit-test 376 OK (skipped=1)
  - Zed v1.20.2 release existence and BOTH arch SHA256 independently confirmed against GitHub asset digests
    (gh api .assets[].digest == installer-pins values) — stronger than worker's single-source hash
  - gnome_settings.sh: session+writability guards, unmappable list documented; natural-scroll/screensaver
    correctly NOT invented (absent from defaults.sh) — endorsed over the task's example list
  - B13b Chromium in misc.sh main() adds ~200MB snap install to CI misc bats — accepted (parity intent;
    revisit if CI time degrades). Tailscale keyring deviation (already-binary noarmor.gpg) verified rationale
  - self-caught fixup 481fb0f reviewed (upgrade_fixture zed mocks) — endorsed
  - CompactionDB decision befac170-eb33-46f8-859f-1a7d2e2a6581 registered (worker DB)
cost: n/a
