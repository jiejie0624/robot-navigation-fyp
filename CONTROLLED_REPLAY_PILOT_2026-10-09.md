# Controlled replay pilot — 2026-10-09

## What was run

The simulator now has a separate **固定更新回放** action. At each predetermined checkpoint, A* and D* Lite receive the same current cell, goal, newly revealed obstacle cells, and cumulative known-obstacle set. Repeated A* starts a fresh search at each checkpoint. D* Lite retains its search state and updates it with the same new cells and checkpoint positions. Both run planners generate a proposed path, which is checked independently for legal adjacent steps, known-obstacle avoidance, and correct goal termination. Reachability is checked with a separate breadth-first traversal.

Four deterministic traces were used: one blocker, sequential blockers, updates off the direct route, and a wall that eventually disconnects the goal. Each trace has three checkpoints. Ten recorded repetitions plus one unrecorded warm-up were run per trace/planner at each of the 15 × 15 and 25 × 25 sizes.

## Pilot integrity results

- 480 checkpoint rows total: 4 traces × 3 checkpoints × 10 repetitions × 2 planners × 2 sizes.
- 240 map-matched A*/D* Lite checkpoint pairs; all had identical current positions, newly revealed cells, and known-obstacle sets.
- 400 successful path results and 80 correctly reported no-route results across both sizes.
- Zero path-validation errors and zero outcome mismatches.

The wall trace uses obstacles across the full row, including the grid edge cells, so the planner cannot route around either end inside the grid. Its first checkpoint is reachable before the wall is revealed; the following two checkpoints correctly have no route.

## Preliminary measurements

For each trace and repetition, expanded nodes and planning time were summed across its three checkpoints. The table reports paired D* Lite minus A* median differences over ten repeats. Negative expansions indicate fewer expanded nodes for D* Lite; positive time indicates higher measured planning time for D* Lite.

| Grid | Trace | Median expansion difference | Median total planning-time difference |
|---|---|---:|---:|
| 15 × 15 | Single blocker | −13 | +0.60 ms |
| 15 × 15 | Sequential blockers | −13 | +0.85 ms |
| 15 × 15 | Off-route updates | −18 | +0.10 ms |
| 15 × 15 | Goal cut off | −91 | +2.00 ms |
| 25 × 25 | Single blocker | −23 | +1.00 ms |
| 25 × 25 | Sequential blockers | −23 | +1.05 ms |
| 25 × 25 | Off-route updates | −33 | +0.25 ms |
| 25 × 25 | Goal cut off | −276 | +3.20 ms |

D* Lite expanded fewer nodes in all 80 trace/repeat comparisons. Its measured total planning time was higher in 77 of 80 comparisons and equal in three; it was not faster in any comparison. This is a descriptive pilot on four hand-designed traces and one browser session. Ten repeats do not create more independent traces, and the no-route case is just one trace. The controlled trace prescribes checkpoint locations instead of letting each planner's route determine the next location, so it isolates replanning computation but does not compare autonomous route execution. These measurements do not establish a general ranking of A* and D* Lite.

## Reproduce and inspect

- `controlled-replay-pilot-2026-10-09.csv`: raw checkpoint rows from both grid sizes.
- `controlled-replay-pilot-2026-10-09-summary.csv`: per-planner cumulative trace totals.
- `controlled-replay-pilot-2026-10-09-paired-summary.csv`: paired differences across repetitions for each trace and size.
- `analyze_replay.py`: regenerates both summary files.

Run `python analyze_replay.py controlled-replay-pilot-2026-10-09.csv` from the project directory. The simulator's normal end-to-end CSV export and controlled-replay CSV export are separate; do not merge the two experiment types.
