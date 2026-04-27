#!/usr/bin/env ruby
# frozen_string_literal: true

require "bashcov"

Bashcov.parse_options!(ARGV)

require "bashcov/runner"

# This wrapper intentionally mirrors Bashcov's executable flow so repository-
# specific trace filtering can run before Bashcov converts coverage into
# SimpleCov data. Review this file when upgrading the bashcov gem.
module DotfilesBashcovRunnerFilter
  PROJECT_ROOT = File.expand_path("..", __dir__)
  COVERED_ROOTS = %w[install scripts].map do |relative_path|
    File.join(PROJECT_ROOT, relative_path) + File::SEPARATOR
  end.freeze

  def expunge_invalid_files!
    @coverage.delete_if do |filename, _coverage|
      absolute_path = File.expand_path(filename.to_s, PROJECT_ROOT)
      next true if COVERED_ROOTS.none? { |covered_root| absolute_path.start_with?(covered_root) }

      if !filename.file?
        write_warning "#{filename} was executed but has been deleted since then - it won't be reported in coverage."
        true
      elsif !@detective.shellscript?(filename)
        write_warning "#{filename} was partially executed but has invalid Bash syntax - it won't be reported in coverage."
        true
      else
        false
      end
    end
  end

  def convert_coverage
    @coverage.each_with_object({}) do |(filename, coverage), converted|
      path = filename.to_s
      next unless File.file?(path)

      lines = coverage.is_a?(Hash) ? coverage["lines"] : coverage
      next unless lines.respond_to?(:first)

      line_count = File.foreach(path).count
      converted[path] = lines.first(line_count)
    rescue Errno::ENOENT
      next
    end
  end
end

Bashcov::Runner.prepend(DotfilesBashcovRunnerFilter)

runner = Bashcov::Runner.new(Bashcov.command)
status = runner.run
coverage = runner.result

require "simplecov"

SimpleCov.start
SimpleCov.command_name(Bashcov.command_name)
SimpleCov.root(Bashcov.root_directory)

result = SimpleCov::Result.new(coverage)
if SimpleCov.use_merging
  SimpleCov::ResultMerger.store_result(result)
  result = SimpleCov::ResultMerger.merged_result
end

SimpleCov.at_exit do
  puts "Run completed using #{Bashcov.fullname}" unless Bashcov.mute

  begin
    original_stdout = $stdout

    if Bashcov.mute
      require "stringio"
      $stdout = StringIO.new
    end

    result.format!
  ensure
    $stdout = original_stdout
  end
end

exit(status.exitstatus)
