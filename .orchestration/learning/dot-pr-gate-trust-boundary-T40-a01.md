# T40 learning triage

[memory:failure] Matching merge-bases prevents shrinking the PR diff but does not authenticate collector code from a descendant commit. A malicious sibling branch can preserve the merge-base while replacing or deleting the collector. Tests reproduced both attacks; execution is now pinned to the independently verified GitHub base SHA.

[memory:failure] Resolving only the evidence target allows another changed symlink path to be omitted. Validate the specified path and its resolved target, and exclude only the intended lexical entry. Both directions are covered by runnable regression tests.

No rule or skill promotion. Worklog creation is waived for T40. Task-local evidence and independent-review findings are saved in the authorized validation files.

[memory:failure] macOS represents temporary paths through /var while Git reports /private/var. Comparing lexical absolute paths directly to a resolved repository root rejects valid evidence. Normalize only ancestor aliases at/above the repository, keeping internal symlink paths lexical. A Linux test with a parent-directory alias reproduces this portability error.

[memory:failure] A user-selected older diff base must not also define the accepted fixed-commit range: a merged side-parent can make base commits appear new. Use the independently authenticated GitHub base for dispositions. Clear GH_REPO during local repository discovery, compare evidence repo, and explicitly pass the verified repo to both metadata lookup and recollection. GitHub reviews exposed both issues; failing reproductions and independent follow-up verified commit 10dfc10.
