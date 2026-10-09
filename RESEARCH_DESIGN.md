# Draft Research Design

This is a working design for discussion with the project supervisor. It is not a confirmed university-approved proposal.

## Working title

**A Simulation Study of Repeated A* and D* Lite for Navigation through Initially Unknown Obstacles**

## Research question

On four-neighbor grid maps with initially unknown, stationary obstacles, how do repeated A* and D* Lite compare in end-to-end task completion, route length, number of expanded cells, and measured planning time across map sizes and obstacle layouts?

The purpose is to characterize where the two approaches differ, not to assume D* Lite is always faster. D* Lite reuses search information across related planning problems; repeated A* solves a new search from the robot's current cell after map updates. The original D* Lite work studies navigation in unknown terrain, while a later position paper argues that incremental search should be evaluated across diverse cases and reports that repeated A* may be faster on easy navigation tasks. See the sources below.

## Scope of the current simulator

- The room is a square, four-neighbor grid with uniform movement cost and known boundaries.
- The robot starts with interior cells treated as traversable. Obstacles are stationary and hidden until a simulated directional sensor detects them.
- The sensor scans up to three cells ahead. This is a prototype assumption, not a claim about physical sensor hardware.
- The planner is called on the browser's main thread. The elapsed time is JavaScript planning time, not robot travel time or end-to-end wall-clock mission duration.
- The supported map sizes are 15 × 15 and 25 × 25. Each size is a separate experimental condition.

## Variables and outcomes

### Experimental factors

- **Planner:** repeated A* or D* Lite.
- **Map size:** 15 × 15 or 25 × 25.
- **Map layout:** open room, direct blocker, detour wall, corridor, winding maze, no-route wall, and seeded random maps.
- **Requested random obstacle density:** 8%, 16%, or 24% for seeded maps. Record the realized density as well.

### Fixed conditions within each map pair

The paired A* and D* Lite trials use the same underlying obstacle map, grid dimensions, start, initial heading, goal, sensor range, movement costs, and browser session. Seeds and the full obstacle coordinates are exported so a map can be reconstructed.

### Outcomes to report

- **Correctness and safety first:** goal reached when a route exists; no-route reported for the wall-separated case; unexpected outcomes and attempts to enter a blocked cell.
- **Task cost:** moves taken and number of replanning episodes.
- **Search work:** expanded cells.
- **Measured planner time:** initial-plan time, cumulative replanning time, and total planning time.

Expanded-cell count is a useful measure of search work, but it is not a substitute for runtime: two algorithms can process each expanded cell at different costs. Report both counts and timing, and describe timing as specific to the browser, device, and implementation.

## Important pairing limitation

The current experiment matches trials by the same map and repeat, but the planners are free to choose different routes. A different route can reveal a different sequence of obstacles and cause a different number of replanning events. Therefore, the current paired differences estimate **end-to-end navigation performance on the same underlying task**. They do not isolate planner speed under an identical sequence of map updates.

If the final FYP needs to isolate the incremental-search effect more tightly, add a separate replay experiment: record a fixed ordered sequence of obstacle discoveries and apply exactly those same map updates to both planners from the same robot positions. Treat that as a distinct experiment, since it no longer measures autonomous end-to-end navigation.

## Batch procedure

1. At each grid size, use the same 24 layouts: six fixed scenarios and 18 deterministic seeded maps.
2. The seeded maps vary start, heading, goal, and obstacle pattern. A deterministic retry is used if the generated start-to-goal route is disconnected; these generated cases therefore focus on reachable random tasks. Use the fixed no-route wall as a separate correctness case.
3. For each map and planner, run one unrecorded warm-up and ten recorded repetitions. Alternate planner order by map and repeat.
4. One selected grid size produces 24 × 2 × 10 = 480 measured rows. Run a separate batch for the other size, producing 960 rows total when both sizes are included.
5. Save the raw CSV before analysis. The end-to-end batch CSV records map/task details but not all browser/device metadata; record the browser, device, date, and background workload alongside that export. The controlled-replay CSV records browser user-agent/platform, viewport, and device-pixel ratio, but the pilot still came from one session.
6. Run `python analyze_benchmark.py <csv-file>`. It writes per-planner/map summaries, per-map/repeat paired differences, and per-map paired medians/quartiles. Inspect completion, expected outcomes, and blocked attempts before interpreting search-work or timing differences.

## Analysis plan

- Report each map-size condition separately.
- For each planner and scenario/map group, show the number of rows, success rate, expected-outcome rate, blocked-attempt rows, and the median with interquartile range for moves, replans, expanded cells, and planning times.
- Use the generated D* Lite-minus-A* differences for trials with the same batch, map, and repeat ID. Summarize the median and spread of those differences; keep no-route results as a separate correctness category.
- Do not treat ten repetitions on one map as ten independent maps. The independent layout count remains 24 per size.
- Show map-level results as well as any overall summary so difficult maps cannot be hidden by many easy outcomes.
- Add an exploratory map-family summary: five fixed reachable presets, six seeded maps at each requested density, and the single no-route preset as its own correctness case. First reduce repetitions to per-map medians, then summarize across maps so repeats are not misrepresented as independent layouts. The current output is in `STRATIFIED_ANALYSIS_2026-10-09.md`.
- Do not declare a universal winner from a lower expansion count or one browser timing average.

For a narrower comparison under identical map updates, use the separate controlled planner-replay design in `FAIR_REPLAY_PROTOCOL.md`. Prescribe the same update list and current-position query at each checkpoint for both methods. This isolates replanning computation but does not measure a robot autonomously following the planner's route; keep its data separate from the end-to-end task comparison.

The current expanded replay pilot uses 34 traces (four hand-designed plus 30 seeded) at three checkpoints per trace and ten repetitions, on both grid sizes: 4,080 planner/checkpoint rows in total. The interface reported zero parity mismatches and zero route/outcome errors. See `CONTROLLED_REPLAY_EXPANDED_PILOT_2026-10-10.md` for the integrity summary and limitations.

## Threats to validity and limitations

- The grid, sensor, and motion are idealized; there is no sensor noise, wheel slip, turning cost, continuous localization, or moving obstacle.
- The 3-cell directional sensor differs from the adjacent-cell observation model in foundational D* Lite experiments. Conclusions apply to this simulator's model unless the experiment is later adapted.
- Small maps and browser timing can make elapsed-time observations noisy. The benchmark is a pilot, not a final sample-size justification.
- Connectivity retries alter the effective random seed. Keep the recorded effective seed and full map configuration when analyzing results.
- The route chosen by each planner affects the obstacle discoveries it receives. Use the pairing interpretation above and do not overstate causal isolation.
- The university's required format, proposal scope, and supervisor expectations are not yet known.

## Literature review status

The initial source synthesis is in `LITERATURE_REVIEW_DRAFT.md`; it covers A*, D* Lite, evidence that planner performance depends on task difficulty, and the gap between a grid simulator and a real navigation stack. It is a starting draft, not a completed systematic search or an approved literature chapter.

## Primary sources

1. Koenig, S. and Likhachev, M. (2002). “D* Lite.” *Proceedings of the Eighteenth National Conference on Artificial Intelligence*, pp. 476–483. [AAAI paper PDF](https://aaai.org/Papers/AAAI/2002/AAAI02-072.pdf) · [Carnegie Mellon publication record](https://publications.ri.cmu.edu/d-lite)
2. Hernández, C., Baier, J. A., Uras, T., and Koenig, S. (2012). “Position Paper: Incremental Search Algorithms Considered Poorly Understood.” *Proceedings of the Fifth Annual Symposium on Combinatorial Search*, pp. 159–161. [DOI](https://doi.org/10.1609/socs.v3i1.18268) · [Author-hosted paper](https://idm-lab.org/bib/abstracts/papers/socs12b.pdf)
