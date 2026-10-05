- [P2] high implementation `scripts/generate-agent-configs.py:701` — `Path.is_dir()` follows symlinks, whereas Codex excludes symlinked version directories. With a real `4.12.0` directory and a `local` symlink, this implementation hashes `local` while Codex loads `4.12.0`, replacing valid trust with a mismatched hash. Exclude symlinks and add a regression test. [Codex source](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/core-plugin-common/src/installed.rs)

- [P2] high implementation `scripts/generate-agent-configs.py:659` — The SemVer regex accepts numeric prerelease identifiers with leading zeros. Reproduction: it selects `1.10.0-01` over `1.9.0`; Codex’s parser rejects the former as SemVer and falls back to lexical ordering, selecting `1.9.0`. This also hashes the wrong installed hook. Match the parser’s validity rules before comparing versions. [Parser source](https://raw.githubusercontent.com/dtolnay/semver/master/src/parse.rs)

Specification: changed files fit the amended scope, and all five required evidence artifacts exist. The earlier sandbox deviation is explicitly recorded and dispositioned.

Evidence: all 41 generated outputs match the final head in an independent in-memory check; the known permgate hash reproduces. Pasted final validation matches all 12 successful checks in the feedback JSON. That JSON contains **no Bot review threads**; it records quota/skipped-review notices, consistent with the worker’s report. Live GitHub verification through `gh` was unavailable.

📝 まとめ: Audited the named changeset and evidence; two plugin-version selection defects require correction.

Verdict: incorrect