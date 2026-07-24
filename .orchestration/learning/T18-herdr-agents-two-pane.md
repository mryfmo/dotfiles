# T18 learning triage

## Candidate reusable learning

- `crit comment --help` is not a help command in the installed Crit CLI; it creates a review-level comment whose body is `--help`. Use documented `crit status --json` and `crit comments --all --json <review.json>` flows instead of probing `crit comment` with `--help`.
- Extensionless shell executables do not match this repository's `.editorconfig` `[*.sh]` section. Format and validate them with the Makefile convention explicitly: `shfmt --indent 4 --space-redirects`, not bare `shfmt`.

## Validation

- Observed directly during T18: the command created review record `r_881c9c`.
- The accidental record was replied to with an explanation and resolved before evidence export.
- Bare shfmt converted the target to tabs; the repository flags restored four-space indentation, and the target-specific diff check then passed.

## Disposition

- Keep as a learning candidate only. No rule or skill promotion was authorized by this task.
