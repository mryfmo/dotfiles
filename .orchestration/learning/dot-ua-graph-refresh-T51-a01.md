# Learning: dot-ua-graph-refresh-T51-a01

1. **UA 2.9.7 incremental gate vs unparsed scripts.** Unowned callables in files that scan as language unknown (extension-less shell, misnamed Python modify_ scripts) block publication even with unchanged IDs; check the plan's files for such paths before dispatching analyzers, since a block there is certain. Status: validated (merge exit 1).
2. **A tree's .ua graph is not that tree's baseline.** The graph whose meta names commit X may be committed after X; take the old graph from the commit whose meta.gitCommitHash is X. Status: validated.
