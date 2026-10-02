# Validation: dot-macos-brew-untrusted-taps-T57-a01

- PR: #228 https://github.com/mryfmo/dotfiles/pull/228
- Head SHA: f314ab2a5f0606f3987f23e1d295a3ec91dd97b0 (one commit on origin/main 18d192aa)

## Task validation commands (verbatim)

```
$ git diff origin/main --stat
 .github/workflows/test.yaml          | 14 ++++++--------
 README.md                            |  2 ++
 install/macos/common/brew.sh         | 31 +++++++++++++++++++++++++++++--
 tests/install/macos/common/brew.bats | 26 ++++++++++++++++++++++++++
 4 files changed, 63 insertions(+), 10 deletions(-)
(exit 0)
$ shellcheck install/macos/common/brew.sh
(exit 0)
$ shfmt -d install/macos/common/brew.sh   # task command verbatim (bare shfmt: tabs default, ignores the repo style)
(exit 1; 56 +/- lines, full output below)
[1mdiff install/macos/common/brew.sh.orig install/macos/common/brew.sh
--- install/macos/common/brew.sh.orig
+++ install/macos/common/brew.sh
[36m@@ -13,7 +13,7 @@
[0m readonly HOMEBREW_INSTALL_SHA256="99287f194a8b3c9e6b0203a11a5fa54518be57209343e6bb954dec4635796d9d"
 
 if [ "${DOTFILES_DEBUG:-}" ]; then
[31m-    set -x
[32m+	set -x
[0m fi
 
 #
[36m@@ -20,7 +20,7 @@
[0m # @description Check whether Homebrew is already available on `PATH`.
 #
 function is_homebrew_exists() {
[31m-    command -v brew &> /dev/null
[32m+	command -v brew &> /dev/null
[0m }
 
 #
[36m@@ -27,20 +27,20 @@
[0m # @description Install Homebrew when it is not present.
 #
 function install_homebrew() {
[31m-    if ! is_homebrew_exists; then
-        (
-            local actual installer
-            installer="$(mktemp)"
-            trap 'rm -f "${installer}"' EXIT
-            curl -fsSL "https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh" -o "${installer}"
-            actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
-            [ "${actual}" = "${HOMEBREW_INSTALL_SHA256}" ] || {
-                printf 'Homebrew installer checksum mismatch\n' >&2
-                return 1
-            }
-            NONINTERACTIVE=1 /bin/bash "${installer}"
-        )
-    fi
[32m+	if ! is_homebrew_exists; then
+		(
+			local actual installer
+			installer="$(mktemp)"
+			trap 'rm -f "${installer}"' EXIT
+			curl -fsSL "https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh" -o "${installer}"
+			actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
+			[ "${actual}" = "${HOMEBREW_INSTALL_SHA256}" ] || {
+				printf 'Homebrew installer checksum mismatch\n' >&2
+				return 1
+			}
+			NONINTERACTIVE=1 /bin/bash "${installer}"
+		)
+	fi
[0m }
 
 #
[36m@@ -47,7 +47,7 @@
[0m # @description Disable Homebrew analytics for the current user.
 #
 function opt_out_of_analytics() {
[31m-    brew analytics off
[32m+	brew analytics off
[0m }
 
 #
[36m@@ -61,19 +61,19 @@
[0m #   Does nothing unless `CI` is exactly `true`.
 #
 function handle_ci_untrusted_taps() {
[31m-    [ "${CI:-}" = "true" ] || return 0
-
-    local listing taps
-    if ! listing="$(brew untrust --tap 2> /dev/null)"; then
-        printf 'brew has no tap trust (no brew untrust command); skipping untrusted tap handling\n' >&2
-        return 0
-    fi
-    # The listing is a header line followed by one indented tap name per line.
-    taps="$(sed -n 's/^  //p' <<< "${listing}")"
-    [ -n "${taps}" ] || return 0
-
-    # shellcheck disable=SC2086 # One tap name per word, word splitting intended.
-    brew trust ${taps}
[32m+	[ "${CI:-}" = "true" ] || return 0
+
+	local listing taps
+	if ! listing="$(brew untrust --tap 2> /dev/null)"; then
+		printf 'brew has no tap trust (no brew untrust command); skipping untrusted tap handling\n' >&2
+		return 0
+	fi
+	# The listing is a header line followed by one indented tap name per line.
+	taps="$(sed -n 's/^  //p' <<< "${listing}")"
+	[ -n "${taps}" ] || return 0
+
+	# shellcheck disable=SC2086 # One tap name per word, word splitting intended.
+	brew trust ${taps}
[0m }
 
 #
[36m@@ -80,11 +80,11 @@
[0m # @description Install Homebrew and apply repository defaults.
 #
 function main() {
[31m-    install_homebrew
-    handle_ci_untrusted_taps
-    opt_out_of_analytics
[32m+	install_homebrew
+	handle_ci_untrusted_taps
+	opt_out_of_analytics
[0m }
 
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
[31m-    main
[32m+	main
[0m fi
$ git show origin/main:install/macos/common/brew.sh > "$TMPDIR/brew-main.sh"; shfmt -d "$TMPDIR/brew-main.sh" >/dev/null; echo $?   # the bare-shfmt diff predates this change
1
$ mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d install/macos/common/brew.sh   # the repository/CI form (test.yaml "Run shfmt", Makefile, .editorconfig)
(exit 0)
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dot-ci-runner-label-pin-T58-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dot-macos-brew-untrusted-taps-T57-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dot-ua-graph-refresh-T55-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-audit.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-git-ignore-cc-writes-T56-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T55-a01.md
agent asset validation ok
(exit 0)
$ bash "$TMPDIR/t57-smoke.sh"   # local plain-bash stand-in for the bats case (bats run in CI only)
no-op outside CI: ok
CI=true rc=0 calls:
untrust --tap
trust aws/tap azure/bicep hashicorp/tap
no-untrusted-taps rc=0 calls:
untrust --tap
brew has no tap trust (no brew untrust command); skipping untrusted tap handling
brew-without-untrust rc=0
(exit 0)
$ cat "$TMPDIR/t57-smoke.sh"
#!/usr/bin/env bash
# Plain-bash smoke test of handle_ci_untrusted_taps with a fake brew (not bats).
source install/macos/common/brew.sh
calls="${TMPDIR:-/tmp}/t57-smoke-calls"
: > "${calls}"
brew() {
    printf '%s\n' "$*" >> "${calls}"
    if [ "$*" = "untrust --tap" ]; then printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n'; fi
}
(
    unset CI
    handle_ci_untrusted_taps
)
for v in "" false 1 yes; do CI="${v}" handle_ci_untrusted_taps; done
[ -s "${calls}" ] && echo "FAIL: brew called outside CI" || echo "no-op outside CI: ok"
CI=true handle_ci_untrusted_taps
echo "CI=true rc=$? calls:"
cat "${calls}"
: > "${calls}"
brew() {
    printf '%s\n' "$*" >> "${calls}"
    if [ "$*" = "untrust --tap" ]; then echo "No untrusted taps, formulae, casks or commands."; fi
}
CI=true handle_ci_untrusted_taps
echo "no-untrusted-taps rc=$? calls:"
cat "${calls}"
brew() {
    echo "Error: Unknown command: untrust" >&2
    return 1
}
CI=true handle_ci_untrusted_taps
echo "brew-without-untrust rc=$?"
```

## gh pr checks 228 and acceptance count (verbatim, unsandboxed, final head f314ab2a)

```
$ gh pr checks 228
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37027430349/job/110905524556	
test (ubuntu-latest, server)	pass	4m25s	https://github.com/mryfmo/dotfiles/actions/runs/37027429533/job/110905842934	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37027429533/job/110905844590	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37027429533/job/110905521442	
private-bootstrap (macos-14, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905522811	
private-bootstrap (ubuntu-latest, client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905523436	
private-bootstrap (ubuntu-latest, server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905523206	
public-bootstrap (macos-14, client)	pass	9m36s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905523047	
public-bootstrap (ubuntu-latest, client)	pass	9m21s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905523086	
public-bootstrap (ubuntu-latest, server)	pass	7m18s	https://github.com/mryfmo/dotfiles/actions/runs/37027429870/job/110905522964	
test (macos-14, client)	pass	4m51s	https://github.com/mryfmo/dotfiles/actions/runs/37027429533/job/110905843030	
test (ubuntu-latest, client)	pass	7m8s	https://github.com/mryfmo/dotfiles/actions/runs/37027429533/job/110905843044	
validate	pass	16s	https://github.com/mryfmo/dotfiles/actions/runs/37027430304/job/110905525465	
(exit 0)
$ python3 scripts/pr-feedback.py 228 --json "$TMPDIR/t57-feedback.json" && python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print('untrusted-tap warnings:',sum(1 for i in d['items'] if i.get('level')=='warning' and 'taps are not trusted' in (i.get('body') or '')))" "$TMPDIR/t57-feedback.json"
pr-feedback: mryfmo/dotfiles#228 head f314ab2: 14 items (annotation:notice=12, issue_comment:comment=1, status:success=1)
untrusted-tap warnings: 0
$ python3 (all items by source/level, and any warning-level item)
{('issue_comment', 'comment'): 1, ('annotation', 'notice'): 12, ('status', 'success'): 1}
warning-level items: []
$ gh pr view 228 --json number,url,headRefOid,state -q ...
#228 https://github.com/mryfmo/dotfiles/pull/228 f314ab2a5f0606f3987f23e1d295a3ec91dd97b0 OPEN
```

## The function ran on CI (job logs, verbatim excerpts)

```
$ gh run view --job 110905523047 --log | grep -E "Trusted tap|not trusted"   # Snippet install / public-bootstrap (macos-14, client), image macos-14-arm64 20260831.0302.1
2026-10-02T15:31:07.5796600Z Trusted tap: aws/tap
2026-10-02T15:31:07.5798960Z Trusted tap: azure/bicep
2026-10-02T15:31:07.5801060Z Trusted tap: hashicorp/tap
$ gh run view --job 110905843030 --log | grep -cE "Trusted tap|not trusted|no tap trust"   # test (macos-14, client), same image: no output from the function, no warning
0
$ gh run view --job 110892662913 --log | grep "trusted tap"   # PR #227 test (macos-14, client), old inline `brew trust aws/tap azure/bicep`: taps were already trusted in that job
2026-10-02T14:58:39.7573390Z ^[[36;1m  # while an untrusted tap is present, even though this job's^[[0m
2026-10-02T14:58:41.7066260Z Already trusted tap: aws/tap
2026-10-02T14:58:41.7073190Z Already trusted tap: azure/bicep
```

## Homebrew command help and source relied on (Homebrew/brew tag 7.0.7, verbatim)

```
$ gh api 'repos/Homebrew/brew/contents/Library/Homebrew/cmd/trust.rb?ref=7.0.7' -H 'Accept: application/vnd.github.raw' | sed -n '/cmd_args do/,/^      end/p'   # brew help text source (cmd_args)
      cmd_args do
        description <<~EOS
          Trust non-official tap formulae, casks or commands so Homebrew may load them.
          Trusted entries are stored in `${XDG_CONFIG_HOME}/homebrew/trust.json` if
          `$XDG_CONFIG_HOME` is set or `~/.homebrew/trust.json` otherwise.
        EOS
        switch "--tap", "--taps",
               description: "Trust the named tap."
        switch "--formula", "--formulae",
               description: "Trust the named formula."
        switch "--cask", "--casks",
               description: "Trust the named cask."
        switch "--command", "--commands",
               description: "Trust the named external command."
        flag "--json=",
             description: "Print trusted entries as JSON. A <version> number is required. " \
                          "The only accepted value for <version> is `v1`."

        conflicts "--tap", "--formula", "--cask", "--command"

        named_args :target
      end
$ gh api 'repos/Homebrew/brew/contents/Library/Homebrew/cmd/untrust.rb?ref=7.0.7' -H 'Accept: application/vnd.github.raw' | sed -n '/cmd_args do/,/^      end/p'   # brew help text source (cmd_args)
      cmd_args do
        description <<~EOS
          Stop trusting non-official tap formulae, casks or commands.
          Trusted entries are stored in `${XDG_CONFIG_HOME}/homebrew/trust.json` if
          `$XDG_CONFIG_HOME` is set or `~/.homebrew/trust.json` otherwise.
        EOS
        switch "--tap",
               description: "Untrust the named tap."
        switch "--formula", "--formulae",
               description: "Untrust the named formula."
        switch "--cask", "--casks",
               description: "Untrust the named cask."
        switch "--command", "--commands",
               description: "Untrust the named external command."

        conflicts "--tap", "--formula", "--cask", "--command"

        named_args :target
      end
$ gh api 'repos/Homebrew/brew/contents/Library/Homebrew/cmd/untap.rb?ref=7.0.7' -H 'Accept: application/vnd.github.raw' | sed -n '/cmd_args do/,/^      end/p'   # brew help text source (cmd_args)
      cmd_args do
        description <<~EOS
          Remove a tapped formula repository.
        EOS
        switch "-f", "--force",
               description: "Uninstall all formulae and casks from this tap with `--force` before untapping."

        named_args :tap, min: 1
      end
$ gh api 'repos/Homebrew/brew/contents/Library/Homebrew/cmd/tap-info.rb?ref=7.0.7' -H 'Accept: application/vnd.github.raw' | sed -n '/cmd_args do/,/^      end/p'   # brew help text source (cmd_args)
      cmd_args do
        description <<~EOS
          Show detailed information about one or more <tap>s.
          If no <tap> names are provided, display brief statistics for all installed taps.
        EOS
        switch "--installed",
               description: "Show information on each installed tap."
        flag   "--json",
               description: "Print a JSON representation of <tap>. Currently the default and only accepted " \
                            "value for <version> is `v1`. See the docs for examples of using the JSON " \
                            "output: <https://docs.brew.sh/Querying-Brew>"

        named_args :tap
      end
$ (untrust.rb@7.0.7) no-argument listing branch
        if args.no_named?
          types = selected_type ? [selected_type] : [:tap, :formula, :cask, :command]
          printed = T.let(false, T::Boolean)
          types.each do |type|
            values = Homebrew::Trust.untrusted_taps.flat_map do |tap|
              case type
              when :tap
                [tap.name]
              when :formula
                tap.formula_files.filter_map do |file|
                  name = file.basename(file.extname).to_s
                  full_name = "#{tap.name}/#{name}"
$ (trust.rb lib @7.0.7) untrusted_taps / wholly_untrusted_taps
287:    def self.untrusted_taps
288-      Tap.installed.reject(&:official?).reject { |tap| trusted_tap?(tap) }.sort_by(&:name)
289-    end
290-
--
292:    def self.wholly_untrusted_taps
293-      untrusted_taps.reject { |tap| partially_trusted_tap?(tap) }
294-    end
295-
$ (diagnostic.rb @7.0.7) preinstall check
166:      def preinstall_checks
167-        %w[
168-          check_untrusted_taps
169-        ].freeze
170-      end
171-
172-      sig { returns(T::Array[String]) }
--
843:      def check_untrusted_taps
844-        return if Homebrew::EnvConfig.no_require_tap_trust?
845-
846-        untrusted_taps = Homebrew::Trust.wholly_untrusted_taps
847-        return if untrusted_taps.empty?
848-
849-        untrusted_tap_names = untrusted_taps.map(&:name)
$ (formula.rb @7.0.7) Formula.installed swallows load errors
  def self.installed
    Formula.cache[:installed] ||= racks.flat_map do |rack|
      Formulary.from_rack(rack)
    rescue
      []
    end.uniq(&:name)
  end
$ (formulary.rb @7.0.7) load_formula requires trust
  def self.load_formula(name, path, contents, namespace, flags:, ignore_errors:, from_metadata: false)
    raise "Formula loading disabled by `$HOMEBREW_DISABLE_LOAD_FORMULA`!" if Homebrew::EnvConfig.disable_load_formula?

    Homebrew::Trust.require_trusted_formula!(name, path)
$ (untap.rb @7.0.7) refusal when the tap has installed kegs
67-                  unless confirmed
68-                    ofail <<~EOS
69:                      Refusing to untap #{tap} because it contains the following installed #{installed_package_types}:
70-                      #{installed_names}
71-                    EOS
72-                    next
$ gh api repos/mryfmo/dotfiles/check-runs/110875969684/annotations   # the original warning (run 37018721870)
The following taps are not trusted:
  aws/tap
  azure/bicep
  hashicorp/tap

Homebrew is currently ignoring formulae, casks and commands from these taps because tap trust is required.

Prefer trusting only the specific formulae, casks or commands you need.
Trust installed formulae from these taps with:
  brew trust --formula azure/bicep/bicep
  brew trust --formula hashicorp/tap/packer
Trust other specific casks and commands with:
  brew trust --cask <user>/<tap>/<cask>
  brew trust --command <user>/<tap>/<command>
Whole-tap trust is broader and includes all current and future formulae,
casks and commands from the listed taps. Trust whole taps with:
  brew trust aws/tap azure/bicep hashicorp/tap
Untap them with:
  brew untap aws/tap azure/bicep hashicorp/tap
To disable trust checks:
  export HOMEBREW_NO_REQUIRE_TAP_TRUST=1
This is not recommended and will be removed in a later release.
For more information, see:
  https://docs.brew.sh/Tap-Trust
```

## docs.brew.sh/Tap-Trust (fetched 2026-10-02; WebFetch extract, quoted passages)

```
"Prefer trusting the specific formula, cask or command you need. Trust a whole tap only when you accept all current and future formulae, casks and external commands from that tap."
"For one-off installs, automation or software from a vendor you do not fully control, prefer trusting only the required item."
"An untrusted tap is not loaded when tap trust is required unless you explicitly install a fully qualified formula or cask from that tap."
brew untrust            -> "List[s] untrusted taps, formulae, casks and commands."
brew trust user/repository ; brew trust --formula user/repository/formula ; brew untrust user/repository
"HOMEBREW_REQUIRE_TAP_TRUST=1 is deprecated" ; "HOMEBREW_NO_REQUIRE_TAP_TRUST=1 is also deprecated and will be removed in a later release."
```

## CompactionDB (main checkout, unsandboxed)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T57 (operator 2026-10-02): recurring CI/bot findings are fixed at the root once, never dispositioned `not-applicable` repeatedly; image-provided Homebrew taps are handled in `install/macos/common/brew.sh` under `CI=true` only, derived from Homebrew's own tap listing.'
4dd72a5f-3b9e-490f-8f00-fe17c8871d98
(exit 0)
```

# Revise round 1 (task_rev sha256:89a99b97…, after audit of f314ab2a)

- Final head: f568eab6a1032a9d134d89cb43f3b0200f2016fc; measurement commit 50c833b3. No force push.

## Round-1 commands (verbatim)

```
$ sha256sum /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-macos-brew-untrusted-taps-T57-a01.md
89a99b9765952905d8a78405fb15cb398666b4b92287559a77d0535525631f5c  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-macos-brew-untrusted-taps-T57-a01.md
$ git log --oneline -4
f568eab6 fix(macos): fall back to whole-tap trust only for runner taps with nothing installed
50c833b3 fix(macos): trust only installed items from untrusted runner taps
f314ab2a fix(macos): trust untrusted runner-image Homebrew taps once, in brew.sh
18d192aa chore(git): ignore the Claude Code .cc-writes marker so chezmoi apply converges (#227)
$ git ls-remote origin refs/heads/fix/macos-brew-untrusted-taps
f568eab6a1032a9d134d89cb43f3b0200f2016fc	refs/heads/fix/macos-brew-untrusted-taps
$ git diff origin/main --stat
 .github/workflows/test.yaml          | 14 ++++----
 README.md                            |  2 ++
 install/macos/common/brew.sh         | 69 ++++++++++++++++++++++++++++++++++--
 tests/install/macos/common/brew.bats | 32 +++++++++++++++++
 4 files changed, 107 insertions(+), 10 deletions(-)
$ git grep -n -i "not derivable\|cannot list" -- install/macos/common/brew.sh .github/workflows/test.yaml tests/install/macos/common/brew.bats README.md; echo $?   # the false claim is gone from committed text
1
$ shellcheck install/macos/common/brew.sh
(exit 0)
$ shfmt -d install/macos/common/brew.sh >/dev/null; echo $?   # bare form (tabs); fails on origin/main too, see round 0
1
$ mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d install/macos/common/brew.sh   # repository/CI form
(exit 0)
$ make validate-agent-assets 2>&1 | tail -1
agent asset validation ok
(exit 0)
$ bash "$TMPDIR/t57-smoke.sh"   # local stand-in for the bats case
no-op outside CI: ok
CI=true rc=0 calls:
untrust --tap
list --formula --full-name
list --cask --full-name
trust --formula azure/bicep/bicep hashicorp/tap/packer
trust --cask hashicorp/tap/vagrant
trust aws/tap
no-untrusted-taps rc=0 calls:
untrust --tap
brew has no tap trust (no brew untrust command); skipping untrusted tap handling
brew-without-untrust rc=0
(exit 0)

$ gh api "repos/Homebrew/brew/contents/Library/Homebrew/cmd/list.rb?ref=7.0.7" -H "Accept: application/vnd.github.raw" | sed -n 104,120p   # the --full-name path reads keg receipts
        if args.full_name? &&
           !(args.installed_on_request? || installed_as_dependency ||
             args.poured_from_bottle? || args.built_from_source?)
          unless args.cask?
            full_formula_names = if args.no_named?
              Formula.racks.map do |rack|
                name = rack.basename.to_s
                tap = begin
                  Keg.from_rack(rack)&.tab&.tap
                rescue JSON::ParserError, SystemCallError, Tap::InvalidNameError
                  opoo "Could not identify the tap for #{name} from its installation receipt."
                  nil
                end
                (tap.nil? || tap.core_tap?) ? name : "#{tap}/#{name}"
              end
            else
              args.named.to_resolved_formulae.map(&:full_name)
```
```
$ gh run view --job 110914945531 --log | grep -E "Trusted (tap|formula|cask)|##\[warning\]"   # measurement 1: 50c833b3, item-level only
2026-10-02T15:54:57.6848910Z Trusted formula: azure/bicep/bicep
2026-10-02T15:54:57.6853980Z Trusted formula: hashicorp/tap/packer
2026-10-02T15:55:03.1470350Z ##[warning]The following taps are not trusted:
$ gh api repos/mryfmo/dotfiles/check-runs/110914945531/annotations --jq ".[] | select(.annotation_level==\"warning\") | .message"
The following taps are not trusted:
  aws/tap

Homebrew is currently ignoring formulae, casks and commands from these taps because tap trust is required.

Untap them with:
  brew untap aws/tap
Trust specific formulae, casks and commands with:
  brew trust --formula <user>/<tap>/<formula>
  brew trust --cask <user>/<tap>/<cask>
  brew trust --command <user>/<tap>/<command>
Whole-tap trust is broader and includes all current and future formulae,
casks and commands from the listed taps. Trust whole taps with:
  brew trust aws/tap
To disable trust checks:
  export HOMEBREW_NO_REQUIRE_TAP_TRUST=1
This is not recommended and will be removed in a later release.
For more information, see:
  https://docs.brew.sh/Tap-Trust
$ gh run view --job 110919109271 --log | grep -E "Trusted (tap|formula|cask)|##\[warning\]"   # measurement 2: f568eab6, final
2026-10-02T16:05:45.3322740Z Trusted formula: azure/bicep/bicep
2026-10-02T16:05:45.3329710Z Trusted formula: hashicorp/tap/packer
2026-10-02T16:05:45.5761980Z Trusted tap: aws/tap
$ gh api repos/mryfmo/dotfiles/check-runs/110919109271/annotations --jq ".[] | .annotation_level" | sort | uniq -c
      1 notice
$ gh pr checks 228   # final head f568eab6
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
build	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37031476876/job/110919109048	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37031476966/job/110919109155	
private-bootstrap (macos-14, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109005	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/37031476966/job/110919181270	
private-bootstrap (ubuntu-latest, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109498	
private-bootstrap (ubuntu-latest, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109116	
public-bootstrap (macos-14, client)	pass	9m9s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109271	
public-bootstrap (ubuntu-latest, client)	pass	9m3s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109190	
public-bootstrap (ubuntu-latest, server)	pass	6m29s	https://github.com/mryfmo/dotfiles/actions/runs/37031476934/job/110919109075	
test (macos-14, client)	pass	4m56s	https://github.com/mryfmo/dotfiles/actions/runs/37031476966/job/110919179038	
test (ubuntu-latest, client)	pass	7m4s	https://github.com/mryfmo/dotfiles/actions/runs/37031476966/job/110919179102	
test (ubuntu-latest, server)	pass	4m28s	https://github.com/mryfmo/dotfiles/actions/runs/37031476966/job/110919178939	
validate	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/37031476766/job/110919108303	
(exit 0)
$ python3 scripts/pr-feedback.py 228 --json "$TMPDIR/t57-feedback.json" && python3 -c "...untrusted-tap warnings..." "$TMPDIR/t57-feedback.json"
pr-feedback: mryfmo/dotfiles#228 head f568eab: 16 items (annotation:notice=12, issue_comment:comment=1, review:commented=1, review_comment:comment=1, status:success=1)
untrusted-tap warnings: 0
$ python3 (items by source/level; warning/failure items)
{('issue_comment', 'comment'): 1, ('review', 'commented'): 1, ('review_comment', 'comment'): 1, ('annotation', 'notice'): 12, ('status', 'success'): 1}
warning/failure items: []
review_comment chatgpt-codex-connector[bot] install/macos/common/brew.sh 105 https://github.com/mryfmo/dotfiles/pull/228#discussion_r4167450604 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Trust each untrusted tap, not only installed packages**
$ gh pr view 228 --json number,url,headRefOid,state -q ...
#228 https://github.com/mryfmo/dotfiles/pull/228 f568eab6a1032a9d134d89cb43f3b0200f2016fc OPEN
```
