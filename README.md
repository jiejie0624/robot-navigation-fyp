# Room Rover — Robot Navigation FYP

An early browser-based simulator for a CS final-year project about indoor robot navigation in a room with initially unknown obstacles.

## Run the prototype

- Open the live demo in a modern browser: [Room Rover on GitHub Pages](https://jiejie0624.github.io/robot-navigation-fyp/).
- The page adapts to phones; the square map scrolls horizontally on narrow screens and the setup controls stack below it. The simulator is public, so do not enter private information.
- To work locally, open `index.html` in a modern browser.

## Current prototype behavior

- Set the robot's start cell, initial facing direction, and destination.
- Place obstacles in the scenario; their locations are hidden from the robot during a run.
- The simulated sensor scans forward and reveals obstacles as the robot approaches.
- Select A* (recompute) or D* Lite (incremental replanning) for cells not yet known to be blocked.
- The map and mission log show detected obstacles, movement, and replanning counts.
- The run summary includes expanded nodes and planner computation time; completed runs can be exported to CSV.
- Repeatable presets cover an open room, a direct blocker, a long detour wall, a corridor, and a no-route wall.
- Use “比较全部场景” to run both planners on five fixed presets and nine deterministic random maps: three seeds at each of three requested obstacle densities (8%, 16%, and 24%). This creates 28 rows total.
- Each CSV row includes the expected and observed outcome, planner, measures, grid size, sensor range, start, heading, goal, obstacle coordinates, requested density, actual density, and seed for generated maps. Timing is split into initial planning, cumulative replanning, and total planning time. The random generator retries with a recorded derived seed if a generated map disconnects start and goal.
- A raw export from the second diagnostic run is kept in [`diagnostic-benchmark-2026-10-09.csv`](diagnostic-benchmark-2026-10-09.csv); it is for debugging and reproducibility, not a research conclusion.
- A third diagnostic export after optimizing the D* Lite priority queue is kept in [`diagnostic-benchmark-after-heap-2026-10-09.csv`](diagnostic-benchmark-after-heap-2026-10-09.csv). It again produced 26 successes, two expected no-route results, and zero unexpected outcomes; mean times were 1.61 ms for A* and 4.71 ms for D* Lite. Treat this as preliminary debugging data only.

The simulator is grid-based and does not model real motors, sensor noise, or localization drift. The 28-case comparison has been run three times: all outcomes matched expectations and no blocked-cell attempts occurred. This is a prototype check, not enough evidence for a research conclusion; D* Lite's search-time overhead and route lengths still need study. Read `PROJECT_BRIEF.md`, `EVALUATION_PLAN.md`, and `ROADMAP.md` for scope and next steps.

## GitHub Pages visibility note

GitHub Pages sites are publicly accessible on the internet. Do not publish private information, API keys, credentials, or student data in this project. See [GitHub's Pages publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
