#!/usr/bin/env python3
"""Summarize Room Rover CSV exports using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import fmean, median


METRICS = (
    "moves",
    "replans",
    "found",
    "blockedAttempts",
    "expanded",
    "initialPlanningMs",
    "replanPlanningMs",
    "planningMs",
)


def number(row: dict[str, str], field: str) -> float | None:
    value = row.get(field, "").strip()
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def csv_value(value: object) -> object:
    if isinstance(value, float):
        return round(value, 6)
    return value


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({key: csv_value(value) for key, value in row.items()} for row in rows)


def summarize(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row.get("mapWidth", ""), row.get("mapHeight", ""), row.get("scenario", ""), row.get("planner", ""))].append(row)

    summaries: list[dict[str, object]] = []
    for (width, height, scenario, planner), group in sorted(groups.items()):
        count = len(group)
        success_count = sum(row.get("outcome") == "success" for row in group)
        expected_rows = [row for row in group if row.get("expectedOutcome", "").strip()]
        expected_count = sum(row.get("expectedOutcome") == row.get("outcome") for row in expected_rows)
        result: dict[str, object] = {
            "mapWidth": width,
            "mapHeight": height,
            "scenario": scenario,
            "planner": planner,
            "rows": count,
            "successRate": success_count / count if count else 0,
            "expectedOutcomeRows": len(expected_rows),
            "expectedOutcomeRate": expected_count / len(expected_rows) if expected_rows else "",
            "rowsWithBlockedAttempt": sum((number(row, "blockedAttempts") or 0) > 0 for row in group),
        }
        for metric in METRICS:
            values = [value for row in group if (value := number(row, metric)) is not None]
            result[f"{metric}Mean"] = fmean(values) if values else ""
            result[f"{metric}Median"] = median(values) if values else ""
            result[f"{metric}Q1"] = quantile(values, 0.25) if values else ""
            result[f"{metric}Q3"] = quantile(values, 0.75) if values else ""
        summaries.append(result)
    return summaries


def paired_differences(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], int]:
    """Return D* Lite minus A* rows, pairing only identical map/repeat conditions."""
    index: dict[tuple[str, ...], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row.get("planner") not in {"astar", "dstar"}:
            continue
        batch_id = row.get("batchId", "").strip()
        repeat = row.get("repeat", "").strip()
        # Old interactive diagnostics lack these identifiers; never infer pairs from row order.
        if not batch_id or not repeat:
            continue
        key = (
            batch_id,
            row.get("mapWidth", ""),
            row.get("mapHeight", ""),
            row.get("mapId", row.get("scenario", "")),
            repeat,
        )
        index[key][row["planner"]] = row

    differences: list[dict[str, object]] = []
    unpaired = 0
    for key, planners in sorted(index.items()):
        if "astar" not in planners or "dstar" not in planners:
            unpaired += 1
            continue
        astar, dstar = planners["astar"], planners["dstar"]
        record: dict[str, object] = {
            "batchId": key[0],
            "mapWidth": key[1],
            "mapHeight": key[2],
            "mapId": key[3],
            "repeat": key[4],
            "astarOutcome": astar.get("outcome", ""),
            "dstarOutcome": dstar.get("outcome", ""),
        }
        for metric in METRICS:
            a_value, d_value = number(astar, metric), number(dstar, metric)
            record[f"dstarMinusAstar_{metric}"] = d_value - a_value if a_value is not None and d_value is not None else ""
        differences.append(record)
    return differences, unpaired


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a Room Rover benchmark CSV without third-party packages.")
    parser.add_argument("csv_file", type=Path, help="CSV downloaded from the simulator")
    args = parser.parse_args()
    if not args.csv_file.is_file():
        parser.error(f"CSV file not found: {args.csv_file}")

    with args.csv_file.open("r", newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        parser.error("CSV contains no data rows")

    summary_rows = summarize(rows)
    differences, unpaired = paired_differences(rows)
    summary_path = args.csv_file.with_name(f"{args.csv_file.stem}-summary.csv")
    pairs_path = args.csv_file.with_name(f"{args.csv_file.stem}-paired-differences.csv")

    summary_fields = list(summary_rows[0])
    pair_fields = ["batchId", "mapWidth", "mapHeight", "mapId", "repeat", "astarOutcome", "dstarOutcome"]
    pair_fields.extend(f"dstarMinusAstar_{metric}" for metric in METRICS)
    write_csv(summary_path, summary_fields, summary_rows)
    write_csv(pairs_path, pair_fields, differences)

    print(f"Read {len(rows)} input rows across {len(summary_rows)} map/planner groups.")
    print(f"Wrote summary: {summary_path}")
    if differences:
        print(f"Wrote {len(differences)} paired D* Lite − A* comparisons: {pairs_path}")
    else:
        print(f"No paired rows found; {unpaired} groups were unpaired. Older diagnostic CSVs do not have batchId/repeat fields, so they cannot be safely paired.")
        print(f"Wrote an empty paired-comparison file: {pairs_path}")
    print("Interpret timing summaries as device- and browser-specific; inspect completion and blocked attempts before comparing speed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
