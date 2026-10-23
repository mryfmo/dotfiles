# Plan 025 v13 → v14: dispositions of review round 12 (R12V-01〜17, R12R-01〜13 = 30 件)

- Inputs: `025-review-r12-verification.md`（17 行）、`025-review-r12-redteam.md`（13 行）、`025-pilot-facts.md` #S0/#B1/#B1 fix round 1/#B1'/#B2/#B3/#B3b、`025-pilot-bridge-omp-compat.patch`（69 行、sha256 `cc0ff8671f82330b…`）、`025-v13-facts-20261023.md`、`025-replan-v13-20261023.md`、plan v13（416 行、sha256 `0c1013a9…`）、D-024-129/130。
- This is the single review round for v13 (plan-before-dispatch): the residual list below is the freeze mechanism, not another round. Priorities are the reviewers'. `where` = plan v14 line unless a file is named.
- Counts: fixed-in-v14 27, handout-only 1, not-applicable 1 (R12R-10, refutation pasted), operator-decision 1 (R12R-08, default applied), residual 0. No residual P1.

| id | P | disposition | where (v14 line or file) | one line |
| --- | --- | --- | --- | --- |
| R12V-01 | P1 | fixed-in-v14 | :157-:161, :111, handout | §4 #19〜#22 rewritten as the operator's handout steps (B1/B1'/B2 done with pasted results, B3/B3b done = negative, B3c next, B4〜B9); the `npm pack` production form moves to W2d's installer and is measured at W2d merge (§7 :242); W2d's dependency names the handout outputs (B3c `-e` form, B5c tool list, B5b `PI_CODING_AGENT_DIR`) |
| R12V-02 | P2 | fixed-in-v14 | :116, :119 | W5b depends on W2a/W2c/W2d/W2e merge + W2b RESULT (PR held to X-0); X depends on the W2b PR being open and audited, merge = X-0 |
| R12V-03 | P2 | fixed-in-v14 | :201, :86 | C-2 row and §2 row now say W5b minimal form after W1/W2 (W4 post-X) and ≤ 150 行【仮定】, full form ≤ 250 行 at W5a |
| R12V-04 | P2 | fixed-in-v14 | :232 | Counted: 15 pre-X operator rows in §7 (採択, J-N2, W1, 5 merge-直後 rows, X 手順 0/1/2/4/5/6, the per-PR row ≈ 10 times); the text now states 15 and that v13 added 4 of them |
| R12V-05 | P2 | fixed-in-v14 | :112, :331 | `gpt-6-astra` tagged 【仮定】 (absent from both facts files), `gpt-6.1-sol` is the measured fallback【実測 pilot-facts #S0】; #23 (:163) measures the id inside the extension and records the error text |
| R12V-06 | P2 | fixed-in-v14 | :334, :112 | `stream:true` is forced by the extension and the request-capture test asserts it; facts §3 `stream:!0` is cited as the codex path only |
| R12V-07 | P2 | fixed-in-v14 | :247 | `audit\|audit-r2\|security` escaped |
| R12V-08 | P3 | fixed-in-v14 | :84, :117, :251 | the three code-span pipes escaped |
| R12V-09 | P3 | fixed-in-v14 | :244, :246 | 4th cell merged into the 3rd |
| R12V-10 | P3 | fixed-in-v14 | :27, :293 | `api.anthropic.com`・`claude.ai` tagged 【仮定】 (closed post-X by 第 2 脚 #11) |
| R12V-11 | P3 | fixed-in-v14 | :293 | hosts cited as 【実測 facts §4】 |
| R12V-12 | P3 | fixed-in-v14 | :112 | `OAuthCallbackFlow` host/path configurability tagged 【未計測】, closed by #23; fallback = own loopback listener |
| R12V-13 | P3 | fixed-in-v14 | :400 | 決定 36 gains 代替 (remove the E1 hook-skip interim at X 手順 6) |
| R12V-14 | P3 | fixed-in-v14 | :36, :101, :256, :290 | hand-merge set unified to the v13 set (≈ 10: W2a, W2b = X-0, W2c, W2d ×2, hook skip, W2e ×2, W5b, W6a, W6b); W3/W0c/W5a/W8/ruleset PR marked X 後 |
| R12V-15 | P3 | fixed-in-v14 | :111, :242 | interactive omp (default profile) gets the bridge by `omp install <install_path>` as the installer's last step (the #B1'/#B2 measured form); seats use `-e`; `openai-siwc` symlink stays chezmoi's (W2e) |
| R12V-16 | P3 | fixed-in-v14 | `025-replan-v13-20261023.md` appendix「v14 で変わった点」 | plan :60/:111 already assign the validator rule + fixture to W2d; the appendix records the omission in re-plan item 1 |
| R12V-17 | P3 | handout-only | handout B7 | B7 records either `slept` or the 120 s timeout text as a measurement (plan :160/:324 already did) |
| R12R-01 | P1 | fixed-in-v14 | :94, :111, :157, :394, :401 (決定 37) | bridge = vendored-with-patch: upstream tarball (shasum `fe28fda3…`, integrity facts §2) + repo patch applied before dependency install; receipt = tarball shasum + patch sha256 + SDK + darwin-arm64 versions; 決定 30 names the patched tree with its `node_modules`; further bridge changes are W2d patch PRs |
| R12R-02 | P1 | fixed-in-v14 | :270 | STOP A7 rewritten: round 1 = omp compat patch (done, #B1'); later load failures are W2d patch PRs, not rounds; the only operator decision point is "abandon the bridge route → `anthropic/` API-key fallback" |
| R12R-03 | P2 | fixed-in-v14 | :111, :157, :158, :394 | `--omit=peer` dropped (`typebox` is a peer imported by `src/askclaude-schema.ts`); the production tree is staged in the trusted path with `node_modules` and loaded by `-e …/src/index.ts`; B3c measures that form on the plugin-store copy before W2d |
| R12R-04 | P2 | fixed-in-v14 | :324, :160, :402 (決定 38) | mechanism corrected: the bridge injects `timeout=120` into omp's bash tool argument; W2d patch removes the injection (default; alternative = configurable); B7 measures |
| R12R-05 | P2 | fixed-in-v14 | :111, :160, :270, :327, :395 | hook skip keys on `PI_CODING_AGENT_DIR` (omp sets `PI_CODING_AGENT_DIR`/`_SESSION_DIR`, no bare name); B5b prints `env \| grep -c PI_CODING_AGENT_DIR` through the bridged bash tool |
| R12R-06 | P2 | fixed-in-v14 | :112, :251, :337, :392 | profiles isolate auth → one SIWC login per profile (audit, audit-r2, security), each its own moment in X 手順 1; 決定 28 names the shared host-id file `~/.omp/agent/openai-siwc/host.json` holding `ext_agent_host_id` + issued `client_id` per accountId; assertion = one `omp-dotfiles` agent after 3 logins |
| R12R-07 | P2 | fixed-in-v14 | :112, :330 | W2e 仕様 lists the fields to strip/rewrite (`prompt_cache_retention`, `max_output_tokens`, `role: developer`/`system` items → `instructions`, no `previous_response_id`) with a request-capture test as the 検証 row |
| R12R-08 | P2 | operator-decision | :393 (決定 29), :251, :119, :95, :35 | default applied: keep the `openai-codex` logins (credentials present, unused) through X, one refresh cycle and one working day of SIWC production use; drop the §7 line at E1; alternative = X 手順 1 (the v13 default) |
| R12R-09 | P2 | fixed-in-v14 | :161, :247 | #22 records the keychain item count before/after; the conditional 3 × `claude login` row exists at :247 (B-3 merge 直後 = before W5a's first seat) |
| R12R-10 | P3 | not-applicable | :329, :394, :158 | Refuted by measurement after the review: pilot-facts #B3b `omp --profile pilot-bridge -e /tmp/claude-501/pcb-patched1/package --no-extensions models claude-bridge` → `No models matching "claude-bridge"`; the loader resolves a directory through `indexNames: ["index.ts","index.js"]` at the root (`loader.ts:527,652`) and does not read `pi.extensions`. v14 therefore uses `-e <trusted path>/pi-claude-bridge/src/index.ts` and keeps the measurement row (B3c) |
| R12R-11 | P3 | fixed-in-v14 | :110 (W2c), :342 | deny-word list (`gh pr merge`, `gh api -X PUT/POST/PATCH/DELETE`, `curl`, `python3 -c`, `~/.ssh`, `~/.config/gh`) added to W2c's amendment with a fixture; 第 1 脚 #14 asserts each |
| R12R-12 | P3 | fixed-in-v14 | :344 | `【実測 v12 §2】` |
| R12R-13 | P2 | fixed-in-v14 | :157, handout | #19 records B1 (failed), fix round 1 (patch sha256 `cc0ff8671f82330b…`) and B1' (passed) with pasted results; the rollback line names `omp plugin uninstall pi-claude-bridge` for the plugin-store copy and leaves the scratch tree |

Post-review pilot facts folded into v14 (not findings): #B2 passed (plugin-store copy at `~/.omp/plugins/node_modules/pi-claude-bridge`, doctor 4 ok); #B3 negative (`PLUGINS_DIR = path.join(getAgentDir(), "plugins")`, `--profile` switches the agent dir → the default-profile plugin is invisible to seat profiles = 決定 30's `-e` rationale); #B3b negative (see R12R-10). Next operator step = B3c in the handout.
