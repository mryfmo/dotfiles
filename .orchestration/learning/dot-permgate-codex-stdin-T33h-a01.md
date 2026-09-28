# T33h learning triage

## Candidates

1. To test that a subprocess never depends on its caller's stdin, pass an
   `os.pipe()` read end as the parent's stdin and keep the write end open.
   That reproduces a "blocked on inherited stdin" failure deterministically
   in any runner, unlike relying on how the suite was launched
   (`sleep N |`).
2. Pick the entry point that actually inherits the caller's stdin. The
   permgate hook path pipes its payload in and reaches EOF, so it hides the
   bug; `bench` does not, so it exposes it.

## Promotion

None. These are candidates only.
