# dot-builtin-git-auto-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- Changed both `chezmoi init` and `chezmoi update` invocations in `setup.sh` from `--use-builtin-git true` to `--use-builtin-git auto`.
- Added one regression test that requires both call sites to use `auto` and rejects the old `true` value.
- Kept the existing bootstrap flow and comments unchanged.

## Validation

- Bash syntax, shellcheck, shfmt, the static flag regression, and `git diff --check` pass.
- Local Bats was not run, as required.
- In `adh-test`, a credential-free scratch user with Git on `PATH` recorded an external `git clone` call.
- A second credential-free scratch user with a PATH containing no Git cloned successfully through the built-in fallback.
- Both scratch users and the task-specific VM temporary directory were removed.

## Durable decision

[memory:decision] `setup.sh` passes `--use-builtin-git auto` to both chezmoi Git operations, preferring external Git while retaining built-in Git bootstrap on Git-less systems; both paths are VM-validated.

CompactionDB command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-builtin-git-auto-T1-a01: setup.sh passes --use-builtin-git auto to both chezmoi init and update, preferring external Git when present while preserving built-in Git bootstrap when Git is absent; both paths were verified with credential-free scratch users in adh-test.'
```

Memory ID: `c40194a2-19ed-4a3a-bf76-6a90f3bbc889`

## Side effects

No persistent side effects outside the repository. VM users and temporary files were removed.
