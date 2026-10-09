#!/usr/bin/env python3
"""Summarize controlled-replay CSVs by trace and paired repeat."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import median


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower, upper = math.floor(position), math.ceil(position)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("No replay rows to summarize")
    with path.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def trace_family(row: dict[str, str]) -> str:
    family = row.get("traceFamily", "").strip()
    if family:
        return family
    trace = row.get("traceId", "")
    return "-".join(trace.split("-")[:2]) if trace.startswith("seeded-") else trace


def analyze(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    pair_index: dict[tuple[str, ...], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row.get("planner") not in {"astar", "dstar"}:
            continue
        key = (row.get("batchId", ""), row.get("mapWidth", ""), row.get("traceId", ""), row.get("repeat", ""), row.get("checkpointIndex", ""))
        pair_index[key][row["planner"]] = row

    paired: dict[tuple[str, str, str], dict[str, dict[str, float]]] = defaultdict(lambda: {"astar": {"expanded": 0.0, "planningMs": 0.0}, "dstar": {"expanded": 0.0, "planningMs": 0.0}})
    parity: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    route_errors: dict[tuple[str, str, str], int] = defaultdict(int)
    outcome_matches: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    for key, planners in pair_index.items():
        if not {"astar", "dstar"}.issubset(planners):
            continue
        batch, width, trace, repeat, checkpoint = key
        summary_key = (batch, width, trace)
        a, d = planners["astar"], planners["dstar"]
        same_observation = all(a.get(field) == d.get(field) for field in ("current", "newlyRevealed", "knownObstacles", "goal", "expectedOutcome"))
        parity[summary_key].append(same_observation)
        outcome_matches[summary_key].append(a.get("outcome") == d.get("outcome"))
        for row in (a, d):
            if row.get("routeValid", "").lower() != "true" or row.get("outcome") != row.get("expectedOutcome"):
                route_errors[summary_key] += 1
        for planner, row in (("astar", a), ("dstar", d)):
            slot = paired[(batch, width, trace, repeat)][planner]
            slot["expanded"] += float(row.get("expanded") or 0)
            slot["planningMs"] += float(row.get("planningMs") or 0)

    run_groups: dict[tuple[str, str, str], list[dict[str, float]]] = defaultdict(list)
    for (batch, width, trace, repeat), planners in paired.items():
        run_groups[(batch, width, trace)].append({
            "repeat": float(repeat),
            "astarExpanded": planners["astar"]["expanded"],
            "dstarExpanded": planners["dstar"]["expanded"],
            "expandedDelta": planners["dstar"]["expanded"] - planners["astar"]["expanded"],
            "astarPlanningMs": planners["astar"]["planningMs"],
            "dstarPlanningMs": planners["dstar"]["planningMs"],
            "planningMsDelta": planners["dstar"]["planningMs"] - planners["astar"]["planningMs"],
        })

    planner_summary: list[dict[str, object]] = []
    paired_summary: list[dict[str, object]] = []
    for key, runs in sorted(run_groups.items()):
        batch, width, trace = key
        for planner in ("astar", "dstar"):
            result: dict[str, object] = {"batchId": batch, "mapWidth": width, "traceId": trace, "planner": planner, "repetitions": len(runs), "pairedCheckpoints": len(parity[key]), "matchedObservations": sum(parity[key]), "routeOrOutcomeErrors": route_errors[key]}
            for metric, field in (("expanded", f"{planner}Expanded"), ("planningMs", f"{planner}PlanningMs")):
                values = [run[field] for run in runs]
                result[f"{metric}MedianPerTrace"] = median(values)
                result[f"{metric}Q1"] = quantile(values, 0.25)
                result[f"{metric}Q3"] = quantile(values, 0.75)
            planner_summary.append(result)
        paired_row: dict[str, object] = {"batchId": batch, "mapWidth": width, "traceId": trace, "repetitions": len(runs), "pairedCheckpoints": len(parity[key]), "matchedObservations": sum(parity[key]), "outcomesMatched": sum(outcome_matches[key]), "routeOrOutcomeErrorsBothPlanners": route_errors[key]}
        for metric, field in (("expanded", "expandedDelta"), ("planningMs", "planningMsDelta")):
            values = [run[field] for run in runs]
            paired_row[f"dstarMinusAstar_{metric}Median"] = median(values)
            paired_row[f"dstarMinusAstar_{metric}Q1"] = quantile(values, 0.25)
            paired_row[f"dstarMinusAstar_{metric}Q3"] = quantile(values, 0.75)
            paired_row[f"dstarMinusAstar_{metric}DstarLowerRuns"] = sum(value < 0 for value in values)
            paired_row[f"dstarMinusAstar_{metric}EqualRuns"] = sum(value == 0 for value in values)
            paired_row[f"dstarMinusAstar_{metric}DstarHigherRuns"] = sum(value > 0 for value in values)
        paired_summary.append(paired_row)
    family_groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    row_by_trace = {(row.get("mapWidth", ""), row.get("traceId", "")): row for row in rows}
    for summary in paired_summary:
        source = row_by_trace.get((str(summary["mapWidth"]), str(summary["traceId"])), {})
        family_groups[(str(summary["mapWidth"]), trace_family(source))].append(summary)

    family_summary: list[dict[str, object]] = []
    metrics = (
        "dstarMinusAstar_expandedMedian",
        "dstarMinusAstar_planningMsMedian",
    )
    for (width, family), traces in sorted(family_groups.items()):
        result: dict[str, object] = {
            "mapWidth": width,
            "traceFamily": family,
            "independentTraces": len(traces),
            "pairedCheckpointRows": sum(int(item["pairedCheckpoints"]) for item in traces),
            "routeOrOutcomeErrorsBothPlanners": sum(int(item["routeOrOutcomeErrorsBothPlanners"]) for item in traces),
        }
        for metric in metrics:
            values = [float(item[metric]) for item in traces]
            stem = metric.removesuffix("Median")
            result[f"{stem}MedianAcrossTraceMedians"] = median(values)
            result[f"{stem}Q1AcrossTraceMedians"] = quantile(values, 0.25)
            result[f"{stem}Q3AcrossTraceMedians"] = quantile(values, 0.75)
        family_summary.append(result)

    return planner_summary, paired_summary, family_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    if not args.csv_file.is_file():
        parser.error(f"CSV file not found: {args.csv_file}")
    with args.csv_file.open("r", newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        parser.error("CSV contains no data rows")
    planner_rows, paired_rows, family_rows = analyze(rows)
    planner_path = args.csv_file.with_name(f"{args.csv_file.stem}-summary.csv")
    paired_path = args.csv_file.with_name(f"{args.csv_file.stem}-paired-summary.csv")
    family_path = args.csv_file.with_name(f"{args.csv_file.stem}-family-summary.csv")
    write_csv(planner_path, planner_rows)
    write_csv(paired_path, paired_rows)
    write_csv(family_path, family_rows)
    print(f"Read {len(rows)} checkpoint rows across {len(paired_rows)} size/trace cases.")
    print(f"Wrote per-planner trace totals: {planner_path}")
    print(f"Wrote paired replay differences: {paired_path}")
    print(f"Wrote family summaries (per-trace medians): {family_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
