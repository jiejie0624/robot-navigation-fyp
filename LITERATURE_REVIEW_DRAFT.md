# Preliminary literature review — Room Rover

> Working draft, not a complete systematic review. The sources below are primary research papers or official robotics documentation. Verify the university's citation style and expand the review after supervisor feedback.

## A* as the baseline search method

Hart, Nilsson, and Raphael introduced the heuristic search formulation commonly known as A*. A* orders candidate states using the cost already paid and an estimate of the remaining cost. With a suitable admissible heuristic, it can find a least-cost path in the modeled graph. For Room Rover, four-neighbour movement with unit costs makes Manhattan distance a natural heuristic. Repeated A* means the simulator runs a fresh A* search when newly observed cells change the known map; it is the baseline, rather than a claim that A* itself is incremental.

**Project implication:** document the graph, movement costs, heuristic, and exactly when a new search runs. These choices affect both correctness and measured work.

## D* Lite for changing maps

Koenig and Likhachev introduced D* Lite as an incremental heuristic-search approach for navigation in unknown terrain. A robot can plan with unknown cells provisionally treated as traversable, move while observing the environment, and repair its search when newly discovered obstacles invalidate part of the plan. D* Lite reuses prior search information rather than solving each related problem from scratch. Their later work develops fast replanning for unknown terrain in more detail.

**Project implication:** the simulator's hidden-obstacle model is a reasonable small-scale setting for studying the planner's intended use. It is still a simplified grid model: it does not reproduce the papers' complete robot, sensing, or movement assumptions.

## Why the comparison should not assume a winner

Hernández, Baier, Uras, and Koenig argue that the circumstances in which incremental search is faster than repeated search are not well understood. Their work reports that Repeated Forward A* can be faster on easier tasks that require few searches and motivates evaluation over varied maps and task difficulty. It also uses controlled trajectory comparisons in some experiments, which matters because two planners following different paths may discover different obstacles.

Hernández, Baier, and Asín later propose MPAA*, an enhanced A* method. Their reported improvements concern MPAA*, not plain repeated A*. That result is useful context for the wider design space, but must not be presented as evidence that this project's repeated-A* baseline has the same performance.

**Project implication:** compare correctness, route cost, node expansions, and measured planning time separately. Use both end-to-end navigation (where planners may see different discoveries) and a distinct controlled replay (where both receive the same updates). Treat repetitions on one map as repeated measurements, not additional independent maps.

## Relevance to current robot software

The official Nav2 Smac Planner documentation lists 2D A*, Hybrid-A*, and State Lattice planners. This shows A*-family planning remains relevant in modern mobile-robot software. A physical robot, however, also has to address map representation, footprint and collision costs, kinematics, localization, sensing, and control. Room Rover's four-neighbour grid is an educational algorithm testbed, not a drop-in physical navigation stack.

## Research gap and intended contribution

The project is not claiming a new path-planning algorithm. Its intended contribution is a transparent, reproducible teaching and evaluation tool for comparing repeated A* and D* Lite under a stated model of initially hidden, stationary obstacles. It records task outcomes and search/runtime measures, checks paths independently, and keeps autonomous route comparisons separate from identical-update replay. The results should identify behavior in the implemented simulator and motivate later physical tests; they cannot establish real-world robot performance.

## References

1. Hart, P. E., Nilsson, N. J., and Raphael, B. (1968). “A Formal Basis for the Heuristic Determination of Minimum Cost Paths.” *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100–107. [DOI](https://doi.org/10.1109/TSSC.1968.300136) · [Author/university-hosted copy](https://www.cs.auckland.ac.nz/courses/compsci709s2c/resources/Mike.d/astarNilsson.pdf)
2. Koenig, S. and Likhachev, M. (2002). “D* Lite.” *Proceedings of the Eighteenth National Conference on Artificial Intelligence*, 476–483. [AAAI paper](https://aaai.org/Papers/AAAI/2002/AAAI02-072.pdf) · [CMU publication record](https://publications.ri.cmu.edu/d-lite)
3. Koenig, S. and Likhachev, M. (2005). “Fast Replanning for Navigation in Unknown Terrain.” *IEEE Transactions on Robotics*, 21(3), 354–363. [DOI](https://doi.org/10.1109/TRO.2004.838026) · [Author-hosted paper](https://www.cs.cmu.edu/~maxim/files/dlite_tro05.pdf)
4. Hernández, C., Baier, J. A., Uras, T., and Koenig, S. (2012). “Position Paper: Incremental Search Algorithms Considered Poorly Understood.” *Proceedings of the Fifth Annual Symposium on Combinatorial Search*, 3(1), 159–161. [DOI](https://doi.org/10.1609/socs.v3i1.18268) · [Author-hosted paper](https://idm-lab.org/bib/abstracts/papers/socs12b.pdf)
5. Hernández, C., Baier, J. A., and Asín, R. (2014). “Making A* Run Faster than D*-Lite for Path-Planning in Partially Known Terrain.” *Proceedings of the Twenty-Fourth International Conference on Automated Planning and Scheduling*. [DOI](https://doi.org/10.1609/icaps.v24i1.13675) · [Proceedings article](https://ojs.aaai.org/index.php/ICAPS/article/view/13675)
6. Open Navigation LLC. “Smac Planner.” Official Nav2 documentation. [Documentation](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/planners_plugins/smac/)
