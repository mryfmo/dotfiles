# Learning triage: dotfiles-T129-doctor-sleep-disabled-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A doctor check that reads a system setting is written as its own script with stubs for the binaries it reads (`uname`, `pmset` on PATH), so the test runs on every OS and the Linux branch is a case, not a skip.
2. [memory:decision] `make doctor` inside the Claude sandbox reports the runtime check as failed because the sandbox denies the network host mise's version check needs; the Check asks for the status as is, so the record pastes it with that reason rather than re-running outside the sandbox.
