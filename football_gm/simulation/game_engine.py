"""Game simulation engine — simulates individual games and generates realistic stats."""

import random


class GameResult:
    """Stores the outcome and stats from a simulated game."""

    def __init__(self, home_abbr, away_abbr):
        self.home_abbr = home_abbr
        self.away_abbr = away_abbr
        self.home_score = 0
        self.away_score = 0
        self.home_stats = {}
        self.away_stats = {}
        self.overtime = False

    @property
    def winner(self):
        if self.home_score > self.away_score:
            return self.home_abbr
        elif self.away_score > self.home_score:
            return self.away_abbr
        return None  # tie

    @property
    def loser(self):
        if self.home_score > self.away_score:
            return self.away_abbr
        elif self.away_score > self.home_score:
            return self.home_abbr
        return None

    def summary(self):
        ot = " (OT)" if self.overtime else ""
        return f"{self.away_abbr} {self.away_score} @ {self.home_abbr} {self.home_score}{ot}"


def calculate_team_strength(team):
    """Calculate offensive and defensive strength ratings for a team."""
    starters = team.get_starters()

    # Offensive strength
    off_positions = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT"]
    off_ratings = []
    for pos in off_positions:
        if pos in starters:
            weight = 2.0 if pos == "QB" else 1.0  # QB has outsized impact
            off_ratings.append(starters[pos].overall_rating * weight)

    off_strength = sum(off_ratings) / max(len(off_ratings), 1) if off_ratings else 40

    # Defensive strength
    def_positions = ["DE", "DT", "OLB", "ILB", "CB", "FS", "SS"]
    def_ratings = [starters[pos].overall_rating for pos in def_positions if pos in starters]
    def_strength = sum(def_ratings) / max(len(def_ratings), 1) if def_ratings else 40

    # Coaching adjustment
    coaching_factor = team.head_coach_quality / 100

    return {
        "offense": off_strength * (0.85 + coaching_factor * 0.3),
        "defense": def_strength * (0.85 + coaching_factor * 0.3),
        "overall": (off_strength + def_strength) / 2,
    }


def simulate_game(home_team, away_team):
    """Simulate a single game between two teams. Returns a GameResult."""
    result = GameResult(home_team.abbr, away_team.abbr)

    home_strength = calculate_team_strength(home_team)
    away_strength = calculate_team_strength(away_team)

    # Home field advantage
    HOME_ADVANTAGE = 2.5

    # Expected points calculation
    # Average NFL game: ~22 points per team
    league_avg_points = 22.0

    # Offensive strength vs opposing defensive strength determines scoring
    home_off_factor = home_strength["offense"] / max(away_strength["defense"], 1)
    away_off_factor = away_strength["offense"] / max(home_strength["defense"], 1)

    home_expected = league_avg_points * home_off_factor + HOME_ADVANTAGE
    away_expected = league_avg_points * away_off_factor - HOME_ADVANTAGE * 0.3

    # Clamp to reasonable range
    home_expected = max(6, min(45, home_expected))
    away_expected = max(6, min(45, away_expected))

    # Generate actual scores with variance
    # NFL scores tend to cluster in multiples of 7 and 3
    home_score = _generate_football_score(home_expected)
    away_score = _generate_football_score(away_expected)

    # Handle ties — go to overtime
    if home_score == away_score:
        result.overtime = True
        # Overtime: ~75% chance someone wins, 25% remains tied
        if random.random() < 0.75:
            if random.random() < 0.55:  # slight home advantage
                home_score += random.choice([3, 6, 7])
            else:
                away_score += random.choice([3, 6, 7])

    result.home_score = home_score
    result.away_score = away_score

    # Generate player stats
    result.home_stats = _generate_team_stats(home_team, home_score, "home")
    result.away_stats = _generate_team_stats(away_team, away_score, "away")

    return result


def _generate_football_score(expected_points):
    """Generate a realistic football score centered around expected points."""
    # Football scores are built from: TD(7), FG(3), Safety(2), missed XP TD(6)
    score = 0
    remaining = expected_points + random.gauss(0, 5)
    remaining = max(0, remaining)

    # Simulate scoring drives
    while remaining > 0:
        roll = random.random()
        if roll < 0.55 and remaining >= 7:
            score += 7  # TD + XP
            remaining -= 7
        elif roll < 0.60 and remaining >= 6:
            score += 6  # TD + missed XP
            remaining -= 6
        elif roll < 0.90 and remaining >= 3:
            score += 3  # FG
            remaining -= 3
        else:
            break  # remaining drives fizzle

        # Random chance to stop scoring
        if random.random() < 0.25:
            break

    return score


def _generate_team_stats(team, score, side):
    """Generate box score stats for a team based on their score and roster."""
    starters = team.get_starters()
    stats = {
        "passing_yards": 0,
        "rushing_yards": 0,
        "first_downs": 0,
        "turnovers": 0,
        "sacks_allowed": 0,
        "time_of_possession": 0,
    }

    # More points generally means more yards
    yard_factor = score / 22.0  # normalized to league average

    # Passing
    base_pass = random.gauss(225, 50) * yard_factor
    stats["passing_yards"] = max(50, round(base_pass))

    # Rushing
    base_rush = random.gauss(110, 35) * yard_factor
    stats["rushing_yards"] = max(20, round(base_rush))

    # First downs
    total_yards = stats["passing_yards"] + stats["rushing_yards"]
    stats["first_downs"] = max(5, round(total_yards / random.gauss(17, 3)))

    # Turnovers (inversely related to QB quality)
    qb = starters.get("QB")
    qb_rating = qb.overall_rating if qb else 50
    turnover_chance = max(0.05, 0.30 - qb_rating * 0.003)
    stats["turnovers"] = sum(1 for _ in range(5) if random.random() < turnover_chance)

    # Sacks (based on opposing pass rush vs OL)
    stats["sacks_allowed"] = random.randint(0, 5)

    # Time of possession (in minutes, game is 60 min total)
    stats["time_of_possession"] = round(random.gauss(30, 4), 1)

    return stats


def simulate_week(league, week_number):
    """Simulate all games in a given week."""
    games = league.get_week_games(week_number)
    results = []

    for home_abbr, away_abbr in games:
        home_team = league.teams[home_abbr]
        away_team = league.teams[away_abbr]

        result = simulate_game(home_team, away_team)

        # Update team records
        if result.winner == home_abbr:
            home_team.wins += 1
            away_team.losses += 1
        elif result.winner == away_abbr:
            away_team.wins += 1
            home_team.losses += 1
        else:
            home_team.ties += 1
            away_team.ties += 1

        home_team.points_for += result.home_score
        home_team.points_against += result.away_score
        away_team.points_for += result.away_score
        away_team.points_against += result.home_score

        results.append(result)

    # Check for injuries this week
    _process_weekly_injuries(league)

    league.advance_week()
    return results


def _process_weekly_injuries(league):
    """Randomly injure players during the week's games."""
    injury_types = [
        ("Hamstring", 1, 4),
        ("Ankle Sprain", 1, 3),
        ("Knee Sprain", 2, 6),
        ("Concussion", 1, 3),
        ("Shoulder", 2, 6),
        ("ACL Tear", 8, 18),
        ("Broken Bone", 4, 10),
        ("Back", 1, 4),
        ("Calf", 1, 3),
        ("Groin", 1, 3),
    ]

    for team in league.teams.values():
        for player in team.players:
            if player.injured:
                continue

            # Base injury chance per game: ~5% per player
            injury_chance = 0.05

            # Adjust for durability
            durability = player.attributes.get("injury_resistance", 50)
            injury_chance *= (1.5 - durability / 100)

            # Older players get hurt more
            if player.age > 30:
                injury_chance *= 1.2
            if player.age > 34:
                injury_chance *= 1.3

            if random.random() < injury_chance:
                injury_name, min_weeks, max_weeks = random.choice(injury_types)

                # ACL tears are rarer
                if injury_name == "ACL Tear" and random.random() > 0.15:
                    injury_name, min_weeks, max_weeks = ("Knee Sprain", 2, 6)

                weeks = random.randint(min_weeks, max_weeks)
                player.apply_injury(injury_name, weeks)
