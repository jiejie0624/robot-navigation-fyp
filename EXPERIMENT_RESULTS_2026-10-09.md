# Simulator experiment results — 2026-10-09

## Experiment setup

Two batches were run in the public Room Rover simulator, one on a 15 × 15 grid and one on a 25 × 25 grid. Each batch contains 24 map layouts (six fixed scenarios and 18 seeded maps), two planners (A* and D* Lite), and ten recorded repetitions per map/planner combination: 480 rows per grid size, 960 total. The simulator performed one unrecorded warm-up for each map/planner combination. Both batches used the simulator's three-cell directional sensor and four-neighbour movement.

The raw records include map coordinates, start, heading, goal, seed, planner, outcome, moves, replans, expanded nodes, and planning times. Planning time excludes animation delay. The batch does not record the computer model or browser version, so millisecond timings should be treated as observations from this particular browser session.

## Outcome and safety check

| Grid | Planner | Reached goal | Expected no-route | Unexpected outcome | Blocked-cell attempts |
|---|---|---:|---:|---:|---:|
| 15 × 15 | A* | 230 / 240 | 10 / 240 | 0 | 0 |
| 15 × 15 | D* Lite | 230 / 240 | 10 / 240 | 0 | 0 |
| 25 × 25 | A* | 230 / 240 | 10 / 240 | 0 | 0 |
| 25 × 25 | D* Lite | 230 / 240 | 10 / 240 | 0 | 0 |

All 240 map/repeat pairs at each grid size had matching A* and D* Lite outcomes. The ten no-route records per planner are expected: the preset map has a wall separating the start and goal. Neither planner attempted to move into a blocked cell in any recorded run.

## Per-run metric distributions

Values below are medians, with the interquartile range (Q1–Q3) in parentheses. Timing is in milliseconds; moves, replans, and expanded values are counts. Each planner contributes 240 rows per grid size, including the expected no-route scenario.

| Grid | Planner | Planning time, ms | Expanded nodes | Moves | Replans |
|---|---|---:|---:|---:|---:|
| 15 × 15 | A* | 0.20 (0.10–0.55) | 72 (46–215) | 15 (8.5–25) | 3 (1–9) |
| 15 × 15 | D* Lite | 0.70 (0.40–1.60) | 57 (27–119.5) | 16 (8.5–21) | 3 (1–8.5) |
| 25 × 25 | A* | 0.20 (0.10–0.95) | 111.5 (65–417.5) | 20 (15–33) | 2.5 (1–6) |
| 25 × 25 | D* Lite | 0.90 (0.60–2.35) | 74.5 (52.5–170) | 20 (15–33) | 2.5 (1–7) |

## Map-matched comparison

The analysis file computes D* Lite minus A* for each matching map and repeat. Across the 240 comparisons at each size, the median difference in total planning time was +0.50 ms (Q1–Q3: +0.20 to +1.05 ms) on 15 × 15 and +0.55 ms (+0.30 to +1.00 ms) on 25 × 25. The median expanded-node difference was −30.5 (−101.5 to −1) and −35.5 (−162 to −15), respectively. A negative expanded-node difference means D* Lite expanded fewer nodes in these observations.

The median move difference was zero at both sizes, although some maps had different route lengths: 30 comparisons were shorter and 30 longer for D* Lite on 15 × 15; 20 were shorter and 30 longer on 25 × 25. This supports a limited observation: D* Lite expanded fewer nodes in most paired runs, while its measured planning time was higher in most runs in this implementation and browser session. Expanded-node count is not elapsed runtime, and these data do not establish that one algorithm is generally better.

These are **map-matched end-to-end task comparisons**, not runs that replay an identical sequence of newly discovered obstacles. Because the planners can select different routes, they may encounter different cells and receive different map updates. Ten repetitions of the same layouts characterize repeat variation; they do not increase the number of independent maps beyond 24 per grid size. No physical robot was tested.

## Files

- `benchmark-15x15-2026-10-09.csv` and `benchmark-25x25-2026-10-09.csv`: raw 480-row exports.
- `benchmark-*-summary.csv`: outcome counts and per-planner metric summaries.
- `benchmark-*-paired-differences.csv`: 240 matched map/repeat comparisons per grid size.
- `benchmark-*-paired-summary.csv`: per-map paired medians and quartiles.
- `analyze_benchmark.py`: reproducible summary generator.

