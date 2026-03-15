# Monday Morning GM — Game Design Document

**Working Title:** Monday Morning GM
**Genre:** NFL Front Office Management Simulation
**Inspiration:** OOTP Baseball depth + Football Manager intuitiveness + real NFL complexity
**Core Fantasy:** You are the GM. Every contract, every cut, every draft pick, every trade — it's all on you.

---

## Design Philosophy

- **Pure NFL rules as the default.** The core experience mirrors the real NFL as closely as possible.
- **Cross-sport features are opt-in toggles** in a custom mode for players who want more depth.
- **Cap analysis is on the player.** No hand-holding — you learn to manage the cap yourself.
- **AI teams play by the same rules.** Full realistic AI cap management. No cheating AI.
- **Deep & immersive, not fast & shallow.** Major events (free agency, draft) are experiences, not menus.
- **Difficulty modes planned for the future:** Casual (simplified), Standard (full NFL rules), Advanced (NFL + cross-sport features), Custom (toggle everything).

---

## 1. Salary Cap System

### Core Mechanics (Always On)
- **Hard salary cap** — Cannot exceed at any point during the league year
- **Salary cap floor (89%)** — Must spend at least 89% over a rolling 4-year period
- **Cap rollover** — Unused cap space carries to next year
- **Top-51 rule** — Only top 51 cap hits count during the offseason; full 53-man roster counts during regular season
- **Compensatory draft picks** — Teams losing more/better FAs than they sign receive extra picks (rounds 3-7)

### GM Tools (Always On)
- **Franchise & transition tags** — Exclusive/non-exclusive franchise tag and transition tag. One per team per year
- **Contract restructures** — Convert base salary to signing bonus to create cap space (pushes cap hit to future years)
- **Void years** — Add fake years to spread signing bonus proration further
- **June 1st cut designation** — Spread dead cap from a cut across two league years. Limited to 2 per team per year

### Player Cut Mechanics
- **Full NFL realism:** Dead cap from remaining prorated signing bonus
- June 1st designation option to spread dead cap across two years
- Post-June 1 cuts
- Vested vs. non-vested veterans

---

## 2. Contract System

### Contract Components (All Available)
- **Base salary** — Per-year salary, counts against cap in full that year
- **Signing bonus** — Upfront cash, prorates evenly across contract (max 5 years)
- **Guaranteed base salary** — Guaranteed for specific years; still hits cap if player is cut
- **Roster bonus** — Paid if player is on roster on a specific date (usually March)
- **Option bonus / option year** — Team option to trigger a bonus and keep player, or decline
- **LTBE / NLTBE incentives** — Likely To Be Earned (counts against current cap) vs. Not Likely (counts next year if earned), based on prior year stats
- **Escalators / de-escalators** — Annual adjustments based on playing time, Pro Bowl, or other criteria
- **No-trade clause** — Prevents trading without player consent. Typically for veteran stars

### Contract Structure
- **Full complexity:** Each year has base salary, signing bonus proration, roster bonus, option bonus, and incentives
- Player designs each year individually when offering a contract

---

## 3. Toggleable Cross-Sport Contract Features (Custom Mode)

All disabled by default. Each can be toggled on independently.

### Tier 1: High-Impact
| Feature | Origin | Description |
|---------|--------|-------------|
| Loyalty Rights | NBA Bird Rights | Players with 3+ consecutive years on your roster are cheaper to re-sign (cap discount or accept below-market deals) |
| Deferred Money | MLB | Pay less now, more later with interest penalty. Lets GMs mortgage the future for a win-now window |
| Salary Retention in Trades | NHL | When trading a player, retain 25-50% of cap hit. Limited to 2-3 active retention slots and % of cap ceiling |
| Player Loans | European Soccer | Temporarily loan players for half/full season with optional buy clauses at pre-negotiated draft pick cost |
| Stretch Dead Money | NBA Stretch Provision | Spread cut player's dead cap over 2x remaining years + 1 instead of accelerating |
| Supermax Designation | NBA Supermax | Elite players (Pro Bowl/All-Pro) can receive above-normal max contracts. Only current team can offer |

### Tier 2: Interesting Additions
| Feature | Origin | Description |
|---------|--------|-------------|
| Opt-Out Clauses | MLB | Player can void remaining years at specific contract points |
| Vesting/Mutual Options | MLB | Contract years auto-activate based on performance thresholds or require mutual agreement |
| Release Clauses | European Soccer | A price at which any team can acquire the player, bypassing trade negotiations |
| Sell-On Clauses | European Soccer | When trading a player, retain % of any future trade compensation |
| Compliance Buyouts | NHL | Limited guilt-free contract terminations with no cap hit (1 per team every 3-5 years) |

---

## 4. Free Agency System

### Calendar Structure
- **Structured offseason free agency** with defined periods (legal tampering, FA opening, ongoing)
- **In-season street free agent signings** (like real NFL)

### Flow
- **Turn-based with advances:** Player handles negotiations, then advances time to see what happened around the league
- **Cascading market:** Players don't "walk away" — they sign elsewhere while you're still negotiating. You must pivot to secondary targets. Best players get best deals but don't necessarily sign first
- **Full market ripple effects:** A top player signing affects same-position demands, extension timing for players in final contract years, team budget recalibrations

### Target Board System
- **Pre-FA target board + manual override** (default)
- Build a ranked list of FA targets before FA opens (like a real draft board for free agency)
- Front office staff (assistant GMs, coaches) provide input to help build the board
- Board acts as "autopilot" between active decisions; player can manually override at any time

### Negotiation System
- **Deep & immersive** — Free agency is an event, not a menu
- **Direct player dialogue** — You negotiate face-to-face with the player character. No agents. Players speak for themselves with personality and voice (e.g., "I appreciate the offer, but I need more guaranteed money to feel secure about my family's future.")
- **Full personality system** — Players have personalities, preferences, and priorities (ring chasing, hometown, weather, no income tax, role, scheme fit). Money matters but isn't everything

#### Player Negotiation Styles (Core Innovation)
Each player has a negotiation **tendency** that shifts based on **context** (market demand, age, desperation, number of offers). Styles are **revealed during negotiation**, not known upfront.

Example styles:
- **Transparent:** "Team X offered me $Y/year. Beat it by $Z and you have a deal."
- **Hardball:** "You need to improve your offer to stay in the running." (No specifics shared)
- **Best-offer-wins:** "I don't do back-and-forth. Every team gives me their best offer, I pick the one I like most."
- **Loyalty-leaning:** Willing to take less to stay with current team or go to a specific situation
- **Money-first:** Highest total value wins, period
- *More styles TBD*

### Information & Intelligence
- **No insider info / no cheating** — No magical knowledge of other teams' offers
- **Assistant GMs provide analysis:** Which players they deduce other teams will prioritize, estimated contract ranges for each player, adjustments as FA progresses
- Staff quality affects accuracy of these projections

### GM Reputation System
- **Persistent reputation score** affected by:
  - Honoring commitments
  - Withdrawing offers
  - Overpaying / underpaying
  - Winning record
  - Treatment of veterans (cutting stars vs. loyalty)
- Reputation affects free agent willingness to sign with your team

### AI Cap Management
- **Full realistic AI cap management** — AI teams follow the same rules, make realistic signings, manage dead cap, and restructure contracts
- This is the hardest engineering challenge but the #1 differentiator for long-term playability

---

## 5. Front Office Staff System

### Roles
| Role | Function |
|------|----------|
| **Assistant GM** | Helps build FA board, evaluates trade targets, manages roster strategy. Skill level affects quality of roster-building advice |
| **Scouting Director** | Evaluates college talent (draft) and pro talent (trades/FA). Better scouts = more accurate player ratings revealed |
| **Coaching Staff** | Head coach and coordinators influence scheme fit evaluation, player development rates, and which players want to play for your team |

### Staff Quality
- **Toggleable display:** Real numerical ratings OR vague reputation-based "metric" for immersion
- Player chooses which display mode they prefer

### Notable Design Choice
- **No Cap/Finance Analyst role** — Cap analysis is entirely on the player. This is a core skill the player develops, not something the game does for you.

---

## 6. Systems Still To Design

- [ ] Draft system (scouting, combine, draft day flow)
- [ ] Trade system (trade logic, valuations, trade deadline)
- [ ] Scouting system (college scouting, pro scouting, accuracy)
- [ ] Coaching & schemes (hiring/firing, scheme effects, player fit)
- [ ] Player development details
- [ ] Game simulation refinements
- [ ] UI/UX approach
- [ ] Season calendar & offseason flow
- [ ] Awards, records, and historical tracking

---

## Technical Foundation (Already Implemented)

- Python 3.10+, no external dependencies
- 32 fictional teams across 2 conferences, 8 divisions
- 19 positions with position-specific attribute weights
- Player generation with talent distribution
- Game simulation engine with statistical outcomes
- Player aging, development curves, and retirement
- Injury system with realistic types and recovery
- 18-week, 17-game schedule generation
- 14-team playoff structure
- Core contract and salary cap mechanics (need updating to match this GDD)

---

*This is a living document. Systems will be added as design decisions are made.*
