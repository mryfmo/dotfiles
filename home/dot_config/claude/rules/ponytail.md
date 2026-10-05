## Ponytail

- Use Ponytail (`ponytail@ponytail`) on coding work when available: prefer YAGNI, existing code, the standard library, native platform features, installed dependencies, and the smallest correct diff, in that order.
- Ponytail is not code golf: never remove trust-boundary validation, data-loss handling, security, accessibility basics, or explicitly requested behavior.
- The default mode is `full`; override it only when needed with `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off` or Ponytail commands. Restart Claude Code after `make update` refreshes the plugin.
