# Room Rover — Robot Navigation FYP

An early browser-based simulator for a CS final-year project about indoor robot navigation in a room with initially unknown obstacles.

## Run the prototype

- Open the live demo in a modern browser: [Room Rover on Vercel](https://room-rover-eight.vercel.app/). The GitHub Pages copy is also available at [jiejie0624.github.io](https://jiejie0624.github.io/robot-navigation-fyp/).
- The page adapts to phones; the square map scrolls horizontally on narrow screens and the setup controls stack below it. The simulator is public, so do not enter private information.
- To work locally, open `index.html` in a modern browser.

## Current prototype behavior

- Set the robot's start cell, initial facing direction, and destination.
- To compare planners on the same map, finish a run, choose the other planner, then use **Restart same test**. It resets the robot to the original start, clears discovered obstacles and run metrics, and preserves the room, obstacles, goal, and initial heading. Use **New test (reset to North)** to clear the room and return the heading to North.
- Place obstacles in the scenario; they appear faintly on the operator's map but remain unknown to the robot during a run.
- The simulated sensor scans forward and marks discovered obstacles with a stronger color as the robot approaches.
- Select A* (recompute) or D* Lite (incremental replanning) for cells not yet known to be blocked.
- The map and mission log show detected obstacles, movement, and replanning counts.
- The run summary includes expanded nodes and planner computation time; completed runs can be exported to CSV.
- **Compare A* vs D* Lite (same updates)** runs a controlled replay and displays side-by-side median expanded nodes and planning time for paired trials. The two planners may draw the same route because they optimize the same path cost; compare search work and timing instead.
- Choose a 15 × 15 baseline grid or a larger 25 × 25 grid. Changing size reloads the selected preset so all start, goal, and obstacle coordinates remain valid.
- Repeatable presets cover an open room, a direct blocker, a long detour wall, a corridor with two offset openings, an alternating-opening maze, and a no-route wall.
- Use “重复比较” to run both planners on six fixed presets and 18 deterministic random maps: six seeds at each of three requested obstacle densities (8%, 16%, and 24%). Seeded maps also derive different start cells, goals, and headings from their seeds. Each map/planner pair gets one unrecorded warm-up and ten recorded repetitions, for 480 measured rows per batch at the selected grid size. Planner order alternates across repetitions to balance order effects.
- Each CSV row includes the benchmark batch ID, map ID, repeat number, expected and observed outcome, planner, measures, grid size, sensor range, start, heading, goal, obstacle coordinates, requested density, actual density, and seed for generated maps. Timing is split into initial planning, cumulative replanning, and total planning time. The random generator retries with a recorded derived seed if a generated map disconnects start and goal.
- After downloading a benchmark CSV, run `python analyze_benchmark.py <csv-file>` with Python 3.10 or later. It writes a planner/map summary, per-map/repeat D* Lite-minus-A* differences, and per-map paired medians/quartiles beside the input CSV. Paired rows match the same underlying map and repeat, but each planner may choose a different route and see different obstacles; interpret them as end-to-end task comparisons. It refuses to infer pairs from row order; older diagnostic exports without batch/repeat IDs receive summaries but no paired analysis.
- Ten repeats help show timing variation on the current maps; they do not add new map layouts. To compare map size, export a separate batch at each grid size and analyze the 15 × 15 and 25 × 25 rows as separate conditions.
- Completed 480-row batches for both grid sizes are reported in [`EXPERIMENT_RESULTS_2026-10-09.md`](EXPERIMENT_RESULTS_2026-10-09.md). The report links the raw exports and generated summaries; it describes these as simulator pilot results, not physical-robot evidence or a general algorithm ranking.
- [`STRATIFIED_ANALYSIS_2026-10-09.md`](STRATIFIED_ANALYSIS_2026-10-09.md) separates fixed presets, seeded maps by requested obstacle density, and the no-route case. Regenerate its map-level tables with `python analyze_strata.py <benchmark-csv>`; repeated trials are not counted as independent maps.
- [`FAIR_REPLAY_PROTOCOL.md`](FAIR_REPLAY_PROTOCOL.md) specifies a separate controlled experiment in which both planners receive identical obstacle updates and planning query positions. It isolates replanning work and is not mixed with autonomous end-to-end navigation results.
- The fixed-update replay runner applies the same obstacle discoveries and query positions to both planners. It includes four hand-designed traces plus 30 seeded maps (10 at each requested density: 8%, 16%, 24%), each with three checkpoints. Ten repetitions produce 2,040 checkpoint rows per grid-size batch. The separate replay CSV records seed/density, browser user-agent/platform, viewport and device-pixel ratio, checkpoint state, revealed/known obstacles, and path-validity results. The expanded pilot passed integrity checks at both grid sizes: D* Lite expanded fewer nodes across all 34 traces but took longer in this one-session browser run. Raw CSVs and generated summaries are retained. See [`FAIR_REPLAY_PROTOCOL.md`](FAIR_REPLAY_PROTOCOL.md) and [`CONTROLLED_REPLAY_EXPANDED_PILOT_2026-10-10.md`](CONTROLLED_REPLAY_EXPANDED_PILOT_2026-10-10.md); analyze a CSV with `python analyze_replay.py <replay-csv>`.
- A first-pass literature synthesis is in [`LITERATURE_REVIEW_DRAFT.md`](LITERATURE_REVIEW_DRAFT.md); it is not a complete literature review.
- A sourced, non-purchase proposal for connecting the simulator to a small 2WD robot is in [`HARDWARE_FEASIBILITY_PLAN.md`](HARDWARE_FEASIBILITY_PLAN.md).
- A raw export from the second diagnostic run is kept in [`diagnostic-benchmark-2026-10-09.csv`](diagnostic-benchmark-2026-10-09.csv); it is for debugging and reproducibility, not a research conclusion.
- A third diagnostic export after optimizing the D* Lite priority queue is kept in [`diagnostic-benchmark-after-heap-2026-10-09.csv`](diagnostic-benchmark-after-heap-2026-10-09.csv). It again produced 26 successes, two expected no-route results, and zero unexpected outcomes; mean times were 1.61 ms for A* and 4.71 ms for D* Lite. Treat this as preliminary debugging data only.

The simulator is grid-based and does not model real motors, sensor noise, or localization drift. The 28-case comparison has been run three times: all outcomes matched expectations and no blocked-cell attempts occurred. This is a prototype check, not enough evidence for a research conclusion; D* Lite's search-time overhead and route lengths still need study. Read `PROJECT_BRIEF.md`, `RESEARCH_DESIGN.md`, `EVALUATION_PLAN.md`, and `ROADMAP.md` for scope, methodology, and next steps.

For a supervisor-ready starting point, see [`FYP_PROPOSAL_DRAFT.md`](FYP_PROPOSAL_DRAFT.md). It is a generic working draft and must be adapted to the university's required template and approved scope.

## GitHub Pages visibility note

GitHub Pages sites are publicly accessible on the internet. Do not publish private information, API keys, credentials, or student data in this project. See [GitHub's Pages publishing-source guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
