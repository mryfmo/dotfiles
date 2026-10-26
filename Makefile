DOCKER_IMAGE_NAME=dotfiles
HOST ?= 127.0.0.1
PORT ?= 8000
# The documentation build installs exactly the versions in scripts/mkdocs-requirements.txt.
MKDOCS_UV = uv run --no-project --with-requirements scripts/mkdocs-requirements.txt
MKDOCS = NO_MKDOCS_2_WARNING=true $(MKDOCS_UV) mkdocs
MKDOCS_PYTHON = NO_MKDOCS_2_WARNING=true $(MKDOCS_UV) python

#
# Docker
#

# The container engine for docker-image, docker and apply-check: docker, else podman. A command line or
# environment value wins.
CONTAINER_ENGINE ?= $(shell for engine in docker podman; do command -v "$$engine" && break; done 2> /dev/null)

.PHONY: docker-image
# The chezmoi release setup.sh bootstraps. The tag stays in a shell variable: fetched text never
# becomes Make or shell source. A build has no gh, so the archive's checksum and release attestation
# are checked here on the host, and the Dockerfile checks its download against the verified sha256.
# An existing image is reused only when this recipe built it from this Dockerfile: its chezmoi.sha256
# label marks a host-verified archive and its dotfiles.dockerfile label the Dockerfile's git blob id;
# an image missing either, or built from another Dockerfile, is rebuilt.
docker-image:
	@engine="$(CONTAINER_ENGINE)"; \
	[ -n "$${engine}" ] || { echo "no container engine: install docker or podman (neither is on PATH)" >&2; exit 1; }; \
	dockerfile_id="$$(git hash-object Dockerfile)" || { echo "git hash-object Dockerfile failed; the image's Dockerfile is unknown" >&2; exit 1; }; \
	chezmoi_version="$$(bash -c 'source scripts/lib/github-release.sh && github_release_tag twpayne/chezmoi')"; \
	chezmoi_version="$${chezmoi_version#v}"; \
	[ -n "$${chezmoi_version}" ] || { echo "could not resolve a twpayne/chezmoi release" >&2; exit 1; }; \
	"$${engine}" info > /dev/null 2>&1 || { echo "$${engine} is installed but not reachable: start its daemon or machine (Docker Desktop, colima, podman machine start)" >&2; exit 1; }; \
	image_version="$$("$${engine}" inspect -f '{{ index .Config.Labels "chezmoi.version" }}' $(DOCKER_IMAGE_NAME) 2>/dev/null)"; \
	image_sha256="$$("$${engine}" inspect -f '{{ index .Config.Labels "chezmoi.sha256" }}' $(DOCKER_IMAGE_NAME) 2>/dev/null)"; \
	image_dockerfile="$$("$${engine}" inspect -f '{{ index .Config.Labels "dotfiles.dockerfile" }}' $(DOCKER_IMAGE_NAME) 2>/dev/null)"; \
	if [ "$${image_version}" != "$${chezmoi_version}" ] || [ "$${#image_sha256}" -ne 64 ] || [ "$${image_dockerfile}" != "$${dockerfile_id}" ]; then \
		case "$${engine##*/}" in \
		podman) arch="$$("$${engine}" info --format '{{ .Host.Arch }}')" ;; \
		*) arch="$$("$${engine}" version --format '{{ .Server.Arch }}')" ;; \
		esac || { echo "$${engine} did not report its architecture" >&2; exit 1; }; \
		artifact="chezmoi_$${chezmoi_version}_linux_$${arch}.tar.gz"; \
		status=0; \
		chezmoi_sha256="$$(bash -c 'source scripts/lib/github-release.sh && github_release_verified_sha256 twpayne/chezmoi "$$@"' _ "v$${chezmoi_version}" "$${artifact}" "chezmoi_$${chezmoi_version}_checksums.txt")" || status=$$?; \
		case "$${status}" in \
		0) ;; \
		2) echo "chezmoi v$${chezmoi_version}: its release attestation needs gh 2.93.0 or newer logged in to github.com: run make gh-auth, then make docker" >&2; exit 1 ;; \
		*) echo "chezmoi v$${chezmoi_version} failed its checksum or release attestation; nothing was built" >&2; exit 1 ;; \
		esac; \
		"$${engine}" build -t $(DOCKER_IMAGE_NAME) . --build-arg USERNAME="$$(whoami)" --build-arg DOCKERFILE_ID="$${dockerfile_id}" --build-arg CHEZMOI_VERSION="$${chezmoi_version}" --build-arg CHEZMOI_SHA256="$${chezmoi_sha256}"; \
	fi

.PHONY: docker
docker: docker-image
	"$(CONTAINER_ENGINE)" run -it -v "$$(pwd):/home/$$(whoami)/.local/share/chezmoi" --hostname dotfiles-test $(DOCKER_IMAGE_NAME) /bin/bash --login

.PHONY: apply-check
# Applies this working tree as a fresh Ubuntu client, then as a fresh server, each in a throwaway container,
# and runs scripts/apply-check.sh's credential-free doctor checks; that script says what is checked and what
# is left out. The tree is mounted read-only and copied inside; the container gets no network, no credential
# and no host HOME, and --rm discards it. GITHUB_ACTIONS and RUNNER_TEMP declare it a CI runner in the sense
# of scripts/lib/ci-runner.sh: as keyless as a runner, so the chezmoi config renders without age encryption.
# The apply-container job of .github/workflows/apply-check.yml runs this same target.
apply-check: docker-image
	@status=0; summary=""; \
	for system in client server; do \
		if "$(CONTAINER_ENGINE)" run --rm --network none -e GITHUB_ACTIONS=true -e RUNNER_TEMP=/tmp \
			-v "$(CURDIR):/src:ro" $(DOCKER_IMAGE_NAME) bash /src/scripts/apply-check.sh --system "$${system}"; then \
			summary="$${summary} $${system}=passed"; \
		else \
			summary="$${summary} $${system}=failed"; status=1; \
		fi; \
	done; \
	printf '\nmake apply-check:%s\n' "$${summary}"; \
	exit "$${status}"

#
# Chezmoi
#

.PHONY: setup
setup:
	./setup.sh

.PHONY: init
init:
	chezmoi init --apply --verbose

.PHONY: update
# Pulls, applies, updates installed tools through each manager's own safety
# features (scripts/upgrade-tools.sh; SYSTEM=1 adds apt), then refreshes agent assets.
# Operator phase (interactive, once per machine): ./setup.sh (chezmoi init prompts,
# age passphrase, sudo keepalive, macOS CLT read, Ubuntu chsh, SSH/gh/codex logins,
# run_once_* scripts), plus `sudo -v` right before `make update` when the pulled
# diff touches install/** or .chezmoiscripts/**, and with SYSTEM=1.
# Unattended `make update`: never prompts, except a Homebrew cask whose upgrade runs sudo.
update:
	@git fetch --quiet origin main || true
	@branch="$$(git branch --show-current 2>/dev/null || true)"; \
	upstream="$$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"; \
	reason=""; \
	if [ -n "$$(git ls-files -u)" ]; then \
		reason="index has unmerged files; resolve the conflict (git add/commit or git reset) before pulling"; \
	elif [ "$$branch" != main ]; then \
		reason="current branch is $${branch:-detached}, not main"; \
	elif [ "$$upstream" != origin/main ]; then \
		reason="upstream is $${upstream:-unset}, not origin/main"; \
	elif ! git diff --quiet || ! git diff --cached --quiet; then \
		reason="tracked files have staged or unstaged changes"; \
	fi; \
	if [ -n "$$reason" ]; then \
		printf "Notice: local source not pulled (%s); run 'git -C %s pull' to fetch remote updates.\n" "$$reason" "$(CURDIR)"; \
	elif ! git pull --ff-only; then \
		printf 'Warning: git pull --ff-only failed; continuing with local source.\n' >&2; \
	fi
	@$(MAKE) --no-print-directory update-tree

.PHONY: update-tree
# Everything after the pull, in a second make that reads the Makefile the pull
# just fetched, so a recipe change lands in the same run. SYSTEM reaches it
# through MAKEFLAGS.
update-tree:
	@# The archive externals, fetched retried and verified into chezmoi's cache before apply reads them (U96).
	bash -c 'source scripts/lib/chezmoi-externals.sh && prefetch_chezmoi_externals chezmoi'
	chezmoi apply --verbose
	@if [ -d "$$HOME/.local/share/chezmoi-private" ] && [ -f "$$HOME/.config/chezmoi-private/chezmoi.yaml" ]; then \
		chezmoi --source "$$HOME/.local/share/chezmoi-private" \
			--config "$$HOME/.config/chezmoi-private/chezmoi.yaml" \
			apply --verbose; \
	else \
		echo "Warning: private chezmoi source/config not found. Skipping private dotfiles."; \
	fi
	./scripts/upgrade-tools.sh $(if $(filter 1 true yes,$(SYSTEM)),--system,)
	./scripts/update-agent-assets.sh
	@if ! command -v herdr > /dev/null 2>&1; then \
		echo "Herdr command not found; skipping config reload."; \
		exit 0; \
	fi; \
	if ! herdr_status="$$(herdr status server --json)" || \
		! server_status="$$(printf '%s\n' "$$herdr_status" | jq -er '\
		if type == "object" and (.status | type == "string") \
		then .status else error("invalid Herdr server status") end')"; then \
		server_status=unreachable; \
	fi; \
	case "$$server_status" in \
		running) \
			if reload_output="$$(herdr server reload-config 2>&1)"; then \
				[ -z "$$reload_output" ] || printf '%s\n' "$$reload_output"; \
			else \
				[ -z "$$reload_output" ] || printf '%s\n' "$$reload_output" >&2; \
				case "$$reload_output" in \
					*protocol_mismatch*) printf '%s\n' "Herdr was updated; restart the server with 'herdr server stop' or recreate the Ghostty session, then run 'herdr server reload-config' manually." >&2 ;; \
					*) exit 1 ;; \
				esac; \
			fi ;; \
		not_running) echo "Herdr server is not running; skipping config reload." ;; \
		*) echo "Herdr server unreachable; skipping config reload." >&2 ;; \
	esac

.PHONY: apply
apply: update

.PHONY: gh-auth
# Interactive: log in this machine's GitHub account when gh holds no working login.
gh-auth:
	./scripts/gh-auth.sh

.PHONY: doctor
doctor:
	@tool_status=0; runtime_status=0; runtime_result=passed; \
	./scripts/check-tools.sh || tool_status=$$?; \
	./scripts/check-sleep.sh || tool_status=$$?; \
	if [ -x "$$HOME/.local/bin/omp" ]; then ./scripts/update-agent-assets.sh check_pi_claude_bridge || tool_status=$$?; \
		./scripts/update-agent-assets.sh check_pstack || tool_status=$$?; \
	else echo "optional warning: pi-claude-bridge and pstack checks skipped because omp is not installed"; fi; \
	if [ -d home/dot_agents ] && [ -d home/dot_claude ] && [ -d home/dot_codex ]; then \
		./scripts/check-agent-runtime.py || runtime_status=$$?; \
		./scripts/lint-retired-terms.py || runtime_status=$$?; \
	else \
		echo "optional warning: agent runtime check skipped because source roots are incomplete"; \
		runtime_result=not-applicable; \
	fi; \
	[ "$$runtime_status" -eq 0 ] || runtime_result=failed; \
	tool_result=passed; [ "$$tool_status" -eq 0 ] || tool_result=failed; \
	printf '\nDoctor summary: tools=%s; runtime=%s\n' "$$tool_result" "$$runtime_result"; \
	[ "$$tool_status" -eq 0 ] && [ "$$runtime_status" -eq 0 ]

.PHONY: usage-snapshot
usage-snapshot:
	./scripts/usage-snapshot.sh

.PHONY: usage-report
usage-report:
	uv run python scripts/usage-report.py

.PHONY: watch
watch:
	DOTFILES_DEBUG=1 watchexec -- chezmoi apply --verbose

.PHONY: reset
reset:
	chezmoi state delete-bucket --bucket=scriptState

.PHONY: reset-config
reset-config:
	chezmoi init --data=false

# The lint tools' versions (U97): each is one value in this mise config, the `version` of [tools."http:shellcheck"],
# [tools."http:shfmt"] and [tools."http:ruff"] and the exact "npm:prettier", which hosts get from mise and CI installs
# from a copy of the same file. scripts/ci/pinned-tool-version.sh runs first in each lint target and refuses a tool on
# PATH of any other version, naming both.
LINT_PIN_CONFIG := home/dot_mise/config.toml
# Each check reads one tracked-file set from scripts/ci/run-on-lint-files.sh, the same call CI's steps make, so an
# untracked or ignored file is never read and local and CI check the same files (U97).

.PHONY: format
format:
	@scripts/ci/pinned-tool-version.sh $(LINT_PIN_CONFIG) shfmt ruff prettier
	scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d
	scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check
	scripts/ci/run-on-lint-files.sh markdown prettier --check

# UNIT_TEST_JOBS=1 is the serial run; any other count runs the test modules in parallel shards, that many at a time
# (0, the default, is the CPU count), with one combined summary (scripts/ci/unittest-shards.py). Tests that run
# `uv run --offline --with pyyaml` against the real uv cache found PyYAML there only because an
# earlier module of the serial order had fetched it; the shards keep no such order, so the cache gets it first.
UNIT_TEST_JOBS ?= 0

.PHONY: unit-test
unit-test:
ifeq ($(UNIT_TEST_JOBS),1)
	uv run python -m unittest discover -s tests/unit -v
else
	$(UV_PYYAML) python -c 'import yaml'
	uv run python scripts/ci/unittest-shards.py --start tests/unit --jobs $(UNIT_TEST_JOBS)
endif

# The index form fails inside the Claude sandbox even while the uv cache holds PyYAML, so a probe picks the cache first.
UV_PYYAML = $(if $(shell uv run --offline --with pyyaml python -c 'import yaml' 2> /dev/null && echo y),uv run --offline --with pyyaml,uv run --with pyyaml)

.PHONY: validate-agent-assets
validate-agent-assets:
	$(UV_PYYAML) scripts/validate-agent-assets.py

.PHONY: codex-hook-trust
# Re-apply only the managed Codex config files so their modify scripts re-hash the trusted hooks;
# `make update` already does this as the last step of scripts/update-agent-assets.sh.
codex-hook-trust:
	bash -c 'source ./scripts/update-agent-assets.sh && refresh_codex_hook_trust'

.PHONY: render-check
render-check:
	$(UV_PYYAML) scripts/generate-agent-configs.py --check

.PHONY: retired-terms
# The retired-term lint over scripts/retired-terms.tsv, the one list of retired names, paths and removals (U72). CI runs
# it through tests/unit/test_lint_retired_terms.py, `make doctor` with the runtime checks, and
# the weekly drift watch (scripts/drift-watch.py: exit 1 lines become findings, any other non-zero a read failure).
retired-terms:
	./scripts/lint-retired-terms.py

.PHONY: drift
# The weekly drift watch (.github/workflows/drift-watch.yml) on this tree: prints its Markdown report. Reads
# api.github.com only; an exported GITHUB_TOKEN raises the GitHub API's 60-requests-an-hour anonymous limit. make
# turns every failing recipe into its own status 2, so the recipe prints the script's status (3: drift, 4: a read
# failed) on stderr before it fails; run scripts/drift-watch.py directly for the raw status.
drift:
	@status=0; $(UV_PYYAML) python -I scripts/drift-watch.py || status=$$?; \
	if [ "$$status" -ne 0 ]; then printf 'drift-watch.py exited %s (3: drift, 4: an upstream read failed)\n' "$$status" >&2; fi; \
	exit "$$status"

# ShellCheck groups (regime-cutover U38, U38b), git pathspecs; CI's ShellCheck step runs this target and nothing else
# (tests/unit/test_shellcheck_target.py pins the step, the groups and the checks). Each group's bash scripts (by
# shebang) are linted with the root .shellcheckrc, which turns on check-extra-masked-returns (SC2312), and with
# scripts/ci/masked-dirname-check.sh (a walk over shfmt's syntax tree; shfmt must be on PATH), which refuses any
# command substitution nested inside another, the dirname/basename shape SC2312 exempts included. A group whose pathspecs list no file, or no bash script, is refused. The installer group (mode
# `every`) also refuses a listed file that is not a bash script; the masked group (mode `bash`) skips the Python and
# other scripts among its files.
SHELLCHECK_INSTALLER_GROUP := setup.sh install/*.sh install/**/*.sh scripts/*.sh scripts/lib/*
SHELLCHECK_MASKED_GROUP := scripts/orchestrator/* home/dot_local/bin/common/executable_*
SHELLCHECK_PATHSPECS = $(foreach group,$(1),'$(group)')
# $(1) the mode (every or bash), $(2) the group.
SHELLCHECK_GROUP = bash -euo pipefail -c 'mode=$$1; shift; listed=$$(git ls-files -- "$$@"); \
	[[ -n $$listed ]] || { echo "shellcheck: no file in $$*" >&2; exit 1; }; \
	files=$$(awk '\''FNR == 1 && /^\#!.*bash/ { print FILENAME } { nextfile }'\'' $$listed); \
	[[ -n $$files ]] || { echo "shellcheck: no bash script in $$*" >&2; exit 1; }; \
	[[ $$mode != every || $$files == "$$listed" ]] || { echo "shellcheck: not a bash script, in $$*:" >&2; \
		printf "%s\n" $$listed | grep -vxF "$$files" >&2; exit 1; }; \
	printf "%s\n" $$files; status=0; shellcheck -x $$files || status=1; \
	scripts/ci/masked-dirname-check.sh $$files || status=1; exit $$status' _ $(1) $(call SHELLCHECK_PATHSPECS,$(2))

.PHONY: shellcheck
shellcheck:
	@scripts/ci/pinned-tool-version.sh $(LINT_PIN_CONFIG) shellcheck shfmt
	@printf '==> ShellCheck with .shellcheckrc and masked-dirname-check, every file of: %s\n' "$(SHELLCHECK_INSTALLER_GROUP)"
	$(call SHELLCHECK_GROUP,every,$(SHELLCHECK_INSTALLER_GROUP))
	@printf '==> ShellCheck with .shellcheckrc and masked-dirname-check, bash scripts of: %s\n' "$(SHELLCHECK_MASKED_GROUP)"
	$(call SHELLCHECK_GROUP,bash,$(SHELLCHECK_MASKED_GROUP))

#
# Documentation
#

.PHONY: docs
docs:
	@echo "==> Generating docs"
	./scripts/generate-docs.sh
	@echo "==> Refreshing TOC"
	$(MKDOCS_PYTHON) scripts/refresh-mkdocs-toc.py
	@echo "==> Building docs"
	$(MKDOCS) build --clean --strict

.PHONY: serve
serve: docs
	@echo "==> Serving docs"
	$(MKDOCS) serve -a $(HOST):$(PORT)

.PHONY: deploy
deploy: docs
	@echo "==> Deploying docs"
	$(MKDOCS) gh-deploy --force --ignore-version

.PHONY: clean
clean:
	@echo "==> Cleaning generated docs"
	rm -rf docs/reference site
	rm -f docs/index.md docs/catalog.md
