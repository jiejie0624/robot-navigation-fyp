# Project guidance for AI agents

## How to work on this project

- Discuss with the student in simple Chinese unless they request another language.
- Take the lead on research, technical choices, planning, and implementation. Do not require the student to already know programming or hardware terminology.
- Before substantial changes, read `PROJECT_BRIEF.md` and `ROADMAP.md`. Keep those files current when a project decision or milestone changes.
- The student wants a computer simulation first and a real robot later. Keep the simulation useful as a standalone demonstration while designing it so the navigation logic can later be reused with hardware.
- Keep the control console usable on both desktop and smartphone screens; treat the phone as a possible interface for the future physical-robot demo.
- Explain technical choices plainly. Distinguish confirmed requirements from assumptions and proposals; do not present an unconfirmed choice as the student's decision.
- For current prices, device capabilities, or software versions, check reliable current sources and link them in the response.
- Do not expose API keys or put secrets in browser code. If an external API is introduced, route credentials through a backend.
- When the student asks for implementation, make the change in the project files and give a short summary of what changed, how to run it, and any limitations.
- If a tool blocks a requested preview or environment action, record the limitation and continue with independent work; do not try to bypass the tool's security boundary.

## Confirmed project concept

The project is a CS final-year project about indoor robot navigation and obstacle avoidance. A user sets the robot's initial location and facing direction, then selects a destination on a square-room map. The room boundary is known, but interior obstacles are initially unknown to the robot. While moving, the robot detects obstacles, updates its map, and plans a safe route again. It must avoid repeatedly attempting a route already found to be blocked and stop safely if no route is available.

The intended development sequence is:

1. Build and demonstrate a computer simulation.
2. Refine and evaluate the navigation and replanning behavior in simulation.
3. If practical, connect the same navigation flow to a small physical robot and compare results.

Do not assume a robot has already been purchased or that a particular board, sensor, framework, or budget has been selected.

## Current prototype

- `index.html` is the first standalone browser prototype, published at https://jiejie0624.github.io/robot-navigation-fyp/.
- It uses a 15 × 15 grid, a simulated forward sensor, selectable A* or D* Lite planning, five fixed presets, 18 seeded random maps with varied start/goal/heading, and ten repeated batch runs per map/planner pair with configuration-rich CSV export.
- Obstacles placed in setup are hidden from the robot until detected.
- The simulation uses discrete grid movement; it does not yet model wheel slip, physical sensor noise, continuous motion, or real localization.
- The deployed page was checked in desktop and phone-sized browser layouts. Treat this as a UI availability check, not proof of algorithm correctness; review simulation outputs before using them as research evidence.
