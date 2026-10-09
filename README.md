# Room Rover — Robot Navigation FYP

An early browser-based simulator for a CS final-year project about indoor robot navigation in a room with initially unknown obstacles.

## Run the prototype

- On a computer, open `index.html` in a modern browser.
- On a phone, the controls are touch-friendly and the map can scroll horizontally on narrow screens. To use the phone without copying the file manually, publish the static page with a web host such as GitHub Pages after choosing repository visibility.

## Current prototype behavior

- Set the robot's start cell, initial facing direction, and destination.
- Place obstacles in the scenario; their locations are hidden from the robot during a run.
- The simulated sensor scans forward and reveals obstacles as the robot approaches.
- Select A* (recompute) or D* Lite (incremental replanning) for cells not yet known to be blocked.
- The map and mission log show detected obstacles, movement, and replanning counts.
- The run summary includes expanded nodes and planner computation time; completed runs can be exported to CSV.
- Repeatable presets cover an open room, a direct blocker, a long detour wall, a corridor, and a no-route wall.
- Use “比较全部场景” to run both planners on all five presets and add the 10 rows to the downloadable CSV.

The simulator is grid-based and does not model real motors, sensor noise, or localization drift. It is not yet browser-verified. Read `PROJECT_BRIEF.md`, `EVALUATION_PLAN.md`, and `ROADMAP.md` for scope and next steps.

## GitHub Pages visibility note

GitHub Pages sites are publicly accessible on the internet. With a personal GitHub Free account, Pages is available for public repositories. Do not publish private information, API keys, credentials, or student data in this project. See [GitHub's Pages publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
