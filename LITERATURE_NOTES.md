# Early literature notes

Research checked: 2026-10-09. These are starting sources for the literature review, not a complete review.

## D* Lite and navigation in unknown terrain

Koenig and Likhachev introduced D* Lite by applying incremental heuristic search to robot navigation in unknown terrain. Their described navigation strategy computes a path under the assumption that unknown cells are traversable, follows it while observing the environment, and replans from the robot's current position after discovering an untraversable cell. This closely matches the proposed FYP scene. Their paper reports theoretical properties and experiments for the studied tasks.

- Koenig, S. and Likhachev, M. (2002), “D* Lite,” AAAI/IAAI 2002. Carnegie Mellon University publication record: https://publications.ri.cmu.edu/d-lite
- Author-hosted paper: https://www.cs.cmu.edu/afs/cs/Web/People/motionplanning/papers/sbp_papers/integrated3/koenig_dstarlite_aaai02b.pdf

Koenig and Likhachev later describe fast replanning for navigation in unknown terrain and explain that incremental methods reuse previous search results when the map changes, instead of solving every changed problem from scratch.

- Koenig, S. and Likhachev, M. (2005), “Fast Replanning for Navigation in Unknown Terrain,” IEEE Transactions on Robotics. Author-hosted paper: https://www.cs.cmu.edu/~maxim/files/dlite_tro05.pdf

## A* planners in a current robotics stack

Nav2's official Smac Planner documentation lists 2D A*, Hybrid-A*, and State Lattice A* planners. This is useful evidence that A*-family planning is an established robotics baseline. It does not mean the FYP must use Nav2; keeping the first simulator self-contained may make its algorithm and evaluation easier to explain.

- Nav2 documentation, “Smac Planner”: https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/planners_plugins/smac/

## Implications for this FYP

- Start with repeated A* as the simple, understandable baseline.
- Add D* Lite only after the simulator's unknown-cell model and measurements are stable.
- The foundational D* Lite study uses an eight-connected grid and observes adjacent cells. The current prototype uses four-connected movement and a directional simulated sensor, so the FYP should state its own model clearly rather than claim to reproduce the paper's exact setup.
- Give both planners the same initial pose, destination, obstacle layout, sensing range, and movement rules.
- Measure expanded cells as well as planning time. Small maps can make elapsed-time comparisons noisy or uninformative.
- Report route cost, completion, collisions/blocked-cell attempts, replanning count, expanded cells, and planning time. Include a no-route case and confirm safe stopping.
- The papers establish a suitable comparison, but do not predetermine which planner will perform best on this FYP's small maps. That is what the experiment should determine.
