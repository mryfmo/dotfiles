## Ponytail

- Use Ponytail (`ponytail@ponytail`) on coding work when available: prefer YAGNI, existing code, the standard library, native platform features, installed dependencies, and the smallest correct diff in that order.
- Ponytail is not code golf. Do not remove trust-boundary validation, data-loss handling, security, accessibility basics, or explicitly requested behavior.
- The managed agent asset lifecycle installs and updates Ponytail; restart Claude Code after plugin updates so lifecycle hooks and skills are loaded.
- The default upstream mode is `full`. Override only when needed with `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off` or Ponytail commands.
