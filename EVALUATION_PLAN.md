# Draft Evaluation Plan

This plan is for the computer simulation first. Update it after the simulator and algorithm comparison are implemented.

## Research comparison

- Baseline: run A* from the robot's current cell after each newly detected obstacle.
- Candidate: D* Lite, which reuses search information after map changes.
- Give both methods the same room, start, heading, goal, sensor range, obstacle layout, and movement cost.
- Unknown cells are assumed traversable for planning. The simulated sensor reveals a blocked cell before the robot enters it.
- Obstacles remain stationary during an individual run in the MVP.

## Scenario set

Use a small, named set of repeatable maps rather than only hand-picked successful examples:

1. Open room with a clear route.
2. Single obstacle directly in the initial route.
3. Long wall that requires a detour.
4. Narrow corridor with a blockage.
5. Dead end requiring the robot to reverse its chosen direction.
6. Destination unreachable because walls or obstacles separate it from the start.
7. Eighteen seeded maps: six seeds at each requested obstacle density of 8%, 16%, and 24%. Each seed deterministically varies the start cell, heading, goal, and obstacle layout. The generator records the effective seed and retries deterministically if a map disconnects start and goal.

For every map, save its dimensions, obstacle coordinates, start, heading, destination, sensor range, requested and actual obstacle density, and seed (if generated). These fields are included in the CSV export so a map can be reconstructed.

## Measures

- **Completion:** whether the robot reaches the destination.
- **Safety:** collision count and number of moves attempted into a blocked cell. The intended successful behavior is zero collisions.
- **Route length:** number of grid moves before reaching the goal.
- **Replanning:** number of replanning episodes after new information.
- **Search effort:** number of cells/nodes expanded by the planner.
- **Planning time:** algorithm computation time per initial plan and replan, measured separately from the animation delay.
- **No-route behavior:** whether the robot stops and reports that no route exists.

## Fair comparison procedure

1. Run each map with both planners using identical initial conditions.
2. Record each result automatically in a CSV or JSON log.
3. Check correctness first: both planners must obey known obstacles and reach the goal or correctly report no route.
4. Compare per-map route length, expanded nodes, and planning time; summarize results across the map set.
5. Keep the simulation animation delay out of planner timing.
6. Report limitations: grid abstraction, idealized sensing, stationary obstacles, and lack of physical localization error.

## Next experiment-design refinement

The current batch contains 23 map layouts at one 15 × 15 grid size: five fixed presets and 18 seeded maps with varied start, heading, goal, and obstacle layout. It performs one unrecorded warm-up and ten recorded repetitions for each map/planner pair, with planner order balanced across repeats. Repetitions help characterize timing noise on the same map; they do not create more independent map layouts. A 2012 position paper on incremental search notes that Repeated A* can run faster than D* Lite on easy navigation tasks with few searches and recommends more diverse testbeds. Therefore the evaluation should not assume D* Lite is faster in every condition.

Before drawing a performance conclusion:

1. Keep a set of named difficulty bands: easy routes with zero or few newly discovered obstacles, moderate routes with several replans, and harder corridor/maze cases. Keep no-route tests as a separate correctness category.
2. Run both planners on the same recorded maps and repeat each map/planner condition. Add at least one larger grid size and more structured maze/corridor layouts so results are not tied to one tiny map family. Treat ten repeats as a pilot setting, not a final sample-size decision.
3. Preserve paired records per map. Summarize completion and blocked attempts first; then compare route moves, expanded nodes, replan count, initial planning time, cumulative replan time, and total planning time by difficulty band.
4. Report median and spread for timing across repeated trials, plus the number of maps and runs. Keep animation delay outside algorithm timing and record the browser/device used.
5. Treat elapsed-time results as implementation- and device-specific. A lower node count does not automatically mean lower runtime, and the current diagnostic results are not enough to establish a winner.

Implementation note: benchmark CSV rows include a batch ID, map ID, repeat number, initial planning time, cumulative replanning time, and total planning time, alongside total expanded nodes. Each map/planner pair receives one warm-up that is omitted from the CSV, then ten recorded runs with counterbalanced planner order. Larger grids and more structured maps are still needed before drawing conclusions.

## Implementation status

The prototype includes selectable A* and D* Lite planners, search-expansion and planner-time counters, CSV export, five fixed presets, and a repeated comparison (both planners on 23 maps, ten measured repetitions each, for 460 rows). The live page has been opened in desktop and phone-sized browser layouts.

### Diagnostic runs (2026-10-09)

- Two browser runs each produced 26 goal arrivals and two expected `no_route` outcomes, one for each planner on the wall-separated map.
- Neither run attempted to enter an obstacle (`blockedAttempts = 0`), and all outcomes matched their expected outcomes.
- Across the 14 map/planner rows per method, mean expanded-node counts were 461 for A* and 183 for D* Lite. Mean planning-time observations ranged from 1.64–1.89 ms for A* and 4.60–5.05 ms for D* Lite.
- These are prototype checks on a 15 × 15 grid, not research evidence. Timing is noisy at this scale, and D* Lite's queue implementation currently has more overhead despite fewer expanded nodes. The planners can also take different routes, so route length needs separate analysis.
- The raw CSV from the second run is preserved at `diagnostic-benchmark-2026-10-09.csv`.

### Diagnostic run after queue optimization (2026-10-09)

- A third 28-run browser comparison was completed after replacing D* Lite's repeated array sorting with an indexed binary min-heap.
- Results: 26 goal arrivals, two expected `no_route` outcomes, zero unexpected outcomes, and zero blocked attempts. Each planner had 13 successes and one expected no-route result.
- Mean expanded nodes were 461 for A* and 183.43 for D* Lite. Mean planner times were 1.61 ms for A* and 4.71 ms for D* Lite. The heap change did not remove D* Lite's timing overhead in this small browser benchmark.
- These values are diagnostic only; one run, 15 × 15 maps, browser timing noise, and route-length differences do not support a general performance claim. The post-optimization raw CSV is preserved in `diagnostic-benchmark-after-heap-2026-10-09.csv`.
- The literature-supported interpretation and proposed broader evaluation are recorded above. The simulator now exports initial-plan and cumulative replan timing separately and runs ten recorded repeats per map/planner pair across 23 maps. Larger grids and more structured map layouts remain future work.
