# Learning triage: dotfiles-T128-chain-github-scripts-followup-a01

These are candidates only; nothing is promoted.

1. [memory:failure] A shell line continuation inside single quotes is not a continuation. My first draft split the single-quoted GraphQL mutation with a trailing `\`, which would have sent a literal backslash and newline inside the query. GraphQL rejects that outside a string. shellcheck and shfmt both passed it: shellcheck reported only SC2016, the `$threadId` inside single quotes. The draft was caught by reading the diff before any test ran.
   - Mechanism candidate: keep a GraphQL text that holds `$` variables in one single-quoted constant on one line, with the SC2016 directive saying why. A test that pins the exact mutation text, as `test_resolve_threads_passes_the_thread_id_as_a_graphql_variable` now does, catches the next one.
2. [memory:decision] An owner task whose rows come from several sources (a Bot thread, a local review, the audit) can list one defect under several ids. The acceptance record's `audit_findings` reasons said which ids were the same defect. Reading them first turned five rows into three changes, each with its test. The report maps every row to its change and test, so the audit can check the row-to-hunk claim without re-deriving it.
3. [memory:decision] Naming the beyond-row candidates in an alive PONG before `gh pr ready` (learning 4 of `dotfiles-T128-chain-review-scripts-a01`) costs no INV-6 count, because it is not a question. The orchestrator can then write an owner for them before the Bot raises any of them.
