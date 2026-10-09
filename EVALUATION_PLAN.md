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
7. Nine seeded maps: three seeds at each requested obstacle density of 8%, 16%, and 24%. The generator records the effective seed and retries deterministically if a map disconnects start and goal.

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

## Implementation status

The prototype includes selectable A* and D* Lite planners, search-expansion and planner-time counters, CSV export, five fixed presets, and a 28-run comparison (both planners on the five presets and nine seeded maps). The live page has been opened in desktop and phone-sized browser layouts.

### First diagnostic run (2026-10-09)

- 26 of the 28 planner runs reached the goal; the two `no-route` runs correctly returned `no_route` for both planners.
- No run attempted to enter an obstacle (`blockedAttempts = 0`).
- Across all 14 map/planner rows per method, the observed mean expanded-node count was 461 for A* and 183 for D* Lite. The observed mean planning time was 1.89 ms and 5.05 ms, respectively.
- These are one browser run on a 15 × 15 grid. Treat them only as a debugging baseline: timing is noisy at this scale, and a single run is not evidence that one algorithm is better.
