# Learning triage: dotfiles-T128-chain-review-scripts-followup-a05

These are candidates only; nothing is promoted.

1. [memory:decision] To take an id from a file name, strip the exact known prefix (`${name#prefix}`) and validate the whole remainder; the longest-match strip `${name##*-sep-}` reads only the last separator, so a name holding the separator twice passes as its tail.
