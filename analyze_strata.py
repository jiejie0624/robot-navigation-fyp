#!/usr/bin/env python3
"""Aggregate Room Rover results by map family without treating repeats as maps."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import median

METRICS = ("moves", "replans", "expanded", "planningMs")


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower, upper = math.floor(position), math.ceil(position)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def stratum(row: dict[str, str]) -> str:
    scenario = row.get("scenario", "")
    if scenario == "no-route":
        return "no_route"
    if scenario.startswith("seeded-"):
        return scenario.rsplit("-", 1)[0]
    return "fixed_reachable"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    maps: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("planner") in {"astar", "dstar"}:
            maps[(row.get("mapWidth", ""), row.get("mapHeight", ""), row.get("mapId", ""), stratum(row), row["planner"])].append(row)

    map_level: dict[tuple[str, str, str, str], dict[str, dict[str, object]]] = defaultdict(dict)
    for (width, height, map_id, family, planner), trials in maps.items():
        result: dict[str, object] = {
            "mapWidth": width,
            "mapHeight": height,
            "mapId": map_id,
            "stratum": family,
            "planner": planner,
            "trials": len(trials),
            "successes": sum(r.get("outcome") == "success" for r in trials),
            "expectedNoRoute": sum(r.get("expectedOutcome") == "no_route" and r.get("outcome") == "no_route" for r in trials),
            "unexpectedOutcomes": sum(bool(r.get("expectedOutcome")) and r.get("expectedOutcome") != r.get("outcome") for r in trials),
            "blockedAttemptRows": sum((float(r.get("blockedAttempts") or 0)) > 0 for r in trials),
        }
        for metric in METRICS:
            values = [float(r[metric]) for r in trials if r.get(metric, "")]
            result[f"{metric}Median"] = median(values) if values else ""
        map_level[(width, height, map_id, family)][planner] = result

    strata: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for (width, height, _map_id, family), planners in map_level.items():
        for planner, result in planners.items():
            strata[(width, height, family)].append(result)

    paired_map_diffs: dict[tuple[str, str, str], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    paired_counts: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    trial_index: dict[tuple[str, str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row.get("planner") not in {"astar", "dstar"} or not row.get("repeat"):
            continue
        key = (row.get("mapWidth", ""), row.get("mapHeight", ""), row.get("mapId", ""), row["repeat"])
        trial_index[key][row["planner"]] = row
    for (width, height, map_id, _repeat), planners in trial_index.items():
        if not {"astar", "dstar"}.issubset(planners):
            continue
        a, d = planners["astar"], planners["dstar"]
        family = stratum(a)
        group_key = (width, height, family)
        paired_counts[group_key].append(a.get("outcome") == d.get("outcome"))
        for metric in METRICS:
            if a.get(metric, "") and d.get(metric, ""):
                paired_map_diffs[(width, height, map_id, family)][metric].append(float(d[metric]) - float(a[metric]))

    diff_by_stratum: dict[tuple[str, str, str], dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for (width, height, _map_id, family), metrics in paired_map_diffs.items():
        for metric, values in metrics.items():
            diff_by_stratum[(width, height, family)][metric].append(median(values))

    output: list[dict[str, object]] = []
    for key, planner_rows in sorted(strata.items()):
        width, height, family = key
        for planner in ("astar", "dstar"):
            selected = [r for r in planner_rows if r["planner"] == planner]
            if not selected:
                continue
            result: dict[str, object] = {
                "mapWidth": width,
                "mapHeight": height,
                "stratum": family,
                "planner": planner,
                "independentMaps": len(selected),
                "trials": sum(int(r["trials"]) for r in selected),
                "successes": sum(int(r["successes"]) for r in selected),
                "expectedNoRoute": sum(int(r["expectedNoRoute"]) for r in selected),
                "unexpectedOutcomes": sum(int(r["unexpectedOutcomes"]) for r in selected),
                "blockedAttemptRows": sum(int(r["blockedAttemptRows"]) for r in selected),
                "outcomesMatchedPairs": sum(paired_counts[key]),
                "pairedTrials": len(paired_counts[key]),
            }
            for metric in METRICS:
                values = [float(r[f"{metric}Median"]) for r in selected if r[f"{metric}Median"] != ""]
                result[f"{metric}MapMedian"] = median(values) if values else ""
                result[f"{metric}MapQ1"] = quantile(values, 0.25) if values else ""
                result[f"{metric}MapQ3"] = quantile(values, 0.75) if values else ""
            for metric in METRICS:
                values = diff_by_stratum[key][metric]
                result[f"dstarMinusAstar_{metric}MapMedian"] = median(values) if values else ""
                result[f"dstarMinusAstar_{metric}MapQ1"] = quantile(values, 0.25) if values else ""
                result[f"dstarMinusAstar_{metric}MapQ3"] = quantile(values, 0.75) if values else ""
            output.append(result)
    return output


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
    results = analyze(rows)
    output = args.csv_file.with_name(f"{args.csv_file.stem}-strata-summary.csv")
    write_csv(output, results)
    print(f"Read {len(rows)} trials; summarized map-level medians across map families: {output}")
    print("The independent-map count is reported separately from repeated trials.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
