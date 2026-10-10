# Project Roadmap

## Stage 1 — Define the FYP

- Review relevant work on unknown-terrain navigation and replanning. Initial notes are in `LITERATURE_NOTES.md`.
- A preliminary literature synthesis now lives in `LITERATURE_REVIEW_DRAFT.md`; it distinguishes plain repeated A* results from later enhanced A* variants.
- Proposed comparison: repeated A* versus D* Lite for a grid world where obstacles are revealed while the robot moves.
- Draft controlled evaluation procedure recorded in `EVALUATION_PLAN.md`.
- Confirm the university's proposal, report, and demonstration requirements when available.
- Finalize the research question, scope, and evaluation measures after requirements are known.
- A generic supervisor-discussion proposal draft is in `FYP_PROPOSAL_DRAFT.md`; confirm the university template and supervisor scope before submission.

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

- Initial hardware architecture, Malaysia price check, integration flow, staged validation procedure, and safety risks are documented in `HARDWARE_FEASIBILITY_PLAN.md`.
- Keep hardware selection within the student's confirmed budget and access constraints; do not assume a purchase.
- Calibrate motion and sensing in a small, controlled test area.
- Connect robot telemetry and commands to the control console if feasible.
- Treat camera-assisted target recognition as an optional extension; see `CAMERA_EXTENSION_PLAN.md`. Start with a known visual marker and safe approach, not arbitrary photo-to-coordinate navigation.

## Stage 5 — Real-world evaluation and report

- Repeat physical trials across several obstacle layouts.
- Compare simulation and real-robot results and explain differences such as sensor noise and wheel slip.
- Prepare the final report, diagrams, demo instructions, limitations, and presentation materials.

## Status

- Stage 1: in progress; initial primary sources, a preliminary literature review, a draft algorithm comparison, an experimental-design note, and a generic proposal draft are recorded in the project docs. University proposal/report requirements and supervisor approval remain outstanding.
- Stage 2: public simulator is deployed on GitHub Pages and opened in desktop and phone-sized browser layouts. It includes six fixed presets, 18 deterministic random maps across three requested densities, selectable 15 × 15 / 25 × 25 grids, seed-derived start/heading/goal, planner counters, repeated batch comparison, and CSV records with reconstructable map configuration. The map generator records its effective seed after deterministic retries to ensure a route exists in generated cases.
- Stage 3: the end-to-end benchmark has completed at both grid sizes (480 rows each), with raw data, paired comparisons, and stratified summaries in `EXPERIMENT_RESULTS_2026-10-09.md` and `STRATIFIED_ANALYSIS_2026-10-09.md`. The controlled-update replay pilot has four hand-designed and 30 seeded traces, three checkpoints per trace, and ten repetitions at each grid size. Its two retained CSVs contain 2,040 rows each; integrity checks passed, and paired trace/family summaries are generated. D* Lite expanded fewer nodes on all 34 traces but took longer in the one-session browser timings. Physical robot stages remain unstarted.
- Stage 4: desk research completed as a proposal only. No hardware has been selected for purchase or built; budget, soldering access, supervisor scope, local control bridge, calibration, and physical tests remain open.
- Stage 5: not started.
- Camera extension: feasibility and scope documented in `CAMERA_EXTENSION_PLAN.md`; no camera or vision API is currently required by the core simulator.
