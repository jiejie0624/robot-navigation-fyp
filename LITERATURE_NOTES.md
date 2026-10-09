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

## When incremental search is faster

Hernandez, Baier, Uras, and Koenig revisit goal-directed navigation in initially unknown terrain and point out that it is not generally understood when D* Lite beats Repeated A* in runtime. Their position paper reports that Repeated A* appears faster on easy navigation problems where the agent needs only a small number of searches. They recommend evaluating incremental search on more diverse testbeds. This is directly relevant to the prototype: in its current 15 × 15, 14-map diagnostic run, D* Lite expanded fewer nodes but its measured mean planning time remained higher. That observation is plausible and worth studying; it is not evidence that either algorithm is universally faster.

- Hernandez, C., Baier, J., Uras, T., and Koenig, S. (2012), “Position Paper: Incremental Search Algorithms Considered Poorly Understood,” Proceedings of the International Symposium on Combinatorial Search, 3(1), 159–161. DOI: https://doi.org/10.1609/socs.v3i1.18268

### Experimental-design details relevant to this prototype

The 2012 paper uses four-neighbor random grids, varies both obstacle density and start/goal cells, and explicitly makes Repeated Forward A* and D* Lite follow the same trajectory in its random-grid comparison. It also studies game maps, office maps, and mazes. This supports the broader map family and varied endpoint design in Room Rover. However, the current simulator lets each planner choose its own route; matching by underlying map and repeat is not the same as replaying an identical obstacle-discovery sequence. Current results must therefore be described as end-to-end task comparisons. A future replay experiment could isolate the cost of responding to the same map changes.

The paper further notes that expanded-cell counts are not sufficient to compare runtime because the methods can process an expansion at different speeds. Room Rover should report expanded cells and measured planner time as separate outcomes; neither should be treated as a substitute for the other.

- Hernández et al. (2012), author-hosted full text, experimental setup and conclusions: https://idm-lab.org/bib/abstracts/papers/socs12b.pdf
- Koenig and Likhachev (2002), official AAAI proceedings PDF: https://aaai.org/Papers/AAAI/2002/AAAI02-072.pdf

## Implications for this FYP

- Start with repeated A* as the simple, understandable baseline.
- Add D* Lite only after the simulator's unknown-cell model and measurements are stable.
- The foundational D* Lite study uses an eight-connected grid and observes adjacent cells. The current prototype uses four-connected movement and a directional simulated sensor, so the FYP should state its own model clearly rather than claim to reproduce the paper's exact setup.
- Give both planners the same initial pose, destination, obstacle layout, sensing range, and movement rules.
- Measure expanded cells as well as planning time. Small maps can make elapsed-time comparisons noisy or uninformative.
- Report route cost, completion, collisions/blocked-cell attempts, replanning count, expanded cells, and planning time. Include a no-route case and confirm safe stopping.
- The papers establish a suitable comparison, but do not predetermine which planner will perform best on this FYP's small maps. That is what the experiment should determine.
- Do not assume D* Lite must win. Include easy maps with few replans and harder maps with more obstacle discoveries; report the results by difficulty as well as overall.
- Repeat runs on the same recorded maps and vary map seeds to distinguish map difficulty from timing noise. Report median and spread, not a lone timing or only an overall mean.
- Separate initial-plan time from cumulative replan time (and, if feasible, per-replan time). A single total can hide whether a method is slower to start but cheaper to repair, or the reverse.
