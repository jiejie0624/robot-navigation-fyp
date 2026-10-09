# Controlled map-update replay protocol

## Purpose

The existing benchmark asks an end-to-end question: starting with the same task and hidden obstacle layout, how do A* and D* Lite navigate? Because each planner can choose a different route, each may discover a different sequence of obstacles. This separate replay experiment asks a narrower question: given the same map updates and the same planning query positions, how much search work and planner time does each algorithm use?

It must be reported as a **controlled planner-replay experiment**, separate from autonomous navigation. The robot does not choose its own route between replay queries, so this does not replace the end-to-end results.

## Replay unit

One replay case is a predetermined sequence:

1. Grid size, static true obstacle map, start, goal, sensor model, and movement costs.
2. An ordered list of checkpoints. Each checkpoint specifies the robot cell and heading at which a new observation is delivered.
3. An ordered list of newly revealed obstacle cells for that checkpoint. Both planners receive exactly the same cells at exactly the same point in the sequence.
4. A final query after the last update, with the same current cell and goal for both planners.

The checkpoint positions must be valid free cells in the true map. Every revealed obstacle must be a real obstacle that has not appeared in an earlier update. The generator should reject malformed sequences before either planner runs. Include cases with no update, one update that blocks the current best route, several updates, irrelevant updates away from the route, and a final update that makes the goal unreachable.

## Planner procedure

For each replay case, run both algorithms from the same initial knowledge state. A* starts a fresh search at each checkpoint after applying the checkpoint's obstacle updates. D* Lite retains its search state across those same updates and adjusts its start state consistently when the checkpoint position changes. At every checkpoint, both planners must receive the same current position, heading, goal, known obstacle set, movement model, and update order.

The algorithm may produce a route for diagnostic purposes, but route execution is not used to determine the next checkpoint. The next checkpoint is supplied by the replay trace. This controlled schedule is what keeps the update and query sequence identical.

## Outcomes

Record each checkpoint separately:

- path found / no path;
- route length and route validity against the currently known blocked cells;
- expanded nodes and queue operations, if available;
- initial-search and update/replanning time separately;
- cumulative planner time for the replay;
- known-map version, checkpoint index, current cell, goal, and newly revealed cells.

Validate each returned path in a planner-independent checker. A path must start at the checkpoint cell, end at the goal, use only legal four-neighbor transitions, and avoid all currently known obstacles. If a path exists in the known map, failure to return one is an error. If no route exists, the planner must report that condition. Keep correctness and blocked-cell violations as gate metrics before comparing performance.

## Case construction and reporting

- Reuse the 15 × 15 and 25 × 25 dimensions, but generate replay traces specifically for this experiment rather than extracting unequal discovery histories from the autonomous runs.
- Use several independent true maps at each obstacle-density band and several update schedules per map. Keep each map as the independent sampling unit; checkpoints and repeated timing runs are nested observations.
- Pre-register the map-generation seeds, checkpoint-selection rules, and number of cases before observing planner results.
- Warm both planners once on a separate warm-up case. Alternate planner execution order across cases. Run both planners in the same browser session and record browser/device metadata.
- Report map-level paired differences and medians/IQR for expanded nodes and time. Keep no-path checkpoints separate. Do not use a mean over all checkpoints as if checkpoints were independent maps.
- Report that checkpoint positions are prescribed and do not depend on the planner's chosen route. State clearly that this design isolates replanning work but does not estimate autonomous route efficiency.

## Implementation plan

1. Add a deterministic replay-trace schema and sample trace files.
2. Add a pure replay runner that applies the trace to each planner and records one row per case/checkpoint/planner.
3. Add an independent path validator and reject invalid traces before execution.
4. Add replay-specific CSV analysis that pairs by trace ID and checkpoint ID.
5. Run a small pilot to verify trace parity and result validation; then freeze the map set and execute the planned runs.

Do not modify the existing batch-comparison CSV interpretation or merge replay rows into it. Keep the replay experiment as a distinct condition with its own data and results report.
