# Learning triage: dotfiles-T129-audit-inherit-replan-json-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] `git patch-id` (with or without `--verbatim`) hashes a patch's hunks without their line numbers. That is right for "the same change rebased", and wrong for "the same behaviour": a merge that moves an inserted line from one block to an identical block keeps the patch-id. The test's fixture is two copies of `L L L M L L L` with `NEW` after the first or the second `M`. Content evidence that must bind an exact tree needs a tree comparison. Here that is `git merge-tree --write-tree head^1 head^2` against `head^{tree}`: a clean merge of the two parents reproduces an honest update-branch head exactly, and any conflict resolution or extra edit does not.
2. [memory:decision] A summary that carries its evidence's origin in a first-line marker (`inherited-from: <sha7>`) must be read by every consumer through that marker, not through the file name. In this lineage, chain-integrate.sh writes the marker, and ledger-check.py now reads it (owned row `local:741e242:2`). Any other reader that derives audit ids from the file name is the same class of gap.
