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

DOTFILES_SIMPLECOV_PROJECT_ROOT = project_root unless defined?(DOTFILES_SIMPLECOV_PROJECT_ROOT)
DOTFILES_SIMPLECOV_COVERED_ROOTS = covered_roots unless defined?(DOTFILES_SIMPLECOV_COVERED_ROOTS)

if defined?(Bashcov::Runner)
  # Bashcov records every traced Bash file before SimpleCov filters run. Drop
  # temporary and third-party traces early, then clamp coverage arrays to the
  # maintained file length so Cobertura output stays warning-free.
  module DotfilesBashcovRunnerFilter
    def expunge_invalid_files!
      @coverage.each_key do |filename|
        absolute_path = File.expand_path(filename.to_s, DOTFILES_SIMPLECOV_PROJECT_ROOT)
        if DOTFILES_SIMPLECOV_COVERED_ROOTS.none? { |covered_root| absolute_path.start_with?(covered_root) }
          @coverage.delete filename
        elsif !filename.file?
          @coverage.delete filename
          write_warning "#{filename} was executed but has been deleted since then - it won't be reported in coverage."
        elsif !@detective.shellscript?(filename)
          @coverage.delete filename
          write_warning "#{filename} was partially executed but has invalid Bash syntax - it won't be reported in coverage."
        end
      end
    end

    def convert_coverage
      @coverage.each_with_object({}) do |(filename, coverage), converted|
        line_count = File.readlines(filename.to_s).length
        converted[filename.to_s] = coverage.first(line_count)
      end
    end
  end

  Bashcov::Runner.prepend(DotfilesBashcovRunnerFilter)
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
