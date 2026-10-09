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
- Each CSV row includes the expected and observed outcome, planner, measures, grid size, sensor range, start, heading, goal, obstacle coordinates, requested density, actual density, and seed for generated maps. The random generator retries with a recorded derived seed if a generated map disconnects start and goal.

The simulator is grid-based and does not model real motors, sensor noise, or localization drift. The public page has been opened in a desktop browser and inspected at a phone-sized viewport, but the planner comparison still needs systematic runtime verification before its CSV is used as research evidence. Read `PROJECT_BRIEF.md`, `EVALUATION_PLAN.md`, and `ROADMAP.md` for scope and next steps.

## GitHub Pages visibility note

GitHub Pages sites are publicly accessible on the internet. Do not publish private information, API keys, credentials, or student data in this project. See [GitHub's Pages publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
