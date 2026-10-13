[P1] High — `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:25`: The trust-boundary row still declares four acceptance-record fixtures, while item 3 requires seven; update the row so all three new adversarial fixtures are explicitly covered.

[P2] High — `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:94`: Validation still requires “the four new tests” although item 3 now requires at least nine, so completion evidence can omit the five additional tests, including the required `parse_constant` test.

[P2] High — `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:104`: The amendment summary says two fixtures are added, contradicting item 3 and the review task, which add three: wrong-PR, duplicate-key, and NaN.

Amendment verdict: dotfiles-T128-gate-evidence-a03: revise