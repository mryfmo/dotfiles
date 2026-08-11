# T37 Codex Understand-Anything runtime provisioning

Implemented Codex runtime provisioning after the verified upstream installer completes.

- Selects the highest versioned Claude release-cache directory whose plugin manifest version matches the installed Codex source plugin.
- Replaces `packages/core/dist`, optional `packages/core/node_modules`, and top-level `node_modules` from that release artifact.
- Removes stale destination directories only when their source artifact exists, and prints the specified non-fatal message when no matching artifact exists.
- Falls back to lexical cache-directory sorting if a matching directory name is not numeric.
- Added lifecycle grep coverage, asset-validation tokens, and README documentation.

No installer was executed and no live home/vendor directory was modified.
