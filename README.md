# Football GM Simulator

The most in-depth and realistic Football GM simulation game in existence.

A pure front-office management simulation inspired by Out of the Park Baseball,
built for the NFL. No play-calling, no watching games — just the chess match of
roster construction, salary cap management, player development, scouting, and
long-term franchise building.

## Features (Planned)

- **Realistic Salary Cap & Contracts** — Fully modeled NFL salary cap with
  signing bonuses, dead cap, franchise tags, restructures, and cap casualties
- **Player Development & Regression** — Attribute progression based on age,
  position, coaching, injuries, and usage
- **Deep Scouting System** — Draft prospects with hidden attributes, combine
  results, and scouting accuracy tiers
- **Game Simulation Engine** — Statistical game outcomes driven by player
  ratings, schemes, and matchups
- **Dynamic Free Agency** — Market-driven contract demands, compensatory picks
- **Trade System** — AI-driven trade logic with realistic valuations
- **Coaching & Schemes** — Hire/fire staff, set schemes that affect player fit
- **Injury Model** — Realistic injury frequency, severity, and recovery timelines
- **Multi-Season Franchise Mode** — Build a dynasty across decades

## Project Structure

```
football_gm/
├── core/           # Data models (Player, Team, League, Contract)
├── simulation/     # Game sim engine, stat generation
├── systems/        # GM systems (free agency, draft, trades, salary cap)
├── data/           # Static data (team names, position configs, name lists)
├── utils/          # Helpers (random generation, formatting)
└── main.py         # Entry point
```

## Tech Stack

- Python 3.10+
- No external dependencies (foundation phase)

## Getting Started

```bash
python -m football_gm.main
```
