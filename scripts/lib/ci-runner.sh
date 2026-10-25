#!/usr/bin/env bash
# shellcheck shell=bash

# @file scripts/lib/ci-runner.sh
# @brief The repository's one definition of "running in CI": a GitHub Actions runner.
# @description
#   CI-only paths (the dirty-source guard skip, `brew info` instead of `brew
#   install`, the runner's Homebrew tap trust, the `make update` skip, the
#   chezmoi config without age encryption) must never run on an operator's host.
#   The generic `CI` variable cannot tell them apart: agent shells such as omp's
#   bash tool export `CI=true` into every command they run. Only a GitHub
#   Actions runner sets both `GITHUB_ACTIONS=true` and `RUNNER_TEMP`, so the
#   decision reads those and never `CI`.
#   Sourced by scripts and installers; the chezmoi scripts include it before
#   their own body. setup.sh runs before the repository exists, so it carries a
#   copy of the function below, and home/.chezmoi.yaml.tmpl states the same test
#   in template syntax; tests/unit/test_ci_runner.py keeps all three equal.

#
# @description Succeed on a GitHub Actions runner, whatever `CI` holds.
# @exitcode 0 `GITHUB_ACTIONS` is `true` and `RUNNER_TEMP` is set.
# @exitcode 1 Anywhere else, an agent shell exporting `CI=true` included.
#
function is_ci_runner() {
    [ "${GITHUB_ACTIONS:-}" = true ] && [ -n "${RUNNER_TEMP:-}" ]
}
