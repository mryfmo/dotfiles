# frozen_string_literal: true

# Keep bashcov focused on repository-maintained shell sources. Bats and
# third-party installer helpers create temporary files while traced by bashcov;
# filtering them before formatting prevents noisy warnings for deleted or
# non-project files without hiding coverage for maintained scripts.
project_root = File.expand_path(__dir__)
covered_roots = %w[install scripts].map do |relative_path|
  File.join(project_root, relative_path) + File::SEPARATOR
end

SimpleCov.add_filter do |source_file|
  absolute_path = File.expand_path(source_file.filename, project_root)
  covered_roots.none? { |covered_root| absolute_path.start_with?(covered_root) }
end

SimpleCov.add_group 'Install scripts', 'install'
SimpleCov.add_group 'Repository scripts', 'scripts'
