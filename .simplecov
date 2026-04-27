# frozen_string_literal: true

# Core coverage engine used by bashcov to build SimpleCov::Result.
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

project_root = File.expand_path(__dir__)
covered_roots = %w[install scripts].map do |relative_path|
  File.join(project_root, relative_path) + File::SEPARATOR
end

SimpleCov.start do
  # CI workflow expects this exact directory and uploads `coverage/coverage.xml`.
  coverage_dir "coverage"

  # Keep bashcov focused on repository-maintained shell sources. Bats and
  # third-party installer helpers create temporary files while traced by bashcov;
  # filtering them before formatting prevents noisy warnings for deleted or
  # non-project files without hiding coverage for maintained scripts.
  add_filter do |source_file|
    absolute_path = File.expand_path(source_file.filename, project_root)
    covered_roots.none? { |covered_root| absolute_path.start_with?(covered_root) }
  end

  add_group "Install scripts", "install"
  add_group "Repository scripts", "scripts"
end
