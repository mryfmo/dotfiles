# frozen_string_literal: true

# Core coverage engine (used by bashcov to build SimpleCov::Result).
require "simplecov"
# Export Cobertura XML for Codecov ingestion.
require "simplecov-cobertura"
# Keep local HTML output for debugging artifact inspection.
require "simplecov-html"

# Generate both human-readable and machine-readable outputs in one run:
# - HTML: quick local/manual diagnosis
# - Cobertura XML: CI upload target (`coverage/coverage.xml`)
SimpleCov.formatters = SimpleCov::Formatter::MultiFormatter.new(
  [
    SimpleCov::Formatter::HTMLFormatter,
    SimpleCov::Formatter::CoberturaFormatter,
  ]
)

SimpleCov.start do
  # CI workflow expects this exact directory and uploads `coverage/coverage.xml`.
  coverage_dir "coverage"

  # Exclude tests themselves from target coverage metrics.
  add_filter "/tests/"
  # Exclude generated coverage artifacts to avoid recursive self-counting.
  add_filter "/coverage/"
  # Exclude transient Bats/bashcov implementation files and external helper
  # scripts that can disappear before SimpleCov formats the final report.
  add_filter %r{^/tmp/bats-run-}
  add_filter %r{^/home/runner/\.tmux/plugins/tpm/}
  add_filter %r{^/Users/runner/\.tmux/plugins/tpm/}
  add_filter %r{^/etc/profile$}
  add_filter %r{^\.$}
  add_filter %r{^environment$}
  add_filter %r{^main$}
end
