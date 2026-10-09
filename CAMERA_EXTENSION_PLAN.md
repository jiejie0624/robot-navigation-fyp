# Camera-Assisted Goal Selection — Feasibility and Scope

## Purpose

This document evaluates a possible camera extension to the indoor robot navigation FYP. It is an optional later stage. The current research core remains the comparison of A* and D* Lite in a grid simulator with initially unknown obstacles.

## The idea

A user wants the robot to reach a meaningful place, such as a room exit. A camera could help identify a target, but a camera image and a navigation goal are different kinds of information:

- An image may show a door, sign, or visual marker.
- The path planner needs a goal represented as a reachable location in the robot's map, plus the robot's current location in that same map.

Therefore, detecting something that looks like a door does not by itself tell the planner which map cell to reach. A single ordinary room photo also does not reliably provide the complete room layout, distances, or hidden obstacles.

## Feasibility by approach

| Approach | What it can demonstrate | Main limitation | Feasibility |
|---|---|---|---|
| Upload one room photo and ask a vision/LLM API to return the exit's robot coordinates | Image description or a rough candidate door | A normal image has perspective and no reliable map coordinates; occlusion and ambiguous doors make coordinates unsafe to assume | Low as the first physical prototype |
| User taps a goal in a live camera image | Human-selected visual target | The selected pixel must be transformed into a map position; this needs camera calibration, robot pose, and a map | Medium to high effort |
| Put a known visual marker at the target, detect its ID and pose | A repeatable target-recognition and approach demo | Needs a camera, marker, calibration, and a way to relate camera pose to robot motion/map | Best bounded camera extension |
| User marks a goal directly on the known simulator map | Tests path planning and goal reachability without vision | Does not test camera perception | Already supported by the current project concept |

## Recommended staged design

### Stage 0 — Keep the current FYP core

Use the simulator's explicit map and goal selection. Obstacles and walls are represented in the grid. Compare the planners under identical maps, start/goal positions, and obstacle-reveal events. Do not describe this stage as camera-based room understanding.

### Stage 1 — Camera proof of concept (optional)

Use a small camera mounted on a robot or a stationary test rig and place a known marker (for example, a printed AprilTag/ArUco marker) at a designated goal. The system should:

1. Capture frames and detect the known marker ID.
2. Reject unknown IDs and low-confidence detections.
3. Estimate the marker's relative position only after camera calibration.
4. Convert that relative observation into a goal/approach point using a documented coordinate transform, or use the marker only as a final-approach cue while the simulator/map provides the global goal.
5. Stop at a safe approach distance; never set the goal to a wall surface or the marker's physical surface.
6. Log detection success, false detections, stopping distance, and any navigation failure.

For an early integration, keep map-based route planning unchanged and let vision provide only a clearly defined target cue. If localization and coordinate transforms are not available, explicitly limit the demo to marker detection and stopping nearby; do not claim full room-level navigation from the camera.

### Stage 2 — Broader visual goal selection (future work)

Only consider selecting doors or objects from ordinary images after the project has a reliable map, robot localization, calibrated camera, and a tested transformation from camera coordinates to map coordinates. The system should ask a person to confirm an ambiguous target before moving.

## Does this need DeepSeek or another LLM?

No LLM is needed for the core navigation comparison or for detecting a known visual marker. A marker detector or computer-vision library is deterministic and easier to evaluate. A vision-language API could describe an image or suggest candidate objects, but its response should not be treated as a precise, safety-valid robot coordinate. If used later, the system must still verify the candidate against the map and require confirmation when uncertain.

## Minimum acceptance criteria for a camera extension

- Correctly recognize the intended marker ID in a defined test area.
- Reject an unrecognized marker and report that no valid target was found.
- Demonstrate repeatable target approach/stop behavior over multiple trials.
- Record detection rate, false positives, stopping-distance error, and trial conditions.
- Keep the existing path-planning benchmark separable from camera results, so perception errors are not mistaken for planner errors.
- Clearly state whether the extension uses a pre-mapped goal, a marker-relative approach, or full map localization.

## Risks and controls

| Risk | Control |
|---|---|
| Door-like objects or wrong marker selected | Use unique IDs and require confirmation for the selected target |
| Camera detects a target but cannot locate it on the map | Limit initial claim to relative approach, or provide calibrated localization before map-based routing |
| Lighting, blur, viewing angle, or occlusion causes missed detections | Test a stated range of conditions and stop safely when detection is lost |
| Camera/API output produces an unsafe or unreachable goal | Validate all goals against the map and use a safe approach point |
| Hardware integration expands beyond available time/budget | Keep the extension optional and finish simulator evaluation first |

## Scope decision for now

The camera is a possible extension, not a dependency of the current FYP. The recommended first camera experiment is known-marker recognition and safe approach in a small controlled area. Automatic understanding of arbitrary room photos and exact exit coordinates is out of scope unless the supervisor, time, hardware, and localization plan support it.
