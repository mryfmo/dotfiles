[PR #412](https://github.com/mryfmo/dotfiles/pull/412), head `2b6fc7f`: two findings.

1. **P1 · High confidence · `scripts/validate-agent-assets.py:1632`** — `.toml.tmpl` files bypass structured parsing, allowing TOML continuation syntax to conceal a literal credential assignment from the raw scanner.

   Reproduction in an applied `.toml.tmpl` file:

   ```toml
   [tasks.audit]
   run = """export ANTHROPIC_API_\
     KEY=audit_dummy"""
   ```

   TOML decodes this to `export ANTHROPIC_API_KEY=audit_dummy`. The validator returns **0 without diagnostics**; identical content in `.toml` returns **1**. Classify and inspect rendered structured templates. This is outside the documented runtime-assembly residual: the retained TOML parser already detects it.

2. **P2 · High confidence · `scripts/validate-agent-assets.py:1733`** — List-item fences are not recognized, so `- ```sh\n  ANTHROPIC_API_KEY\n  ```` produces only a note and exits **0**, despite the required refusal of credential occurrences in code blocks.

   Independently reproduced the recorded `a05-worker-verification-1`. Assignment-bearing controls still refuse. The recorded a06 ownership does not resolve the finding.

Threat-table assessment:

| Control row | Assessment |
|---|---|
| Validator | Fixed regex matches the task exactly; template discovery and Markdown classification have the findings above. |
| Tests | Existing corpus passes; it misses the template bypass. |
| a05 artifact directory | Scoped artifacts observed; predecessor records remain historical. |
| Comparison-lint baseline | Added hash matches only the intended line 1626. |
| Task copies | Current SHA matches the report; independent dispatch equality and first-push bookkeeping remain unverified. |
| Evidence records | No repository secret-pattern or home-path flags across 31 changed evidence files; live CI claims remain unverified. |
| Applied-file inputs | Fixed Git discovery, symlink exclusion and diagnostic redaction hold; structured-template inspection does not. |
| Task metadata | Dispatch/acceptance consistency checks remain external and unverified. |
| Metadata separators | Front-matter boundary is present; independent whole-file binding remains unverified. |
| In-process effects | Parsers and renderer inspect data without executing applied scripts or shell expansions. |
| Workflow/interpreter/environment | Unchanged; missing PyYAML and failed discovery refuse validation. |
| New/renamed executables | None introduced. |
| Merge | Procedural control; not executed or verified here. |
| Update-branch | Procedural control; refreshed integration evidence remains external. |
| Forced worker removal | Procedural control; not executed or verified here. |

Validation: 425 corpus rows passed 595 in-memory entry-point checks; 36 redaction regressions passed; the actual tracked applied-tree check passed with cached PyYAML. No additional injection, unsafe-deserialization, authorization or path-traversal finding was established.

📝 まとめ: Read-only security review completed with one P1 and one P2; acceptance remains with the orchestrator.

Not checked: live GitHub CI (`gh` connectivity failed), the full fixture-writing suite, or integration gates. No files were changed.
Verdict: incorrect