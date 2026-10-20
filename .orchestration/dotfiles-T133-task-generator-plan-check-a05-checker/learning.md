# Learning triage

Validated observations:

- Shared lexical normalization must reject forbidden forms after normalization; checking raw prefixes before removing ./ permits a semantic bypass. Applies to task-path parsers.
- A no-follow directory walk must still check a scope's relevant directory-symlink prefix for confinement before filtering complete matches. Skipping traversal must not suppress a boundary finding.
- Fixed-prefix association cannot distinguish *.py from *.sh at the same root. Full matching patterns must determine each concrete token's entry before directory/child precedence is applied.
- Positive same-byte tests must check authorization was retained, not only exit0: a warning-and-skip mutation can otherwise survive.
- A temporary baseline clone needs the relevant main refs as well as identical source; missing refs create unrelated guard failures. Preserve and label invalid runs rather than calling all failures inherited.
- Pass a clean child environment as subprocess env rather than NAME=value arguments to env when preserving credentials; argument-boundary assertions must accompany received-environment assertions.

No skill, memory, canonical decision or broad repository rule was promoted. The repairs are validated by saved real-CLI regressions,24 killed mutations and fresh independent review; the root recorded re-plan:glob-filter and a separate owner for regime fixture grammar. AutoSkill status is separate. Parent execution and cache-hardening requirements remain their named owners' work.

Validated after owner2750: run the repository's changed-file comparison-lint regression before publication, since a baseline-clean file can acquire statement-local R4 hits after selective porting. Existing lexical normalization and POSIX path APIs satisfy that rule without new baseline rows; actual pre-fix6R4/exit1 and post-fix CI-named test/exit0. Temporary tool paths can disappear across task turns: preserve exact command/runtime hashes and obtain an explicit owner rebuild disposition rather than silently switching tools after an unavailable operation.

Validated revise1: lexical Unicode normalization must not replace the enumerated filesystem object at confinement; non-followed directory symlinks still need explicit rejection/coverage; item-row validation must count every occurrence and reject multi-item rows even if valid standalone rows also exist. Named real-CLI red/green controls and four independent mutations verify these cases; Unicode-sensitive filesystem behavior is modeled on native-insensitive Mac.
