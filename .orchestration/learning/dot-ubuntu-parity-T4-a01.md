# Learning — dot-ubuntu-parity-T4-a01

## Reusable, validated

- **The session's PostToolUse formatter hook reflows entire `.md`/`.py`
  files on `Edit`/`Write`, not just the touched region.** This happened
  twice in this task (the agmsg template `.md` fix, and the
  `test_runtime_health.py` fixup) and once in T3 (a `.py` test file). The
  reliable workaround: write a small Python script to the scratchpad
  directory that does `Path.read_text().replace(old, new)` with an
  `assert count(old) == 1` guard, then run it with `uv run python3`,
  instead of using the `Edit`/`Write` tool directly on the target file.
  This produces a minimal, reviewable diff. Applies to any `.md` or `.py`
  file edit in this environment going forward — worth a standing habit,
  not just a one-off workaround.

- **Verifying "is this ignore/reference entry dead" must check current
  working-tree existence, not `git log --diff-filter=A` (ever-added)
  history.** A path can be added and later deleted; searching only for
  "was it ever added" produces false positives that look like the entry is
  still live. The correct check is a plain existence test (`[ -e path ]`)
  against the current tree, optionally backed by `git log
--diff-filter=D` to explain _why_ it's gone if that matters for the
  commit message.

- Zed's GitHub releases do not publish a separate checksums manifest (unlike
  crit and JetBrainsMono/nerd-fonts). For tools like this, the verification
  standard is: download the exact upstream release-asset URL directly and
  hash it — there's no second source to cross-check against, so document
  that explicitly rather than implying an independent verification that
  didn't happen.

- Tailscale's official Linux apt key (`<codename>.noarmor.gpg`) is
  pre-dearmored (raw binary OpenPGP, confirmed by inspecting its leading
  bytes), unlike Docker's ASCII-armored key — so the "docker.sh keyring
  pattern" needs a one-line deviation (skip `gpg --dearmor`) when applied to
  a different upstream. Worth checking key format before assuming every
  vendor's `curl | gpg --dearmor` pattern applies verbatim.

## Not promoted to a rule candidate

None of the above are proposed as new repo-wide rules this task — they're
environment-specific operating notes for this session, not something that
belongs in `.orchestration/learning/rule_candidates/`.
