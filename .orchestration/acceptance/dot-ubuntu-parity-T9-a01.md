# dot-ubuntu-parity-T9-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot
evidence:
  - visibility guard at ${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user path with rationale comments
  - validation shows both branches exercised verbatim (real unit present -> proceeds; fake HOME -> skip exit 0)
cost: n/a
