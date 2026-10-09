# Project Roadmap

## Stage 1 — Define the FYP

- Review relevant work on unknown-terrain navigation and replanning. Initial notes are in `LITERATURE_NOTES.md`.
- Proposed comparison: repeated A* versus D* Lite for a grid world where obstacles are revealed while the robot moves.
- Draft controlled evaluation procedure recorded in `EVALUATION_PLAN.md`.
- Confirm the university's proposal, report, and demonstration requirements when available.
- Finalize the research question, scope, and evaluation measures after requirements are known.

## Stage 2 — Computer simulation

- Refine the 2D grid control console and robot behavior.
- Make unknown-obstacle detection and map updates clear in the demo.
- Handle repeated blockage, stale obstacle information, and no-route cases safely.
- Add repeatable test maps and collect evaluation data.

## Stage 3 — Algorithm study

- Establish a reliable baseline planner.
- Decide whether to compare replanning methods after literature and scope review.
- Compare methods using identical maps and report success, route length, and planning/replanning time.

## Stage 4 — Physical robot feasibility

- Research suitable low-cost chassis, controller, motor driver, sensors, and battery using current sources.
- Keep hardware selection within the student's confirmed budget and access constraints; do not assume a purchase.
- Calibrate motion and sensing in a small, controlled test area.
- Connect robot telemetry and commands to the control console if feasible.

## Stage 5 — Real-world evaluation and report

- Repeat physical trials across several obstacle layouts.
- Compare simulation and real-robot results and explain differences such as sensor noise and wheel slip.
- Prepare the final report, diagrams, demo instructions, limitations, and presentation materials.

## Status

- Stage 1: in progress; initial primary sources and a draft algorithm comparison are recorded. University proposal/report requirements remain unknown.
- Stage 2: public simulator is deployed on GitHub Pages and opened in desktop and phone-sized browser layouts. It includes five fixed presets, nine deterministic random maps across three requested densities, planner counters, batch comparison, and CSV records with reconstructable map configuration. The map generator records its effective seed after deterministic retries to ensure a route exists in generated cases.
- Stage 3: A* and D* Lite comparison is implemented across 14 maps (28 planner runs). Three diagnostic runs each had 26 goal arrivals, two expected no-route outcomes, zero blocked attempts, and no unexpected results. After replacing D* Lite's array-sorted queue with an indexed binary min-heap, the latest run still measured 4.71 ms mean planner time versus A* at 1.61 ms, despite D* Lite expanding fewer nodes (183 versus 461). Literature supports evaluating easy and hard navigation separately because Repeated A* can be faster on easy tasks. The CSV now separates initial-plan and cumulative replan time; before research claims, expand the testbed and repeat paired trials as described in `EVALUATION_PLAN.md`.
- Stages 4–5: not started.
