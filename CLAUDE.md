# Monday Morning GM — Project Context

## What This Is

An NFL front-office management simulation game (think OOTP Baseball but for the NFL). The player is the GM — no play-calling, no watching games. Pure roster construction, salary cap management, scouting, drafting, and franchise building.

**Working Title:** Monday Morning GM
**Tech:** Python 3.10+, no external dependencies (foundation phase)
**Run:** `python -m football_gm.main`

## Project Structure

```
football_gm/
├── core/           # Data models (Player, Team, League, Contract)
│   ├── player.py   # Player attributes, aging, development, retirement
│   ├── team.py     # Team roster, scheme, staff
│   ├── league.py   # League structure, schedule, playoffs
│   └── contract.py # Contract components, salary cap math
├── simulation/     # Game sim engine, stat generation
│   └── game_engine.py
├── systems/        # GM systems (free agency, draft, trades, salary cap) — mostly TBD
├── data/           # Static data
│   ├── teams.py    # 32 fictional teams, 2 conferences, 8 divisions
│   ├── positions.py # 19 positions with attribute weights
│   └── names.py    # Name generation lists
├── utils/
│   └── player_generator.py  # Talent distribution, rookie generation
└── main.py         # Entry point
```

## What's Already Built

- 32 fictional teams across 2 conferences, 8 divisions
- 19 positions with position-specific attribute weights
- Player generation with talent distribution curves
- Game simulation engine with statistical outcomes
- Player aging, development curves, and retirement logic
- Injury system with realistic types and recovery timelines
- 18-week, 17-game schedule generation
- 14-team playoff structure
- Basic contract and salary cap mechanics (need updating to match the GDD)

## Key Design Documents

- **GDD.md** — The full Game Design Document. READ THIS FIRST for any design questions. It covers:
  - Salary cap system (hard cap, cap floor, rollover, Top-51 rule, comp picks)
  - Contract system (base salary, signing bonus proration, guarantees, roster bonuses, option bonuses, LTBE/NLTBE incentives, escalators, no-trade clauses)
  - Toggleable cross-sport features for custom mode (loyalty rights, deferred money, salary retention, player loans, stretch dead money, supermax, opt-outs, release clauses, etc.)
  - Free agency system (calendar, target board, negotiation with player personalities and negotiation styles, GM reputation)
  - Front office staff (assistant GM, scouting director, coaching staff)
- **README.md** — High-level feature overview

## Design Philosophy

1. **Pure NFL rules as the default** — Mirror real NFL as closely as possible
2. **Cross-sport features are opt-in toggles** in custom mode
3. **Cap analysis is on the player** — No hand-holding, no cap analyst role
4. **AI teams play by the same rules** — Full realistic AI cap management, no cheating
5. **Deep & immersive, not fast & shallow** — Major events (FA, draft) are experiences, not menus

## Systems Still To Design & Build

- Draft system (scouting, combine, draft day flow)
- Trade system (trade logic, valuations, trade deadline)
- Scouting system (college scouting, pro scouting, accuracy tiers)
- Coaching & schemes (hiring/firing, scheme effects, player fit)
- Player development details (beyond current aging curves)
- Game simulation refinements
- UI/UX approach
- Season calendar & offseason flow
- Awards, records, and historical tracking
- Free agency system (designed in GDD, not yet implemented)
- Front office staff system (designed in GDD, not yet implemented)
- Contract system update (current code needs updating to match GDD complexity)

## Development Notes

- The contract/salary cap code in `core/contract.py` is a foundation but needs significant expansion to match the full GDD spec (signing bonus proration, void years, June 1st cuts, restructures, etc.)
- AI cap management is the hardest engineering challenge and the biggest differentiator
- Free agency negotiation system with player personalities/styles is a core innovation — prioritize getting this right
- No external dependencies by design during foundation phase; may revisit later for UI
