"""Football GM Simulator — Main entry point."""

import random
from football_gm.core.league import League
from football_gm.core.contract import Contract, SALARY_CAP, VETERAN_MINIMUM
from football_gm.utils.player_generator import generate_roster, generate_draft_class
from football_gm.simulation.game_engine import simulate_week


def create_new_league():
    """Initialize a new league with rosters and contracts."""
    print("\n=== CREATING NEW LEAGUE ===\n")
    league = League(year=2025)

    # Generate rosters for all 32 teams
    print("Generating rosters for 32 teams...")
    for team in league.teams.values():
        generate_roster(team)

        # Give each player a basic contract
        for player in team.players:
            years = random.randint(1, 4)
            ovr = player.overall_rating

            # Contract value scales with overall rating
            if ovr >= 85:
                base_value = random.randint(15_000_000, 35_000_000) * years
            elif ovr >= 75:
                base_value = random.randint(8_000_000, 18_000_000) * years
            elif ovr >= 65:
                base_value = random.randint(3_000_000, 10_000_000) * years
            else:
                base_value = random.randint(VETERAN_MINIMUM, 3_000_000) * years

            signing_bonus = round(base_value * random.uniform(0.15, 0.40))
            guaranteed = round(base_value * random.uniform(0.30, 0.65))

            contract = Contract(
                player_id=player.id,
                team_abbr=team.abbr,
                total_value=base_value,
                years=years,
                signing_bonus=signing_bonus,
                guaranteed_money=guaranteed,
            )
            player.contract = contract

    # Generate some free agents
    print("Generating free agent pool...")
    for _ in range(150):
        from football_gm.utils.player_generator import generate_player
        from football_gm.data.positions import POSITIONS
        pos = random.choice(POSITIONS)
        player = generate_player(pos)
        league.free_agents.append(player)

    print(f"League created: {len(league.teams)} teams, "
          f"{sum(t.roster_size for t in league.teams.values())} rostered players, "
          f"{len(league.free_agents)} free agents\n")

    return league


def select_team(league):
    """Let the player choose which team to manage."""
    print("\n=== SELECT YOUR TEAM ===\n")

    teams_list = sorted(league.teams.values(), key=lambda t: t.full_name)
    for i, team in enumerate(teams_list, 1):
        print(f"  {i:2}. {team.full_name} ({team.abbr}) — "
              f"OVR: {team.overall_rating} | Cap Space: ${team.cap_space:,.0f}")

    while True:
        try:
            choice = input("\nEnter team number (1-32): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(teams_list):
                selected = teams_list[idx]
                print(f"\nYou are now the GM of the {selected.full_name}!")
                return selected
        except (ValueError, IndexError):
            pass
        print("Invalid choice. Try again.")


def display_roster(team):
    """Show the current roster with ratings and contract info."""
    print(f"\n=== {team.full_name} ROSTER ({team.roster_size}/53) ===")
    print(f"{'':2} {'Name':<22} {'Pos':<4} {'Age':<4} {'OVR':<5} "
          f"{'Cap Hit':<14} {'Yrs Left':<9} {'Status'}")
    print("-" * 85)

    players = sorted(team.players, key=lambda p: (-p.overall_rating,))
    for i, p in enumerate(players, 1):
        cap_hit = f"${p.contract.current_cap_hit:,.0f}" if p.contract else "No Contract"
        yrs = f"{p.contract.years_remaining}yr" if p.contract else "-"
        status = f"INJ ({p.injury_type}, {p.injury_weeks_remaining}wk)" if p.injured else "Active"
        print(f"{i:2}. {p.full_name:<22} {p.position:<4} {p.age:<4} {p.overall_rating:<5} "
              f"{cap_hit:<14} {yrs:<9} {status}")


def display_standings(league):
    """Show league standings by division."""
    print(f"\n=== {league.year} STANDINGS (Week {league.week}) ===\n")

    for conf in ["AC", "PC"]:
        conf_name = "Atlantic Conference" if conf == "AC" else "Pacific Conference"
        print(f"  {conf_name}")
        print(f"  {'':2} {'Team':<28} {'W':>3} {'L':>3} {'T':>3} {'PCT':>6} {'PF':>5} {'PA':>5} {'DIFF':>5}")
        print(f"  {'-' * 65}")

        for div in ["East", "North", "South", "West"]:
            teams = league.get_division_teams(conf, div)
            teams.sort(key=lambda t: (t.win_pct, t.point_differential), reverse=True)
            print(f"  {div}")
            for t in teams:
                print(f"     {t.full_name:<28} {t.wins:>3} {t.losses:>3} {t.ties:>3} "
                      f"{t.win_pct:>6.3f} {t.points_for:>5} {t.points_against:>5} "
                      f"{t.point_differential:>+5}")
        print()


def display_cap_info(team):
    """Show detailed salary cap information."""
    print(f"\n=== {team.full_name} SALARY CAP ===")
    print(f"  Salary Cap:     ${team.salary_cap:>14,.0f}")
    print(f"  Cap Carryover:  ${team.cap_carryover:>14,.0f}")
    print(f"  Effective Cap:  ${team.salary_cap + team.cap_carryover:>14,.0f}")
    print(f"  Cap Used:       ${team.total_cap_used:>14,.0f}")
    print(f"  Dead Cap:       ${team.dead_cap:>14,.0f}")
    print(f"  Cap Space:      ${team.cap_space:>14,.0f}")

    print(f"\n  Top Cap Hits:")
    top = sorted(team.players, key=lambda p: p.contract.current_cap_hit if p.contract else 0, reverse=True)
    for p in top[:10]:
        if p.contract:
            print(f"    {p.full_name:<22} {p.position:<4} "
                  f"${p.contract.current_cap_hit:>12,.0f}  "
                  f"({p.contract.years_remaining}yr remaining)")


def display_free_agents(league, position=None):
    """Show available free agents."""
    fas = league.free_agents
    if position:
        fas = [p for p in fas if p.position == position]

    fas.sort(key=lambda p: p.overall_rating, reverse=True)
    print(f"\n=== FREE AGENTS ({len(fas)} available) ===")
    print(f"{'':2} {'Name':<22} {'Pos':<4} {'Age':<4} {'OVR':<5}")
    print("-" * 45)
    for i, p in enumerate(fas[:30], 1):  # show top 30
        print(f"{i:2}. {p.full_name:<22} {p.position:<4} {p.age:<4} {p.overall_rating:<5}")

    if len(fas) > 30:
        print(f"  ... and {len(fas) - 30} more")


def sim_regular_season(league, my_team):
    """Simulate the entire regular season week by week."""
    print(f"\n=== SIMULATING {league.year} REGULAR SEASON ===\n")

    for week in range(1, 19):
        results = simulate_week(league, week)

        # Show my team's game
        my_game = None
        for r in results:
            if r.home_abbr == my_team.abbr or r.away_abbr == my_team.abbr:
                my_game = r
                break

        if my_game:
            print(f"  Week {week:2}: {my_game.summary()}  "
                  f"| {my_team.abbr} Record: {my_team.record}")
        else:
            print(f"  Week {week:2}: BYE WEEK  | {my_team.abbr} Record: {my_team.record}")

    print(f"\nFinal Record: {my_team.full_name} {my_team.record}")


def main_menu(league, my_team):
    """Main game loop."""
    while True:
        print(f"\n{'=' * 50}")
        print(f"  FOOTBALL GM — {league.year} | {league.phase.upper()}")
        print(f"  {my_team.full_name} ({my_team.record})")
        print(f"  Cap Space: ${my_team.cap_space:,.0f}")
        print(f"{'=' * 50}")
        print("  1. View Roster")
        print("  2. View Standings")
        print("  3. View Salary Cap")
        print("  4. View Free Agents")
        print("  5. Simulate Season")
        print("  6. Advance to Next Season")
        print("  7. View Team Rankings")
        print("  0. Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            display_roster(my_team)
        elif choice == "2":
            display_standings(league)
        elif choice == "3":
            display_cap_info(my_team)
        elif choice == "4":
            pos = input("  Filter by position (or Enter for all): ").strip().upper()
            display_free_agents(league, pos if pos else None)
        elif choice == "5":
            league.start_new_season()
            sim_regular_season(league, my_team)
        elif choice == "6":
            retired = league.advance_to_offseason()
            my_retired = [p for p in retired if p.team_abbr == my_team.abbr]
            if my_retired:
                print(f"\n  Retired from your team:")
                for p in my_retired:
                    print(f"    {p.full_name} ({p.position}, Age {p.age})")
            print(f"\n  Advanced to {league.year} offseason.")
            print(f"  {len(retired)} players retired league-wide.")
        elif choice == "7":
            print(f"\n=== TEAM POWER RANKINGS ===")
            ranked = sorted(league.teams.values(),
                            key=lambda t: t.overall_rating, reverse=True)
            for i, t in enumerate(ranked, 1):
                marker = " <<<" if t.abbr == my_team.abbr else ""
                print(f"  {i:2}. {t.full_name:<28} OVR: {t.overall_rating}{marker}")
        elif choice == "0":
            print("\nThanks for playing Football GM!")
            break
        else:
            print("Invalid choice.")


def main():
    """Entry point."""
    print("=" * 50)
    print("  FOOTBALL GM SIMULATOR")
    print("  The Ultimate Front Office Experience")
    print("=" * 50)
    print("\n  1. New Game")
    print("  0. Quit")

    choice = input("\n> ").strip()
    if choice == "1":
        league = create_new_league()
        my_team = select_team(league)
        main_menu(league, my_team)
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
