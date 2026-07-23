#!/usr/bin/env python3
"""Report model-family usage changes without modifying model profiles."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


DEFAULT_USAGE_DIR = Path(".agents/worklog/claude/usage")
DEFAULT_BASELINE = DEFAULT_USAGE_DIR / "20260723-baseline.json"
REVIEW_WINDOWS_DAYS = (7, 14)
FABLE_FAMILY = "claude-fable"
MANUAL_QUALITY_LINE = (
    "quality side (rework/review misses) is manual — "
    "decide via PR, never automatically"
)
TOKEN_FIELDS = ("inputTokens", "outputTokens", "cacheReadTokens")
FAMILY_NAMES = {
    "claude-fable": "claude-fable",
    "claude-opus": "claude-opus",
    "claude-sonnet": "claude-sonnet",
    "claude-haiku": "claude-haiku",
}


def model_family(model_name: str) -> str:
    """Return the stable family used for comparisons."""
    lowered = model_name.lower()
    for prefix, family in FAMILY_NAMES.items():
        if lowered.startswith(prefix):
            return family
    if lowered.startswith("gpt-") and "sol" in lowered:
        return "gpt-sol"
    return lowered or "unknown"


def snapshot_sort_key(path: Path) -> tuple[str, str]:
    """Sort dated snapshots deterministically, including malformed JSON files."""
    match = re.match(r"(\d{8})", path.name)
    return (match.group(1) if match else "", path.name)


def load_snapshot(path: Path, warnings: list[str]) -> dict[str, Any]:
    """Load one snapshot and convert errors into report warnings."""
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        warnings.append(f"WARN: unable to read snapshot {path}: {error}")
        return {}
    if not isinstance(data, dict):
        warnings.append(f"WARN: snapshot {path} is not a JSON object")
        return {}
    return data


def records_from_snapshot(
    data: dict[str, Any], path: Path, warnings: list[str]
) -> list[Any]:
    """Return one supported ccusage record list, preferring weekly data."""
    for section_name, list_name in (("weekly", "weekly"), ("daily", "daily")):
        section = data.get(section_name)
        if isinstance(section, dict):
            records = section.get(list_name)
            if isinstance(records, list):
                return records
    warnings.append(f"WARN: snapshot {path} has no supported ccusage records")
    return []


def token_value(
    value: Any, field: str, path: Path, warnings: list[str]
) -> int:
    """Return a non-negative token count or zero for malformed values."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        warnings.append(f"WARN: ignored invalid {field} in {path}")
        return 0
    return int(value)


def aggregate_models(
    data: dict[str, Any], path: Path, warnings: list[str]
) -> dict[str, dict[str, int]]:
    """Aggregate supported model breakdowns by stable model family."""
    totals: dict[str, dict[str, int]] = {}
    for record in records_from_snapshot(data, path, warnings):
        if not isinstance(record, dict):
            warnings.append(f"WARN: ignored malformed ccusage record in {path}")
            continue
        breakdowns = record.get("modelBreakdowns")
        if not isinstance(breakdowns, list):
            warnings.append(f"WARN: ignored record without modelBreakdowns in {path}")
            continue
        for breakdown in breakdowns:
            if not isinstance(breakdown, dict):
                warnings.append(f"WARN: ignored malformed model breakdown in {path}")
                continue
            name = breakdown.get("modelName")
            if not isinstance(name, str) or not name:
                warnings.append(f"WARN: ignored model breakdown without modelName in {path}")
                continue
            family = model_family(name)
            family_totals = totals.setdefault(
                family, {"inputTokens": 0, "outputTokens": 0, "cacheReadTokens": 0}
            )
            for field in TOKEN_FIELDS:
                family_totals[field] += token_value(
                    breakdown.get(field, 0), field, path, warnings
                )
    return totals


def captured_date(
    data: dict[str, Any], path: Path, warnings: list[str]
) -> date | None:
    """Read the capture date, falling back to the dated filename."""
    captured_at = data.get("captured_at")
    if isinstance(captured_at, str):
        try:
            return datetime.fromisoformat(captured_at).date()
        except ValueError:
            warnings.append(f"WARN: invalid captured_at in {path}")
    match = re.match(r"(\d{8})", path.name)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d").date()
    warnings.append(f"WARN: unable to determine capture date for {path}")
    return None


def percentage(numerator: int, denominator: int) -> float:
    """Return a percentage, using zero for an empty denominator."""
    return 100.0 * numerator / denominator if denominator else 0.0


def signed_integer(value: int) -> str:
    """Format an integer delta with an explicit sign."""
    return f"{value:+d}"


def resolve_paths(
    usage_dir: Path, baseline_path: Path | None, warnings: list[str]
) -> tuple[Path | None, Path | None]:
    """Resolve the baseline and latest snapshots."""
    snapshots = sorted(usage_dir.glob("*.json"), key=snapshot_sort_key)
    if baseline_path is not None and baseline_path.is_file():
        baseline = baseline_path
    elif snapshots:
        if baseline_path is not None:
            warnings.append(
                f"WARN: baseline {baseline_path} is unavailable; using oldest snapshot"
            )
        baseline = snapshots[0]
    else:
        warnings.append(f"WARN: no usage snapshots found in {usage_dir}")
        return None, None

    candidates = snapshots[:]
    if baseline not in candidates:
        candidates.append(baseline)
    latest = max(candidates, key=snapshot_sort_key)
    return baseline, latest


def model_lines(
    baseline: dict[str, dict[str, int]],
    latest: dict[str, dict[str, int]],
) -> list[str]:
    """Render per-family totals, shares, ratios, and baseline deltas."""
    latest_output_total = sum(item["outputTokens"] for item in latest.values())
    baseline_output_total = sum(item["outputTokens"] for item in baseline.values())
    lines: list[str] = []
    zero = {"inputTokens": 0, "outputTokens": 0, "cacheReadTokens": 0}
    for family in sorted(set(baseline) | set(latest)):
        current = latest.get(family, zero)
        previous = baseline.get(family, zero)
        current_total = sum(current.values())
        previous_total = sum(previous.values())
        output_share = percentage(current["outputTokens"], latest_output_total)
        previous_output_share = percentage(
            previous["outputTokens"], baseline_output_total
        )
        cache_ratio = percentage(current["cacheReadTokens"], current_total)
        previous_cache_ratio = percentage(
            previous["cacheReadTokens"], previous_total
        )
        lines.append(
            f"{family}: "
            f"input={current['inputTokens']} "
            f"({signed_integer(current['inputTokens'] - previous['inputTokens'])}), "
            f"output={current['outputTokens']} "
            f"({signed_integer(current['outputTokens'] - previous['outputTokens'])}), "
            f"cache-read={current['cacheReadTokens']} "
            f"({signed_integer(current['cacheReadTokens'] - previous['cacheReadTokens'])}), "
            f"output-share={output_share:.1f}% "
            f"({output_share - previous_output_share:+.1f}pp), "
            f"cache-read-ratio={cache_ratio:.1f}% "
            f"({cache_ratio - previous_cache_ratio:+.1f}pp)"
        )
    return lines


def candidate_line(latest: dict[str, dict[str, int]]) -> str:
    """Render the Fable non-cache dominance verdict and its inputs."""
    claude_usage = {
        family: values["inputTokens"] + values["outputTokens"]
        for family, values in latest.items()
        if family.startswith("claude-")
    }
    total = sum(claude_usage.values())
    fable_usage = claude_usage.get(FABLE_FAMILY, 0)
    if claude_usage:
        largest_family, largest_usage = max(
            sorted(claude_usage.items()), key=lambda item: item[1]
        )
    else:
        largest_family, largest_usage = "none", 0
    verdict = "yes" if fable_usage > 0 and fable_usage == largest_usage else "no"
    return (
        f"interactive-downgrade-candidate: {verdict} "
        f"({FABLE_FAMILY} non-cache={fable_usage}, "
        f"share={percentage(fable_usage, total):.1f}%; "
        f"largest={largest_family} {largest_usage})"
    )


def due_lines(usage_dir: Path, baseline_date: date | None, today: date) -> list[str]:
    """Render reminders for elapsed review windows without matching notes."""
    if baseline_date is None:
        return []
    lines = []
    for days in REVIEW_WINDOWS_DAYS:
        due_date = baseline_date + timedelta(days=days)
        note = usage_dir / f"review-{due_date.isoformat()}.md"
        if today >= due_date and not note.is_file():
            lines.append(f"REVIEW DUE (+{days}d): {note.name} is missing")
    return lines


def generate_report(
    usage_dir: Path,
    baseline_path: Path | None = None,
    today: date | None = None,
) -> list[str]:
    """Generate a complete informational report as printable lines."""
    warnings: list[str] = []
    lines: list[str] = []
    baseline_path, latest_path = resolve_paths(usage_dir, baseline_path, warnings)
    if baseline_path is None or latest_path is None:
        return [*warnings, MANUAL_QUALITY_LINE]

    baseline_data = load_snapshot(baseline_path, warnings)
    latest_data = load_snapshot(latest_path, warnings)
    baseline_totals = aggregate_models(baseline_data, baseline_path, warnings)
    latest_totals = aggregate_models(latest_data, latest_path, warnings)
    baseline_date = captured_date(baseline_data, baseline_path, warnings)

    lines.extend(warnings)
    lines.append(f"baseline: {baseline_path}")
    lines.append(f"latest: {latest_path}")
    lines.extend(model_lines(baseline_totals, latest_totals))
    lines.extend(due_lines(usage_dir, baseline_date, today or date.today()))
    lines.append(candidate_line(latest_totals))
    lines.append(MANUAL_QUALITY_LINE)
    return lines


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("usage_dir", nargs="?", type=Path, default=DEFAULT_USAGE_DIR)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    return parser.parse_args()


def main() -> int:
    """Print the report and never act as a gate."""
    try:
        args = parse_args()
    except SystemExit:
        return 0
    try:
        lines = generate_report(args.usage_dir, args.baseline)
    except Exception as error:
        lines = [f"WARN: unable to generate usage report: {error}", MANUAL_QUALITY_LINE]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
