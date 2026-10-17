# Evidence consistency

[memory:failure] Updating a report while leaving tracked validation at an older blocked state makes the PR proof incomplete, even when current validation exists in untracked supplements.

[memory:decision] Keep the committed implementation-head snapshot self-contained. A later evidence-only commit states which immutable implementation head it proves, demonstrates unchanged source/tests and reports its own CI/Bot separately after publication.
