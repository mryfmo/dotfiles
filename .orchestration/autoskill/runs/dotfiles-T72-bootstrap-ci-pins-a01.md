# Autoskill: dotfiles-T72-bootstrap-ci-pins-a01

- **Decision:** no new skill.
- **Candidate:** a check that workflow `GITHUB_ENV` names avoid tool-owned prefixes (`MISE_`). It is recorded in the learning file; it is a single occurrence, so it was not promoted.
- **User correction:** none.
- **Task errors:** the `MISE_PIN` CI failure (fixed in `52ec8f88`), and a mid-task slip: I rewrote a captured output with `sed` before discarding and recapturing it.
