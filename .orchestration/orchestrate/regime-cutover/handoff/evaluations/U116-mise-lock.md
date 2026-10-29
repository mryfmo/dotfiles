# U116 mise.lock evaluation (plan P-36, research V4-9)

Measured 2026-10-29 (UTC) with `mise 2026.10.19 macos-arm64 (2026-10-24)` on the macOS host, every mise command under a scratch HOME.

## Question

Should CI and the hosts install the versions one committed `mise.lock` records, instead of each resolving `latest` on its own clock? If yes, where would that lockfile live under chezmoi, given that `home/dot_mise/config.toml` is the global mise config and renders byte for byte to `~/.config/mise/config.toml`?

The plan row P-36 (`handoff/05-remediation-plan.md:116`) asks for a decisions row with the measured output of `mise lock --global --dry-run`. The earlier row of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`) records "defer with a condition" and names `handoff/research/05-eval-mise-lock.md` as its evidence, a file the store does not hold. This file is that evidence, measured again under a scratch HOME so a reader can rerun it.

## Commands run

Every output below is pasted whole from the file the command wrote under `$TMPDIR/U116-out/`. Two substitutions apply to every pasted block, because the store refuses the login name and absolute home paths: the owner column of `ls -la` reads `<user>`, and the home directory reads `~`. Nothing else was edited. `$TMPDIR` on this host is `/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/`; mise prints it through its `/private` alias.

### The scratch home and the config copy (CHANGE 1)

```sh
scratch="$TMPDIR/U116-home"
mkdir -p "$scratch/.config/mise" "$scratch/.local/share" "$scratch/.cache" "$scratch/.local/state"
cp /tmp/dotfiles-wt/U116/home/dot_mise/config.toml "$scratch/.config/mise/config.toml"
ls -la ~/.config/mise   # before
```

```text
total 8
drwxr-xr-x  3 <user> staff   96 Oct 26 23:40 .
drwxr-xr-x 24 <user> staff  768 Oct 16 17:44 ..
-rw-r--r--  1 <user> staff 6962 Oct 26 23:40 config.toml
```

### The runner

Every mise command runs through this script. `run_mise` is the `env -i` form of the brief, `timed` records the start, the end, the elapsed seconds and the exit status of each run in a `.time` file beside its output.

```sh
#!/bin/bash
# Runs the U116 dry runs under the scratch HOME; every mise call goes through env -i.
set -u
scratch="$TMPDIR/U116-home"
out="$TMPDIR/U116-out"
run_mise() {
    env -i HOME="$scratch" PATH="$PATH" TMPDIR="$TMPDIR" \
        XDG_CONFIG_HOME="$scratch/.config" XDG_DATA_HOME="$scratch/.local/share" \
        XDG_CACHE_HOME="$scratch/.cache" XDG_STATE_HOME="$scratch/.local/state" \
        MISE_TRUSTED_CONFIG_PATHS="$scratch/.config/mise/config.toml" \
        perl -e 'alarm 900; exec @ARGV' mise "$@"
}
timed() {
    local name="$1"
    shift
    local start end
    start="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    SECONDS=0
    run_mise "$@" > "$out/$name.txt" 2>&1
    local status=$?
    end="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'start=%s end=%s elapsed=%ss exit=%s\n' "$start" "$end" "$SECONDS" "$status" > "$out/$name.time"
    printf '%s: %s\n' "$name" "$(cat "$out/$name.time")"
}
timed b-lock-dry-run lock --global --dry-run
timed c-lock-dry-run-4-platforms lock --global --dry-run --platform linux-x64,linux-arm64,macos-x64,macos-arm64
timed d-lock-bump-json lock --global --dry-run --bump --json
timed e-npm-package-manager settings get npm.package_manager
timed f-minimum-release-age settings get minimum_release_age
ls -la "$scratch/.config/mise" > "$out/g-scratch-after.txt" 2>&1
ls -la ~/.config/mise > "$out/g-real-after.txt" 2>&1
printf 'done\n'
```

### `mise lock --help`, first eight lines

```sh
run_mise lock --help
```

```text
Create or refresh lockfile versions, checksums, and download URLs

Operates on the current config root, including tools declared by tasks.
Existing matching locked versions are preserved unless `--bump` re-resolves
their requests. This command does not install tools; `--dry-run` previews
changes.

`mise lock TOOL@VERSION` locks that exact version. When the version falls
```

### Attempt 1: cwd under the real home (not the measured run)

The runner was first started from the coordinator checkout `~/Workspace/dotfiles`, with `HOME` and the four XDG variables pointed at the scratch home. The three `mise lock` runs exited 1 in 0 seconds:

```text
mise ERROR error parsing config file: ~/.config/mise/config.toml
mise ERROR Config files in ~/.config/mise/config.toml are not trusted.
Trust them with `mise trust`. See https://mise.jdx.dev/cli/trust.html for more information.
mise ERROR Version: 2026.10.19 macos-arm64 (2026-10-24)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
```

The (c) and (d) runs printed the same five lines; their files are `attempt1-cwd-checkout/c-lock-dry-run-4-platforms.txt` and `attempt1-cwd-checkout/d-lock-bump-json.txt` under `$TMPDIR/U116-out/`. The `settings get` runs (e) and (f) printed `npm` and `72h` and exited 0. The attempt-1 listings of the scratch and the real `~/.config/mise` are identical to the attempt-2 listings in (g) below.

Reading: the error names the real `~/.config/mise/config.toml`, although `HOME` pointed elsewhere. mise walks the parent directories of the cwd for project config files, and `.config/mise/config.toml` is one of the names it looks for, so the real home directory, an ancestor of the checkout, supplied a project config that the scratch trust store does not know (inferred from the path in the error and from the fact that the same command succeeds from a cwd outside the real home). mise refused to load it and did not write to it. Lesson for the next rerun: the cwd of a scratch-HOME mise run must sit outside the real home. The measured run below uses `cd "$TMPDIR/U116-home"` first.

### Attempt 2: cwd `$TMPDIR/U116-home` (the measured run)

```sh
cd "$TMPDIR/U116-home" && bash /tmp/U116-run.sh
```

(a) `run_mise --version`

```text
2026.10.19 macos-arm64 (2026-10-24)
```

(b) `run_mise lock --global --dry-run`, `start=2026-10-29T07:38:16Z end=2026-10-29T07:38:24Z elapsed=8s exit=0`

```text
→ Targeting 7 platform(s) for /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock: linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64
→ Processing 36 tool(s): node@26.12.1, rust@1.99.1, python@3.15.1, age@1.3.2, bun@1.4.4, chezmoi@2.73.3, dotenvx@2.38.2, cargo:eza@0.23.5, fd@10.5.0, jq@1.8.2, hugo-extended@0.168.0, uv@0.13.5, yazi@26.9.1, aqua:micro-editor/micro@2.0.15, aqua:mikefarah/yq@4.54.1, aqua:watchexec/watchexec@2.8.0, npm:@anthropic-ai/claude-code@2.1.310, npm:@openai/codex@0.164.0, npm:@anthropic-ai/sandbox-runtime@0.0.81, npm:bash-language-server@5.8.1, npm:ccstatusline@2.2.32, npm:ccusage@20.0.37, npm:pyright@1.1.414, npm:fast-cli@6.0.0, npm:prettier@3.9.10, npm:pnpm@12.8.1, github:x-motemen/ghq@1.11.2, github:d-kuro/gwq@0.1.2, github:cli/cli@2.103.2, github:ogulcancelik/herdr@0.9.5, cargo:pueue@4.0.4, http:bats@1.14.0, http:gcloud@590.0.0, http:shellcheck@0.11.0, http:shfmt@3.14.1, http:ruff@0.17.2
→ Dry run - would update:
  ✓ node@26.12.1 for linux-arm64
  ✓ node@26.12.1 for linux-arm64-musl
  ✓ node@26.12.1 for linux-x64
  ✓ node@26.12.1 for linux-x64-musl
  ✓ node@26.12.1 for macos-arm64
  ✓ node@26.12.1 for macos-x64
  ✓ node@26.12.1 for windows-x64
  ✓ rust@1.99.1 for linux-arm64
  ✓ rust@1.99.1 for linux-arm64-musl
  ✓ rust@1.99.1 for linux-x64
  ✓ rust@1.99.1 for linux-x64-musl
  ✓ rust@1.99.1 for macos-arm64
  ✓ rust@1.99.1 for macos-x64
  ✓ rust@1.99.1 for windows-x64
  ✓ python@3.15.1 for linux-arm64
  ✓ python@3.15.1 for linux-arm64-musl
  ✓ python@3.15.1 for linux-x64
  ✓ python@3.15.1 for linux-x64-musl
  ✓ python@3.15.1 for macos-arm64
  ✓ python@3.15.1 for macos-x64
  ✓ python@3.15.1 for windows-x64
  ✓ age@1.3.2 for linux-arm64
  ✓ age@1.3.2 for linux-arm64-musl
  ✓ age@1.3.2 for linux-x64
  ✓ age@1.3.2 for linux-x64-musl
  ✓ age@1.3.2 for macos-arm64
  ✓ age@1.3.2 for macos-x64
  ✓ age@1.3.2 for windows-x64
  ✓ bun@1.4.4 for linux-arm64
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-x64
  ✓ bun@1.4.4 for linux-x64-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for linux-x64-musl-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for macos-arm64
  ✓ bun@1.4.4 for macos-x64
  ✓ bun@1.4.4 for macos-x64-baseline
  ✓ bun@1.4.4 for windows-x64
  ✓ bun@1.4.4 for windows-x64-baseline
  ✓ chezmoi@2.73.3 for linux-arm64
  ✓ chezmoi@2.73.3 for linux-arm64-musl
  ✓ chezmoi@2.73.3 for linux-x64
  ✓ chezmoi@2.73.3 for linux-x64-musl
  ✓ chezmoi@2.73.3 for macos-arm64
  ✓ chezmoi@2.73.3 for macos-x64
  ✓ chezmoi@2.73.3 for windows-x64
  ✓ dotenvx@2.38.2 for linux-arm64
  ✓ dotenvx@2.38.2 for linux-arm64-musl
  ✓ dotenvx@2.38.2 for linux-x64
  ✓ dotenvx@2.38.2 for linux-x64-musl
  ✓ dotenvx@2.38.2 for macos-arm64
  ✓ dotenvx@2.38.2 for macos-x64
  ✓ dotenvx@2.38.2 for windows-x64
  ✓ cargo:eza@0.23.5 for linux-arm64
  ✓ cargo:eza@0.23.5 for linux-arm64-musl
  ✓ cargo:eza@0.23.5 for linux-x64
  ✓ cargo:eza@0.23.5 for linux-x64-musl
  ✓ cargo:eza@0.23.5 for macos-arm64
  ✓ cargo:eza@0.23.5 for macos-x64
  ✓ cargo:eza@0.23.5 for windows-x64
  ✓ fd@10.5.0 for linux-arm64
  ✓ fd@10.5.0 for linux-arm64-musl
  ✓ fd@10.5.0 for linux-x64
  ✓ fd@10.5.0 for linux-x64-musl
  ✓ fd@10.5.0 for macos-arm64
  ✓ fd@10.5.0 for macos-x64
  ✓ fd@10.5.0 for windows-x64
  ✓ jq@1.8.2 for linux-arm64
  ✓ jq@1.8.2 for linux-arm64-musl
  ✓ jq@1.8.2 for linux-x64
  ✓ jq@1.8.2 for linux-x64-musl
  ✓ jq@1.8.2 for macos-arm64
  ✓ jq@1.8.2 for macos-x64
  ✓ jq@1.8.2 for windows-x64
  ✓ hugo-extended@0.168.0 for linux-arm64
  ✓ hugo-extended@0.168.0 for linux-arm64-musl
  ✓ hugo-extended@0.168.0 for linux-x64
  ✓ hugo-extended@0.168.0 for linux-x64-musl
  ✓ hugo-extended@0.168.0 for macos-arm64
  ✓ hugo-extended@0.168.0 for macos-x64
  ✓ hugo-extended@0.168.0 for windows-x64
  ✓ uv@0.13.5 for linux-arm64
  ✓ uv@0.13.5 for linux-arm64-musl
  ✓ uv@0.13.5 for linux-x64
  ✓ uv@0.13.5 for linux-x64-musl
  ✓ uv@0.13.5 for macos-arm64
  ✓ uv@0.13.5 for macos-x64
  ✓ uv@0.13.5 for windows-x64
  ✓ yazi@26.9.1 for linux-arm64
  ✓ yazi@26.9.1 for linux-arm64-musl
  ✓ yazi@26.9.1 for linux-x64
  ✓ yazi@26.9.1 for linux-x64-musl
  ✓ yazi@26.9.1 for macos-arm64
  ✓ yazi@26.9.1 for macos-x64
  ✓ yazi@26.9.1 for windows-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64-musl
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64-musl
  ✓ aqua:micro-editor/micro@2.0.15 for macos-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-x64
  ✓ aqua:micro-editor/micro@2.0.15 for windows-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64-musl
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64-musl
  ✓ aqua:mikefarah/yq@4.54.1 for macos-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-x64
  ✓ aqua:mikefarah/yq@4.54.1 for windows-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64-musl
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64-musl
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for windows-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64-musl
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64-musl
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for windows-x64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64-musl
  ✓ npm:@openai/codex@0.164.0 for linux-x64
  ✓ npm:@openai/codex@0.164.0 for linux-x64-musl
  ✓ npm:@openai/codex@0.164.0 for macos-arm64
  ✓ npm:@openai/codex@0.164.0 for macos-x64
  ✓ npm:@openai/codex@0.164.0 for windows-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64-musl
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64-musl
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for windows-x64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64-musl
  ✓ npm:bash-language-server@5.8.1 for linux-x64
  ✓ npm:bash-language-server@5.8.1 for linux-x64-musl
  ✓ npm:bash-language-server@5.8.1 for macos-arm64
  ✓ npm:bash-language-server@5.8.1 for macos-x64
  ✓ npm:bash-language-server@5.8.1 for windows-x64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64-musl
  ✓ npm:ccstatusline@2.2.32 for linux-x64
  ✓ npm:ccstatusline@2.2.32 for linux-x64-musl
  ✓ npm:ccstatusline@2.2.32 for macos-arm64
  ✓ npm:ccstatusline@2.2.32 for macos-x64
  ✓ npm:ccstatusline@2.2.32 for windows-x64
  ✓ npm:ccusage@20.0.37 for linux-arm64
  ✓ npm:ccusage@20.0.37 for linux-arm64-musl
  ✓ npm:ccusage@20.0.37 for linux-x64
  ✓ npm:ccusage@20.0.37 for linux-x64-musl
  ✓ npm:ccusage@20.0.37 for macos-arm64
  ✓ npm:ccusage@20.0.37 for macos-x64
  ✓ npm:ccusage@20.0.37 for windows-x64
  ✓ npm:pyright@1.1.414 for linux-arm64
  ✓ npm:pyright@1.1.414 for linux-arm64-musl
  ✓ npm:pyright@1.1.414 for linux-x64
  ✓ npm:pyright@1.1.414 for linux-x64-musl
  ✓ npm:pyright@1.1.414 for macos-arm64
  ✓ npm:pyright@1.1.414 for macos-x64
  ✓ npm:pyright@1.1.414 for windows-x64
  ✓ npm:fast-cli@6.0.0 for linux-arm64
  ✓ npm:fast-cli@6.0.0 for linux-arm64-musl
  ✓ npm:fast-cli@6.0.0 for linux-x64
  ✓ npm:fast-cli@6.0.0 for linux-x64-musl
  ✓ npm:fast-cli@6.0.0 for macos-arm64
  ✓ npm:fast-cli@6.0.0 for macos-x64
  ✓ npm:fast-cli@6.0.0 for windows-x64
  ✓ npm:prettier@3.9.10 for linux-arm64
  ✓ npm:prettier@3.9.10 for linux-arm64-musl
  ✓ npm:prettier@3.9.10 for linux-x64
  ✓ npm:prettier@3.9.10 for linux-x64-musl
  ✓ npm:prettier@3.9.10 for macos-arm64
  ✓ npm:prettier@3.9.10 for macos-x64
  ✓ npm:prettier@3.9.10 for windows-x64
  ✓ npm:pnpm@12.8.1 for linux-arm64
  ✓ npm:pnpm@12.8.1 for linux-arm64-musl
  ✓ npm:pnpm@12.8.1 for linux-x64
  ✓ npm:pnpm@12.8.1 for linux-x64-musl
  ✓ npm:pnpm@12.8.1 for macos-arm64
  ✓ npm:pnpm@12.8.1 for macos-x64
  ✓ npm:pnpm@12.8.1 for windows-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64-musl
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64-musl
  ✓ github:x-motemen/ghq@1.11.2 for macos-arm64
  ✓ github:x-motemen/ghq@1.11.2 for macos-x64
  ✓ github:x-motemen/ghq@1.11.2 for windows-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64-musl
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64-musl
  ✓ github:d-kuro/gwq@0.1.2 for macos-arm64
  ✓ github:d-kuro/gwq@0.1.2 for macos-x64
  ✓ github:d-kuro/gwq@0.1.2 for windows-x64
  ✓ github:cli/cli@2.103.2 for linux-arm64
  ✓ github:cli/cli@2.103.2 for linux-arm64-musl
  ✓ github:cli/cli@2.103.2 for linux-x64
  ✓ github:cli/cli@2.103.2 for linux-x64-musl
  ✓ github:cli/cli@2.103.2 for macos-arm64
  ✓ github:cli/cli@2.103.2 for macos-x64
  ✓ github:cli/cli@2.103.2 for windows-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64-musl
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64-musl
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for windows-x64
  ✓ cargo:pueue@4.0.4 for linux-arm64
  ✓ cargo:pueue@4.0.4 for linux-arm64-musl
  ✓ cargo:pueue@4.0.4 for linux-x64
  ✓ cargo:pueue@4.0.4 for linux-x64-musl
  ✓ cargo:pueue@4.0.4 for macos-arm64
  ✓ cargo:pueue@4.0.4 for macos-x64
  ✓ cargo:pueue@4.0.4 for windows-x64
  ✓ http:bats@1.14.0 for linux-arm64
  ✓ http:bats@1.14.0 for linux-arm64-musl
  ✓ http:bats@1.14.0 for linux-x64
  ✓ http:bats@1.14.0 for linux-x64-musl
  ✓ http:bats@1.14.0 for macos-arm64
  ✓ http:bats@1.14.0 for macos-x64
  ✓ http:bats@1.14.0 for windows-x64
  ✓ http:gcloud@590.0.0 for linux-arm64
  ✓ http:gcloud@590.0.0 for linux-arm64-musl
  ✓ http:gcloud@590.0.0 for linux-x64
  ✓ http:gcloud@590.0.0 for linux-x64-musl
  ✓ http:gcloud@590.0.0 for macos-arm64
  ✓ http:gcloud@590.0.0 for macos-x64
  ✓ http:gcloud@590.0.0 for windows-x64
  ✓ http:shellcheck@0.11.0 for linux-arm64
  ✓ http:shellcheck@0.11.0 for linux-arm64-musl
  ✓ http:shellcheck@0.11.0 for linux-x64
  ✓ http:shellcheck@0.11.0 for linux-x64-musl
  ✓ http:shellcheck@0.11.0 for macos-arm64
  ✓ http:shellcheck@0.11.0 for macos-x64
  ✓ http:shellcheck@0.11.0 for windows-x64
  ✓ http:shfmt@3.14.1 for linux-arm64
  ✓ http:shfmt@3.14.1 for linux-arm64-musl
  ✓ http:shfmt@3.14.1 for linux-x64
  ✓ http:shfmt@3.14.1 for linux-x64-musl
  ✓ http:shfmt@3.14.1 for macos-arm64
  ✓ http:shfmt@3.14.1 for macos-x64
  ✓ http:shfmt@3.14.1 for windows-x64
  ✓ http:ruff@0.17.2 for linux-arm64
  ✓ http:ruff@0.17.2 for linux-arm64-musl
  ✓ http:ruff@0.17.2 for linux-x64
  ✓ http:ruff@0.17.2 for linux-x64-musl
  ✓ http:ruff@0.17.2 for macos-arm64
  ✓ http:ruff@0.17.2 for macos-x64
  ✓ http:ruff@0.17.2 for windows-x64
```

(c) `run_mise lock --global --dry-run --platform linux-x64,linux-arm64,macos-x64,macos-arm64`, `start=2026-10-29T07:38:24Z end=2026-10-29T07:38:24Z elapsed=0s exit=0`

```text
→ Targeting 4 platform(s) for /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock: linux-arm64, linux-x64, macos-arm64, macos-x64
→ Processing 36 tool(s): node@26.12.1, rust@1.99.1, python@3.15.1, age@1.3.2, bun@1.4.4, chezmoi@2.73.3, dotenvx@2.38.2, cargo:eza@0.23.5, fd@10.5.0, jq@1.8.2, hugo-extended@0.168.0, uv@0.13.5, yazi@26.9.1, aqua:micro-editor/micro@2.0.15, aqua:mikefarah/yq@4.54.1, aqua:watchexec/watchexec@2.8.0, npm:@anthropic-ai/claude-code@2.1.310, npm:@openai/codex@0.164.0, npm:@anthropic-ai/sandbox-runtime@0.0.81, npm:bash-language-server@5.8.1, npm:ccstatusline@2.2.32, npm:ccusage@20.0.37, npm:pyright@1.1.414, npm:fast-cli@6.0.0, npm:prettier@3.9.10, npm:pnpm@12.8.1, github:x-motemen/ghq@1.11.2, github:d-kuro/gwq@0.1.2, github:cli/cli@2.103.2, github:ogulcancelik/herdr@0.9.5, cargo:pueue@4.0.4, http:bats@1.14.0, http:gcloud@590.0.0, http:shellcheck@0.11.0, http:shfmt@3.14.1, http:ruff@0.17.2
→ Dry run - would update:
  ✓ node@26.12.1 for linux-arm64
  ✓ node@26.12.1 for linux-x64
  ✓ node@26.12.1 for macos-arm64
  ✓ node@26.12.1 for macos-x64
  ✓ rust@1.99.1 for linux-arm64
  ✓ rust@1.99.1 for linux-x64
  ✓ rust@1.99.1 for macos-arm64
  ✓ rust@1.99.1 for macos-x64
  ✓ python@3.15.1 for linux-arm64
  ✓ python@3.15.1 for linux-x64
  ✓ python@3.15.1 for macos-arm64
  ✓ python@3.15.1 for macos-x64
  ✓ age@1.3.2 for linux-arm64
  ✓ age@1.3.2 for linux-x64
  ✓ age@1.3.2 for macos-arm64
  ✓ age@1.3.2 for macos-x64
  ✓ bun@1.4.4 for linux-arm64
  ✓ bun@1.4.4 for linux-arm64-musl
  ✓ bun@1.4.4 for linux-x64
  ✓ bun@1.4.4 for linux-x64-baseline
  ✓ bun@1.4.4 for linux-x64-musl
  ✓ bun@1.4.4 for linux-x64-musl-baseline
  ✓ bun@1.4.4 for macos-arm64
  ✓ bun@1.4.4 for macos-x64
  ✓ bun@1.4.4 for macos-x64-baseline
  ✓ chezmoi@2.73.3 for linux-arm64
  ✓ chezmoi@2.73.3 for linux-x64
  ✓ chezmoi@2.73.3 for macos-arm64
  ✓ chezmoi@2.73.3 for macos-x64
  ✓ dotenvx@2.38.2 for linux-arm64
  ✓ dotenvx@2.38.2 for linux-x64
  ✓ dotenvx@2.38.2 for macos-arm64
  ✓ dotenvx@2.38.2 for macos-x64
  ✓ cargo:eza@0.23.5 for linux-arm64
  ✓ cargo:eza@0.23.5 for linux-x64
  ✓ cargo:eza@0.23.5 for macos-arm64
  ✓ cargo:eza@0.23.5 for macos-x64
  ✓ fd@10.5.0 for linux-arm64
  ✓ fd@10.5.0 for linux-x64
  ✓ fd@10.5.0 for macos-arm64
  ✓ fd@10.5.0 for macos-x64
  ✓ jq@1.8.2 for linux-arm64
  ✓ jq@1.8.2 for linux-x64
  ✓ jq@1.8.2 for macos-arm64
  ✓ jq@1.8.2 for macos-x64
  ✓ hugo-extended@0.168.0 for linux-arm64
  ✓ hugo-extended@0.168.0 for linux-x64
  ✓ hugo-extended@0.168.0 for macos-arm64
  ✓ hugo-extended@0.168.0 for macos-x64
  ✓ uv@0.13.5 for linux-arm64
  ✓ uv@0.13.5 for linux-x64
  ✓ uv@0.13.5 for macos-arm64
  ✓ uv@0.13.5 for macos-x64
  ✓ yazi@26.9.1 for linux-arm64
  ✓ yazi@26.9.1 for linux-x64
  ✓ yazi@26.9.1 for macos-arm64
  ✓ yazi@26.9.1 for macos-x64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for linux-x64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-arm64
  ✓ aqua:micro-editor/micro@2.0.15 for macos-x64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for linux-x64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-arm64
  ✓ aqua:mikefarah/yq@4.54.1 for macos-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for linux-x64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-arm64
  ✓ aqua:watchexec/watchexec@2.8.0 for macos-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for linux-x64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-arm64
  ✓ npm:@anthropic-ai/claude-code@2.1.310 for macos-x64
  ✓ npm:@openai/codex@0.164.0 for linux-arm64
  ✓ npm:@openai/codex@0.164.0 for linux-x64
  ✓ npm:@openai/codex@0.164.0 for macos-arm64
  ✓ npm:@openai/codex@0.164.0 for macos-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for linux-x64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-arm64
  ✓ npm:@anthropic-ai/sandbox-runtime@0.0.81 for macos-x64
  ✓ npm:bash-language-server@5.8.1 for linux-arm64
  ✓ npm:bash-language-server@5.8.1 for linux-x64
  ✓ npm:bash-language-server@5.8.1 for macos-arm64
  ✓ npm:bash-language-server@5.8.1 for macos-x64
  ✓ npm:ccstatusline@2.2.32 for linux-arm64
  ✓ npm:ccstatusline@2.2.32 for linux-x64
  ✓ npm:ccstatusline@2.2.32 for macos-arm64
  ✓ npm:ccstatusline@2.2.32 for macos-x64
  ✓ npm:ccusage@20.0.37 for linux-arm64
  ✓ npm:ccusage@20.0.37 for linux-x64
  ✓ npm:ccusage@20.0.37 for macos-arm64
  ✓ npm:ccusage@20.0.37 for macos-x64
  ✓ npm:pyright@1.1.414 for linux-arm64
  ✓ npm:pyright@1.1.414 for linux-x64
  ✓ npm:pyright@1.1.414 for macos-arm64
  ✓ npm:pyright@1.1.414 for macos-x64
  ✓ npm:fast-cli@6.0.0 for linux-arm64
  ✓ npm:fast-cli@6.0.0 for linux-x64
  ✓ npm:fast-cli@6.0.0 for macos-arm64
  ✓ npm:fast-cli@6.0.0 for macos-x64
  ✓ npm:prettier@3.9.10 for linux-arm64
  ✓ npm:prettier@3.9.10 for linux-x64
  ✓ npm:prettier@3.9.10 for macos-arm64
  ✓ npm:prettier@3.9.10 for macos-x64
  ✓ npm:pnpm@12.8.1 for linux-arm64
  ✓ npm:pnpm@12.8.1 for linux-x64
  ✓ npm:pnpm@12.8.1 for macos-arm64
  ✓ npm:pnpm@12.8.1 for macos-x64
  ✓ github:x-motemen/ghq@1.11.2 for linux-arm64
  ✓ github:x-motemen/ghq@1.11.2 for linux-x64
  ✓ github:x-motemen/ghq@1.11.2 for macos-arm64
  ✓ github:x-motemen/ghq@1.11.2 for macos-x64
  ✓ github:d-kuro/gwq@0.1.2 for linux-arm64
  ✓ github:d-kuro/gwq@0.1.2 for linux-x64
  ✓ github:d-kuro/gwq@0.1.2 for macos-arm64
  ✓ github:d-kuro/gwq@0.1.2 for macos-x64
  ✓ github:cli/cli@2.103.2 for linux-arm64
  ✓ github:cli/cli@2.103.2 for linux-x64
  ✓ github:cli/cli@2.103.2 for macos-arm64
  ✓ github:cli/cli@2.103.2 for macos-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for linux-x64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-arm64
  ✓ github:ogulcancelik/herdr@0.9.5 for macos-x64
  ✓ cargo:pueue@4.0.4 for linux-arm64
  ✓ cargo:pueue@4.0.4 for linux-x64
  ✓ cargo:pueue@4.0.4 for macos-arm64
  ✓ cargo:pueue@4.0.4 for macos-x64
  ✓ http:bats@1.14.0 for linux-arm64
  ✓ http:bats@1.14.0 for linux-x64
  ✓ http:bats@1.14.0 for macos-arm64
  ✓ http:bats@1.14.0 for macos-x64
  ✓ http:gcloud@590.0.0 for linux-arm64
  ✓ http:gcloud@590.0.0 for linux-x64
  ✓ http:gcloud@590.0.0 for macos-arm64
  ✓ http:gcloud@590.0.0 for macos-x64
  ✓ http:shellcheck@0.11.0 for linux-arm64
  ✓ http:shellcheck@0.11.0 for linux-x64
  ✓ http:shellcheck@0.11.0 for macos-arm64
  ✓ http:shellcheck@0.11.0 for macos-x64
  ✓ http:shfmt@3.14.1 for linux-arm64
  ✓ http:shfmt@3.14.1 for linux-x64
  ✓ http:shfmt@3.14.1 for macos-arm64
  ✓ http:shfmt@3.14.1 for macos-x64
  ✓ http:ruff@0.17.2 for linux-arm64
  ✓ http:ruff@0.17.2 for linux-x64
  ✓ http:ruff@0.17.2 for macos-arm64
  ✓ http:ruff@0.17.2 for macos-x64
```

(d) `run_mise lock --global --dry-run --bump --json`, `start=2026-10-29T07:38:24Z end=2026-10-29T07:38:24Z elapsed=0s exit=0`

```text
[
  {
    "name": "node",
    "backend": "core:node",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.12.1"
    ]
  },
  {
    "name": "rust",
    "backend": "core:rust",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.99.1"
    ]
  },
  {
    "name": "python",
    "backend": "core:python",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.15.1"
    ]
  },
  {
    "name": "age",
    "backend": "aqua:FiloSottile/age",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.3.2"
    ]
  },
  {
    "name": "bun",
    "backend": "core:bun",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.4.4"
    ]
  },
  {
    "name": "chezmoi",
    "backend": "aqua:twpayne/chezmoi",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.73.3"
    ]
  },
  {
    "name": "dotenvx",
    "backend": "aqua:dotenvx/dotenvx",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.38.2"
    ]
  },
  {
    "name": "cargo:eza",
    "backend": "cargo:eza",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.23.5"
    ]
  },
  {
    "name": "fd",
    "backend": "aqua:sharkdp/fd",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "10.5.0"
    ]
  },
  {
    "name": "jq",
    "backend": "aqua:jqlang/jq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.8.2"
    ]
  },
  {
    "name": "hugo-extended",
    "backend": "aqua:gohugoio/hugo/hugo-extended",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.168.0"
    ]
  },
  {
    "name": "uv",
    "backend": "aqua:astral-sh/uv",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.13.5"
    ]
  },
  {
    "name": "yazi",
    "backend": "aqua:sxyazi/yazi",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "26.9.1"
    ]
  },
  {
    "name": "aqua:micro-editor/micro",
    "backend": "aqua:micro-editor/micro",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.0.15"
    ]
  },
  {
    "name": "aqua:mikefarah/yq",
    "backend": "aqua:mikefarah/yq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.54.1"
    ]
  },
  {
    "name": "aqua:watchexec/watchexec",
    "backend": "aqua:watchexec/watchexec",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.8.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/claude-code",
    "backend": "npm:@anthropic-ai/claude-code",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.1.310"
    ]
  },
  {
    "name": "npm:@openai/codex",
    "backend": "npm:@openai/codex",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.164.0"
    ]
  },
  {
    "name": "npm:@anthropic-ai/sandbox-runtime",
    "backend": "npm:@anthropic-ai/sandbox-runtime",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.0.81"
    ]
  },
  {
    "name": "npm:bash-language-server",
    "backend": "npm:bash-language-server",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "5.8.1"
    ]
  },
  {
    "name": "npm:ccstatusline",
    "backend": "npm:ccstatusline",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.2.32"
    ]
  },
  {
    "name": "npm:ccusage",
    "backend": "npm:ccusage",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "20.0.37"
    ]
  },
  {
    "name": "npm:pyright",
    "backend": "npm:pyright",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.1.414"
    ]
  },
  {
    "name": "npm:fast-cli",
    "backend": "npm:fast-cli",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "6.0.0"
    ]
  },
  {
    "name": "npm:prettier",
    "backend": "npm:prettier",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.9.10"
    ]
  },
  {
    "name": "npm:pnpm",
    "backend": "npm:pnpm",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "12.8.1"
    ]
  },
  {
    "name": "github:x-motemen/ghq",
    "backend": "github:x-motemen/ghq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.11.2"
    ]
  },
  {
    "name": "github:d-kuro/gwq",
    "backend": "github:d-kuro/gwq",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.1.2"
    ]
  },
  {
    "name": "github:cli/cli",
    "backend": "github:cli/cli",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "2.103.2"
    ]
  },
  {
    "name": "github:ogulcancelik/herdr",
    "backend": "github:ogulcancelik/herdr",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.9.5"
    ]
  },
  {
    "name": "cargo:pueue",
    "backend": "cargo:pueue",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "4.0.4"
    ]
  },
  {
    "name": "http:bats",
    "backend": "http:bats",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "1.14.0"
    ]
  },
  {
    "name": "http:gcloud",
    "backend": "http:gcloud",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "590.0.0"
    ]
  },
  {
    "name": "http:shellcheck",
    "backend": "http:shellcheck",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.11.0"
    ]
  },
  {
    "name": "http:shfmt",
    "backend": "http:shfmt",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "3.14.1"
    ]
  },
  {
    "name": "http:ruff",
    "backend": "http:ruff",
    "lockfile": "/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/U116-home/.config/mise/mise.lock",
    "old_versions": [],
    "new_versions": [
      "0.17.2"
    ]
  }
]
```

(e) `run_mise settings get npm.package_manager`, `start=2026-10-29T07:38:24Z end=2026-10-29T07:38:24Z elapsed=0s exit=0`

```text
npm
```

(f) `run_mise settings get minimum_release_age`, `start=2026-10-29T07:38:24Z end=2026-10-29T07:38:24Z elapsed=0s exit=0`

```text
72h
```

(g) `ls -la "$scratch/.config/mise"` after all runs

```text
total 16
drwxr-xr-x@ 3 <user>  staff    96 Oct 29 15:09 .
drwxr-xr-x@ 3 <user>  staff    96 Oct 29 15:09 ..
-rw-r--r--@ 1 <user>  staff  6962 Oct 29 15:09 config.toml
```

(g) `ls -la ~/.config/mise` after all runs

```text
total 16
drwxr-xr-x   3 <user>  staff    96 Oct 26 23:40 .
drwxr-xr-x  24 <user>  staff   768 Oct 16 17:44 ..
-rw-r--r--@  1 <user>  staff  6962 Oct 26 23:40 config.toml
```

### Further checks

`test ! -e "$TMPDIR/U116-home/.config/mise/mise.lock" && echo none-written`

```text
none-written
```

The before listing of CHANGE 1 came from the shell's built-in `ls` (GNU format: `total 8`, one-space columns), the (g) listing from `/bin/ls` inside the runner script (BSD format: `total 16`, wider columns, `@` for extended attributes). The entries are the same three in both. For a like-for-like pair, the same built-in `ls -la ~/.config/mise` after attempt 2, which `diff` reports identical to the before listing:

```text
total 8
drwxr-xr-x  3 <user> staff   96 Oct 26 23:40 .
drwxr-xr-x 24 <user> staff  768 Oct 16 17:44 ..
-rw-r--r--  1 <user> staff 6962 Oct 26 23:40 config.toml
```

Modification times of the real mise directories, `stat -f "%Sm %N" -t "%Y-%m-%dT%H:%M:%S"`, taken before attempt 2 started and after it ended. mise on macOS keeps its cache under `~/Library/Caches/mise`, so `~/.cache/mise` does not exist on this host.

```text
2026-10-26T23:40:46 ~/.config/mise
2026-10-29T14:51:19 ~/.local/share/mise
stat: cannot stat '~/.cache/mise': No such file or directory (os error 2)
2026-10-28T09:59:20 ~/.local/state/mise
2026-10-26T23:41:00 ~/Library/Caches/mise
```

```text
2026-10-26T23:40:46 ~/.config/mise
2026-10-29T14:51:19 ~/.local/share/mise
2026-10-26T23:41:00 ~/Library/Caches/mise
2026-10-28T09:59:20 ~/.local/state/mise
```

`grep -c -F -f <(gh auth token) <file>` on every output file of both attempts (the brief requires `0` before any paste; no run needed `MISE_GITHUB_TOKEN`, so none was set):

```text
a-version.txt 0
b-lock-dry-run.txt 0
c-lock-dry-run-4-platforms.txt 0
d-lock-bump-json.txt 0
e-npm-package-manager.txt 0
f-minimum-release-age.txt 0
g-real-after.txt 0
g-scratch-after.txt 0
help.txt 0
real-before.txt 0
real-dirs-mtime-after.txt 0
real-dirs-mtime-before.txt 0
scratch-tree.txt 0
attempt1-cwd-checkout/b-lock-dry-run.txt 0
attempt1-cwd-checkout/c-lock-dry-run-4-platforms.txt 0
attempt1-cwd-checkout/d-lock-bump-json.txt 0
attempt1-cwd-checkout/e-npm-package-manager.txt 0
attempt1-cwd-checkout/f-minimum-release-age.txt 0
attempt1-cwd-checkout/g-real-after.txt 0
attempt1-cwd-checkout/g-scratch-after.txt 0
```

What the scratch home holds after attempt 2, `find "$TMPDIR/U116-home" -maxdepth 4` with `$TMPDIR` written back:

```text
$TMPDIR/U116-home
$TMPDIR/U116-home/.cache
$TMPDIR/U116-home/.cache/mise
$TMPDIR/U116-home/.cache/mise/cargo-eza
$TMPDIR/U116-home/.cache/mise/cargo-eza/remote_versions-cfe45.msgpack.z
$TMPDIR/U116-home/.cache/mise/cargo-pueue
$TMPDIR/U116-home/.cache/mise/cargo-pueue/remote_versions-711b5.msgpack.z
$TMPDIR/U116-home/.cache/mise/github
$TMPDIR/U116-home/.cache/mise/github-cli-cli
$TMPDIR/U116-home/.cache/mise/github-cli-cli/remote_versions-fbf2d.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-astral-sh-uv-latest-75f152cbb3234e33-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-cli-cli-latest-c422894432b07a75-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-cli-cli-versions-fdcb0a0009af6507-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-d-kuro-gwq-latest-6c17f18eaf4e3a2b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-dotenvx-dotenvx-latest-851010c943271a76-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-filo-sottile-age-latest-5aaeb641c690722-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-gohugoio-hugo-latest-7e8a758b278d01f5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-jqlang-jq-latest-bdd9320085deaae5-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-micro-editor-micro-latest-e2cefac8305717dd-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-mikefarah-yq-latest-a3188cde7430c1ee-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-ogulcancelik-herdr-latest-b515115e6d3664ca-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-sharkdp-fd-latest-a69cff9e0d9ad20b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-sxyazi-yazi-latest-29d17fd18245505c-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-twpayne-chezmoi-latest-ab43663cda310c28-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-watchexec-watchexec-latest-130a48c37d16befe-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/github/https-api-github-com-x-motemen-ghq-latest-1d789ce64118519b-hosted-2-2f6a0.msgpack.z
$TMPDIR/U116-home/.cache/mise/http-bats
$TMPDIR/U116-home/.cache/mise/http-gcloud
$TMPDIR/U116-home/.cache/mise/http-ruff
$TMPDIR/U116-home/.cache/mise/http-shellcheck
$TMPDIR/U116-home/.cache/mise/http-shfmt
$TMPDIR/U116-home/.cache/mise/latest-version.releases-v1
$TMPDIR/U116-home/.cache/mise/node
$TMPDIR/U116-home/.cache/mise/node/remote_versions-73876.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-claude-code
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-claude-code/latest_version-999a7.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-claude-code/remote_versions-999a7.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-sandbox-runtime
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-sandbox-runtime/latest_version-dab3a.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-anthropic-ai-sandbox-runtime/remote_versions-dab3a.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-bash-language-server
$TMPDIR/U116-home/.cache/mise/npm-bash-language-server/latest_version-1b050.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-bash-language-server/remote_versions-1b050.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-fast-cli
$TMPDIR/U116-home/.cache/mise/npm-fast-cli/latest_version-81575.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-fast-cli/remote_versions-81575.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-meta
$TMPDIR/U116-home/.cache/mise/npm-meta/origin-3c364d36b2d92b17
$TMPDIR/U116-home/.cache/mise/npm-openai-codex
$TMPDIR/U116-home/.cache/mise/npm-openai-codex/latest_version-50bdb.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-openai-codex/remote_versions-50bdb.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-pyright
$TMPDIR/U116-home/.cache/mise/npm-pyright/latest_version-30d9a.msgpack.z
$TMPDIR/U116-home/.cache/mise/npm-pyright/remote_versions-30d9a.msgpack.z
$TMPDIR/U116-home/.cache/mise/python
$TMPDIR/U116-home/.cache/mise/python/remote_versions-ee8bb.msgpack.z
$TMPDIR/U116-home/.cache/mise/uv
$TMPDIR/U116-home/.cache/mise/uv/remote_versions-3ed32.msgpack.z
$TMPDIR/U116-home/.cache/mise/versions-index
$TMPDIR/U116-home/.cache/mise/versions-index/index.v1
$TMPDIR/U116-home/.cache/mise/versions-index/index.v1.validated
$TMPDIR/U116-home/.config
$TMPDIR/U116-home/.config/mise
$TMPDIR/U116-home/.config/mise/config.toml
$TMPDIR/U116-home/.local
$TMPDIR/U116-home/.local/share
$TMPDIR/U116-home/.local/state
$TMPDIR/U116-home/.local/state/mise
$TMPDIR/U116-home/.local/state/mise/incomplete-installs
$TMPDIR/U116-home/.local/state/mise/tracked-configs
```

## Measured facts

### From the outputs

| Run                                           | Platforms       | Tools | Entries mise would write             | Elapsed | Exit |
| --------------------------------------------- | --------------- | ----- | ------------------------------------ | ------- | ---- |
| (b) default platform set                      | 7               | 36    | 258                                  | 8 s     | 0    |
| (c) the four platforms the `http:` tables pin | 4               | 36    | 149                                  | 0 s     | 0    |
| (d) `--bump --json`                           | 7 (same target) | 36    | 36 objects, all `old_versions` empty | 0 s     | 0    |

- **Platforms.** With no `lockfile_platforms` setting and no existing lockfile, mise targets `linux-arm64, linux-arm64-musl, linux-x64, linux-x64-musl, macos-arm64, macos-x64, windows-x64` (first line of (b)). That is the vendor's new-lockfile set from the reference page, and it matches the "7 platforms" of row 233.
- **Entries.** (b) lists 258 `✓` lines: 36 tools times 7 platforms is 252, and bun adds six more keys (`linux-x64-baseline`, `linux-x64-musl-baseline`, `macos-x64-baseline`, `windows-x64-baseline`, and `linux-arm64-musl` and `linux-x64-musl` listed a second time). (c) lists 149: 144 plus bun's `linux-arm64-musl`, `linux-x64-baseline`, `linux-x64-musl`, `linux-x64-musl-baseline` and `macos-x64-baseline`. Counted with `grep -c '^  ✓'` on the two files.
- **Backends.** Every one of the 36 tools resolved: 4 core (`node`, `rust`, `python`, `bun`), 11 aqua (`age`, `chezmoi`, `dotenvx`, `fd`, `jq`, `hugo-extended`, `uv`, `yazi`, `micro`, `yq`, `watchexec`; the backend names come from the `backend` field of (d)), 10 npm, 4 github, 2 cargo, 5 http. No line reports a failure, a skipped platform or a rate limit, and no run needed `MISE_GITHUB_TOKEN`.
- **What a bump would move today.** Nothing moves: every object in (d) has `"old_versions": []`, because no lockfile exists. The 36 `new_versions` equal the versions (b) resolved, so today's bump PR would be the first write of the file, not an update. The exact pins resolve to themselves (`npm:ccstatusline@2.2.32`, `npm:ccusage@20.0.37`, `npm:prettier@3.9.10`, `npm:pnpm@12.8.1`, the five `http:` tools), as the vendor says for `--bump`.
- **Elapsed.** (b) took 8 s wall time, and (c) and (d) returned in under a second because mise reused the version lists (b) had cached under the scratch `~/.cache/mise` (the `remote_versions-*.msgpack.z` files in the scratch tree). The brief's estimate of "about 36 tools per platform over the network" taking minutes did not hold: mise resolves a version once per tool, not once per platform, and the dry run downloads no artifact.
- **Hosts contacted.** No packet capture was taken. The cache file names show `api.github.com` (sixteen `github/https-api-github-com-*` entries), the mise versions index (`versions-index/index.v1`) and an npm registry origin (`npm-meta/origin-*`). All are in the brief's host list. Whether any other host was contacted is unverified.
- **Nothing written.** The scratch `~/.config/mise` holds `config.toml` alone before and after, and `none-written` printed. The real `~/.config/mise` holds the same single entry before and after (`config.toml`, 6962 bytes, dated Oct 26 23:40, no `mise.lock`), and the like-for-like listing pair under Further checks is identical. The modification times of the real `~/.config/mise`, `~/.local/share/mise`, `~/Library/Caches/mise` and `~/.local/state/mise` are identical before and after attempt 2. mise wrote only under the scratch home: version-list caches under `.cache/mise` and the `tracked-configs` and `incomplete-installs` directories under `.local/state/mise`.
- **Settings.** `npm.package_manager` is `npm` and `minimum_release_age` is `72h` in the copy, as `config.toml:112-113` and `:107` set them.
- **Attempt 1.** With the cwd under the real home, mise read the real `~/.config/mise/config.toml` as an untrusted project config and stopped. The file was opened, not changed (its listing and mtime are unchanged). This is the one way the unit touched a real mise path, and it is a property of mise's config discovery, not of `HOME`.

### From the tree

1. `tests/unit/test_supply_chain_policy.py:444-462` renders `home/dot_config/mise/config.toml.tmpl` with chezmoi and asserts the result equals `home/dot_mise/config.toml` byte for byte.
2. `home/dot_mise/config.toml:3-43` requests `latest` for every tool that is not held; `:26-36` hold ccstatusline, ccusage, prettier and pnpm at exact versions with a one-line reason above each; `:46-103` hold the five `http:` tools with per-platform URL and sha256 tables at `:60-64`, `:73-77`, `:86-90` and `:99-103`.
3. `README.md:199-202` states that only a held tool commits a version and that there is no `mise.lock`; `README.md:250-255` names the trade-off (machines may differ in tool versions, CI tests the latest safe versions) and that the applied file no longer turns on lockfile mode for other projects.
4. `home/.chezmoiremove:21` is `.config/mise/mise.lock`: chezmoi deletes the rendered lockfile on every apply.
5. `tests/unit/test_supply_chain_policy.py:404-421` asserts that `lockfile`, `locked` and `lockfile_platforms` are absent from `[settings]` (`:408-409`), that `home/dot_mise/mise.lock` and `home/dot_config/mise/mise.lock.tmpl` do not exist (`:419-420`) and that `.chezmoiremove` lists the rendered lock (`:421`). `:464-466` asserts that `install/common/mise.sh`, `Makefile` and `scripts/update-agent-assets.sh` contain no `--locked`.
6. `.github/workflows/test.yaml:259-261` copies `home/dot_mise/config.toml` alone to `RUNNER_TEMP/statusline-mise/mise.toml`; `:263-270` runs `jdx/mise-action` with `install: false`; `:276-279` installs node, the statusline tools, ruff and prettier with `mise -C "${RUNNER_TEMP}/statusline-mise" install …`.
7. `scripts/upgrade-tools.sh:318` runs `mise upgrade --yes <tool>` for each tool that is neither an `http:` pin nor held.
8. `scripts/update-agent-assets.sh:148` repairs a broken agent CLI with `MISE_NPM_PACKAGE_MANAGER=npm mise install --force <tool>`, and `tests/unit/test_runtime_health.py:249` and `:347` assert that exact call with the npm installer.

### From the vendor pages, read 2026-10-29

- <https://mise.jdx.dev/dev-tools/mise-lock.html>: "`mise.lock` records the exact versions that the requests in `mise.toml` resolved to, with download URLs and checksums where the backend provides them. Commit it next to `mise.toml` so every machine and CI job installs the same tools." "`mise install --locked` fails instead of resolving a version when the lockfile has no matching entry, which catches an incomplete lockfile in CI". On the setting: "`true` in a config file: mise creates lockfiles and keeps them up to date." and "only `lockfile = true` in a config file turns on automatic creation." On graphs: "Format version 2 and later lock the transitive dependencies of npm and PyPI tools, not only their top-level version. mise stores each graph in the package manager's own format, `aube-lock.yaml` for npm tools installed with embedded aube and `uv.lock` for PyPI tools when uv 0.12.10 or newer is installed, in a sidecar directory (`.mise/locks/` by default)." The dotfiles section: "If `~/.config/mise/config.toml` is a symlink into a dotfiles repository, such as `~/dotfiles/mise.toml`, `mise lock` run inside the repository reports that there is nothing to lock, because mise treats the file as global config. Run `mise lock --global` from inside the repository to write `~/dotfiles/mise.lock`. From other directories mise reads and writes `~/.config/mise/mise.lock`, so also symlink that path to `~/dotfiles/mise.lock`. Sidecars follow the symlink target." On the cooldown: "A version recorded in `mise.lock` installs even when it is newer than `minimum_release_age`; the cutoff applies only when mise selects a new version." On CI: "`jdx/mise-action` adds `--locked` itself when the repository has a `mise.lock`." The command table lists `mise upgrade` and `mise upgrade node` as updating `mise.lock` ("Yes"), and the backend table lists "npm (embedded aube) and pypi (uv)" as recording "The version, plus a dependency graph in format version 2 and later" and "cargo, dotnet, gem, go, spinel, core:dotnet, core:rust" as "The top-level version only".
- <https://mise.jdx.dev/dev-tools/mise-lock-reference.html>: format versions 0 (no field), 1 (`specifiers`), 2 ("npm and PyPI dependency graphs in sidecar directories"), 3 (`repository_ids` for packslip tools); "New lockfiles use version 3." Platform keys: "`mise lock` writes these keys for a new lockfile, plus the current platform's: `linux-x64`, `linux-x64-musl`, `linux-arm64`, `linux-arm64-musl`, `macos-x64`, `macos-arm64` and `windows-x64`." and "Bun adds `-baseline` on x64 CPUs without AVX2". Sidecar location for the global lockfile: "`~/.config/mise/mise.lock` (global) | `~/.config/mise/locks/`". "If `mise.lock` is a symlink, mise resolves sidecar paths relative to the symlink's target and writes new sidecars beside it."
- <https://mise.jdx.dev/dev-tools/backends/npm.html>: "With the embedded aube installer, `mise.lock` records each npm tool's full dependency graph (lockfile format 2 or later, which new lockfiles use)." "Other installers cannot replay an embedded-aube graph; use embedded aube, or refresh the lockfile for the installer you select." The installer table maps `npm` to `npm install -g`. "For a locked graph, the cutoff applies when the graph is resolved; installs replay the committed dependencies." No sentence on the page says what the lock records under `package_manager = "npm"`; "version only" follows from the two sentences above (the graph exists only for embedded aube) and from the backend table on the lockfile page, so research 4.2's "inferred" label stays, with these two sentences as its basis.
- <https://mise.jdx.dev/cli/lock.html> and `mise lock --help` above: `--minimum-release-age <AGE>` is documented as "Only lock versions released before a date or at least a duration ago", "It filters only requests that are not exact". `--platform` "Defaults to the `lockfile_platforms` setting plus the current platform when that setting is configured, else the platforms already in the lockfile, else a common set for a new lockfile." `--bump`: "If the remote versions cannot be fetched, it fails rather than keep the locked version."
- <https://raw.githubusercontent.com/jdx/mise-action/main/README.md>: "With a committed `mise.lock`, mise verifies cached downloads against lockfile checksums before use, so a poisoned or stale cache cannot change what gets installed." "If a repo mise lock file such as `mise.lock` is present in the working directory or one of its parents, this action automatically runs `mise install --locked`." "If you provide `mise_toml` or `tool_versions` inputs, the action does not automatically force locked mode."

### The five V4-9 answers

**Where the lock lives under chezmoi.** The dry run names its target as `<HOME>/.config/mise/mise.lock`, beside the global config (first line of (b)), and the reference page puts the global sidecars in `~/.config/mise/locks/`. Under chezmoi the source would be `home/dot_mise/mise.lock` with a `home/dot_config/mise/mise.lock.tmpl` include, the same shape as the config today; both files are forbidden by `test_supply_chain_policy.py:419-420`, and `.chezmoiremove:21` deletes the rendered `~/.config/mise/mise.lock` on every apply. The vendor's command table says `mise upgrade` updates `mise.lock`, so a host `mise upgrade` rewrites the rendered file, and chezmoi then reports that file as drift until the next apply deletes or replaces it. With the embedded installer the sidecar directory `~/.config/mise/locks/` would need the same treatment.

**Whether `make update` becomes `mise lock --bump` in a PR followed by `mise install --locked` on hosts.** Today `scripts/upgrade-tools.sh:318` runs `mise upgrade --yes <tool>` per unheld tool on the host, which is exactly the command that would rewrite the lock. The lockfile workflow replaces that step with a scheduled `mise lock --bump --minimum-release-age 72h` (run (d) shows the shape of its output: one JSON object per moved tool) that opens a PR, and hosts run `mise install --locked` from the applied lock. `README.md:250-255` records the present trade-off on purpose, and `test_supply_chain_policy.py:464-466` forbids `--locked` in the three lifecycle files. The change is therefore a workflow decision for the operator (hosts stop upgrading on their own), not a CI fix, as research 4.4 says.

**How the CI copy step would carry `mise.lock` and `.mise/locks/`.** `test.yaml:259-261` copies one file into `RUNNER_TEMP/statusline-mise/mise.toml`. With a lock, the step also copies `mise.lock` beside it and, under the embedded installer, the sidecar directory as `.mise/locks/` (the project layout the reference page gives for a `mise.lock` beside `mise.toml`). mise-action does not add `--locked` here: it adds the flag when a lockfile sits in the working directory or its parents, and `test.yaml:263-270` runs it with `install: false` on the checkout, not on the copy. The four `mise -C … install` lines at `test.yaml:276-279` would carry `--locked` themselves.

**Whether `package_manager = "npm"` or the embedded installer is wanted.** Run (e) confirms `npm`. Under that setting the lock records the version only, so the npm supply-chain gain of the lockfile (the replayed dependency graph) does not apply to the ten `npm:` tools, which include the two agent CLIs. The embedded installer would record the graph, but `scripts/update-agent-assets.sh:148` repairs the agent CLIs with `MISE_NPM_PACKAGE_MANAGER=npm`, `tests/unit/test_runtime_health.py:347` asserts that call, and the npm cooldown work of U89 and U114 (`~/.npmrc` `min-release-age`, the publish-time check in `upgrade-tools.sh`) is built on npm's own behaviour. Switching the installer is its own unit with its own measurement (the ccstatusline and ccusage graphs under aube are listed under Left out).

**The 72 h policy moves to the bump schedule.** The lockfile page states that a locked version installs even when newer than `minimum_release_age`, and the npm page adds that for a locked graph the cutoff applies when the graph is resolved. Run (f) confirms the config's `72h`. Under a lock, the host no longer applies the cooldown at install time; the `--minimum-release-age 72h` flag of `mise lock --bump` (in the help text above) applies it when the bump resolves, so the policy holds only if every bump run carries that flag and no one hand-edits the lock.

## Recommendation

**defer.** The measured output agrees with row 233 of `decisions.tsv` (`2026-10-28T09:40:00Z`, phase `plan-P-36`): the same 7 platforms and 36 tools, nothing written, and the lock is technically ready (every backend resolved in 8 s, no token, no failure). What the dry run adds is the entry counts (258 and 149), the fact that today's bump would be a first write and not a move, and the attempt-1 finding about mise's config discovery. None of this changes the facts the deferral rests on: the tree forbids the lock in three places by policy, `make update` would rewrite it on every host run, the CI copy carries one file, `package_manager = "npm"` records the version only, and the 72 h cooldown would move from install time to the bump schedule.

The condition that would change the recommendation to `adopt` is an operator decision, recorded in `decisions.tsv`, to stop unattended host upgrades (`upgrade-tools.sh:318`) and take every unheld version from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in `test.yaml:276-279`, plus a decision on the npm installer. The condition that would change it to `reject` is a decision to keep the present `latest` behind the cooldown as the permanent policy, in which case the lockfile settings test and `.chezmoiremove:21` are the complete record and this question closes. Absent either, the no-lock policy stands as `README.md:199-202` and `:250-255` describe it.

## Draft decisions row

| field    | value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ts       | 2026-10-29T07:39:59Z                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| phase    | plan-P-36                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| decision | mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 8 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first |
| why      | the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config                                                                                                                                                                                       |
| evidence | handoff/evaluations/U116-mise-lock.md                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| result   | proposed; the coordinator records                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

The same row as one line with literal tab separators:

```text
2026-10-29T07:39:59Z	plan-P-36	mise.lock evaluation measured (plan P-36, research V4-9): defer; corrects the evidence of the 2026-10-28T09:40:00Z row, whose file handoff/research/05-eval-mise-lock.md was never written. Measured 2026-10-29 under a scratch HOME with mise 2026.10.19: `mise lock --global --dry-run` targets 7 platforms and 36 tools and would write 258 entries (36 x 7 plus 6 bun variant keys); the 4-platform set the http tables pin gives 149 entries; `--bump --dry-run --json` lists 36 first-time entries and no move; every backend (4 core, 11 aqua, 10 npm, 4 github, 2 cargo, 5 http) resolved in 8 s without a GitHub token; no lockfile written, the real ~/.config/mise unchanged. The condition stands: an operator decision to stop host-side `mise upgrade` (scripts/upgrade-tools.sh:318) and take versions from a scheduled `mise lock --bump --minimum-release-age 72h` PR, with `mise install --locked` on hosts and in the CI copy step (.github/workflows/test.yaml:259-261), and the npm installer question settled first	the plan's acceptance asks for the measured output on record; the dry run changed no fact row 233 rests on: the tree's policy (README.md:199-202 and 250-255, home/.chezmoiremove:21, tests/unit/test_supply_chain_policy.py:404-421 and 464-466) forbids the lock and `--locked`, `make update` would rewrite the rendered lock on every run (vendor table: `mise upgrade` updates mise.lock), npm.package_manager=npm records the version only (the dependency graph needs the embedded installer, which scripts/update-agent-assets.sh:148 and tests/unit/test_runtime_health.py:347 do not use), and a locked version bypasses minimum_release_age so the 72 h policy would move to the bump schedule; one new fact: with a cwd under the real home, mise's parent-directory walk reads the real ~/.config/mise/config.toml as a project config	handoff/evaluations/U116-mise-lock.md	proposed; the coordinator records
```

## Left out

- A real `mise lock --global` write, on any host or in the worktree. Every `mise lock` above carries `--dry-run`.
- `mise install --locked` on any host, so the install side of the workflow is unmeasured.
- The ccstatusline and ccusage dependency graphs under the embedded installer. Run (e) shows the npm installer, under which the lock records the version only, and the unit did not switch the installer.
- The Ubuntu host. Every command ran on the macOS host; the `linux-*` platform entries above come from mise's own resolution, not from a Linux run.
- A network capture. The hosts contacted are read from mise's cache file names.
- The handoff `README.md` row for `evaluations/`, which the coordinator writes.
