# Robot Navigation and Obstacle Replanning — Project Brief

## Purpose

Develop a CS FYP that demonstrates how an indoor mobile robot can reach a user-selected destination when it does not initially know where obstacles are. The project should be understandable in a live demo and measurable in repeatable scenarios.

## User scenario

1. The user opens a square-room map in a phone or computer control console.
2. The user marks the robot's starting cell and its facing direction.
3. The user selects a destination.
4. Obstacles exist in the room but are not shown on the robot's known map.
5. The robot moves toward the destination and senses obstacles along the way.
6. When it detects a blocked route, it stops, records the obstacle, and replans from its current position.
7. If no safe route exists, it stops and reports that it cannot proceed.
8. The console shows the robot, discovered obstacles, route, and task status.

The console should work on both desktop and smartphone screens. Smartphone support is for setting destinations and monitoring a future robot demo; algorithm development and detailed evaluation remain comfortable on a computer.

## Core research question (draft proposal)

On grid-based maps with initially unknown obstacles, how does incremental replanning with D* Lite compare with running A* again after each newly detected obstacle, in planning effort and route cost, while still reaching the goal safely?

The comparison is a recommended research direction, not yet a final commitment. D* Lite reuses previous search information, while repeated A* is a clear baseline. On a small grid, elapsed-time differences may be tiny, so count of expanded cells should also be measured. Refine this question against the university's FYP requirements and literature review.

## Initial minimum viable project

- Interactive square-grid room with known boundaries.
- Settable start location, initial facing direction, destination, and hidden test obstacles.
- Robot movement based on its known map only.
- Simulated sensor reveals obstacles as the robot approaches.
- Route replanning begins from the robot's current location.
- Previously blocked cells/routes are not repeatedly attempted.
- Safe stop and clear message if the destination becomes unreachable.
- Mission log and basic measures: completion, travel distance, discovered obstacles, replans, and elapsed simulation time.
- Treat obstacles as stationary during one mission in the minimum version. Moving obstacles are a possible extension, not part of the initial claim.

## Evaluation ideas

Use the same repeatable maps, start/goal positions, sensor model, and obstacle-discovery rules for each planner. Include open rooms, corridors, mazes, and blocked passages. Record:

- task completion rate;
- collisions and attempts to enter a newly discovered blocked cell;
- route length;
- number of replans;
- expanded-cell count and planning time for each planning episode;
- success in stopping safely when no route exists.

Use deterministic maps or recorded random seeds so results can be reproduced. Report the map size, obstacle density, sensor range, planner settings, and summary statistics. Do not claim one algorithm is better from a single run or based only on noisy timing measurements.

## Current assumptions and open decisions

- A grid-based simulator is the first implementation because it keeps the behavior visible and testable.
- The current prototype offers A* and D* Lite with a simulated forward sensor, selectable 15 × 15 / 25 × 25 map sizes, and six fixed layouts plus seeded maps. These are implementation choices for the prototype, not final FYP decisions.
- Compare the methods only after checking project scope and literature; the research question remains a draft.
- Physical robot hardware, sensor type, room scale, budget, and university format remain undecided.
- Real hardware will introduce localization drift, sensor errors, turning and wheel-motion errors; the simulator alone cannot validate those effects.
- The current prototype is a discrete four-neighbor grid with a directional sensor that scans up to three cells. This is a simulation assumption, not a physical sensor specification.
- A camera is an optional later extension, not part of the current core objective. See `CAMERA_EXTENSION_PLAN.md`. A photo detector must not be assumed to produce an accurate map coordinate without calibration and robot localization.
