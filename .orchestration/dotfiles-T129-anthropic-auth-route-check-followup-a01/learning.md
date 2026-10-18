# Learning triage: dotfiles-T129-anthropic-auth-route-check-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A check over files whose syntax has quoting, escapes and delimiters reads them through their parser, not a regex over raw lines: PR #389 spent three rounds on raw-line bypasses of one root (quoted keys, `+=`, `\u` escapes). Parse to data, walk every key path once, and keep the line grammar only for text formats.
2. [memory:decision] In a chezmoi source tree a file's suffix does not decide its format: `modify_`, `run_`, `symlink_` and `encrypted_` sources hold a script, a link target or ciphertext. Strip the attribute prefixes from the basename first; eight of this repository's 35 `.json`/`.toml`/`.yaml` sources are `modify_` scripts.
3. [memory:decision] `json.loads` and `yaml.safe_load` keep the last of duplicate keys, so a literal can hide behind a later reference. `object_pairs_hook` and the YAML node graph (`yaml.compose_all`) keep every pair; walk YAML nodes once each so aliases cannot multiply the work.

## Strict decode before parse

Replacement decoding turns malformed UTF8 into valid structured strings. Classify first, strictly decode structured sources, and report only fixed error type because exception text may expose bytes. Text behavior unchanged. RED/GREEN covers3 formats and script compatibility.
