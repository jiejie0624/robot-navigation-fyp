# FYP Proposal Draft — Room Rover

> Working draft for supervisor discussion. Adapt it to the university's required format, word count, and scope before submission.

- **Student:** [Add name and student ID]
- **Programme:** [Add programme]
- **Supervisor:** [Add supervisor]
- **Date:** [Add date]

## Proposed title

**A Simulation Study of Repeated A* and D* Lite for Indoor Navigation with Initially Unknown Obstacles**

## Abstract

Indoor mobile robots may discover obstacles only after they begin moving through an environment. When new information blocks a planned route, the robot must find another safe route to its destination. This project will develop a browser-based grid simulator and compare two search approaches: repeated A*, which runs a new A* search after a relevant map update, and D* Lite, which reuses search information across updates. Both planners will receive the same maps, start and goal positions, movement rules, sensor model, and obstacle layouts. The evaluation will report task completion and safe stopping first, followed by route length, replanning effort, expanded cells, and browser-measured planning time. Results will be analyzed by map size and scenario rather than used to claim that one algorithm is universally superior. The initial project is simulation-based; a camera and physical robot are optional future extensions and are not required for the core study.

## 1. Background

A robot navigating a room needs a route from its current position to a goal while avoiding obstacles. In an unfamiliar or partially known environment, its map may be incomplete. After sensing a previously unknown obstacle, it can compute a new route from scratch or update an earlier search.

A* is a widely used heuristic search method and provides a clear baseline when run again after map changes. D* Lite is an incremental search method designed to reuse information when related path-planning problems change. Their relative performance depends on the maps, update patterns, implementation, and measured outcome; fewer expanded cells do not necessarily mean lower runtime. This project will compare them empirically under a defined simulator model.

## 2. Problem statement

Many simple path-planning demonstrations assume that the complete map is known before movement begins. This does not show how planners behave when obstacles are initially hidden and are revealed only as a robot travels. A reproducible simulator is needed to model this process and evaluate how repeated A* and D* Lite respond to newly discovered obstacles while tracking both task correctness and computational effort.

## 3. Aim

To develop a reproducible simulator for indoor grid navigation with initially unknown obstacles and evaluate repeated A* and D* Lite under the same navigation scenarios.

## 4. Objectives

1. Design and implement an interactive grid-room simulator with a robot start pose, destination, hidden stationary obstacles, and simulated obstacle sensing.
2. Implement repeated A* and D* Lite for route planning and replanning when new obstacles are revealed.
3. Validate that both planners avoid known blocked cells, reach reachable goals, and stop safely when no route exists.
4. Compare the planners on task completion, route length, replanning/search effort, expanded cells, and planning time across selected map sizes and layouts.
5. Document the simulator assumptions, experimental procedure, results, and limitations so that trials can be reproduced.

## 5. Research question

On four-neighbor grid maps with initially unknown, stationary obstacles, how do repeated A* and D* Lite compare in task completion, route length, expanded-cell count, and measured planning time across different map sizes and obstacle layouts?

### Sub-questions

- Do both planners reach the destination when a valid route exists and report no route when the destination is blocked off?
- How do route length, replanning count, and expanded-cell count vary across easier and harder layouts?
- Does measured planner time follow the same pattern as expanded-cell count, or does implementation overhead produce a different result?

## 6. Scope

### Included

- A browser-based, two-dimensional square grid representing a room.
- Four-direction movement with uniform step cost and known room boundaries.
- A robot starting from a user-selected cell and heading, with a user-selected goal.
- Stationary obstacles that exist in the test map but are initially unknown to the planner.
- A simulated directional sensor that reveals obstacles as the robot approaches them.
- Repeated A* and D* Lite planners, route visualization, status/logging, and CSV export.
- Separate evaluation conditions for 15 × 15 and 25 × 25 grids, using fixed layouts and seeded generated maps.

### Excluded from the core study

- Physical robot construction and real-world navigation claims.
- Camera-based room understanding, visual localization, and automatic conversion of photographs into map coordinates.
- Moving obstacles, dynamic human avoidance, uncertain wheel motion, sensor noise, and continuous-space motion planning.
- Language-model APIs as route planners. The path-planning algorithms are deterministic and run locally in the browser.

Camera-assisted recognition of a known target marker may be considered as future work if time, equipment, and supervisor scope allow. Its feasibility and boundary are described separately in `CAMERA_EXTENSION_PLAN.md`.

## 7. Proposed methodology

### 7.1 System implementation

The simulator will represent the room as grid cells. The test map stores the true obstacle locations, while the planner begins with an incomplete known map. The simulated sensor reveals blocked cells before the robot attempts to enter them. After each relevant map update, the selected planner produces a route from the robot's current cell toward the goal. The system will reject invalid paths and stop safely if the goal becomes unreachable.

### 7.2 Experimental design

The independent factors are planner (repeated A* or D* Lite), grid size, and map layout. The two planners will be run against the same underlying map configuration, start, heading, goal, movement cost, and sensor range. The map set will include fixed scenarios (clear route, direct blocker, detour, corridor, winding route, and no-route case) and seeded maps with varied obstacle density. The current prototype supports 15 × 15 and 25 × 25 grids and 18 seeded cases at requested densities of 8%, 16%, and 24%; actual generated density and map coordinates will also be recorded.

Each map/planner condition will be repeated to characterize run-to-run timing variation. Repetitions on the same map will not be counted as independent map layouts. Planner order will be balanced where practical. A separate fixed-update replay can be reported as a secondary experiment because it gives both planners identical map updates; its results will not be mixed with autonomous end-to-end navigation results.

### 7.3 Measures

- **Correctness and safety:** goal reached, expected no-route result, unexpected outcome, and attempted entry into a known blocked cell.
- **Navigation cost:** number of moves and number of replanning episodes.
- **Search effort:** expanded cells.
- **Computation:** initial planning time, cumulative replanning time, and total planning time measured with the browser's high-resolution timer, excluding animation delay.

### 7.4 Analysis

Correctness and safety outcomes will be checked before performance comparisons. Results will be summarized separately by grid size and map family, using medians and spread for repeated measures. Paired comparisons will match planner runs by the same map and repeat ID. Because each planner may choose a different route and consequently observe a different sequence of obstacles, this is an end-to-end map-matched comparison rather than a comparison under identical update sequences. Planning time will be described as specific to the implementation, browser, and device used. Expanded cells and runtime will be reported separately.

## 8. Expected deliverables

- A browser-accessible simulator and source code.
- Implementations of repeated A* and D* Lite with visible route/replanning behavior.
- Repeatable maps, exported trial data, and analysis scripts.
- An evaluation report with correctness checks, per-scenario comparisons, and limitations.
- A final written report and demonstration, following the university's requirements.

## 9. Expected contribution and value

The project will provide a transparent, repeatable environment for examining how two planners behave when map information changes during a navigation task. It will make correctness, route cost, search effort, and runtime visible together. The contribution is an empirical comparison under a clearly stated simulator model, not proof that one planner is best for all robots or real rooms.

## 10. Limitations and risks

- A discrete grid and idealized sensor do not capture continuous motion, sensor noise, localization drift, turning cost, wheel slip, or human activity.
- Small maps and browser timing may make runtime differences noisy; hardware and browser metadata must be recorded.
- Different routes can cause the planners to discover different obstacles in the end-to-end experiment; conclusions must respect this pairing limitation.
- A camera image does not directly provide a safe goal coordinate without calibration, localization, and a map. Camera use is therefore excluded from the core objectives.
- The number of maps, repetitions, and final evaluation thresholds should be confirmed with the supervisor and university requirements.

## 11. Proposed work plan

The schedule below is milestone-based because the submission date and semester length have not been provided. An expanded 34-trace controlled-replay pilot has run at both grid sizes; see `CONTROLLED_REPLAY_EXPANDED_PILOT_2026-10-10.md`. It is pilot evidence and is not yet a supervisor-approved final protocol.

| Milestone | Work | Completion evidence |
|---|---|---|
| 1. Scope approval | Review this draft with the supervisor and confirm university format | Approved scope and research question |
| 2. Literature review | Expand and organize primary research on A*, D* Lite, unknown-terrain navigation, and evaluation | Referenced literature review |
| 3. Simulator refinement | Verify map model, sensing, planner behavior, logging, and failure handling | Demonstrable simulator and correctness checks |
| 4. Pilot and protocol freeze | Finalize scenarios, seeds, run counts, environment metadata, and analysis procedure | Frozen evaluation protocol |
| 5. Main experiments | Run paired batches and the separate fixed-update replay if retained | Raw CSVs and reproducible analysis |
| 6. Analysis and report | Summarize outcomes, discuss validity limits, and prepare final demonstration | Final report and demonstration |

## 12. Initial references

See `LITERATURE_REVIEW_DRAFT.md` for the preliminary synthesis. Additional references include Hart et al. (1968), the foundational A* paper ([DOI](https://doi.org/10.1109/TSSC.1968.300136)), and Hernández, Baier, and Asín (2014), which studies MPAA*, an enhanced A* variant rather than plain repeated A* ([DOI](https://doi.org/10.1609/icaps.v24i1.13675)).

1. Koenig, S. and Likhachev, M. (2002). “D* Lite.” *Proceedings of the Eighteenth National Conference on Artificial Intelligence*, pp. 476–483. [AAAI paper](https://aaai.org/Papers/AAAI/2002/AAAI02-072.pdf).
2. Koenig, S. and Likhachev, M. (2005). “Fast Replanning for Navigation in Unknown Terrain.” *IEEE Transactions on Robotics*. [Author-hosted paper](https://www.cs.cmu.edu/~maxim/files/dlite_tro05.pdf).
3. Hernández, C., Baier, J. A., Uras, T., and Koenig, S. (2012). “Position Paper: Incremental Search Algorithms Considered Poorly Understood.” *Proceedings of the Fifth Annual Symposium on Combinatorial Search*, 3(1), pp. 159–161. [DOI](https://doi.org/10.1609/socs.v3i1.18268).
4. Nav2. “Smac Planner.” Official navigation planner documentation. [Documentation](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/smac/).

## Items to confirm before submission

- Required proposal template, sections, word count, and citation style.
- Supervisor approval of the comparison between repeated A* and D* Lite.
- Whether both grid sizes, the fixed-update replay, and all seeded-map density bands fit the available time.
- Semester dates, final deadline, and required demonstration format.
